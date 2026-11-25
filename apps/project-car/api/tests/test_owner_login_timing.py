"""Owner login pays one scrypt for unknown, demo, wrong, and accepted passwords."""

from __future__ import annotations

import hashlib

from fastapi.testclient import TestClient

from app.config import get_settings

_WRONG_PASSWORD = "wrong-password"
_OWNER_EMAIL = "owner@projectcar.ca"
_DEMO_PASSWORD = "changeme"


def _login(client: TestClient, email: str, password: str):
    return client.post("/auth/login", json={"email": email, "password": password})


class _ScryptCounter:
    def __init__(self) -> None:
        self.calls = 0
        self._real = hashlib.scrypt

    def install(self, monkeypatch) -> None:
        real = self._real

        def wrapped(*args, **kwargs):
            self.calls += 1
            return real(*args, **kwargs)

        monkeypatch.setattr(hashlib, "scrypt", wrapped)


def test_owner_login_scrypt_call_counts(client: TestClient, monkeypatch) -> None:
    """Unknown, default-demo, wrong, and accepted owner logins each scrypt once.

    The default demo password is still rejected when shop dev mode is off, and
    accepted for the owner email when shop dev mode is on.
    """
    counter = _ScryptCounter()
    counter.install(monkeypatch)

    unknown = _login(client, "nobody@example.com", _WRONG_PASSWORD)
    assert unknown.status_code == 401
    assert counter.calls == 1

    monkeypatch.delenv("SHOP_DEV_MODE", raising=False)
    get_settings.cache_clear()
    assert get_settings().shop_dev_mode is False
    counter.calls = 0
    demo_denied = _login(client, _OWNER_EMAIL, _DEMO_PASSWORD)
    assert demo_denied.status_code == 401
    assert demo_denied.json()["error"]["code"] == "invalid_credentials"
    assert counter.calls == 1

    monkeypatch.setenv("SHOP_DEV_MODE", "1")
    get_settings.cache_clear()
    assert get_settings().shop_dev_mode is True
    counter.calls = 0
    try:
        accepted = _login(client, _OWNER_EMAIL, _DEMO_PASSWORD)
    finally:
        get_settings.cache_clear()
    assert accepted.status_code == 200, accepted.text
    assert accepted.json()["role"] == "owner"
    assert counter.calls == 1

    counter.calls = 0
    rejected = _login(client, _OWNER_EMAIL, _WRONG_PASSWORD)
    assert rejected.status_code == 401
    assert counter.calls == 1
