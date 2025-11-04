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


def test_update_claim_status_endpoint(client: TestClient):
    response = client.put(
        "/api/claims/CLM-001/status",
        json={"status": "denied", "reason": "Documentation missing"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["claim"]["status"] == "denied"
    assert payload["claim"]["denial_reason"] == "Documentation missing"
    quick_stats = payload["quick_stats"]
    assert quick_stats["provider_summary"]
    assert quick_stats["days_pending_label"]


def test_update_claim_status_not_found(client: TestClient):
    response = client.put(
        "/api/claims/UNKNOWN/status",
        json={"status": "approved"},
    )

    assert response.status_code == 404

def test_update_claim_notes_endpoint(client: TestClient):
    response = client.put(
        "/api/claims/CLM-002/notes",
        json={"note": "Reviewed by supervisor"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["claim"]["processor_notes"] == "Reviewed by supervisor"
