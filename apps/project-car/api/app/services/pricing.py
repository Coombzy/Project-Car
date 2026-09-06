"""Duration × band × overlay × fill reserve quotes (Docs/token-pricing.md).

`base_tokens = hours × 100`
`final_reserve_cost = (hours × 100) × band_multiplier × advance_multiplier × fill_multiplier`

Bands are looked up in America/Regina from the booking **start**. Overlay is
measured at reserve time (now → start). Fill is an explicit next-day factor
(default 1.0) — it does not change locked band / overlay math. Cancel /
complete must reuse the locked quote — never re-run this table.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time, timedelta
from decimal import ROUND_HALF_UP, Decimal

from app.shop_time import PRICING_TZ, as_utc, shop_now

BASE_TOKENS_PER_HOUR = Decimal("100")
PRICING_TZ_NAME = "America/Regina"
HOURS_QUANT = Decimal("0.0001")
MONEY_QUANT = Decimal("0.01")

WEEKDAY_DAY = ("weekday_day", "Weekday day (base)", Decimal("1.00"))
WEEKDAY_EVE = ("weekday_eve", "Weekday evening", Decimal("1.25"))
WEEKEND_FRI_EVE = ("weekend_fri_eve", "Weekend / Fri eve", Decimal("1.50"))
LATE_NIGHT = ("late_night", "Late night / early morning", Decimal("0.75"))

ADVANCE = ("advance", "Advance", Decimal("0.85"))
STANDARD = ("standard", "Standard", Decimal("1.00"))
LAST_MINUTE = ("last_minute", "Last-minute", Decimal("1.25"))


class PricingError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True)
class Band:
    id: str
    label: str
    multiplier: Decimal


@dataclass(frozen=True)
class Overlay:
    id: str
    label: str
    multiplier: Decimal


@dataclass(frozen=True)
class FillFactor:
    id: str
    label: str
    multiplier: Decimal
    discount_pct: Decimal


NO_FILL = FillFactor(
    id="none",
    label="No fill",
    multiplier=Decimal("1.00"),
    discount_pct=Decimal("0"),
)


@dataclass(frozen=True)
class ReserveQuote:
    hours: Decimal
    band: Band
    overlay: Overlay
    base_tokens: Decimal
    final_reserve_cost: Decimal
    fill: FillFactor = NO_FILL
    tz: str = PRICING_TZ_NAME

    def as_rule(self) -> dict[str, str]:
        return {
            "band_id": self.band.id,
            "band_label": self.band.label,
            "band_multiplier": _factor_str(self.band.multiplier),
            "overlay_id": self.overlay.id,
            "overlay_label": self.overlay.label,
            "advance_multiplier": _factor_str(self.overlay.multiplier),
            "fill_id": self.fill.id,
            "fill_label": self.fill.label,
            "fill_multiplier": _factor_str(self.fill.multiplier),
            "fill_discount_pct": _factor_str(self.fill.discount_pct),
            "hours": _factor_str(self.hours),
            "base_tokens": _factor_str(self.base_tokens),
            "final_reserve_cost": _money_str(self.final_reserve_cost),
            "tz": self.tz,
        }

    def ledger_meta(self) -> dict[str, dict[str, str]]:
        return {"pricing_rule": self.as_rule()}


def _factor_str(value: Decimal) -> str:
    quantized = value.quantize(MONEY_QUANT, rounding=ROUND_HALF_UP)
    if quantized == quantized.to_integral():
        return str(int(quantized))
    text = format(quantized, "f").rstrip("0").rstrip(".")
    return text or "0"


def _money_str(value: Decimal) -> str:
    return format(value.quantize(MONEY_QUANT, rounding=ROUND_HALF_UP), "f")


def _as_band(row: tuple[str, str, Decimal]) -> Band:
    return Band(id=row[0], label=row[1], multiplier=row[2])


def _as_overlay(row: tuple[str, str, Decimal]) -> Overlay:
    return Overlay(id=row[0], label=row[1], multiplier=row[2])


def resolve_band(start_at: datetime) -> Band:
    """Band that contains the booking start in America/Regina. Half-open intervals."""
    local = as_utc(start_at).astimezone(PRICING_TZ)
    weekday = local.weekday()  # Mon=0
    clock = local.time()

    if weekday == 5:
        return _as_band(WEEKEND_FRI_EVE)
    if weekday == 6:
        if clock < time(21, 0):
            return _as_band(WEEKEND_FRI_EVE)
        return _as_band(LATE_NIGHT)
    if clock < time(8, 0):
        return _as_band(LATE_NIGHT)
    if clock < time(16, 0):
        return _as_band(WEEKDAY_DAY)
    if weekday == 4:
        return _as_band(WEEKEND_FRI_EVE)
    if clock < time(21, 0):
        return _as_band(WEEKDAY_EVE)
    return _as_band(LATE_NIGHT)


def resolve_overlay(*, start_at: datetime, reserved_at: datetime) -> Overlay:
    """Advance overlay from reserve time → start. Docs/token-pricing.md boundaries."""
    delta = as_utc(start_at) - as_utc(reserved_at)
    if delta >= timedelta(days=7):
        return _as_overlay(ADVANCE)
    if delta >= timedelta(hours=48):
        return _as_overlay(STANDARD)
    return _as_overlay(LAST_MINUTE)


def duration_hours(start_at: datetime, end_at: datetime) -> Decimal:
    start_at = as_utc(start_at)
    end_at = as_utc(end_at)
    if end_at <= start_at:
        raise PricingError("invalid_window", "Booking end must be after start.")
    seconds = Decimal(str((end_at - start_at).total_seconds()))
    hours = seconds / Decimal("3600")
    return hours.quantize(HOURS_QUANT, rounding=ROUND_HALF_UP)


def quote_reserve(
    start_at: datetime,
    end_at: datetime,
    *,
    reserved_at: datetime | None = None,
    fill: FillFactor | None = None,
) -> ReserveQuote:
    hours = duration_hours(start_at, end_at)
    band = resolve_band(start_at)
    overlay = resolve_overlay(start_at=start_at, reserved_at=reserved_at or shop_now())
    fill_factor = fill or NO_FILL
    base = (hours * BASE_TOKENS_PER_HOUR).quantize(MONEY_QUANT, rounding=ROUND_HALF_UP)
    final = (base * band.multiplier * overlay.multiplier * fill_factor.multiplier).quantize(
        MONEY_QUANT, rounding=ROUND_HALF_UP
    )
    if final <= 0:
        raise PricingError("invalid_tokens", "Reserved tokens must be greater than zero.")
    return ReserveQuote(
        hours=hours,
        band=band,
        overlay=overlay,
        fill=fill_factor,
        base_tokens=base,
        final_reserve_cost=final,
    )
