import reflex as rx
import httpx
from typing import List, Dict
from datetime import datetime, timezone
from claimsiq.config import API_URL, DATA_OPERATIONS_ENABLED


DEFAULT_MODAL_CLAIM = {
    "id": "—",
    "claim_amount": 0.0,
    "claim_amount_formatted": "$0.00",
    "claim_date": "—",
    "status": "unknown",
    "provider_name": "Unknown",
    "provider_id": "Unknown",
    "patient_id": "—",
    "procedure_code": "—",
    "procedure_codes": "—",
    "diagnosis_code": "—",
    "risk_score": 0.0,
    "ui_risk_level": "low",
    "ui_risk_reason": "",
    "ui_has_reason": False,
    "days_pending": 0,
    "approved_amount": 0.0,
    "approved_amount_formatted": "—",
    "processor_notes": "",
    "denial_reason": None,
    "processed_date": None,
}

DEFAULT_QUICK_STATS = {
    "provider_summary": "No provider history available.",
    "similar_summary": "No similar claims found.",
    "days_pending_label": "0 days pending",
}

class ClaimsState(rx.State):
    claims_data: List[Dict] = []
    summary_stats: Dict = {}
    risk_analysis: Dict = {}
    provider_metrics: List[Dict] = []

    is_loading_summary: bool = False
    is_loading_claims: bool = False
    error_message: str = ""
    selected_status: str = "all"
    time_range: str = "90d"
    last_updated: str = ""

    total_claims: int = 0
    approved_count: int = 0
    pending_count: int = 0
    flagged_count: int = 0
    approval_rate: float = 0.0

    # Pagination
    current_page: int = 1
    page_size: int = 25
    total_pages: int = 1

    # Search
    search_query: str = ""

    # Sorting
    sort_column: str = "id"
    sort_direction: str = "asc"

    # Advanced filters
    date_start: str = ""
    date_end: str = ""
    amount_min: float = 0.0
    amount_max: float = 100000.0
    risk_filters: list[str] = []

    # Modal state
    selected_claim_id: str = ""
    show_claim_modal: bool = False
    modal_claim: Dict = DEFAULT_MODAL_CLAIM.copy()
    modal_quick_stats: Dict = DEFAULT_QUICK_STATS.copy()
    modal_notes: str = ""
    modal_action_reason: str = ""

    # Theme
    dark_mode: bool = False

    is_processing_claim: bool = False
    is_saving_notes: bool = False
    data_ops_enabled: bool = DATA_OPERATIONS_ENABLED

    # Notifications
    notification_message: str = ""
    notification_type: str = "info"  # info, success, warning, error
    show_notification: bool = False
    
    async def load_summary(self):
        self.is_loading_summary = True
        try:
            params = {"time_range": self.time_range}
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/api/claims/summary", params=params)
                if response.status_code == 200:
                    data = response.json()
                    self.summary_stats = data
                    self.total_claims = data.get("total_claims", 0)
                    self.approved_count = data.get("approved_count", 0)
                    self.pending_count = data.get("pending_count", 0)
                    self.flagged_count = data.get("flagged_count", 0)
                    self.approval_rate = data.get("approval_rate", 0.0)
                    self.last_updated = datetime.now(timezone.utc).isoformat()
                    self.error_message = ""
                else:
                    self.error_message = f"Failed to load summary: {response.status_code}"
        except Exception as e:
            self.error_message = f"Error loading summary: {str(e)}"
        finally:
            self.is_loading_summary = False
    
    async def load_claims(self):
        self.is_loading_claims = True
        try:
            params = {
                "limit": 100,
                "offset": 0,
                "time_range": self.time_range if self.time_range else None,
                "date_start": self.date_start if self.date_start else None,
                "date_end": self.date_end if self.date_end else None,
            }
            if self.selected_status != "all":
                params["status"] = self.selected_status
            if self.risk_filters:
                params["risk_levels"] = ",".join(self.risk_filters)
            # Remove None values to avoid sending them
            params = {k: v for k, v in params.items() if v is not None}

            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/api/claims", params=params)
                if response.status_code == 200:
                    data = response.json()
                    raw_claims = data.get("claims", [])
                    self.claims_data = [self._normalize_claim(raw) for raw in raw_claims]
                    if self.selected_claim_id:
                        self._sync_modal_claim()
                    self.error_message = ""
                else:
                    self.error_message = f"Failed to load claims: {response.status_code}"
        except Exception as e:
            self.error_message = f"Error loading claims: {str(e)}"
        finally:
            self.is_loading_claims = False
    
    async def load_risk_analysis(self):
        try:
            params = {"time_range": self.time_range}
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/api/analytics/risks", params=params)
                if response.status_code == 200:
                    self.risk_analysis = response.json()
        except Exception as e:
            print(f"Error loading risk analysis: {str(e)}")
    
    async def load_providers(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/api/providers")
                if response.status_code == 200:
                    self.provider_metrics = response.json()
        except Exception as e:
            print(f"Error loading providers: {str(e)}")
    
    async def set_status_filter(self, status: str):
        self.selected_status = status
        self.current_page = 1  # Reset to first page when filtering
        await self.load_claims()

    def set_search_query(self, query: str):
        self.search_query = query
        self.current_page = 1  # Reset to first page when searching

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1

    def set_page(self, page: int):
        if 1 <= page <= self.total_pages:
            self.current_page = page

    def set_page_from_input(self, page: str):
        """Set page from input field (converts string to int)"""
        try:
            page_num = int(page)
            self.set_page(page_num)
        except (ValueError, TypeError):
            pass  # Ignore invalid input

    def sort_by(self, column: str):
        if self.sort_column == column:
            # Toggle direction if same column
            self.sort_direction = "desc" if self.sort_direction == "asc" else "asc"
        else:
            self.sort_column = column
            self.sort_direction = "asc"

    @rx.var
    def filtered_claims(self) -> List[Dict]:
        """Filter claims based on search query"""
        claims = self.claims_data

        if self.search_query:
            query = self.search_query.lower()
            claims = [
                claim for claim in claims
                if query in str(claim.get("id", "")).lower()
                or query in str(claim.get("patient_name", "")).lower()
                or query in str(claim.get("status", "")).lower()
                or query in str(claim.get("provider_name", "")).lower()
                or query in str(claim.get("provider_id", "")).lower()
            ]

        if self.risk_filters:
            def bucket(score):
                if score is None:
                    return "unknown"
                if score >= 0.7:
                    return "high"
                if score >= 0.4:
                    return "medium"
                return "low"

            claims = [
                claim
                for claim in claims
                if bucket(claim.get("risk_score")) in self.risk_filters
            ]

        return claims

    @rx.var
    def sorted_claims(self) -> List[Dict]:
        """Sort filtered claims"""
        claims = self.filtered_claims

        if self.sort_column and claims:
            reverse = self.sort_direction == "desc"
            try:
                claims = sorted(
                    claims,
                    key=lambda x: x.get(self.sort_column, ""),
                    reverse=reverse
                )
            except Exception as e:
                print(f"Error sorting: {e}")

        return claims

    @rx.var
    def paginated_claims(self) -> List[Dict]:
        """Get claims for current page"""
        claims = self.sorted_claims
        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size

        # Update total pages
        total = len(claims)
        self.total_pages = max(1, (total + self.page_size - 1) // self.page_size)

        return claims[start:end]

    @rx.var
    def page_start(self) -> int:
        """Starting index for current page"""
        return (self.current_page - 1) * self.page_size + 1

    @rx.var
    def page_end(self) -> int:
        """Ending index for current page"""
        total = len(self.sorted_claims)
        end = self.current_page * self.page_size
        return min(end, total)

    @rx.var
    def is_last_page(self) -> bool:
        """Check if current page is the last page"""
        return self.current_page >= self.total_pages

    # Advanced Filters
    async def set_date_range(self, start: str, end: str):
        self.date_start = start
        self.date_end = end
        self.current_page = 1
        await self.load_claims()

    def set_amount_range(self, min_val: float, max_val: float):
        self.amount_min = min_val
        self.amount_max = max_val
        self.current_page = 1

    async def set_risk_filters(self, filters: list[str]):
        self.risk_filters = filters
        self.current_page = 1
        await self.load_claims()

    async def toggle_risk(self, key: str):
        """Toggle a single risk filter."""
        filters = set(self.risk_filters)
        if key in filters:
            filters.remove(key)
        else:
            filters.add(key)
        self.risk_filters = list(filters)
        self.current_page = 1
        await self.load_claims()

    async def clear_filters(self):
        self.date_start = ""
        self.date_end = ""
        self.amount_min = 0.0
        self.amount_max = 100000.0
        self.risk_filters = []
        self.search_query = ""
        self.selected_status = "all"
        self.current_page = 1
        self.time_range = "90d"
        await self.load_all_data()

    async def update_date_start(self, start: str):
        await self.set_date_range(start, self.date_end)

    async def update_date_end(self, end: str):
        await self.set_date_range(self.date_start, end)

    # Modal actions
    def open_claim_modal(self, event_or_id):
        """Open claim modal. Accepts either an event dict or a claim ID string."""
        claim_id = ""

        if isinstance(event_or_id, dict):
            for possible_key in ["current_target", "currentTarget", "target", "srcElement", "detail"]:
                if possible_key in event_or_id:
                    target = event_or_id[possible_key]
                    if isinstance(target, dict) and "id" in target:
                        claim_id = target["id"]
                        break
            if not claim_id:
                claim_id = str(event_or_id.get("id", "")).strip()
        else:
            claim_id = str(event_or_id).strip()

        if not claim_id:
            self.show_toast("Unable to identify the selected claim.", "error")
            return

        self.selected_claim_id = claim_id
        self.modal_action_reason = ""
        self._sync_modal_claim()
        self.show_claim_modal = True

    def close_claim_modal(self):
        self.show_claim_modal = False
        self.selected_claim_id = ""
        self.modal_claim = self._default_modal_claim()
        self.modal_quick_stats = DEFAULT_QUICK_STATS.copy()
        self.modal_notes = ""
        self.modal_action_reason = ""

    def set_show_claim_modal(self, value: bool):
        """Explicit setter to avoid relying on auto-generated setters."""
        self.show_claim_modal = value
        if not value:
            self.selected_claim_id = ""
            self.modal_claim = self._default_modal_claim()
            self.modal_quick_stats = DEFAULT_QUICK_STATS.copy()
            self.modal_notes = ""
            self.modal_action_reason = ""

    @rx.var
    def selected_claim(self) -> Dict:
        """Get the currently selected claim"""
        for claim in self.claims_data:
            if str(claim.get("id")) == str(self.selected_claim_id):
                return claim
        return {}

    def _sync_modal_claim(self):
        """Update the modal claim dict based on the selected claim id."""
        if not self.selected_claim_id:
            self.modal_claim = self._default_modal_claim()
            self.modal_quick_stats = DEFAULT_QUICK_STATS.copy()
            self.modal_notes = ""
            self.modal_action_reason = ""
            return

        selected = next(
            (
                claim
                for claim in self.claims_data
                if str(claim.get("id")) == str(self.selected_claim_id)
            ),
            None,
        )

        if selected is None:
            self.modal_claim = self._default_modal_claim()
            self.modal_quick_stats = DEFAULT_QUICK_STATS.copy()
            self.modal_notes = ""
            self.modal_action_reason = ""
        else:
            hydrated = {**self._default_modal_claim(), **selected}
            self.modal_claim = hydrated
            self.modal_notes = hydrated.get("processor_notes", "")
            self.modal_quick_stats = self._compute_quick_stats(hydrated)
            self.modal_action_reason = ""

    @rx.var
    def has_modal_claim(self) -> bool:
        claim = self.modal_claim
        return bool(claim and claim.get("id"))

    def _default_modal_claim(self) -> Dict:
        return DEFAULT_MODAL_CLAIM.copy()

    def _normalize_claim(self, claim: Dict) -> Dict:
        data = {**DEFAULT_MODAL_CLAIM, **(claim or {})}

        try:
            amount = float(data.get("claim_amount", 0) or 0)
        except (TypeError, ValueError):
            amount = 0.0
        data["claim_amount"] = amount
        data["claim_amount_formatted"] = f"${amount:,.2f}"

        approved = data.get("approved_amount")
        try:
            approved_value = float(approved) if approved is not None else None
        except (TypeError, ValueError):
            approved_value = None
        data["approved_amount"] = approved_value
        data["approved_amount_formatted"] = (
            f"${approved_value:,.2f}" if approved_value is not None else "—"
        )

        claim_date = data.get("claim_date")
        if isinstance(claim_date, datetime):
            data["claim_date"] = claim_date.strftime("%Y-%m-%d")
        elif claim_date in (None, ""):
            data["claim_date"] = "—"
        else:
            data["claim_date"] = str(claim_date)

        data["id"] = str(data.get("id", ""))
        data["status"] = str(data.get("status", "unknown")).lower()

        try:
            risk_score = float(data.get("risk_score", 0) or 0)
        except (TypeError, ValueError):
            risk_score = 0.0
        data["risk_score"] = round(risk_score, 2)

        existing_days = data.get("days_pending")
        try:
            days_pending = float(existing_days) if existing_days is not None else 0.0
        except (TypeError, ValueError):
            days_pending = 0.0

        if not days_pending:
            try:
                claim_dt = datetime.fromisoformat(data["claim_date"])
                if data["status"] == "pending":
                    days_pending = max((datetime.utcnow() - claim_dt).days, 0)
                else:
                    processed_date = data.get("processed_date")
                    if processed_date:
                        processed_dt = datetime.fromisoformat(str(processed_date))
                        days_pending = max((processed_dt - claim_dt).days, 0)
            except Exception:
                days_pending = 0.0
        data["days_pending"] = float(days_pending)

        reasons: list[str] = []
        if amount > 5000:
            reasons.append("Amount > $5,000")
        if data["status"] == "pending" and data["days_pending"] > 30:
            reasons.append("Pending > 30 days")
        if data.get("denial_reason"):
            reasons.append(str(data["denial_reason"]))
        if data.get("risk_reason"):
            reasons.append(str(data["risk_reason"]))

        if reasons:
            reason_text = " • ".join(dict.fromkeys(reasons))
        else:
            reason_text = ""
        data["ui_risk_reason"] = reason_text
        data["ui_has_reason"] = bool(reason_text)

        data["provider_id"] = str(data.get("provider_id", "Unknown"))
        provider_name = data.get("provider_name") or data["provider_id"] or "Unknown"
        data["provider_name"] = provider_name
        data["patient_id"] = data.get("patient_id") or "—"
        data["procedure_code"] = data.get("procedure_code") or data.get("procedure_codes") or "—"
        data["procedure_codes"] = data.get("procedure_codes") or data["procedure_code"]
        data["diagnosis_code"] = data.get("diagnosis_code") or "—"
        data["processor_notes"] = data.get("processor_notes") or ""

        if risk_score >= 0.7:
            data["ui_risk_level"] = "high"
        elif risk_score >= 0.4:
            data["ui_risk_level"] = "medium"
        else:
            data["ui_risk_level"] = "low"

        return data

    def _compute_quick_stats(self, claim: Dict) -> Dict:
        stats = DEFAULT_QUICK_STATS.copy()
        if not claim:
            return stats

        provider_id = claim.get("provider_id")
        provider_claims = [c for c in self.claims_data if str(c.get("provider_id")) == str(provider_id)]
        total_claims = len(provider_claims)
        approvals = sum(1 for c in provider_claims if c.get("status") == "approved")
        approval_rate = approvals / total_claims if total_claims else 0

        if total_claims <= 1:
            provider_summary = "First time filing with ClaimsIQ."
        else:
            provider_summary = (
                f"Returning provider ({total_claims - 1} prior claims, {int(round(approval_rate * 100))}% approval)."
            )

        claim_id = claim.get("id")
        diagnosis_code = claim.get("diagnosis_code")
        procedure_code = claim.get("procedure_code") or claim.get("procedure_codes")

        same_diag = 0
        same_proc = 0
        for other in self.claims_data:
            if str(other.get("id")) == str(claim_id):
                continue
            if diagnosis_code and other.get("diagnosis_code") == diagnosis_code:
                same_diag += 1
            other_proc = other.get("procedure_code") or other.get("procedure_codes")
            if procedure_code and other_proc == procedure_code:
                same_proc += 1

        if same_diag or same_proc:
            parts = []
            if same_diag:
                parts.append(f"{same_diag} share diagnosis")
            if same_proc:
                parts.append(f"{same_proc} share procedure")
            similar_summary = ", ".join(parts)
        else:
            similar_summary = "No similar claims found."

        days_pending = int(claim.get("days_pending") or 0)
        status = claim.get("status")
        if status == "pending":
            days_label = f"{days_pending} days pending" if days_pending else "Pending (no timer)"
        else:
            days_label = "Processed today" if days_pending == 0 else f"Processed in {days_pending} days"

        stats["provider_summary"] = provider_summary
        stats["similar_summary"] = similar_summary
        stats["days_pending_label"] = days_label
        return stats

    def _patch_claim_in_list(self, updated_claim: Dict):
        normalized = self._normalize_claim(updated_claim)
        patched = []
        for claim in self.claims_data:
            if str(claim.get("id")) == normalized["id"]:
                merged = {**claim, **normalized}
                patched.append(merged)
            else:
                patched.append(claim)
        self.claims_data = patched
        if str(self.selected_claim_id) == normalized["id"]:
            self.modal_claim = {**self._default_modal_claim(), **normalized}
            self.modal_notes = self.modal_claim.get("processor_notes", "")
            self.modal_quick_stats = self._compute_quick_stats(self.modal_claim)

    # Theme toggle
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode

    # Error message setter
    def set_error_message(self, message: str):
        """Set or clear error message"""
        self.error_message = message

    # Notifications
    def show_toast(self, message: str, type: str = "info"):
        self.notification_message = message
        self.notification_type = type
        self.show_notification = True

    def hide_notification(self):
        self.show_notification = False
        self.notification_message = ""

    # Export functionality
    def export_to_csv(self):
        """Export current filtered/sorted claims to CSV"""
        import csv
        import io
        from datetime import datetime

        try:
            # Get current filtered and sorted claims
            claims = self.sorted_claims

            if not claims:
                self.show_toast("No data to export", "warning")
                return

            # Create CSV in memory
            output = io.StringIO()
            fieldnames = ["id", "claim_date", "claim_amount", "status", "risk_score"]
            writer = csv.DictWriter(output, fieldnames=fieldnames)

            writer.writeheader()
            for claim in claims:
                writer.writerow({
                    "id": claim.get("id", ""),
                    "claim_date": claim.get("claim_date", ""),
                    "claim_amount": claim.get("claim_amount", ""),
                    "status": claim.get("status", ""),
                    "risk_score": claim.get("risk_score", ""),
                })

            # Trigger download
            csv_content = output.getvalue()
            filename = f"claims_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

            self.show_toast(f"Exported {len(claims)} claims successfully!", "success")

            return csv_content

        except Exception as e:
            self.show_toast(f"Export failed: {str(e)}", "error")
            return None

    async def load_all_data(self):
        await self.load_summary()
        await self.load_claims()
        await self.load_risk_analysis()
        await self.load_providers()

    async def refresh_all_data(self):
        self.show_toast("Refreshing data...", "info")
        await self.load_all_data()
        self.show_toast("Dashboard updated", "success")

    async def drill_into_status(self, status: str):
        """Set status filter from metric cards and fetch data."""
        self.selected_status = status
        self.current_page = 1
        await self.load_claims()

    async def set_time_range(self, range_key: str):
        """Update the global time range and reload dependent data."""
        self.time_range = range_key
        await self.load_all_data()

    @rx.var
    def last_updated_label(self) -> str:
        if not self.last_updated:
            return "Just now"
        try:
            updated_dt = datetime.fromisoformat(self.last_updated)
            return updated_dt.astimezone().strftime("%b %d, %Y • %I:%M %p")
        except ValueError:
            return "Just now"

    @rx.var
    def approval_rate_label(self) -> str:
        if self.approval_rate and self.approval_rate > 0:
            return f"{self.approval_rate * 100:.1f}% approval rate"
        return "Approval insights"

    @rx.var
    def risk_low_active(self) -> bool:
        return "low" in self.risk_filters

    @rx.var
    def risk_medium_active(self) -> bool:
        return "medium" in self.risk_filters

    @rx.var
    def risk_high_active(self) -> bool:
        return "high" in self.risk_filters

    # Data Management
    is_loading_data: bool = False

    async def load_kaggle_data(self):
        """Load real insurance data from Kaggle"""
        if not self.data_ops_enabled:
            self.show_toast("Data operations are disabled in this environment.", "warning")
            return
        self.is_loading_data = True
        self.show_toast("Downloading Kaggle dataset...", "info")

        try:
            async with httpx.AsyncClient(timeout=300.0) as client:  # 5 min timeout
                response = await client.post(f"{API_URL}/api/data/load-kaggle")

                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        message = f"Loaded {result.get('claims_count', 0)} claims and {result.get('providers_count', 0)} providers from Kaggle!"
                        self.show_toast(message, "success")
                        # Reload data
                        await self.load_all_data()
                    else:
                        self.show_toast(result.get("message", "Failed to load Kaggle data"), "error")
                else:
                    self.show_toast("Failed to load Kaggle data. Check API logs.", "error")

        except httpx.TimeoutException:
            self.show_toast("Request timed out. Kaggle download may take a few minutes on first run.", "warning")
        except Exception as e:
            self.show_toast(f"Error loading Kaggle data: {str(e)}", "error")
        finally:
            self.is_loading_data = False

    async def generate_sample_data(self, num_claims: int = 1000):
        """Generate synthetic sample data"""
        if not self.data_ops_enabled:
            self.show_toast("Data operations are disabled in this environment.", "warning")
            return
        self.is_loading_data = True
        self.show_toast(f"Generating {num_claims} sample claims...", "info")

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{API_URL}/api/data/generate-sample",
                    params={"num_claims": num_claims}
                )

                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        message = f"Generated {result.get('claims_count', 0)} claims and {result.get('providers_count', 0)} providers!"
                        self.show_toast(message, "success")
                        # Reload data
                        await self.load_all_data()
                    else:
                        self.show_toast(result.get("message", "Failed to generate data"), "error")
                else:
                    self.show_toast("Failed to generate sample data. Check API logs.", "error")

        except Exception as e:
            self.show_toast(f"Error generating sample data: {str(e)}", "error")
        finally:
            self.is_loading_data = False

    async def clear_all_data(self):
        """Clear all data from the database"""
        if not self.data_ops_enabled:
            self.show_toast("Data operations are disabled in this environment.", "warning")
            return
        self.is_loading_data = True
        self.show_toast("Clearing all data...", "info")

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(f"{API_URL}/api/data/clear-data")

                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        self.show_toast(result.get("message", "Data cleared successfully"), "success")
                        # Reload data (should be empty now)
                        await self.load_all_data()
                    else:
                        self.show_toast("Failed to clear data", "error")
                else:
                    self.show_toast("Failed to clear data. Check API logs.", "error")

        except Exception as e:
            self.show_toast(f"Error clearing data: {str(e)}", "error")
        finally:
            self.is_loading_data = False

    # Claim Actions (Approve/Deny/Flag)
    async def approve_claim(self, claim_id: str):
        await self._update_claim_status(
            claim_id,
            payload={"status": "approved"},
            success_message=f"✓ Claim {claim_id} approved successfully",
            toast_type="success",
        )

    async def deny_claim(self, claim_id: str):
        reason = (self.modal_action_reason or "").strip()
        await self._update_claim_status(
            claim_id,
            payload={"status": "denied", "reason": reason or None},
            success_message=f"✗ Claim {claim_id} denied",
            toast_type="success",
        )

    async def flag_claim(self, claim_id: str):
        note = (self.modal_action_reason or "").strip()
        await self._update_claim_status(
            claim_id,
            payload={"status": "flagged", "reason": note or None},
            success_message=f"⚠ Claim {claim_id} flagged for review",
            toast_type="warning",
        )

    async def _update_claim_status(self, claim_id: str, payload: Dict, success_message: str, toast_type: str):
        if not claim_id:
            self.show_toast("Select a claim before performing actions.", "warning")
            return
        if self.is_processing_claim:
            return
        self.is_processing_claim = True
        try:
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"{API_URL}/api/claims/{claim_id}/status",
                    json=payload,
                )

            if response.status_code == 200:
                body = response.json()
                claim = body.get("claim", {})
                self._patch_claim_in_list(claim)
                quick_stats = body.get("quick_stats")
                if quick_stats:
                    self.modal_quick_stats = quick_stats
                self.show_toast(success_message, toast_type)
                self.close_claim_modal()
                await self.load_summary()
                await self.load_claims()
            else:
                self.show_toast(
                    f"Failed to update claim ({response.status_code})",
                    "error",
                )
        except Exception as exc:
            self.show_toast(f"Error updating claim: {exc}", "error")
        finally:
            self.is_processing_claim = False
            self.modal_action_reason = ""

    def set_modal_notes(self, value: str):
        self.modal_notes = value

    def set_modal_action_reason(self, value: str):
        self.modal_action_reason = value

    async def save_modal_notes(self):
        if not self.selected_claim_id:
            self.show_toast("Select a claim before saving notes.", "warning")
            return
        if self.is_saving_notes:
            return
        self.is_saving_notes = True
        try:
            trimmed_note = self.modal_notes.strip()
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"{API_URL}/api/claims/{self.selected_claim_id}/notes",
                    json={"note": trimmed_note},
                )

            if response.status_code == 200:
                body = response.json()
                claim = body.get("claim", {})
                self._patch_claim_in_list(claim)
                self.modal_notes = trimmed_note
                self.show_toast("Notes saved", "success")
            else:
                self.show_toast(
                    f"Failed to save notes ({response.status_code})",
                    "error",
                )
        except Exception as exc:
            self.show_toast(f"Error saving notes: {exc}", "error")
        finally:
            self.is_saving_notes = False
