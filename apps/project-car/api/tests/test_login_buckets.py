"""Login failures are counted per realm and per account, not one global bucket.

CLIENT_IP_HEADER is ignored unless the TCP peer is a trusted proxy.
X-Shop-Client-IP counts only when X-Shop-Proxy-Secret matches.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import create_app

PROXY_SECRET = "p" * 32
WRONG = "wrong-guess"


def _peer(client: TestClient, host: str):
    transport = client._transport
    previous = transport.client
    transport.client = (host, 50000)
    return previous


def _restore_peer(client: TestClient, previous) -> None:
    client._transport.client = previous


def test_member_failures_do_not_lock_owner(client: TestClient) -> None:
    for index in range(8):
        denied = client.post(
            "/auth/member/login",
            json={"email": f"member-{index}@example.com", "password": WRONG},
        )
        assert denied.status_code == 401, denied.text
    owner = client.post(
        "/auth/login",
        json={"email": "owner@projectcar.ca", "password": WRONG},
    )
    assert owner.status_code == 401, owner.text
    assert owner.json()["error"]["code"] == "invalid_credentials"


def test_web_login_buckets_are_per_end_user(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    settings = get_settings()
    monkeypatch.setattr(settings, "shop_proxy_secret", PROXY_SECRET)
    headers_a = {"X-Shop-Client-IP": "198.51.100.10", "X-Shop-Proxy-Secret": PROXY_SECRET}
    for index in range(8):
        denied = client.post(
            "/auth/login",
            json={"email": f"stuff-{index}@example.com", "password": WRONG},
            headers=headers_a,
        )
        assert denied.status_code == 401, denied.text
    locked = client.post(
        "/auth/login",
        json={"email": "stuff-9@example.com", "password": WRONG},
        headers=headers_a,
    )
    assert locked.status_code == 429, locked.text
    headers_b = {"X-Shop-Client-IP": "198.51.100.11", "X-Shop-Proxy-Secret": PROXY_SECRET}
    other = client.post(
        "/auth/login",
        json={"email": "other@example.com", "password": WRONG},
        headers=headers_b,
    )
    assert other.status_code == 401, other.text


def test_owner_account_backoff_across_ips(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """One owner email locks even when every attempt comes from a different IP."""
    monkeypatch.setenv("CLIENT_IP_HEADER", "X-Test-Client-IP")
    monkeypatch.setenv("TRUSTED_PROXIES", "203.0.113.90")
    get_settings.cache_clear()
    previous = _peer(client, "203.0.113.90")
    saw_limited = False
    try:
        for index in range(40):
            response = client.post(
                "/auth/login",
                json={"email": "owner@projectcar.ca", "password": WRONG},
                headers={"X-Test-Client-IP": f"198.51.100.{index}"},
            )
            if response.status_code == 429:
                saw_limited = True
                assert response.json()["error"]["code"] == "rate_limited"
                break
            assert response.status_code == 401, response.text
        assert saw_limited
    finally:
        _restore_peer(client, previous)
        get_settings.cache_clear()


def test_client_ip_header_ignored_without_proxy_secret(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A spoofed shop client IP does not split buckets when the secret is absent."""
    settings = get_settings()
    monkeypatch.setattr(settings, "shop_proxy_secret", PROXY_SECRET)
    previous = _peer(client, "203.0.113.80")
    try:
        for index in range(8):
            denied = client.post(
                "/auth/login",
                json={"email": f"spoof-{index}@example.com", "password": WRONG},
                headers={"X-Shop-Client-IP": "198.51.100.20"},
            )
            assert denied.status_code == 401, denied.text
        other = client.post(
            "/auth/login",
            json={"email": "spoof-other@example.com", "password": WRONG},
            headers={"X-Shop-Client-IP": "198.51.100.21"},
        )
        assert other.status_code == 429, other.text
    finally:
        _restore_peer(client, previous)


def test_client_ip_header_ignored_from_untrusted_peer(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("CLIENT_IP_HEADER", "X-Test-Client-IP")
    monkeypatch.setenv("TRUSTED_PROXIES", "127.0.0.1,::1")
    get_settings.cache_clear()
    previous = _peer(client, "203.0.113.81")
    try:
        for _ in range(8):
            denied = client.post(
                "/auth/login",
                json={"email": f"peer-{_}@example.com", "password": WRONG},
                headers={"X-Test-Client-IP": "198.51.100.30"},
            )
            assert denied.status_code == 401, denied.text
        other = client.post(
            "/auth/login",
            json={"email": "peer-other@example.com", "password": WRONG},
            headers={"X-Test-Client-IP": "198.51.100.31"},
        )
        assert other.status_code == 429, other.text
    finally:
        _restore_peer(client, previous)
        get_settings.cache_clear()


def test_xff_rejected_as_client_ip_header_at_startup(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SHOP_DEV_MODE", "1")
    monkeypatch.setenv("CLIENT_IP_HEADER", "X-Forwarded-For")
    get_settings.cache_clear()
    try:
        with pytest.raises(RuntimeError, match="X-Forwarded-For"):
            create_app()
    finally:
        get_settings.cache_clear()
