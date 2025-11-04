from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel, validator
from typing import Optional
from backend.services.claims_service import ClaimsService
from backend.models.schema import SummaryResponse, ClaimsListResponse

router = APIRouter()


class UpdateClaimStatusRequest(BaseModel):
    status: str
    reason: Optional[str] = None

    @validator("status")
    def validate_status(cls, value: str) -> str:
        allowed = {"approved", "pending", "denied", "flagged"}
        status = value.lower()
        if status not in allowed:
            raise ValueError(f"status must be one of {sorted(allowed)}")
        return status


class UpdateClaimNotesRequest(BaseModel):
    note: Optional[str] = None


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


@router.put("/claims/{claim_id}/status")
async def update_claim_status(claim_id: str, payload: UpdateClaimStatusRequest):
    try:
        updated_claim, quick_stats = ClaimsService.update_claim_status(
            claim_id=claim_id,
            status=payload.status,
            reason=payload.reason,
        )
        return {
            "success": True,
            "claim": updated_claim,
            "quick_stats": quick_stats,
        }
    except ClaimsService.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except ClaimsService.InvalidStatusError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to update claim: {exc}")


@router.put("/claims/{claim_id}/notes")
async def update_claim_notes(claim_id: str, payload: UpdateClaimNotesRequest):
    try:
        updated_claim = ClaimsService.update_claim_notes(claim_id, payload.note)
        return {"success": True, "claim": updated_claim}
    except ClaimsService.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to update claim notes: {exc}")
