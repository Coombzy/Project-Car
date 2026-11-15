"""Tests for calendar OAuth routes (R167)."""

from __future__ import annotations

from unittest.mock import patch

from fastapi.testclient import TestClient

AUTH = {"Authorization": "Bearer dev-owner-secret"}


def test_google_start_returns_200_with_configured_oauth(client: TestClient) -> None:
    """GET /calendar/google/start returns authorize_url when the URL helper returns one."""
    fake_url = "https://accounts.google.com/o/oauth2/v2/auth?client_id=foo&redirect_uri=https%3A%2F%2Fexample.test%2Fcb"

    with patch(
        "app.routers.calendar.google_authorize_url",
        return_value=fake_url,
    ):
        resp = client.get("/calendar/google/start", headers=AUTH)

    assert resp.status_code == 200
    body = resp.json()
    assert body["configured"] is True
    assert body["authorize_url"] == fake_url


def test_google_callback_returns_501(client: TestClient) -> None:
    """GET /calendar/google/callback returns 501 and leaves calendar status unchanged."""
    before = client.get("/calendar/status", headers=AUTH)
    assert before.status_code == 200
    before_body = before.json()

    resp = client.get("/calendar/google/callback")
    assert resp.status_code == 501
    assert resp.json()["error"]["code"] == "calendar_oauth_not_complete"

    after = client.get("/calendar/status", headers=AUTH)
    assert after.status_code == 200
    assert after.json() == before_body


def test_calendar_status_without_auth_returns_401(client: TestClient) -> None:
    """GET /calendar/status without a token returns 401."""
    resp = client.get("/calendar/status")
    assert resp.status_code == 401
    assert resp.json()["error"]["code"] == "unauthorized"
