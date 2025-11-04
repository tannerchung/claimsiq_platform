import math
import pandas as pd
from typing import Optional, List, Dict, Any
from datetime import datetime
from backend.services.data_service import DataService
from backend.services.analytics_service import AnalyticsService

DEFAULT_CLAIM_TEMPLATE: Dict[str, Any] =  {
    "id": "",
    "claim_amount": 0.0,
    "claim_amount_formatted": "$0.00",
    "approved_amount": None,
    "approved_amount_formatted": "—",
    "claim_date": "—",
    "status": "unknown",
    "risk_score": 0.0,
    "days_pending": 0.0,
    "denial_reason": None,
    "processed_date": None,
    "provider_id": "Unknown",
    "provider_name": "Unknown",
    "patient_id": "—",
    "procedure_code": "—",
    "procedure_codes": "—",
    "diagnosis_code": "—",
    "processor_notes": "",
    "ui_risk_reason": "",
    "ui_has_reason": False,
    "ui_risk_level": "low",
}


class ClaimsService:
    class NotFoundError(Exception):
        """Raised when a claim cannot be located."""

    class InvalidStatusError(Exception):
        """Raised when an unsupported status update is requested."""
    
    @staticmethod
    def get_summary():
        claims_df = DataService.get_claims()
        
        if claims_df.empty:
            return {
                "total_claims": 0,
                "approved_count": 0,
                "pending_count": 0,
                "flagged_count": 0,
                "approval_rate": 0.0
            }
        
        total_claims = len(claims_df)
        approved_count = len(claims_df[claims_df['status'] == 'approved'])
        pending_count = len(claims_df[claims_df['status'] == 'pending'])
        flagged_count = len(claims_df[claims_df['status'] == 'flagged'])
        approval_rate = approved_count / total_claims if total_claims > 0 else 0.0
        
        return {
            "total_claims": total_claims,
            "approved_count": approved_count,
            "pending_count": pending_count,
            "flagged_count": flagged_count,
            "approval_rate": round(approval_rate, 2)
        }
    
    @staticmethod
    def filter_claims(status: Optional[str] = None, start_date: Optional[str] = None, 
                     end_date: Optional[str] = None, limit: int = 100, offset: int = 0):
        claims_df = DataService.get_claims()
        
        if claims_df.empty:
            return {"claims": [], "total": 0, "page": 0, "page_size": limit}
        
        filtered_df = claims_df.copy()
        
        if status and status != 'all':
            filtered_df = filtered_df[filtered_df['status'] == status]
        
        if start_date:
            filtered_df['claim_date'] = pd.to_datetime(filtered_df['claim_date'])
            filtered_df = filtered_df[filtered_df['claim_date'] >= pd.to_datetime(start_date)]
        
        if end_date:
            filtered_df['claim_date'] = pd.to_datetime(filtered_df['claim_date'])
            filtered_df = filtered_df[filtered_df['claim_date'] <= pd.to_datetime(end_date)]
        
        filtered_df['risk_score'] = filtered_df.apply(
            lambda row: AnalyticsService.calculate_risk_score(row.to_dict()), 
            axis=1
        )
        
        total = len(filtered_df)
        page_data = filtered_df.iloc[offset:offset+limit]
        
        claims_list = []
        for _, row in page_data.iterrows():
            normalized = ClaimsService._normalize_claim_row(row.to_dict())
            claims_list.append(normalized)
        
        return {
            "claims": claims_list,
            "total": total,
            "page": offset // limit,
            "page_size": limit
        }
    
    @staticmethod
    def get_provider_metrics():
        claims_df = DataService.get_claims()
        providers_df = DataService.get_providers()

        if claims_df.empty:
            return []
        
        provider_metrics = claims_df.groupby('provider_id').agg({
            'id': 'count',
            'status': lambda x: (x == 'approved').sum() / len(x) if len(x) > 0 else 0,
            'claim_amount': 'mean'
        }).reset_index()
        
        provider_metrics.columns = ['provider_id', 'total_claims', 'approval_rate', 'avg_claim_amount']
        
        if not providers_df.empty:
            provider_metrics = provider_metrics.merge(
                providers_df[['id', 'name']], 
                left_on='provider_id', 
                right_on='id', 
                how='left'
            )
            provider_metrics['name'] = provider_metrics['name'].fillna('Unknown Provider')
        else:
            provider_metrics['name'] = 'Provider ' + provider_metrics['provider_id']
        
        overall_approval = claims_df[claims_df['status'] == 'approved'].shape[0] / len(claims_df)
        provider_metrics['is_unusual'] = (
            (provider_metrics['approval_rate'] > overall_approval + 0.15) |
            (provider_metrics['avg_claim_amount'] > claims_df['claim_amount'].quantile(0.9))
        )

        # Convert to records and replace NaN values
        records = provider_metrics.to_dict('records')
        for record in records:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None

        return records

    @staticmethod
    def update_claim_status(
        claim_id: str,
        status: str,
        reason: Optional[str] = None,
    ) -> Dict:
        """Update a claim's status and persist the change."""

        allowed_statuses = {"approved", "pending", "denied", "flagged"}
        normalized_status = status.lower()
        if normalized_status not in allowed_statuses:
            raise ClaimsService.InvalidStatusError(
                f"Unsupported status '{status}'. Allowed values: {sorted(allowed_statuses)}"
            )

        claims_df = DataService.get_claims()
        if claims_df.empty:
            raise ClaimsService.NotFoundError(f"Claim {claim_id} not found")

        match = claims_df[claims_df["id"] == claim_id]
        if match.empty:
            raise ClaimsService.NotFoundError(f"Claim {claim_id} not found")

        claim_row = match.iloc[0].to_dict()

        processed_ts = datetime.utcnow()
        processed_iso = processed_ts.isoformat()

        claim_date_str = claim_row.get("claim_date")
        days_to_process = 0.0
        if claim_date_str:
            try:
                claim_date = pd.to_datetime(claim_date_str)
                days_to_process = float(max((processed_ts - claim_date).days, 0))
            except Exception:
                days_to_process = 0.0

        updates: Dict[str, Optional[object]] = {
            "status": normalized_status,
            "processed_date": processed_iso,
            "days_to_process": days_to_process,
        }

        if normalized_status == "denied":
            updates["denial_reason"] = reason or "Manual denial"
            updates["approved_amount"] = 0.0
        else:
            updates["denial_reason"] = None
            if normalized_status == "approved":
                approved_amount = claim_row.get("approved_amount")
                if pd.isna(approved_amount) or approved_amount is None:
                    updates["approved_amount"] = float(claim_row.get("claim_amount", 0.0))

        updated_rows = DataService.update_claim_record(claim_id, updates)
        if updated_rows == 0:
            raise ClaimsService.NotFoundError(f"Claim {claim_id} not found")

        refreshed_claim = {**claim_row, **updates}
        refreshed_claim["risk_score"] = AnalyticsService.calculate_risk_score(refreshed_claim)
        normalized_claim = ClaimsService._normalize_claim_row(refreshed_claim)

        claims_df_updated = claims_df.copy()
        for column, value in updates.items():
            if column in claims_df_updated.columns:
                claims_df_updated.loc[claims_df_updated["id"] == claim_id, column] = value

        quick_stats = ClaimsService._build_quick_stats(normalized_claim, claims_df_updated)

        cache_updates = {**updates, "risk_score": normalized_claim["risk_score"], "processor_notes": normalized_claim.get("processor_notes")}
        DataService.update_claim_cache(claim_id, cache_updates)

        return normalized_claim, quick_stats

    @staticmethod
    def update_claim_notes(claim_id: str, note: Optional[str]) -> Dict:
        cleaned_note = note.strip() if isinstance(note, str) else None

        updated_rows = DataService.update_claim_record(
            claim_id,
            {"processor_notes": cleaned_note or None},
        )
        if updated_rows == 0:
            raise ClaimsService.NotFoundError(f"Claim {claim_id} not found")

        DataService.update_claim_cache(claim_id, {"processor_notes": cleaned_note or None})

        claims_df = DataService.get_claims()
        match = claims_df[claims_df["id"] == claim_id]
        if match.empty:
            raise ClaimsService.NotFoundError(f"Claim {claim_id} not found")

        return ClaimsService._normalize_claim_row(match.iloc[0].to_dict())

    @staticmethod
    def _normalize_claim_row(claim: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize claim rows to guarantee JSON-safe values."""

        def safe_float(value: Any, default: float = 0.0) -> float:
            try:
                result = float(value)
                if math.isnan(result) or math.isinf(result):
                    return default
                return result
            except (TypeError, ValueError):
                return default

        def safe_str(value: Any, default: str = "") -> str:
            if value in (None, ""):
                return default
            if isinstance(value, float) and math.isnan(value):
                return default
            return str(value)

        data: Dict[str, Any] = dict(DEFAULT_CLAIM_TEMPLATE)
        data.update(claim or {})

        data["id"] = safe_str(data.get("id"))

        amount = safe_float(data.get("claim_amount"))
        data["claim_amount"] = amount
        data["claim_amount_formatted"] = f"${amount:,.2f}"

        approved = data.get("approved_amount")
        approved_value = None if approved in (None, "") else safe_float(approved)
        data["approved_amount"] = approved_value
        data["approved_amount_formatted"] = f"${approved_value:,.2f}" if approved_value is not None else "—"

        claim_date = data.get("claim_date")
        if isinstance(claim_date, (datetime, pd.Timestamp)):
            data["claim_date"] = claim_date.strftime("%Y-%m-%d")
        else:
            text = safe_str(claim_date, "—")
            data["claim_date"] = text if text else "—"

        data["status"] = safe_str(data.get("status"), "unknown").lower()

        risk_score = data.get("risk_score")
        if risk_score in (None, "") or (isinstance(risk_score, float) and math.isnan(risk_score)):
            risk_score = AnalyticsService.calculate_risk_score(data)
        risk_score = safe_float(risk_score)
        data["risk_score"] = round(risk_score, 2)

        days_pending = safe_float(data.get("days_pending"))
        data["days_pending"] = days_pending

        denial_reason = data.get("denial_reason")
        data["denial_reason"] = safe_str(denial_reason) if denial_reason else None

        processed_date = data.get("processed_date")
        if isinstance(processed_date, (datetime, pd.Timestamp)):
            data["processed_date"] = processed_date.isoformat()
        elif processed_date in (None, ""):
            data["processed_date"] = None
        else:
            data["processed_date"] = safe_str(processed_date)

        provider_id = safe_str(data.get("provider_id"), "Unknown")
        data["provider_id"] = provider_id
        data["provider_name"] = safe_str(data.get("provider_name"), provider_id)

        data["patient_id"] = safe_str(data.get("patient_id"), "—")
        procedure_code = safe_str(data.get("procedure_code") or data.get("procedure_codes"), "—")
        data["procedure_code"] = procedure_code
        data["procedure_codes"] = procedure_code
        data["diagnosis_code"] = safe_str(data.get("diagnosis_code"), "—")
        data["processor_notes"] = safe_str(data.get("processor_notes"), "")
        data["days_to_process"] = safe_float(data.get("days_to_process"))

        reasons: list[str] = []
        if amount > 5000:
            reasons.append("Amount > $5,000")
        if data["status"] == "pending" and days_pending > 30:
            reasons.append("Pending > 30 days")
        if data["denial_reason"]:
            reasons.append(data["denial_reason"])

        risk_reason = " • ".join(dict.fromkeys(reasons)) if reasons else ""
        data["ui_risk_reason"] = risk_reason
        data["ui_has_reason"] = bool(risk_reason)

        if risk_score >= 0.7:
            data["ui_risk_level"] = "high"
        elif risk_score >= 0.4:
            data["ui_risk_level"] = "medium"
        else:
            data["ui_risk_level"] = "low"

        return data

    @staticmethod
    def _build_quick_stats(claim: Dict, claims_df: pd.DataFrame) -> Dict:
        default_stats = {
            "provider_summary": "No provider history available.",
            "similar_summary": "No similar claims found.",
            "days_pending_label": "0 days pending",
        }

        if not claim or claims_df.empty:
            return default_stats

        provider_id = claim.get("provider_id")
        provider_claims = claims_df[claims_df["provider_id"] == provider_id]
        total_claims = int(len(provider_claims))
        status_series = provider_claims["status"].astype(str).str.lower()
        approvals = int((status_series == "approved").sum()) if total_claims else 0
        approval_rate = approvals / total_claims if total_claims else 0

        if total_claims <= 1:
            provider_summary = "First time filing with ClaimsIQ."
        else:
            provider_summary = (
                f"Returning provider ({total_claims - 1} prior claims, {int(round(approval_rate * 100))}% approval)."
            )

        claim_id = claim.get("id")
        diagnosis_code = claim.get("diagnosis_code")
        procedure_code = claim.get("procedure_codes")

        same_diagnosis = 0
        same_procedure = 0
        if diagnosis_code:
            same_diagnosis = int(
                claims_df[
                    (claims_df["diagnosis_code"].astype(str) == str(diagnosis_code))
                    & (claims_df["id"] != claim_id)
                ].shape[0]
            )
        if procedure_code:
            same_procedure = int(
                claims_df[
                    (claims_df["procedure_codes"].astype(str) == str(procedure_code))
                    & (claims_df["id"] != claim_id)
                ].shape[0]
            )

        similar_parts = []
        if same_diagnosis:
            similar_parts.append(f"{same_diagnosis} share diagnosis")
        if same_procedure:
            similar_parts.append(f"{same_procedure} share procedure")
        similar_summary = ", ".join(similar_parts) if similar_parts else "No similar claims found."

        days_pending = int(claim.get("days_pending") or 0)
        if claim.get("status") == "pending":
            days_label = f"{days_pending} days pending" if days_pending else "Pending (no timer)"
        else:
            days_label = "Processed today" if days_pending == 0 else f"Processed in {days_pending} days"

        return {
            "provider_summary": provider_summary,
            "similar_summary": similar_summary,
            "days_pending_label": days_label,
        }
