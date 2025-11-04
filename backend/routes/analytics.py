from fastapi import APIRouter
from backend.services.analytics_service import AnalyticsService
from backend.models.schema import RiskAnalysisResponse

router = APIRouter()

@router.get("/analytics/risks")
async def get_risk_analysis():
    distribution = AnalyticsService.get_risk_distribution()
    high_risk_claims = AnalyticsService.get_high_risk_claims(limit=10)
    
    return {
        "high_risk_count": distribution["high"],
        "distribution": distribution,
        "top_risks": high_risk_claims
    }
