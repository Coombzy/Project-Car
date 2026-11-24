from __future__ import annotations

from fastapi.testclient import TestClient

from app.config import get_settings

OWNER = {"email": "owner@projectcar.ca", "password": "changeme"}


def test_default_owner_password_rejected_without_dev_mode(
    client: TestClient, monkeypatch
) -> None:
    monkeypatch.delenv("SHOP_DEV_MODE", raising=False)
    get_settings.cache_clear()
    assert get_settings().shop_dev_mode is False
    denied = client.post("/auth/login", json=OWNER)
    assert denied.status_code == 401, denied.text
    assert denied.json()["error"]["code"] == "invalid_credentials"


def test_default_owner_password_accepted_when_shop_dev_mode(
    client: TestClient, monkeypatch
) -> None:
    monkeypatch.setenv("SHOP_DEV_MODE", "1")
    get_settings.cache_clear()
    assert get_settings().shop_dev_mode is True
    try:
        accepted = client.post("/auth/login", json=OWNER)
    finally:
        get_settings.cache_clear()
    assert accepted.status_code == 200, accepted.text
    assert accepted.json()["role"] == "owner"
