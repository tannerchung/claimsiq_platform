import pandas as pd
from datetime import datetime
from backend.services.data_service import DataService

class AnalyticsService:
    
    @staticmethod
    def calculate_risk_score(claim: dict) -> float:
        score = 0.0
        
        if claim.get('claim_amount', 0) > 5000:
            score += 0.3
        
        if claim.get('claim_date'):
            try:
                if isinstance(claim['claim_date'], str):
                    claim_date = pd.to_datetime(claim['claim_date'])
                else:
                    claim_date = claim['claim_date']
                days_pending = (datetime.now() - claim_date).days
                if days_pending > 30:
                    score += 0.3
            except:
                pass
        
        providers_df = DataService.get_providers()
        if not providers_df.empty and claim.get('provider_id'):
            if claim['provider_id'] not in providers_df['id'].values:
                score += 0.2
        
        return min(score, 1.0)
    
    @staticmethod
    def get_risk_distribution():
        claims_df = DataService.get_claims()
        
        if claims_df.empty:
            return {"low": 0, "medium": 0, "high": 0}
        
        claims_with_risk = claims_df.copy()
        claims_with_risk['risk_score'] = claims_with_risk.apply(
            lambda row: AnalyticsService.calculate_risk_score(row.to_dict()), 
            axis=1
        )
        
        low = len(claims_with_risk[claims_with_risk['risk_score'] < 0.4])
        medium = len(claims_with_risk[(claims_with_risk['risk_score'] >= 0.4) & (claims_with_risk['risk_score'] < 0.7)])
        high = len(claims_with_risk[claims_with_risk['risk_score'] >= 0.7])
        
        return {"low": low, "medium": medium, "high": high}
    
    @staticmethod
    def get_high_risk_claims(limit: int = 10):
        claims_df = DataService.get_claims()
        
        if claims_df.empty:
            return []
        
        claims_with_risk = claims_df.copy()
        claims_with_risk['risk_score'] = claims_with_risk.apply(
            lambda row: AnalyticsService.calculate_risk_score(row.to_dict()), 
            axis=1
        )
        
        high_risk = claims_with_risk[claims_with_risk['risk_score'] >= 0.7]
        high_risk_sorted = high_risk.sort_values('risk_score', ascending=False).head(limit)
        
        return high_risk_sorted.to_dict('records')
