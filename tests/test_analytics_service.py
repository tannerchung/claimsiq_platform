import pandas as pd

from backend.services.analytics_service import AnalyticsService
from backend.services.data_service import DataService


def test_calculate_risk_score_flags_high_amount(sample_claims_df):
    claim = sample_claims_df.loc[sample_claims_df["id"] == "CLM-003"].iloc[0].to_dict()
    score = AnalyticsService.calculate_risk_score(claim)

    # CLM-003: flagged + high amount + older than 30 days -> should be high risk
    assert score >= 0.7


def test_get_risk_distribution_counts(sample_claims_df):
    distribution = AnalyticsService.get_risk_distribution()

    assert sum(distribution.values()) == len(sample_claims_df)
    assert set(distribution.keys()) == {"low", "medium", "high"}


def test_get_high_risk_claims_limit(sample_claims_df):
    top_claims = AnalyticsService.get_high_risk_claims(limit=1)

    assert len(top_claims) == 1
    assert top_claims[0]["risk_score"] >= 0.7


def test_calculate_risk_score_handles_missing_provider(monkeypatch, sample_claims_df):
    # Force providers cache to empty to simulate unknown provider
    monkeypatch.setattr(DataService, "_providers_cache", pd.DataFrame())

    claim = sample_claims_df.iloc[0].to_dict()
    base_score = AnalyticsService.calculate_risk_score(claim)

    claim_unknown = claim.copy()
    claim_unknown["provider_id"] = "UNKNOWN"
    unknown_score = AnalyticsService.calculate_risk_score(claim_unknown)

    assert unknown_score >= base_score
