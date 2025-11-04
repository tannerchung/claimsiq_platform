from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class ClaimResponse(BaseModel):
    id: str
    policy_id: Optional[str] = None
    claim_date: str
    claim_amount: float
    approved_amount: Optional[float] = None
    status: str
    provider_id: Optional[str] = None
    procedure_codes: Optional[str] = None
    risk_score: Optional[float] = 0.0

class SummaryResponse(BaseModel):
    total_claims: int
    approved_count: int
    pending_count: int
    flagged_count: int
    approval_rate: float

class ClaimsListResponse(BaseModel):
    claims: List[ClaimResponse]
    total: int
    page: int
    page_size: int

class RiskAnalysisResponse(BaseModel):
    high_risk_count: int
    distribution: dict
    top_risks: List[ClaimResponse]

class ProviderMetrics(BaseModel):
    provider_id: str
    name: str
    total_claims: int
    approval_rate: float
    avg_claim_amount: float
    is_unusual: bool
