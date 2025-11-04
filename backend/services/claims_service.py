import pandas as pd
from typing import Optional, List
from backend.services.data_service import DataService
from backend.services.analytics_service import AnalyticsService

class ClaimsService:
    
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
            claim_dict = row.to_dict()
            if 'claim_date' in claim_dict and not isinstance(claim_dict['claim_date'], str):
                claim_dict['claim_date'] = str(claim_dict['claim_date'])
            claims_list.append(claim_dict)
        
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
        
        return provider_metrics.to_dict('records')
