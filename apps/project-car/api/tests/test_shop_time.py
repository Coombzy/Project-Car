from __future__ import annotations

from datetime import datetime

import pytest

from app.shop_time import PRICING_TZ, SHOP_TZ, pricing_now, shop_now

FROZEN = "2026-10-06T15:00:00-06:00"


def test_shop_now_follows_shop_now_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SHOP_NOW", FROZEN)
    instant = datetime.fromisoformat(FROZEN)
    assert shop_now() == instant.astimezone(SHOP_TZ)
    assert pricing_now() == instant.astimezone(PRICING_TZ)


def test_shop_now_ignores_blank_shop_now_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SHOP_NOW", "  ")
    current = shop_now()
    assert current.tzinfo is not None
    assert abs((datetime.now(SHOP_TZ) - current).total_seconds()) < 5
