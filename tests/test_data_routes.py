import pytest
try:
    import pandas as pd
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    pd = None
from fastapi.testclient import TestClient

from backend.routes import data as data_routes
from backend.services.data_service import DataService

if pd is None:  # pragma: no cover - skip module if pandas unavailable
    pytest.skip("pandas is required for data route tests", allow_module_level=True)


def test_generate_sample_dataset(monkeypatch, client: TestClient, sample_claims_df, sample_providers_df):
    """Ensure the generate sample endpoint returns success and refreshes caches."""

    generated_payload = {
        "claims": sample_claims_df.copy(),
        "providers": sample_providers_df.copy(),
    }

    def fake_generate(num_claims: int):
        assert num_claims == 10
        return generated_payload["claims"], generated_payload["providers"]

    load_called = {}

    def fake_load(claims_df: pd.DataFrame, providers_df: pd.DataFrame):
        load_called["claims"] = claims_df
        load_called["providers"] = providers_df

    monkeypatch.setattr(data_routes, "generate_sample_data", fake_generate)
    monkeypatch.setattr(data_routes, "load_data_to_db", fake_load)
    monkeypatch.setattr(DataService, "refresh_cache", staticmethod(lambda: None))

    response = client.post("/api/data/generate-sample", params={"num_claims": 10})
    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True
    assert body["claims_count"] == len(sample_claims_df)
    assert body["providers_count"] == len(sample_providers_df)
    assert "claims" in load_called and "providers" in load_called


def test_generate_sample_dataset_invalid_request(client: TestClient):
    """num_claims outside the allowed range should raise a 400 error."""
    response = client.post("/api/data/generate-sample", params={"num_claims": 0})
    assert response.status_code == 400
