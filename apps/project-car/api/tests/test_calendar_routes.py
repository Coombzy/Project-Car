"""Tests for calendar OAuth routes (R167)."""

from __future__ import annotations

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.config import Settings
from app.main import app
from app.services.calendar_oauth import google_authorize_url


def test_google_start_returns_200_with_configured_oauth(client: TestClient) -> None:
    """GET /calendar/google/start returns authorize_url and configured:true when env is set."""
    fake_url = "https://accounts.google.com/o/oauth2/v2/auth?client_id=foo&redirect_uri=https%3A%2F%2Fexample.test%2Fcb"

    with patch.object(
        app,
        "dependency_overrides",
        {**app.dependency_overrides},
    ):
        # Patch google_authorize_url at the module where it is looked up by the router
        with patch(
            "app.routers.calendar.google_authorize_url",
            return_value=fake_url,
        ):
            resp = client.get("/calendar/google/start", headers={"Authorization": "Bearer dev-owner-secret"})

    assert resp.status_code == 200
    body = resp.json()
    assert body["configured"] is True
    assert body["authorize_url"] == fake_url


def test_google_callback_returns_501(client: TestClient) -> None:
    """GET /calendar/google/callback returns 501 and does not change status."""
    resp = client.get("/calendar/google/callback")
    assert resp.status_code == 501
    assert resp.json()["error"]["code"] == "calendar_oauth_not_complete"


def test_calendar_status_without_auth_returns_401(client: TestClient) -> None:
    """GET /calendar/status without a token returns 401."""
    resp = client.get("/calendar/status")
    assert resp.status_code == 401
    assert resp.json()["error"]["code"] == "unauthorized"
