from fastapi.testclient import TestClient

from backend import app as api_app


def test_health_endpoint(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_endpoint(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == "ClaimsIQ API"
    assert payload["status"] == "running"


def test_claims_summary_endpoint(client: TestClient):
    response = client.get("/api/claims/summary")
    assert response.status_code == 200
    summary = response.json()

    assert summary["total_claims"] == 4
    assert summary["approved_count"] == 2
    assert summary["pending_count"] == 1
    assert summary["flagged_count"] == 1


def test_claims_list_endpoint_filters(client: TestClient):
    response = client.get("/api/claims", params={"status": "approved", "limit": 10})
    assert response.status_code == 200

    payload = response.json()
    assert payload["total"] == 2
    assert len(payload["claims"]) == 2
    assert all(claim["status"] == "approved" for claim in payload["claims"])


def test_analytics_risks_endpoint(client: TestClient):
    response = client.get("/api/analytics/risks")
    assert response.status_code == 200

    payload = response.json()
    assert "high_risk_count" in payload
    assert "distribution" in payload
    assert set(payload["distribution"].keys()) == {"low", "medium", "high"}
