"""AUD-017: --reset only when SHOP_DEV_MODE strips to exactly 1.

settings.shop_dev_mode is not an alternate allow. Login lines name
OWNER_PASSWORD and MEMBER_DEMO_PASSWORD and never print those values.
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest

import app.config as config
from app.seed import main

SENTINEL_OWNER = "sentinel-owner-password-aud017"
SENTINEL_MEMBER = "sentinel-member-password-aud017"

_SUMMARY = {
    "members": 6,
    "hoists": 6,
    "bookings": 1,
    "todos": 1,
    "parts_orders": 1,
    "chat_rooms": 1,
    "waitlist": 1,
    "tiers": 2,
}


def _patch_settings(monkeypatch, *, shop_dev_mode: bool) -> None:
    monkeypatch.setenv("SHOP_HOST", "127.0.0.1")
    monkeypatch.setattr(config.settings, "shop_dev_mode", shop_dev_mode)
    monkeypatch.setattr(config.settings, "owner_password", SENTINEL_OWNER)
    monkeypatch.setattr(config.settings, "member_demo_password", SENTINEL_MEMBER)


def _patch_db(monkeypatch) -> tuple[Mock, Mock]:
    session_local = Mock()
    seed = Mock(return_value=_SUMMARY)
    monkeypatch.setattr("app.seed.SessionLocal", session_local)
    monkeypatch.setattr("app.seed.seed", seed)
    return session_local, seed


def _text(capsys) -> str:
    captured = capsys.readouterr()
    return captured.out + captured.err


def _assert_names_not_secrets(text: str) -> None:
    assert "OWNER_PASSWORD" in text
    assert "MEMBER_DEMO_PASSWORD" in text
    assert SENTINEL_OWNER not in text
    assert SENTINEL_MEMBER not in text


@pytest.mark.parametrize("raw", [None, "", "0", "true", "yes", "01"])
def test_reset_refuses_without_exact_dev_mode(monkeypatch, capsys, raw: str | None) -> None:
    """Unset or non-1 env returns 1, opens no session, and prints no passwords.

    settings.shop_dev_mode stays true so that flag cannot allow the wipe.
    """
    if raw is None:
        monkeypatch.delenv("SHOP_DEV_MODE", raising=False)
    else:
        monkeypatch.setenv("SHOP_DEV_MODE", raw)
    _patch_settings(monkeypatch, shop_dev_mode=True)
    session_local, seed = _patch_db(monkeypatch)

    assert main(["--reset"]) == 1
    session_local.assert_not_called()
    seed.assert_not_called()
    text = _text(capsys)
    assert SENTINEL_OWNER not in text
    assert SENTINEL_MEMBER not in text


@pytest.mark.parametrize("raw", ["1", " 1 ", "\t1\n"])
def test_reset_allows_when_env_strips_to_1(monkeypatch, capsys, raw: str) -> None:
    monkeypatch.setenv("SHOP_DEV_MODE", raw)
    _patch_settings(monkeypatch, shop_dev_mode=False)
    session_local, seed = _patch_db(monkeypatch)

    assert main(["--reset"]) == 0
    session_local.assert_called_once()
    seed.assert_called_once()
    assert seed.call_args.kwargs["reset"] is True
    _assert_names_not_secrets(_text(capsys))


def test_upsert_prints_setting_names_not_passwords(monkeypatch, capsys) -> None:
    monkeypatch.delenv("SHOP_DEV_MODE", raising=False)
    _patch_settings(monkeypatch, shop_dev_mode=True)
    session_local, seed = _patch_db(monkeypatch)

    assert main([]) == 0
    session_local.assert_called_once()
    seed.assert_called_once()
    assert seed.call_args.kwargs["reset"] is False
    _assert_names_not_secrets(_text(capsys))
