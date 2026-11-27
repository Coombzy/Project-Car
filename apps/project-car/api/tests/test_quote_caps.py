"""AUD-045: quote_reserve stand-in caps run before hour segments."""

from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import patch

import pytest

from app.services.pricing import PricingError, quote_reserve
from app.shop_time import PRICING_TZ

START = datetime(2026, 9, 8, 10, tzinfo=PRICING_TZ)


def _end(hours: int = 1, *, days: int = 0) -> datetime:
    return START + timedelta(days=days, hours=hours)


def test_member_over_cap_rejects_before_segments() -> None:
    with patch("app.services.pricing.iter_regina_hours") as hours:
        with pytest.raises(PricingError) as caught:
            quote_reserve(START, _end(13), reserved_at=START, kind="member")
        hours.assert_not_called()
    assert caught.value.code == "booking_too_long"


def test_member_at_cap_and_shop_bounds() -> None:
    quote = quote_reserve(START, _end(12), reserved_at=START, kind="member")
    assert quote.hours == Decimal(12)
    with patch("app.services.pricing.iter_regina_hours") as hours:
        with pytest.raises(PricingError) as caught:
            quote_reserve(START, _end(25), reserved_at=START, kind="shop")
        hours.assert_not_called()
    assert caught.value.code == "booking_too_long"
    shop = quote_reserve(START, _end(24), reserved_at=START, kind="shop")
    assert shop.hours == Decimal(24)


def test_member_lead_time_cap() -> None:
    far = START + timedelta(days=61)
    with patch("app.services.pricing.iter_regina_hours") as hours:
        with pytest.raises(PricingError) as caught:
            quote_reserve(far, far + timedelta(hours=1), reserved_at=START, kind="member")
        hours.assert_not_called()
    assert caught.value.code == "booking_too_far_ahead"
    ok = START + timedelta(days=60)
    quote = quote_reserve(ok, ok + timedelta(hours=1), reserved_at=START, kind="member")
    assert quote.hours == Decimal(1)


def test_omitted_kind_quotes_thirteen_hours() -> None:
    quote = quote_reserve(START, _end(13), reserved_at=START)
    assert quote.hours == Decimal(13)
