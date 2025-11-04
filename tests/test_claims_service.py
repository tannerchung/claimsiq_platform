import pandas as pd

from backend.services.claims_service import ClaimsService
from backend.services.data_service import DataService


def test_get_summary_counts(sample_claims_df):
    summary = ClaimsService.get_summary()

    assert summary["total_claims"] == len(sample_claims_df)
    assert summary["approved_count"] == 2
    assert summary["pending_count"] == 1
    assert summary["flagged_count"] == 1
    # 2 approved out of 4 total -> 0.5 rounded to 2 decimals
    assert summary["approval_rate"] == 0.5


def test_filter_claims_status(sample_claims_df):
    response = ClaimsService.filter_claims(status="approved", limit=10, offset=0)

    assert response["total"] == 2
    assert len(response["claims"]) == 2
    for claim in response["claims"]:
        assert claim["status"] == "approved"
        assert "risk_score" in claim
        assert "claim_amount_formatted" in claim


def test_filter_claims_date_range():
    response = ClaimsService.filter_claims(
        start_date="2023-12-01",
        end_date="2024-01-31",
        limit=10,
        offset=0,
    )

    returned_ids = {claim["id"] for claim in response["claims"]}
    assert returned_ids == {"CLM-001", "CLM-002"}
    assert response["total"] == 2


def test_get_provider_metrics_returns_expected_columns(sample_providers_df):
    metrics = ClaimsService.get_provider_metrics()

    assert len(metrics) == 3
    required_keys = {
        "provider_id",
        "total_claims",
        "approval_rate",
        "avg_claim_amount",
        "name",
        "is_unusual",
    }
    assert all(required_keys.issubset(metric.keys()) for metric in metrics)


def test_filter_claims_empty_dataset(monkeypatch):
    monkeypatch.setattr(DataService, "_claims_cache", pd.DataFrame())

    result = ClaimsService.filter_claims(status="approved")
    assert result == {"claims": [], "total": 0, "page": 0, "page_size": 100}
