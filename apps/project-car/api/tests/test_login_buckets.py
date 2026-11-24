from __future__ import annotations
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from app.auth import _account_backoff_seconds, _account_failures, _account_key
from app.config import Settings, get_settings
from tests.test_client_ip import _peer
OWNER = {"email": "owner@projectcar.ca", "password": "wrong-guess"}
MEMBER = {"email": "nobody-realm@example.com", "password": "wrong-guess"}
def _hit(client: TestClient, path: str, host: str, headers: dict | None = None, body: dict | None = None) -> int:
    with _peer(client, host):
        return client.post(path, json=OWNER if body is None else body, headers=headers).status_code
def test_realm_ip_window(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    clock = {"now": 5000.0}
    monkeypatch.setattr("app.auth.time.monotonic", lambda: clock["now"])
    ip = "203.0.113.80"
    # Distinct emails: one account locks at six, the IP cap stays at eight.
    window = [
        _hit(client, "/auth/login", ip, body={"email": f"window{i}@example.com", "password": "wrong-guess"})
        for i in range(8)
    ]
    assert window == [401] * 8
    assert _hit(client, "/auth/login", ip) == 429
    assert _hit(client, "/auth/member/login", ip, body=MEMBER) == 401
    assert _hit(client, "/auth/login", "203.0.113.81") == 401
    clock["now"] += 15 * 60 + 1
    assert _hit(client, "/auth/login", ip) == 401
def test_forwarded_for_and_shop_secret(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    secret = "shop-secret-value"
    def shop(address: str, token: str = secret) -> dict[str, str]:
        return {"X-Shop-Proxy-Secret": token, "X-Shop-Client-IP": address}
    try:
        monkeypatch.setenv("CLIENT_IP_HEADER", "X-Forwarded-For")
        with pytest.raises(ValidationError):
            Settings()
        monkeypatch.delenv("CLIENT_IP_HEADER")
        get_settings.cache_clear()
        peer = "203.0.113.90"
        sent = [
            _hit(
                client,
                "/auth/login",
                peer,
                {"X-Forwarded-For": f"198.51.100.{i}"},
                {"email": f"fwd{i}@example.com", "password": "wrong-guess"},
            )
            for i in range(8)
        ]
        assert sent == [401] * 8
        assert _hit(client, "/auth/login", peer, {"X-Forwarded-For": "198.51.100.50"}) == 429
        monkeypatch.setenv("SHOP_PROXY_SECRET", secret)
        get_settings.cache_clear()
        locked = "198.51.100.40"
        assert [
            _hit(
                client,
                "/auth/login",
                "203.0.113.91",
                shop(locked),
                {"email": f"shop{i}@example.com", "password": "wrong-guess"},
            )
            for i in range(8)
        ] == [401] * 8
        assert _hit(client, "/auth/login", "203.0.113.91", shop(locked)) == 429
        assert _hit(client, "/auth/login", "203.0.113.91", shop("198.51.100.41")) == 401
        wrong = shop("198.51.100.77", "nope")
        assert [
            _hit(
                client,
                "/auth/login",
                "203.0.113.92",
                wrong,
                {"email": f"bad{i}@example.com", "password": "wrong-guess"},
            )
            for i in range(8)
        ] == [401] * 8
        assert _hit(client, "/auth/login", "203.0.113.92", wrong) == 429
        assert _hit(client, "/auth/login", "203.0.113.93", shop("198.51.100.77")) == 401
    finally:
        get_settings.cache_clear()
def test_account_backoff(client: TestClient) -> None:
    assert _account_backoff_seconds(5) == 0
    assert _account_backoff_seconds(6) == 60
    assert _account_backoff_seconds(10) == 15 * 60
    assert _account_backoff_seconds(1024) == 15 * 60
    ip = "203.0.113.92"
    body = {"email": "backoff@example.com", "password": "wrong-guess"}
    other = {"email": "backoff-other@example.com", "password": "wrong-guess"}
    assert [_hit(client, "/auth/login", ip, body=body) for _ in range(6)] == [401] * 6
    assert _hit(client, "/auth/login", ip, body=body) == 429
    assert _hit(client, "/auth/login", ip, body=other) == 401


def test_account_backoff_expires(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    clock = {"now": 8000.0}
    monkeypatch.setattr("app.auth.time.monotonic", lambda: clock["now"])
    ip = "203.0.113.94"
    body = {"email": "expire@example.com", "password": "wrong-guess"}
    assert [_hit(client, "/auth/login", ip, body=body) for _ in range(6)] == [401] * 6
    assert _hit(client, "/auth/login", ip, body=body) == 429
    clock["now"] += 60 + 1
    assert _hit(client, "/auth/login", ip, body=body) == 401
    assert _account_failures[_account_key("owner", "expire@example.com")][0] == 7
    assert _hit(client, "/auth/login", ip, body=body) == 429
    clock["now"] += 120
    assert _hit(client, "/auth/login", ip, body=body) == 401
