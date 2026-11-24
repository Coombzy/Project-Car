from __future__ import annotations

from datetime import datetime

import pytest

from app.shop_time import PRICING_TZ, SHOP_TZ, pricing_now, shop_now

FROZEN = "2026-10-06T15:00:00-06:00"


def test_shop_now_refused_without_dev_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SHOP_NOW", FROZEN)
    for dev_mode in (None, "", "0", "true", "yes"):
        if dev_mode is None:
            monkeypatch.delenv("SHOP_DEV_MODE", raising=False)
        else:
            monkeypatch.setenv("SHOP_DEV_MODE", dev_mode)
        for clock in (shop_now, pricing_now):
            with pytest.raises(RuntimeError, match="SHOP_NOW") as caught:
                clock()
            message = str(caught.value)
            assert FROZEN not in message
            assert "2026-10-06" not in message
            assert "15:00" not in message


def test_shop_now_follows_shop_now_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SHOP_DEV_MODE", "1")
    monkeypatch.setenv("SHOP_NOW", FROZEN)
    instant = datetime.fromisoformat(FROZEN)
    assert shop_now() == instant.astimezone(SHOP_TZ)
    assert pricing_now() == instant.astimezone(PRICING_TZ)


def test_shop_now_ignores_blank_shop_now_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SHOP_NOW", "  ")
    current = shop_now()
    assert current.tzinfo is not None
    assert abs((datetime.now(SHOP_TZ) - current).total_seconds()) < 5
