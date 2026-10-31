"""The login route does not accept the default demo owner password outside dev."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings


def test_login_rejects_default_owner_password_outside_dev(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    settings = get_settings()
    monkeypatch.setattr(settings, "session_secret", "s" * 32)
    monkeypatch.setattr(settings, "owner_api_secret", "o" * 32)
    monkeypatch.setattr(settings, "ai_api_secret", "a" * 32)
    monkeypatch.setattr(settings, "owner_password", "changeme")

    monkeypatch.setenv("SHOP_DEV_MODE", "1")
    allowed = client.post(
        "/auth/login",
        json={"email": settings.owner_email, "password": "changeme"},
    )
    assert allowed.status_code == 200, allowed.text

    monkeypatch.delenv("SHOP_DEV_MODE", raising=False)
    refused = client.post(
        "/auth/login",
        json={"email": settings.owner_email, "password": "changeme"},
    )
    assert refused.status_code == 401, refused.text
    assert refused.json()["error"]["code"] == "invalid_credentials"
    assert "changeme" not in refused.text

    monkeypatch.setattr(settings, "owner_password", "long-owner-password")
    signed_in = client.post(
        "/auth/login",
        json={"email": settings.owner_email, "password": "long-owner-password"},
    )
    assert signed_in.status_code == 200, signed_in.text
