"""Per-hour band × overlay × fill reserve quotes (Docs/token-pricing.md).

`banded_tokens = Σ over held hours (100 × that hour's band_multiplier)`
`final_reserve_cost = banded_tokens × advance_multiplier × fill_multiplier`

A booking holds every America/Regina clock hour its span touches
(`iter_regina_hours`), and each held hour is charged in full at the band that
contains it (Ben, 2026-10-30). The lead-time overlay is off
(`LEAD_TIME_OVERLAYS_ENABLED`), so only the Owner-editable `standard` row
applies. Fill is an explicit next-day factor (default 1.0). Cancel / complete
must reuse the locked quote — never re-run this table.

The tuples below are the seeded defaults. `quote_reserve` reads
`pricing_bands` and `pricing_overlays` when a session is passed. A call
without a session keeps those same numbers from the tuples, so a unit test
that never opens the database stays on the locked table.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time, timedelta
from decimal import ROUND_HALF_UP, Decimal

from sqlalchemy.orm import Session

from app.models import PricingBand, PricingOverlay
from app.shop_time import PRICING_TZ, as_utc, iter_regina_hours, shop_now

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

# Ben, D6 + D7: no 7-days-ahead discount and no last-minute surcharge. While
# False every booking takes the `standard` overlay row; the `advance` and
# `last_minute` rows stay stored and editable but price nothing.
LEAD_TIME_OVERLAYS_ENABLED = False

MIXED_BAND_ID = "mixed"
MIXED_BAND_LABEL = "Mixed bands (per hour)"


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
class HourSegment:
    start_at: datetime
    end_at: datetime
    band: Band

    @property
    def band_tokens(self) -> Decimal:
        return BASE_TOKENS_PER_HOUR * self.band.multiplier

    def as_rule(self) -> dict[str, str]:
        return {
            "start_at": self.start_at.isoformat(),
            "end_at": self.end_at.isoformat(),
            "band_id": self.band.id,
            "band_label": self.band.label,
            "band_multiplier": _factor_str(self.band.multiplier),
            "band_tokens": _factor_str(self.band_tokens),
        }


@dataclass(frozen=True)
class ReserveQuote:
    hours: Decimal
    band: Band
    overlay: Overlay
    base_tokens: Decimal
    final_reserve_cost: Decimal
    fill: FillFactor = NO_FILL
    tz: str = PRICING_TZ_NAME
    segments: tuple[HourSegment, ...] = ()

    @property
    def banded_tokens(self) -> Decimal:
        return sum((segment.band_tokens for segment in self.segments), Decimal("0"))

    def as_rule(self) -> dict[str, object]:
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
            "banded_tokens": _factor_str(self.banded_tokens),
            "final_reserve_cost": _money_str(self.final_reserve_cost),
            "tz": self.tz,
            "segments": [segment.as_rule() for segment in self.segments],
        }

    def ledger_meta(self) -> dict[str, dict[str, object]]:
        return {"pricing_rule": self.as_rule()}


def _factor_str(value: Decimal) -> str:
    quantized = value.quantize(MONEY_QUANT, rounding=ROUND_HALF_UP)
    if quantized == quantized.to_integral():
        return str(int(quantized))
    text = format(quantized, "f").rstrip("0").rstrip(".")
    return text or "0"


def _money_str(value: Decimal) -> str:
    return format(value.quantize(MONEY_QUANT, rounding=ROUND_HALF_UP), "f")


BAND_ROWS = (WEEKDAY_DAY, WEEKDAY_EVE, WEEKEND_FRI_EVE, LATE_NIGHT)
OVERLAY_ROWS = (ADVANCE, STANDARD, LAST_MINUTE)
MULTIPLIER_QUANT = Decimal("0.0001")


def _as_band(row: tuple[str, str, Decimal]) -> Band:
    return Band(id=row[0], label=row[1], multiplier=row[2])


def _as_overlay(row: tuple[str, str, Decimal]) -> Overlay:
    return Overlay(id=row[0], label=row[1], multiplier=row[2])


def quantize_multiplier(value: Decimal) -> Decimal:
    quantized = Decimal(value).quantize(MULTIPLIER_QUANT, rounding=ROUND_HALF_UP)
    if quantized <= 0:
        raise PricingError("invalid_multiplier", "Multiplier must be greater than zero.")
    return quantized


def ensure_pricing_settings(session: Session) -> None:
    """Insert any missing band or overlay row at the locked default. Never overwrite."""
    missing = False
    for index, row in enumerate(BAND_ROWS):
        if session.get(PricingBand, row[0]) is None:
            session.add(
                PricingBand(id=row[0], label=row[1], multiplier=row[2], sort_order=index)
            )
            missing = True
    for index, row in enumerate(OVERLAY_ROWS):
        if session.get(PricingOverlay, row[0]) is None:
            session.add(
                PricingOverlay(id=row[0], label=row[1], multiplier=row[2], sort_order=index)
            )
            missing = True
    if missing:
        session.flush()


def _stored_band(session: Session | None, row: tuple[str, str, Decimal]) -> Band:
    if session is None:
        return _as_band(row)
    stored = session.get(PricingBand, row[0])
    if stored is None:
        return _as_band(row)
    return Band(id=stored.id, label=stored.label, multiplier=Decimal(stored.multiplier))


def _stored_overlay(session: Session | None, row: tuple[str, str, Decimal]) -> Overlay:
    if session is None:
        return _as_overlay(row)
    stored = session.get(PricingOverlay, row[0])
    if stored is None:
        return _as_overlay(row)
    return Overlay(id=stored.id, label=stored.label, multiplier=Decimal(stored.multiplier))


def resolve_band(start_at: datetime, *, session: Session | None = None) -> Band:
    """Band that contains the booking start in America/Regina. Half-open intervals."""
    local = as_utc(start_at).astimezone(PRICING_TZ)
    weekday = local.weekday()  # Mon=0
    clock = local.time()

    if weekday == 5:
        return _stored_band(session, WEEKEND_FRI_EVE)
    if weekday == 6:
        if clock < time(21, 0):
            return _stored_band(session, WEEKEND_FRI_EVE)
        return _stored_band(session, LATE_NIGHT)
    if clock < time(8, 0):
        return _stored_band(session, LATE_NIGHT)
    if clock < time(16, 0):
        return _stored_band(session, WEEKDAY_DAY)
    if weekday == 4:
        return _stored_band(session, WEEKEND_FRI_EVE)
    if clock < time(21, 0):
        return _stored_band(session, WEEKDAY_EVE)
    return _stored_band(session, LATE_NIGHT)


def resolve_overlay(
    *,
    start_at: datetime,
    reserved_at: datetime,
    session: Session | None = None,
) -> Overlay:
    """Advance overlay from reserve time → start. Docs/token-pricing.md boundaries."""
    if not LEAD_TIME_OVERLAYS_ENABLED:
        return _stored_overlay(session, STANDARD)
    delta = as_utc(start_at) - as_utc(reserved_at)
    if delta >= timedelta(days=7):
        return _stored_overlay(session, ADVANCE)
    if delta >= timedelta(hours=48):
        return _stored_overlay(session, STANDARD)
    return _stored_overlay(session, LAST_MINUTE)


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
    session: Session | None = None,
) -> ReserveQuote:
    if session is not None:
        ensure_pricing_settings(session)
    duration_hours(start_at, end_at)
    segments = tuple(
        HourSegment(start_at=hour_start, end_at=hour_end, band=resolve_band(hour_start, session=session))
        for hour_start, hour_end in iter_regina_hours(start_at, end_at)
    )
    hours = Decimal(len(segments))
    overlay = resolve_overlay(
        start_at=start_at,
        reserved_at=reserved_at or shop_now(),
        session=session,
    )
    fill_factor = fill or NO_FILL
    base = (hours * BASE_TOKENS_PER_HOUR).quantize(MONEY_QUANT, rounding=ROUND_HALF_UP)
    banded = sum((segment.band_tokens for segment in segments), Decimal("0"))
    final = (banded * overlay.multiplier * fill_factor.multiplier).quantize(
        MONEY_QUANT, rounding=ROUND_HALF_UP
    )
    if final <= 0:
        raise PricingError("invalid_tokens", "Reserved tokens must be greater than zero.")
    return ReserveQuote(
        hours=hours,
        band=_summary_band(segments, banded=banded, base=base),
        overlay=overlay,
        fill=fill_factor,
        base_tokens=base,
        final_reserve_cost=final,
        segments=segments,
    )


def _summary_band(segments: tuple[HourSegment, ...], *, banded: Decimal, base: Decimal) -> Band:
    """The one band every hour shares, or ``mixed`` at the effective multiplier."""
    ids = {segment.band.id for segment in segments}
    if len(ids) == 1:
        return segments[0].band
    return Band(
        id=MIXED_BAND_ID,
        label=MIXED_BAND_LABEL,
        multiplier=(banded / base).quantize(MULTIPLIER_QUANT, rounding=ROUND_HALF_UP),
    )
