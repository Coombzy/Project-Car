from __future__ import annotations

import os

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


def test_docs_drops_csp_when_dev_mode_comes_from_settings_not_os_environ(tmp_path, monkeypatch) -> None:
    """Dev mode comes from a temp env file. os.environ has no SHOP_DEV_MODE."""
    monkeypatch.delenv("SHOP_DEV_MODE", raising=False)
    (tmp_path / ".env").write_text("SHOP_DEV_MODE=1\n")
    monkeypatch.chdir(tmp_path)
    get_settings.cache_clear()
    try:
        assert "SHOP_DEV_MODE" not in os.environ
        assert get_settings().shop_dev_mode is True
        with TestClient(create_app()) as client:
            for path in ("/docs", "/redoc"):
                response = client.get(path)
                assert response.status_code == 200, path
                assert "content-security-policy" not in response.headers, path
            health = client.get("/health")
            for name, value in EXPECTED.items():
                assert health.headers[name] == value, name
    finally:
        get_settings.cache_clear()
