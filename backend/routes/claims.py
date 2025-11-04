from fastapi import APIRouter, Query
from typing import Optional
from backend.services.claims_service import ClaimsService
from backend.models.schema import SummaryResponse, ClaimsListResponse

router = APIRouter()

@router.get("/claims/summary", response_model=SummaryResponse)
async def get_summary():
    return ClaimsService.get_summary()

@router.get("/claims", response_model=ClaimsListResponse)
async def get_claims(
    status: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    limit: int = Query(100),
    offset: int = Query(0)
):
    return ClaimsService.filter_claims(
        status=status,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        offset=offset
    )

@router.get("/providers")
async def get_providers():
    return ClaimsService.get_provider_metrics()
