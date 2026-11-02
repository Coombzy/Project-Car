"""Next-day customer-bay openings and the fill-the-gaps discount.

Shop calendar is America/Regina. The shop hoist is excluded. Fill is an
explicit pricing factor on top of locked band × overlay math
(`Docs/token-pricing.md`). More open bay-hours → a higher discount, clamped
to the Owner-configurable 10–25% band.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time
from decimal import ROUND_HALF_UP, Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.config import Settings, get_settings
from app.models import (
    Booking,
    BookingStatus,
    FillOffer,
    FillOfferStatus,
    Hoist,
    HoistStatus,
)
from app.services.pricing import MONEY_QUANT, NO_FILL, FillFactor, duration_hours
from app.shop_time import as_utc, pricing_clock_window, pricing_next_day

FILL_TZ_NAME = "America/Regina"
HOURS_QUANT = Decimal("0.0001")
DEFAULT_MIN_DISCOUNT = Decimal("10")
DEFAULT_MAX_DISCOUNT = Decimal("25")
DEFAULT_DAY_START = time(8, 0)
DEFAULT_DAY_END = time(21, 0)
UNAVAILABLE_HOIST = (HoistStatus.MAINTENANCE, HoistStatus.LOCKED)
OCCUPYING = (BookingStatus.PENDING, BookingStatus.CONFIRMED, BookingStatus.ACTIVE)


class FillError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True)
class Gap:
    hoist_id: UUID
    hoist_name: str
    start_at: datetime
    end_at: datetime
    hours: Decimal


@dataclass(frozen=True)
class FillSnapshot:
    target_date: date
    tz: str
    window_start: datetime
    window_end: datetime
    bay_count: int
    capacity_hours: Decimal
    booked_hours: Decimal
    open_hours: Decimal
    open_ratio: Decimal
    discount_pct: Decimal
    fill_multiplier: Decimal
    urgency: str
    applies: bool
    gaps: list[Gap]
    offer_id: UUID | None = None
    source: str = "none"

    def as_factor(self) -> FillFactor:
        if not self.applies:
            return NO_FILL
        return FillFactor(
            id="next_day_open",
            label=f"Fill the gaps {discount_label(self.discount_pct)}%",
            multiplier=self.fill_multiplier,
            discount_pct=self.discount_pct,
        )


def parse_clock(value: str, *, fallback: time) -> time:
    text = (value or "").strip()
    if not text:
        return fallback
    try:
        hour_text, minute_text = text.split(":", 1)
        return time(int(hour_text), int(minute_text))
    except (TypeError, ValueError):
        return fallback


def fill_window_clocks(settings: Settings | None = None) -> tuple[time, time]:
    cfg = settings or get_settings()
    start = parse_clock(cfg.fill_day_start, fallback=DEFAULT_DAY_START)
    end = parse_clock(cfg.fill_day_end, fallback=DEFAULT_DAY_END)
    if end <= start:
        return DEFAULT_DAY_START, DEFAULT_DAY_END
    return start, end


def discount_bounds(settings: Settings | None = None) -> tuple[Decimal, Decimal]:
    cfg = settings or get_settings()
    minimum = Decimal(str(cfg.fill_min_discount_pct))
    maximum = Decimal(str(cfg.fill_max_discount_pct))
    if minimum < 0:
        minimum = Decimal("0")
    if maximum > 100:
        maximum = Decimal("100")
    if maximum < minimum:
        minimum, maximum = DEFAULT_MIN_DISCOUNT, DEFAULT_MAX_DISCOUNT
    return minimum, maximum


def select_discount_pct(
    open_hours: Decimal,
    capacity_hours: Decimal,
    *,
    min_pct: Decimal = DEFAULT_MIN_DISCOUNT,
    max_pct: Decimal = DEFAULT_MAX_DISCOUNT,
) -> Decimal:
    """Linear map: 0 open hours → 0%; any opening → [min, max]; full open → max.

    More empty bay-hours raise the discount so leftover next-day slots fill.
    """
    if capacity_hours <= 0 or open_hours <= 0:
        return Decimal("0")
    if max_pct < min_pct:
        min_pct, max_pct = DEFAULT_MIN_DISCOUNT, DEFAULT_MAX_DISCOUNT
    ratio = (open_hours / capacity_hours).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
    if ratio > 1:
        ratio = Decimal("1")
    span = max_pct - min_pct
    pct = (min_pct + span * ratio).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if pct < min_pct:
        pct = min_pct
    if pct > max_pct:
        pct = max_pct
    return pct


def discount_label(discount_pct: Decimal) -> str:
    quantized = Decimal(discount_pct).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if quantized == quantized.to_integral():
        return str(int(quantized))
    return format(quantized, "f").rstrip("0").rstrip(".")


def urgency_label(discount_pct: Decimal) -> str:
    if discount_pct >= Decimal("20"):
        return "high"
    if discount_pct >= Decimal("15"):
        return "medium"
    if discount_pct > 0:
        return "low"
    return "none"


def fill_multiplier_for(discount_pct: Decimal) -> Decimal:
    if discount_pct <= 0:
        return Decimal("1.00")
    factor = (Decimal("1") - (discount_pct / Decimal("100"))).quantize(
        MONEY_QUANT, rounding=ROUND_HALF_UP
    )
    if factor <= 0:
        raise FillError("invalid_fill", "Fill multiplier must stay above zero.")
    return factor


def clamp_discount_pct(
    discount_pct: Decimal,
    *,
    min_pct: Decimal,
    max_pct: Decimal,
) -> Decimal:
    value = Decimal(discount_pct).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if value <= 0:
        return Decimal("0")
    if value < min_pct:
        return min_pct
    if value > max_pct:
        return max_pct
    return value


def merge_intervals(intervals: list[tuple[datetime, datetime]]) -> list[tuple[datetime, datetime]]:
    if not intervals:
        return []
    ordered = sorted(intervals, key=lambda row: row[0])
    merged = [ordered[0]]
    for start, end in ordered[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


def clip_interval(
    start: datetime,
    end: datetime,
    window_start: datetime,
    window_end: datetime,
) -> tuple[datetime, datetime] | None:
    clipped_start = max(as_utc(start), as_utc(window_start))
    clipped_end = min(as_utc(end), as_utc(window_end))
    if clipped_end <= clipped_start:
        return None
    return clipped_start, clipped_end


def invert_intervals(
    window_start: datetime,
    window_end: datetime,
    busy: list[tuple[datetime, datetime]],
) -> list[tuple[datetime, datetime]]:
    gaps: list[tuple[datetime, datetime]] = []
    cursor = as_utc(window_start)
    end = as_utc(window_end)
    for start, stop in merge_intervals(busy):
        if start > cursor:
            gaps.append((cursor, start))
        cursor = max(cursor, stop)
    if cursor < end:
        gaps.append((cursor, end))
    return gaps


def interval_hours(start: datetime, end: datetime) -> Decimal:
    return duration_hours(start, end)


def detect_openings(
    *,
    bays: list[Hoist],
    bookings: list[Booking],
    target_date: date,
    window_start: datetime,
    window_end: datetime,
    min_pct: Decimal = DEFAULT_MIN_DISCOUNT,
    max_pct: Decimal = DEFAULT_MAX_DISCOUNT,
    discount_override: Decimal | None = None,
    offer_id: UUID | None = None,
    source: str = "live",
) -> FillSnapshot:
    """Pure opening math. Shop hoist / unavailable bays must already be filtered out."""
    window_start = as_utc(window_start)
    window_end = as_utc(window_end)
    hours_each = interval_hours(window_start, window_end)
    bay_count = len(bays)
    capacity = (hours_each * bay_count).quantize(HOURS_QUANT, rounding=ROUND_HALF_UP)
    booked = Decimal("0")
    gaps: list[Gap] = []
    by_hoist: dict[UUID, list[tuple[datetime, datetime]]] = {bay.id: [] for bay in bays}
    names = {bay.id: bay.name for bay in bays}

    for booking in bookings:
        if booking.hoist_id not in by_hoist:
            continue
        clipped = clip_interval(booking.start_at, booking.end_at, window_start, window_end)
        if clipped is None:
            continue
        by_hoist[booking.hoist_id].append(clipped)

    for hoist_id, busy in by_hoist.items():
        merged = merge_intervals(busy)
        for start, end in merged:
            booked += interval_hours(start, end)
        for start, end in invert_intervals(window_start, window_end, merged):
            gaps.append(
                Gap(
                    hoist_id=hoist_id,
                    hoist_name=names[hoist_id],
                    start_at=start,
                    end_at=end,
                    hours=interval_hours(start, end),
                )
            )

    booked = booked.quantize(HOURS_QUANT, rounding=ROUND_HALF_UP)
    open_hours = (capacity - booked).quantize(HOURS_QUANT, rounding=ROUND_HALF_UP)
    if open_hours < 0:
        open_hours = Decimal("0")
    computed = select_discount_pct(open_hours, capacity, min_pct=min_pct, max_pct=max_pct)
    if discount_override is not None:
        discount = clamp_discount_pct(discount_override, min_pct=min_pct, max_pct=max_pct)
        if open_hours <= 0:
            discount = Decimal("0")
    else:
        discount = computed
    multiplier = fill_multiplier_for(discount)
    applies = open_hours > 0 and discount > 0
    ratio = Decimal("0")
    if capacity > 0:
        ratio = (open_hours / capacity).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
        if ratio > 1:
            ratio = Decimal("1")
    gaps.sort(key=lambda row: (row.hoist_name, row.start_at))
    return FillSnapshot(
        target_date=target_date,
        tz=FILL_TZ_NAME,
        window_start=window_start,
        window_end=window_end,
        bay_count=bay_count,
        capacity_hours=capacity,
        booked_hours=booked,
        open_hours=open_hours,
        open_ratio=ratio,
        discount_pct=discount,
        fill_multiplier=multiplier,
        urgency=urgency_label(discount) if applies else "none",
        applies=applies,
        gaps=gaps,
        offer_id=offer_id,
        source=source if applies else "none",
    )


def customer_bays(session: Session) -> list[Hoist]:
    rows = session.scalars(
        select(Hoist)
        .where(Hoist.is_shop.is_(False), ~Hoist.status.in_(UNAVAILABLE_HOIST))
        .order_by(Hoist.name)
    ).all()
    return list(rows)


def occupying_bookings(
    session: Session,
    hoist_ids: list[UUID],
    window_start: datetime,
    window_end: datetime,
) -> list[Booking]:
    if not hoist_ids:
        return []
    rows = session.scalars(
        select(Booking)
        .options(selectinload(Booking.hoist))
        .where(
            Booking.hoist_id.in_(hoist_ids),
            Booking.status.in_(OCCUPYING),
            Booking.start_at < window_end,
            Booking.end_at > window_start,
        )
        .order_by(Booking.start_at)
    ).all()
    return list(rows)


def published_offer(session: Session, target_date: date) -> FillOffer | None:
    return session.scalars(
        select(FillOffer).where(
            FillOffer.target_date == target_date,
            FillOffer.status == FillOfferStatus.PUBLISHED,
        )
    ).first()


def snapshot_next_day(
    session: Session,
    *,
    now: datetime | None = None,
    discount_override: Decimal | None = None,
    settings: Settings | None = None,
    prefer_published: bool = True,
) -> FillSnapshot:
    cfg = settings or get_settings()
    target = pricing_next_day(now)
    start_clock, end_clock = fill_window_clocks(cfg)
    window_start, window_end = pricing_clock_window(target, start_clock, end_clock)
    min_pct, max_pct = discount_bounds(cfg)
    offer = published_offer(session, target) if prefer_published else None
    bays = customer_bays(session)
    bookings = occupying_bookings(session, [bay.id for bay in bays], window_start, window_end)
    override = discount_override
    source = "live"
    offer_id = None
    if offer is not None and discount_override is None:
        override = Decimal(offer.discount_pct)
        source = "published"
        offer_id = offer.id
    return detect_openings(
        bays=bays,
        bookings=bookings,
        target_date=target,
        window_start=window_start,
        window_end=window_end,
        min_pct=min_pct,
        max_pct=max_pct,
        discount_override=override,
        offer_id=offer_id,
        source=source,
    )


def slot_overlaps_next_day_window(
    start_at: datetime,
    end_at: datetime,
    *,
    now: datetime | None = None,
    settings: Settings | None = None,
) -> bool:
    target = pricing_next_day(now)
    start_clock, end_clock = fill_window_clocks(settings)
    window_start, window_end = pricing_clock_window(target, start_clock, end_clock)
    return as_utc(start_at) < window_end and as_utc(end_at) > window_start


def resolve_fill_for_slot(
    session: Session,
    start_at: datetime,
    end_at: datetime,
    *,
    now: datetime | None = None,
    settings: Settings | None = None,
) -> FillFactor:
    """Fill applies only to slots that overlap next-day customer-bay hours."""
    if not slot_overlaps_next_day_window(start_at, end_at, now=now, settings=settings):
        return NO_FILL
    snapshot = snapshot_next_day(session, now=now, settings=settings)
    return snapshot.as_factor()


def upsert_published_offer(session: Session, snapshot: FillSnapshot) -> FillOffer:
    if not snapshot.applies:
        raise FillError("no_openings", "No next-day customer-bay openings to publish.")
    row = session.scalars(select(FillOffer).where(FillOffer.target_date == snapshot.target_date)).first()
    if row is None:
        row = FillOffer(target_date=snapshot.target_date)
        session.add(row)
    row.open_hours = snapshot.open_hours
    row.booked_hours = snapshot.booked_hours
    row.capacity_hours = snapshot.capacity_hours
    row.discount_pct = snapshot.discount_pct
    row.fill_multiplier = snapshot.fill_multiplier
    row.urgency = snapshot.urgency
    row.status = FillOfferStatus.PUBLISHED
    row.window_start = snapshot.window_start
    row.window_end = snapshot.window_end
    session.flush()
    return row


def none_snapshot(*, now: datetime | None = None, settings: Settings | None = None) -> FillSnapshot:
    cfg = settings or get_settings()
    target = pricing_next_day(now)
    start_clock, end_clock = fill_window_clocks(cfg)
    window_start, window_end = pricing_clock_window(target, start_clock, end_clock)
    return FillSnapshot(
        target_date=target,
        tz=FILL_TZ_NAME,
        window_start=window_start,
        window_end=window_end,
        bay_count=0,
        capacity_hours=Decimal("0"),
        booked_hours=Decimal("0"),
        open_hours=Decimal("0"),
        open_ratio=Decimal("0"),
        discount_pct=Decimal("0"),
        fill_multiplier=Decimal("1.00"),
        urgency="none",
        applies=False,
        gaps=[],
        source="none",
    )
