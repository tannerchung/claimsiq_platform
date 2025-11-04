import pandas as pd
import pytest
from fastapi.testclient import TestClient

from backend import app as api_app
from backend.services.data_service import DataService


@pytest.fixture
def sample_claims_df():
    """Sample claims dataframe used across tests."""
    return pd.DataFrame(
        [
            {
                "id": "CLM-001",
                "status": "approved",
                "claim_amount": 2500.0,
                "approved_amount": 2400.0,
                "claim_date": "2024-01-10",
                "provider_id": "PROV-1",
            },
            {
                "id": "CLM-002",
                "status": "pending",
                "claim_amount": 6200.0,
                "approved_amount": None,
                "claim_date": "2023-12-15",
                "provider_id": "PROV-2",
            },
            {
                "id": "CLM-003",
                "status": "flagged",
                "claim_amount": 15000.0,
                "approved_amount": 0.0,
                "claim_date": "2023-11-30",
                "provider_id": "PROV-3",
            },
            {
                "id": "CLM-004",
                "status": "approved",
                "claim_amount": 4200.0,
                "approved_amount": 4100.0,
                "claim_date": "2024-02-05",
                "provider_id": "PROV-2",
            },
        ]
    )


@pytest.fixture
def sample_providers_df():
    """Sample providers dataframe used across tests."""
    return pd.DataFrame(
        [
            {"id": "PROV-1", "name": "Provider Alpha"},
            {"id": "PROV-2", "name": "Provider Beta"},
            {"id": "PROV-3", "name": "Provider Gamma"},
        ]
    )


@pytest.fixture(autouse=True)
def preload_data(monkeypatch, sample_claims_df, sample_providers_df):
    """Populate the in-memory caches before each test and restore afterwards."""
    original_claims = DataService._claims_cache
    original_providers = DataService._providers_cache

    DataService._claims_cache = sample_claims_df.copy()
    DataService._providers_cache = sample_providers_df.copy()

    monkeypatch.setattr(DataService, "refresh_cache", lambda: None)
    yield

    DataService._claims_cache = original_claims
    DataService._providers_cache = original_providers


@pytest.fixture
def client():
    """FastAPI test client with cache preloaded."""
    with TestClient(api_app.app) as test_client:
        yield test_client
