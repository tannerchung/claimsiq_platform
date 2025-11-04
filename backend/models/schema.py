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
    procedure_description: Optional[str] = None
    diagnosis_code: Optional[str] = None
    diagnosis_description: Optional[str] = None
    patient_age: Optional[int] = None
    patient_gender: Optional[str] = None
    patient_state: Optional[str] = None
    days_to_process: Optional[float] = None
    denial_reason: Optional[str] = None
    processed_date: Optional[str] = None
    risk_score: Optional[float] = 0.0
    claim_amount_formatted: Optional[str] = None
    approved_amount_formatted: Optional[str] = None

    class Config:
        extra = "allow"  # Allow extra fields not defined in the model

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
