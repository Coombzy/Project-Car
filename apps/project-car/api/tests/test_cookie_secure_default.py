"""Session cookies are Secure unless dev mode or COOKIE_SECURE=false opts out."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings


def _set_cookie(response) -> str:
    matches = [
        header
        for header in response.headers.get_list("set-cookie")
        if header.startswith("pc_owner_session=")
    ]
    assert len(matches) == 1, response.headers.get_list("set-cookie")
    return matches[0]


def test_session_cookie_secure_by_default(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    settings = get_settings()
    monkeypatch.delenv("SHOP_DEV_MODE", raising=False)
    monkeypatch.delenv("COOKIE_SECURE", raising=False)
    monkeypatch.setattr(settings, "cookie_secure", None)
    monkeypatch.setattr(settings, "shop_dev_mode", False)
    monkeypatch.setattr(settings, "session_secret", "s" * 32)
    monkeypatch.setattr(settings, "owner_api_secret", "o" * 32)
    monkeypatch.setattr(settings, "ai_api_secret", "a" * 32)
    monkeypatch.setattr(settings, "owner_password", "long-owner-password")

    signed_in = client.post(
        "/auth/login",
        json={"email": settings.owner_email, "password": "long-owner-password"},
    )
    assert signed_in.status_code == 200, signed_in.text
    assert "secure" in _set_cookie(signed_in).lower()

    monkeypatch.setenv("SHOP_DEV_MODE", "1")
    monkeypatch.setattr(settings, "shop_dev_mode", True)
    monkeypatch.setattr(settings, "cookie_secure", None)
    monkeypatch.setattr(settings, "owner_password", "changeme")
    dev_login = client.post(
        "/auth/login",
        json={"email": settings.owner_email, "password": "changeme"},
    )
    assert dev_login.status_code == 200, dev_login.text
    assert "secure" not in _set_cookie(dev_login).lower().split(";", 1)[-1]
