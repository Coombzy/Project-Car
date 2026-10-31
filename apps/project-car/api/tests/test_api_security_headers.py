"""Every API response carries the security headers. Dev docs omit CSP only."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import create_app

EXPECTED = {
    "x-content-type-options": "nosniff",
    "strict-transport-security": "max-age=31536000; includeSubDomains",
    "referrer-policy": "no-referrer",
    "x-frame-options": "DENY",
    "content-security-policy": "default-src 'none'; frame-ancestors 'none'",
}


def _assert_headers(response, *, csp: bool) -> None:
    for name, value in EXPECTED.items():
        if name == "content-security-policy" and not csp:
            assert response.headers.get(name) is None
            continue
        assert response.headers.get(name) == value


def test_health_404_and_401_carry_security_headers(client: TestClient) -> None:
    health = client.get("/health")
    assert health.status_code == 200, health.text
    _assert_headers(health, csp=True)

    missing = client.get("/not-a-route")
    assert missing.status_code == 404
    _assert_headers(missing, csp=True)

    denied = client.get("/me")
    assert denied.status_code == 401
    _assert_headers(denied, csp=True)


def test_dev_docs_omit_csp(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SHOP_DEV_MODE", "1")
    get_settings.cache_clear()
    try:
        with TestClient(create_app()) as dev:
            docs = dev.get("/docs")
            assert docs.status_code == 200, docs.text
            _assert_headers(docs, csp=False)
    finally:
        get_settings.cache_clear()
