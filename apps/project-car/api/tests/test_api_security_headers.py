from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app, create_app

EXPECTED = {
    "x-content-type-options": "nosniff",
    "strict-transport-security": "max-age=31536000; includeSubDomains",
    "referrer-policy": "no-referrer",
    "x-frame-options": "DENY",
    "content-security-policy": "default-src 'none'; frame-ancestors 'none'",
}


def test_every_response_carries_the_five_headers() -> None:
    with TestClient(app) as client:
        for path in ("/health", "/not-a-route"):
            response = client.get(path)
            for name, value in EXPECTED.items():
                assert response.headers[name] == value, (path, name)


def test_dev_docs_keep_headers_but_drop_csp(monkeypatch) -> None:
    monkeypatch.setenv("SHOP_DEV_MODE", "1")
    with TestClient(create_app()) as client:
        for path in ("/docs", "/redoc"):
            response = client.get(path)
            assert response.status_code == 200, path
            assert "content-security-policy" not in response.headers, path
            for name, value in EXPECTED.items():
                if name != "content-security-policy":
                    assert response.headers[name] == value, (path, name)


def test_docs_keep_csp_without_dev_mode(monkeypatch) -> None:
    monkeypatch.delenv("SHOP_DEV_MODE", raising=False)
    with TestClient(create_app()) as client:
        assert "content-security-policy" in client.get("/docs").headers
