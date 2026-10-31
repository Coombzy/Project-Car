"""Startup refuses dev secrets unless SHOP_DEV_MODE is on.

Loopback is not dev. The tunnel binds 127.0.0.1 and must not keep the defaults.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from app.config import get_settings
from app.main import create_app

EXAMPLE = Path(__file__).resolve().parents[1] / ".env.example"

_LONG = {
    "OWNER_API_SECRET": "o" * 32,
    "AI_API_SECRET": "a" * 32,
    "SESSION_SECRET": "s" * 32,
    "OWNER_PASSWORD": "long-owner-password",
    "MEMBER_DEMO_PASSWORD": "long-member-password",
    "SHOP_PROXY_SECRET": "",
}


def _production_env(monkeypatch: pytest.MonkeyPatch, **overrides: str) -> None:
    monkeypatch.delenv("SHOP_DEV_MODE", raising=False)
    for key, value in {**_LONG, **overrides}.items():
        if value == "":
            monkeypatch.delenv(key, raising=False)
        else:
            monkeypatch.setenv(key, value)
    get_settings.cache_clear()


def _assert_refused(name: str, secret: str) -> None:
    with pytest.raises(RuntimeError) as caught:
        create_app()
    message = str(caught.value)
    assert name in message
    assert secret not in message


def test_app_refuses_to_start_with_default_secrets(monkeypatch: pytest.MonkeyPatch) -> None:
    """Each known default is refused with the host unset and on loopback."""
    defaults = {
        "OWNER_API_SECRET": "dev-owner-secret",
        "AI_API_SECRET": "dev-ai-secret",
        "SESSION_SECRET": "dev-session-secret-change-me",
    }
    names = {
        "OWNER_API_SECRET": "owner_api_secret",
        "AI_API_SECRET": "ai_api_secret",
        "SESSION_SECRET": "session_secret",
    }
    try:
        for host in (None, "127.0.0.1"):
            for key, secret in defaults.items():
                if host is None:
                    monkeypatch.delenv("SHOP_HOST", raising=False)
                else:
                    monkeypatch.setenv("SHOP_HOST", host)
                _production_env(monkeypatch, **{key: secret})
                _assert_refused(names[key], secret)
    finally:
        get_settings.cache_clear()


def test_short_secret_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    secret = "x" * 31
    try:
        _production_env(monkeypatch, SESSION_SECRET=secret)
        _assert_refused("session_secret", secret)
    finally:
        get_settings.cache_clear()


def test_short_owner_password_refused_at_startup(monkeypatch: pytest.MonkeyPatch) -> None:
    secret = "y" * 11
    try:
        _production_env(monkeypatch, OWNER_PASSWORD=secret)
        _assert_refused("owner_password", secret)
    finally:
        get_settings.cache_clear()


def test_default_demo_owner_password_refused_at_startup(monkeypatch: pytest.MonkeyPatch) -> None:
    try:
        _production_env(monkeypatch, OWNER_PASSWORD="changeme")
        _assert_refused("owner_password", "changeme")
    finally:
        get_settings.cache_clear()


def test_dev_mode_allows_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    """Dev mode boots the known defaults on loopback and on a public host."""
    try:
        for host in ("127.0.0.1", "projectcar.ca"):
            monkeypatch.setenv("SHOP_DEV_MODE", "1")
            monkeypatch.setenv("SHOP_HOST", host)
            monkeypatch.setenv("OWNER_API_SECRET", "dev-owner-secret")
            monkeypatch.setenv("AI_API_SECRET", "dev-ai-secret")
            monkeypatch.setenv("SESSION_SECRET", "dev-session-secret-change-me")
            monkeypatch.setenv("OWNER_PASSWORD", "changeme")
            get_settings.cache_clear()
            create_app()
    finally:
        get_settings.cache_clear()


def test_env_example_placeholders_fail_check(monkeypatch: pytest.MonkeyPatch) -> None:
    """`.env.example` is dev-only. Dropping SHOP_DEV_MODE makes those values fail."""
    values: dict[str, str] = {}
    for line in EXAMPLE.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, _, value = stripped.partition("=")
        values[key] = value
    assert values.get("SHOP_DEV_MODE") == "1"
    assert any("local dev only" in line.lower() for line in EXAMPLE.read_text().splitlines())
    try:
        for key, value in values.items():
            if key == "SHOP_DEV_MODE":
                continue
            monkeypatch.setenv(key, value)
        monkeypatch.delenv("SHOP_DEV_MODE", raising=False)
        get_settings.cache_clear()
        with pytest.raises(RuntimeError, match="insecure default secret"):
            create_app()
        monkeypatch.setenv("SHOP_DEV_MODE", "1")
        get_settings.cache_clear()
        create_app()
    finally:
        get_settings.cache_clear()
