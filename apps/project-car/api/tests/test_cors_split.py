from __future__ import annotations

from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app

BROCHURE = "https://projectcar.ca"
OPS = "https://ops.projectcar.ca"
LOCAL = "http://localhost:3000"


def _preflight(client: TestClient, origin: str, path: str):
    return client.options(path, headers={"Origin": origin, "Access-Control-Request-Method": "POST"})


def test_brochure_waitlist_preflight_is_public() -> None:
    client = TestClient(app)
    response = _preflight(client, BROCHURE, "/waitlist")
    assert response.status_code in {200, 204}
    assert response.headers["access-control-allow-origin"] == BROCHURE
    assert "access-control-allow-credentials" not in response.headers
    assert _preflight(client, BROCHURE, "/members").headers.get("access-control-allow-origin") is None


def test_credentialed_preflight_keeps_credentials() -> None:
    client = TestClient(app)
    for origin in (OPS, LOCAL):
        response = _preflight(client, origin, "/members")
        assert response.headers["access-control-allow-origin"] == origin
        assert response.headers["access-control-allow-credentials"] == "true"


def test_actual_responses(client: TestClient) -> None:
    waitlist = client.post("/waitlist", json={}, headers={"Origin": BROCHURE})
    assert waitlist.headers["access-control-allow-origin"] == BROCHURE
    assert "access-control-allow-credentials" not in waitlist.headers
    denied = client.post("/members", json={}, headers={"Origin": BROCHURE})
    assert denied.headers.get("access-control-allow-origin") is None
    ops = client.post("/members", json={}, headers={"Origin": OPS})
    assert ops.headers["access-control-allow-origin"] == OPS
    assert ops.headers["access-control-allow-credentials"] == "true"


def test_cors_origin_kind() -> None:
    settings = get_settings()
    assert settings.cors_origin_kind(LOCAL) == "credentialed"  # credentialed wins on both lists
    assert settings.cors_origin_kind(BROCHURE) == "public"
    assert settings.cors_origin_kind("https://evil.example") is None
