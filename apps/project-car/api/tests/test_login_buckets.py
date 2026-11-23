"""Realm+IP login cap, per-account backoff, and shop client IP."""

from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

import app.auth as auth
from app.auth import _account_backoff_seconds
from app.config import get_settings
from tests.test_client_ip import LOGIN_DENIED, LOGIN_LIMIT, _peer

_ENV = ("CLIENT_IP_HEADER", "TRUSTED_PROXIES", "SHOP_PROXY_SECRET")


def _owner(client: TestClient, email: str, headers: dict[str, str] | None = None):
    return client.post(
        "/auth/login",
        json={"email": email, "password": "wrong-guess"},
        headers=headers or {},
    )


def test_realm_ip_window(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    """Eight owner failures lock that realm+IP until the 15 minute window passes."""
    now = {"t": 1_000_000.0}
    monkeypatch.setattr(auth.time, "monotonic", lambda: now["t"])
    with _peer(client, "203.0.113.90"):
        for index in range(8):
            denied = _owner(client, f"w90-{index}@example.com")
            assert denied.status_code == 401, denied.text
            assert denied.json()["error"] == LOGIN_DENIED
        locked = _owner(client, "w90-9@example.com")
        assert locked.status_code == 429, locked.text
        assert locked.json()["error"] == LOGIN_LIMIT
        member = client.post(
            "/auth/member/login",
            json={"email": "w90-m@example.com", "password": "wrong-guess"},
        )
        assert member.status_code == 401, member.text
    with _peer(client, "203.0.113.91"):
        assert _owner(client, "w91@example.com").status_code == 401
    now["t"] += 15 * 60 + 1
    with _peer(client, "203.0.113.90"):
        again = _owner(client, "w90-later@example.com")
        assert again.status_code == 401, again.text


def test_account_backoff(client: TestClient) -> None:
    """Six failures back off the account. A huge streak stays at 15 minutes."""
    assert _account_backoff_seconds(5) == 0
    assert _account_backoff_seconds(6) == 60
    assert _account_backoff_seconds(10) == 15 * 60
    assert _account_backoff_seconds(1024) == 15 * 60
    with _peer(client, "203.0.113.92"):
        for _ in range(6):
            assert _owner(client, "backoff@example.com").status_code == 401
        blocked = _owner(client, "backoff@example.com")
        assert blocked.status_code == 429, blocked.text
        assert blocked.json()["error"] == LOGIN_LIMIT
        assert _owner(client, "backoff-other@example.com").status_code == 401


def test_forwarded_for_and_shop_secret(client: TestClient) -> None:
    """X-Forwarded-For is refused. X-Shop-Client-IP counts only with the secret."""
    previous = {key: os.environ.get(key) for key in _ENV}
    try:
        os.environ["CLIENT_IP_HEADER"] = "X-Forwarded-For"
        get_settings.cache_clear()
        with pytest.raises(ValidationError):
            get_settings()
        os.environ.pop("CLIENT_IP_HEADER", None)
        os.environ["SHOP_PROXY_SECRET"] = "proxy-secret"
        os.environ["TRUSTED_PROXIES"] = ""
        get_settings.cache_clear()
        with _peer(client, "203.0.113.94"):
            for index in range(8):
                denied = _owner(
                    client,
                    f"xff-{index}@example.com",
                    {"X-Forwarded-For": f"198.51.100.{index}"},
                )
                assert denied.status_code == 401, denied.text
            blocked = _owner(
                client, "xff-9@example.com", {"X-Forwarded-For": "198.51.100.99"}
            )
            assert blocked.status_code == 429, blocked.text
        secret = {"X-Shop-Proxy-Secret": "proxy-secret"}
        with _peer(client, "203.0.113.93"):
            for index in range(8):
                headers = {"X-Shop-Client-IP": "198.51.100.50", **secret}
                assert _owner(client, f"shop-{index}@example.com", headers).status_code == 401
            locked_headers = {"X-Shop-Client-IP": "198.51.100.50", **secret}
            assert _owner(client, "shop-9@example.com", locked_headers).status_code == 429
            other = {"X-Shop-Client-IP": "198.51.100.51", **secret}
            assert _owner(client, "shop-b@example.com", other).status_code == 401
            wrong = {"X-Shop-Client-IP": "198.51.100.50", "X-Shop-Proxy-Secret": "nope"}
            assert _owner(client, "shop-wrong@example.com", wrong).status_code == 401
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        get_settings.cache_clear()
