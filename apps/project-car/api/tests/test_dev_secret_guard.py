from __future__ import annotations

from pathlib import Path

import pytest

from app.config import get_settings
from app.main import create_app

LONG = "x" * 40
DEMO = {
    "owner_api_secret": "dev-owner-secret",
    "ai_api_secret": "dev-ai-secret",
    "session_secret": "dev-session-secret-change-me",
    "owner_password": "changeme",
}
WEAK = list(DEMO.items()) + [
    ("owner_api_secret", "z" * 31),
    ("ai_api_secret", "z" * 31),
    ("session_secret", "z" * 31),
    ("owner_password", "z" * 11),
    ("session_secret", "CHANGE_ME" + "a" * 40),
]


@pytest.fixture
def prod_env(monkeypatch):
    """No SHOP_DEV_MODE, strong secrets unless the test overrides one."""
    monkeypatch.delenv("SHOP_DEV_MODE", raising=False)
    for name in DEMO:
        monkeypatch.setenv(name.upper(), "y" * 20 if name == "owner_password" else LONG)
    get_settings.cache_clear()
    yield monkeypatch
    get_settings.cache_clear()


@pytest.mark.parametrize(("name", "value"), WEAK)
def test_weak_secret_refused(prod_env, name, value):
    prod_env.setenv(name.upper(), value)
    with pytest.raises(RuntimeError) as excinfo:
        create_app()
    assert name in str(excinfo.value)
    assert value not in str(excinfo.value)


def test_loopback_bind_is_not_dev_mode(prod_env):
    prod_env.setenv("HOST", "127.0.0.1")
    prod_env.setenv("SESSION_SECRET", DEMO["session_secret"])
    with pytest.raises(RuntimeError, match="session_secret"):
        create_app()


def test_dev_mode_allows_placeholders(monkeypatch):
    for name in DEMO:
        monkeypatch.delenv(name.upper(), raising=False)
    monkeypatch.setenv("SHOP_DEV_MODE", "1")
    get_settings.cache_clear()
    create_app()  # the .env.example placeholders boot under the flag
    get_settings.cache_clear()


def test_env_example_declares_local_dev():
    text = (Path(__file__).resolve().parents[1] / ".env.example").read_text()
    assert "SHOP_DEV_MODE=1" in text
    assert "local dev only" in text.lower()
