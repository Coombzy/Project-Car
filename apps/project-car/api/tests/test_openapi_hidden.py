from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import create_app

LONG = "x" * 40
PATHS = ("/docs", "/redoc", "/openapi.json")


@pytest.fixture
def prod_env(monkeypatch):
    """Strong secrets so only the docs flag is under test."""
    for name in ("OWNER_API_SECRET", "AI_API_SECRET", "SESSION_SECRET", "OWNER_PASSWORD", "MEMBER_DEMO_PASSWORD"):
        monkeypatch.setenv(name, LONG)
    monkeypatch.delenv("SHOP_DEV_MODE", raising=False)
    get_settings.cache_clear()
    yield monkeypatch
    get_settings.cache_clear()


@pytest.mark.parametrize("path", PATHS)
def test_docs_hidden_without_dev_mode(prod_env, path):
    assert TestClient(create_app()).get(path).status_code == 404


def test_docs_served_in_dev_mode(prod_env):
    prod_env.setenv("SHOP_DEV_MODE", "1")
    client = TestClient(create_app())
    for path in PATHS:
        assert client.get(path).status_code == 200
