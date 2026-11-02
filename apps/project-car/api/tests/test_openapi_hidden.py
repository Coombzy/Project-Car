"""Interactive docs and the OpenAPI document stay off unless SHOP_DEV_MODE=1."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import create_app

_LONG = {
    "OWNER_API_SECRET": "o" * 32,
    "AI_API_SECRET": "a" * 32,
    "SESSION_SECRET": "s" * 32,
    "OWNER_PASSWORD": "long-owner-password",
}


def test_openapi_hidden_in_production(monkeypatch: pytest.MonkeyPatch) -> None:
    for key, value in _LONG.items():
        monkeypatch.setenv(key, value)
    monkeypatch.delenv("SHOP_DEV_MODE", raising=False)
    get_settings.cache_clear()
    try:
        with TestClient(create_app()) as production:
            for path in ("/docs", "/redoc", "/openapi.json"):
                hidden = production.get(path)
                assert hidden.status_code == 404, path
        monkeypatch.setenv("SHOP_DEV_MODE", "1")
        get_settings.cache_clear()
        with TestClient(create_app()) as dev:
            for path in ("/docs", "/redoc", "/openapi.json"):
                shown = dev.get(path)
                assert shown.status_code == 200, path
    finally:
        get_settings.cache_clear()
