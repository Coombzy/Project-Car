"""Booking lifecycle and token reserve / debit / refund rules (spec §5)."""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from decimal import ROUND_HALF_UP, Decimal
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.models import (
    Booking,
    BookingHour,
    BookingKind,
    BookingStatus,
    Hoist,
    HoistStatus,
    Incident,
    IncidentKind,
    IncidentSeverity,
    Member,
    MemberStatus,
    TokenTransactionKind,
)
from app.services.fill import resolve_fill_for_slot
from app.services.peak_cap import check_peak_cap
from app.services.pricing import PricingError, quote_reserve
from app.services.tokens import apply_ledger
from app.shop_time import PRICING_TZ, as_utc, iter_regina_hours, shop_now

OPEN_STATUSES = (BookingStatus.PENDING, BookingStatus.CONFIRMED, BookingStatus.ACTIVE)
# Overdue still occupies a tier slot until the Owner completes it. Cancel stays
# limited to OPEN_STATUSES: a late return is not a cancellation.
SIMULTANEOUS_STATUSES = OPEN_STATUSES + (BookingStatus.OVERDUE,)
# Confirmed, active, and overdue already own the hour. Confirm checks these so a
# second pending row left from older data can still lose with 409, without two
# pending rows blocking each other.
OVERLAP_STATUSES = (BookingStatus.CONFIRMED, BookingStatus.ACTIVE, BookingStatus.OVERDUE)
# A bay hour is taken as soon as a booking exists. Cancelled and completed release it.
HOLDING_STATUSES = (
    BookingStatus.PENDING,
    BookingStatus.CONFIRMED,
    BookingStatus.ACTIVE,
    BookingStatus.OVERDUE,
)
BAY_HOUR_TAKEN = "That bay already has a booking on this hour."
NO_BAY = "No member bay is free for every hour of this visit."
UNAVAILABLE_HOIST = (HoistStatus.MAINTENANCE, HoistStatus.LOCKED)
# A bay cannot close over these until they are cancelled. Active and overdue
# visits are already on the bay and are left for the Owner to finish.
CLOSE_BLOCKING_STATUSES = (BookingStatus.PENDING, BookingStatus.CONFIRMED)
# Stand-in until Ben sets how early check-in may open. Needs from Ben.
CHECK_IN_EARLY_MINUTES = 15
# Ben, D2: bookings start and end on the Regina hour and last at least an hour.
BOOKING_MIN_HOURS = 1
# Ben, D3: a member cancel this many hours or more before the start is free.
# Inside the window the shop keeps LATE_CANCEL_KEEP_PCT of the reserve.
FREE_CANCEL_HOURS = 24
LATE_CANCEL_KEEP_PCT = Decimal("50")
# Ben, D4: a confirmed booking that ends without a check-in keeps this share.
NO_SHOW_KEEP_PCT = Decimal("100")
CENTS = Decimal("0.01")


def _error(status: int, code: str, message: str, **extra: object) -> HTTPException:
    detail: dict[str, object] = {"code": code, "message": message}
    for key, value in extra.items():
        detail[key] = format(value, "f") if isinstance(value, Decimal) else value
    return HTTPException(status_code=status, detail=detail)


def reject_start_in_past(start_at: datetime) -> None:
    """Refuse a new start before shop now.

    Confirm, check-in, complete, and cancel do not use this. A row that
    already exists, including a seed week slot, keeps its lifecycle.
    """
    if as_utc(start_at) < as_utc(shop_now()):
        raise _error(400, "start_in_past", "Start is in the past.")


def _on_the_hour(value: datetime) -> bool:
    local = as_utc(value).astimezone(PRICING_TZ)
    return local.minute == 0 and local.second == 0 and local.microsecond == 0


def reject_off_grid(start_at: datetime, end_at: datetime) -> None:
    """Refuse a new span that does not sit on whole Regina hours.

    Every held hour is charged in full, so a span off the grid would pay for
    and block hours the member did not ask for. Existing rows keep their
    lifecycle; only quote and create use this. An end at or before the start
    is left to the ``invalid_window`` checks.
    """
    if as_utc(end_at) <= as_utc(start_at):
        return
    if not (_on_the_hour(start_at) and _on_the_hour(end_at)):
        raise _error(400, "not_on_the_hour", "Bookings start and end on the hour.")
    if as_utc(end_at) - as_utc(start_at) < timedelta(hours=BOOKING_MIN_HOURS):
        raise _error(
            400,
            "below_minimum_length",
            f"A booking is at least {BOOKING_MIN_HOURS} hour long.",
        )


def get_booking(session: Session, booking_id: UUID) -> Booking:
    booking = session.scalars(
        select(Booking)
        .options(selectinload(Booking.member), selectinload(Booking.hoist))
        .where(Booking.id == booking_id)
    ).first()
    if booking is None:
        raise _error(404, "not_found", "Booking not found.")
    return booking


def _locked_booking(session: Session, booking_id: UUID) -> Booking:
    """Lock the booking row before a caller reads its incidents.

    On Postgres, ``FOR UPDATE`` holds until commit, so a second mark waits
    and then sees the incident the first mark inserted. SQLite drops the
    clause; the suite still checks that the statement asks for the lock.
    """
    booking = session.scalars(
        select(Booking)
        .options(selectinload(Booking.member), selectinload(Booking.hoist))
        .where(Booking.id == booking_id)
        .with_for_update()
    ).first()
    if booking is None:
        raise _error(404, "not_found", "Booking not found.")
    return booking


def lock_member(session: Session, member_id: UUID) -> Member:
    """Lock the member row before a token-cache check.

    On Postgres, ``FOR UPDATE`` holds until commit, so a second create or
    shop-hoist approval waits and then sees the cache the first writer
    stored. SQLite drops the clause; the suite still checks that the
    statement asks for the lock. ``populate_existing`` refreshes a member
    this session already loaded (shop-hoist approval loads it with the
    request) so the balance check is not the pre-lock copy.
    """
    member = session.scalars(
        select(Member)
        .options(selectinload(Member.tier))
        .where(Member.id == member_id)
        .with_for_update()
        .execution_options(populate_existing=True)
    ).first()
    if member is None:
        raise _error(404, "not_found", "Member not found.")
    return member


def hoist_has_overlap(
    session: Session,
    hoist_id: UUID,
    start_at: datetime,
    end_at: datetime,
    *,
    exclude_id: UUID | None = None,
    statuses: tuple[BookingStatus, ...] = OVERLAP_STATUSES,
) -> bool:
    """True when this hoist already holds any instant in [start_at, end_at)."""
    stmt = select(Booking.id).where(
        Booking.hoist_id == hoist_id,
        Booking.status.in_(statuses),
        Booking.start_at < end_at,
        Booking.end_at > start_at,
    )
    if exclude_id is not None:
        stmt = stmt.where(Booking.id != exclude_id)
    return session.scalars(stmt).first() is not None


def _reject_if_bay_hour_taken(
    session: Session,
    hoist_id: UUID,
    start_at: datetime,
    end_at: datetime,
    *,
    exclude_id: UUID | None = None,
    statuses: tuple[BookingStatus, ...] = HOLDING_STATUSES,
) -> None:
    if hoist_has_overlap(
        session,
        hoist_id,
        start_at,
        end_at,
        exclude_id=exclude_id,
        statuses=statuses,
    ):
        raise _error(409, "hoist_overlap", BAY_HOUR_TAKEN)


class HoldingHoursConflict(RuntimeError):
    """A holding booking cannot own every Regina hour it spans.

    Backfill raises this instead of inserting a partial set. The booking-hours
    migration rolls the upgrade back.
    """


def _hour_key(value: datetime) -> datetime:
    """Naive UTC instant so SQLite's naive timestamps match aware ones."""
    if value.tzinfo is None:
        normalized = value
    else:
        normalized = value.astimezone(timezone.utc).replace(tzinfo=None)
    return normalized.replace(microsecond=0)


def _add_missing_hours(session: Session, booking: Booking) -> None:
    """Insert missing Regina hour rows and flush. Caller handles IntegrityError."""
    # SQLite returns stored UTC as naive. as_utc would treat that as shop-local.
    start_at = _stored_utc(booking.start_at)
    end_at = _stored_utc(booking.end_at)
    wanted = [hour_start for hour_start, _hour_end in iter_regina_hours(start_at, end_at)]
    owned_starts = session.scalars(
        select(BookingHour.hour_start).where(
            BookingHour.booking_id == booking.id,
            BookingHour.hoist_id == booking.hoist_id,
        )
    ).all()
    owned = {_hour_key(hour_start) for hour_start in owned_starts}
    missing = [hour_start for hour_start in wanted if _hour_key(hour_start) not in owned]
    if not missing:
        return
    for hour_start in missing:
        session.add(
            BookingHour(
                booking_id=booking.id,
                hoist_id=booking.hoist_id,
                hour_start=hour_start,
            )
        )
    session.flush()


def claim_booking_hours(session: Session, booking: Booking) -> None:
    """Insert one row per Regina hour. Unique (hoist_id, hour_start) is the lock.

    A second flush of the same bay hour raises 409 hoist_overlap even when the
    SELECT overlap check is skipped. Claim is done only when this booking
    already owns every Regina hour of this hoist and window. One existing row
    is not enough: confirm must still insert the hours that are missing.

    The conflict path rolls the whole session back. Any-bay retries must not
    call this: they insert inside a savepoint and try the next bay.
    """
    try:
        _add_missing_hours(session, booking)
    except IntegrityError:
        session.rollback()
        raise _error(409, "hoist_overlap", BAY_HOUR_TAKEN) from None


def release_booking_hours(session: Session, booking: Booking) -> None:
    """Free cancelled or completed hours so another booking can take them.

    The caller has already moved this booking out of ``HOLDING_STATUSES``.
    Backfill runs in this same transaction. It fills freed hours only when
    every remaining holding booking can own its whole window. A conflict
    raises ``HoldingHoursConflict`` and the caller rolls back.
    """
    session.execute(delete(BookingHour).where(BookingHour.booking_id == booking.id))
    session.flush()
    backfill_holding_booking_hours(session)


def backfill_holding_booking_hours(session: Session) -> None:
    """Insert missing Regina hour rows for holding bookings that already exist.

    Same ``_stored_utc`` / ``iter_regina_hours`` bounds as ``claim_booking_hours``.
    Pending, confirmed, active, and overdue bookings get one row per hour.
    Cancelled and completed bookings are left with no rows. A second run is a
    no-op when every holding booking already owns its full hour set.

    If any holding booking cannot own every Regina hour, raise
    ``HoldingHoursConflict`` before inserting any row from this call. Do not
    keep the older booking's hour and leave the newer one with a partial set.
    The migration rolls that error back.
    """
    bookings = session.scalars(
        select(Booking)
        .where(Booking.status.in_(HOLDING_STATUSES))
        .order_by(Booking.created_at, Booking.id)
    ).all()
    existing = session.scalars(select(BookingHour)).all()
    owned_by: dict[tuple[UUID, datetime], UUID] = {}
    for row in existing:
        owned_by[(row.hoist_id, _hour_key(row.hour_start))] = row.booking_id

    pending: list[tuple[Booking, datetime]] = []
    for booking in bookings:
        start_at = _stored_utc(booking.start_at)
        end_at = _stored_utc(booking.end_at)
        missing: list[datetime] = []
        for hour_start, _hour_end in iter_regina_hours(start_at, end_at):
            key = (booking.hoist_id, _hour_key(hour_start))
            owner = owned_by.get(key)
            if owner is None:
                missing.append(hour_start)
            elif owner != booking.id:
                raise HoldingHoursConflict(
                    f"Holding booking {booking.id} cannot own every Regina hour "
                    f"on hoist {booking.hoist_id}."
                )
        for hour_start in missing:
            owned_by[(booking.hoist_id, _hour_key(hour_start))] = booking.id
            pending.append((booking, hour_start))

    for booking, hour_start in pending:
        session.add(
            BookingHour(
                booking_id=booking.id,
                hoist_id=booking.hoist_id,
                hour_start=hour_start,
            )
        )
    if pending:
        session.flush()


def open_booking_count(session: Session, member_id: UUID) -> int:
    rows = session.scalars(
        select(Booking.id).where(
            Booking.member_id == member_id,
            Booking.status.in_(SIMULTANEOUS_STATUSES),
        )
    ).all()
    return len(rows)


def _set_hoist_available_if_idle(session: Session, hoist: Hoist) -> None:
    """Free the bay only when nobody is still on it.

    An overdue booking is a late return: the member has not given the bay
    back, so cancelling or completing a different booking must not mark it
    available.
    """
    occupying = session.scalars(
        select(Booking.id).where(
            Booking.hoist_id == hoist.id,
            Booking.status.in_((BookingStatus.ACTIVE, BookingStatus.OVERDUE)),
        )
    ).first()
    if occupying is None and hoist.status == HoistStatus.OCCUPIED:
        hoist.status = HoistStatus.AVAILABLE
        session.add(hoist)


def preview_reserve(
    session: Session,
    *,
    start_at: datetime,
    end_at: datetime,
    member_id: UUID | None = None,
) -> tuple:
    """Return (quote, token_balance, token_balance_after). Balances are None without a member."""
    start_at = as_utc(start_at)
    end_at = as_utc(end_at)
    reject_start_in_past(start_at)
    reject_off_grid(start_at, end_at)
    fill = resolve_fill_for_slot(session, start_at, end_at)
    try:
        quote = quote_reserve(start_at, end_at, fill=fill, session=session)
    except PricingError as exc:
        raise _error(400, exc.code, exc.message) from exc
    if member_id is None:
        return quote, None, None
    member = session.get(Member, member_id)
    if member is None:
        raise _error(404, "not_found", "Member not found.")
    balance = Decimal(member.token_balance)
    return quote, balance, balance - quote.final_reserve_cost


def _bay_number_key(hoist: Hoist) -> tuple[int, str]:
    """Lowest trailing number first. A name with no number sorts last, then by name."""
    match = re.search(r"(\d+)$", hoist.name.strip())
    number = int(match.group(1)) if match else 1_000_000_000
    return (number, hoist.name)


def _member_bays_lowest_first(session: Session) -> list[Hoist]:
    """Member bays that can take a visit. Free means the hour, not the bay's current status.

    A bay checked in right now is ``occupied`` and still free for a later hour.
    Maintenance and locked bays stay out, the same rule as booking a named bay.
    """
    rows = session.scalars(
        select(Hoist).where(
            Hoist.is_shop.is_(False),
            Hoist.status.notin_(UNAVAILABLE_HOIST),
        )
    ).all()
    return sorted(rows, key=_bay_number_key)


def _place_on_any_bay(
    session: Session,
    *,
    member: Member,
    start_at: datetime,
    end_at: datetime,
    tokens: Decimal,
    rule: object,
    notes: str | None,
) -> Booking | None:
    """Save the visit on the first free member bay. A lost hour tries the next bay.

    The hour insert runs inside a savepoint. ``claim_booking_hours`` rolls the
    whole session back, which would throw away the chance to try Bay 2.
    """
    for hoist in _member_bays_lowest_first(session):
        if hoist_has_overlap(
            session,
            hoist.id,
            start_at,
            end_at,
            statuses=HOLDING_STATUSES,
        ):
            continue
        try:
            with session.begin_nested():
                booking = Booking(
                    member_id=member.id,
                    hoist_id=hoist.id,
                    start_at=start_at,
                    end_at=end_at,
                    kind=BookingKind.CUSTOMER,
                    status=BookingStatus.PENDING,
                    reserved_tokens=tokens,
                    pricing_rule=rule,
                    notes=notes,
                )
                session.add(booking)
                session.flush()
                _add_missing_hours(session, booking)
        except IntegrityError:
            continue
        return booking
    return None


def create_booking(
    session: Session,
    *,
    member_id: UUID | None,
    hoist_id: UUID | None,
    start_at: datetime,
    end_at: datetime,
    notes: str | None,
    kind: BookingKind = BookingKind.CUSTOMER,
    shown_tokens: Decimal | None = None,
) -> Booking:
    start_at = as_utc(start_at)
    end_at = as_utc(end_at)
    settle_elapsed_no_shows(session)
    reject_start_in_past(start_at)
    reject_off_grid(start_at, end_at)

    hoist: Hoist | None = None
    if hoist_id is not None:
        hoist = session.get(Hoist, hoist_id)
        if hoist is None:
            raise _error(404, "not_found", "Hoist not found.")
        if hoist.status in UNAVAILABLE_HOIST:
            raise _error(400, "hoist_unavailable", "That hoist is in maintenance or locked.")
    elif kind == BookingKind.SHOP:
        raise _error(400, "not_shop_hoist", "Shop work can only be booked on the shop hoist.")

    if kind == BookingKind.SHOP:
        return _create_shop_booking(
            session,
            hoist=hoist,
            start_at=start_at,
            end_at=end_at,
            notes=notes,
            member_id=member_id,
        )

    if member_id is None:
        raise _error(400, "member_required", "Customer bookings need a member.")

    fill = resolve_fill_for_slot(session, start_at, end_at)
    try:
        quote = quote_reserve(start_at, end_at, fill=fill, session=session)
    except PricingError as exc:
        raise _error(400, exc.code, exc.message) from exc
    tokens = quote.final_reserve_cost
    if shown_tokens is not None and Decimal(shown_tokens).quantize(Decimal("0.01")) != tokens:
        raise _error(
            409,
            "price_changed",
            "The price changed. Book was not saved.",
            reserved_tokens=tokens,
        )
    rule = quote.as_rule()
    meta = quote.ledger_meta()

    member = lock_member(session, member_id)

    if member.status != MemberStatus.ACTIVE:
        raise _error(400, "member_not_bookable", "Only active members can book a hoist.")

    if hoist is not None and hoist.is_shop:
        raise _error(
            400,
            "shop_hoist_request_required",
            "The shop hoist takes a request. It is not a booking until a person or an AI approves it.",
        )

    window = timedelta(days=member.tier.booking_window_days)
    if start_at > as_utc(shop_now()) + window:
        raise _error(
            400,
            "booking_window",
            f"Start is outside this member's {member.tier.booking_window_days}-day booking window.",
        )

    if open_booking_count(session, member.id) >= member.tier.max_simultaneous_bookings:
        raise _error(
            400,
            "max_simultaneous_bookings",
            "Member is already at the tier's simultaneous booking limit.",
        )

    check_peak_cap(session, member.id, start_at, end_at)

    if Decimal(member.token_balance) < tokens:
        raise _error(400, "insufficient_tokens", "Member does not have enough tokens to reserve.")

    if hoist is None:
        booking = _place_on_any_bay(
            session,
            member=member,
            start_at=start_at,
            end_at=end_at,
            tokens=tokens,
            rule=rule,
            notes=notes,
        )
        if booking is None:
            raise _error(409, "no_bay", NO_BAY)
    else:
        _reject_if_bay_hour_taken(session, hoist.id, start_at, end_at)
        booking = Booking(
            member_id=member.id,
            hoist_id=hoist.id,
            start_at=start_at,
            end_at=end_at,
            kind=BookingKind.CUSTOMER,
            status=BookingStatus.PENDING,
            reserved_tokens=tokens,
            pricing_rule=rule,
            notes=notes,
        )
        session.add(booking)
        session.flush()
        claim_booking_hours(session, booking)
    apply_ledger(
        session,
        member,
        kind=TokenTransactionKind.BOOKING_RESERVE,
        amount=-tokens,
        booking_id=booking.id,
        note="Reserve tokens for booking",
        meta=meta,
    )
    session.refresh(booking)
    return get_booking(session, booking.id)


def _create_shop_booking(
    session: Session,
    *,
    hoist: Hoist,
    start_at: datetime,
    end_at: datetime,
    notes: str | None,
    member_id: UUID | None,
) -> Booking:
    if not hoist.is_shop:
        raise _error(400, "not_shop_hoist", "Shop work can only be booked on the shop hoist.")
    if end_at <= start_at:
        raise _error(400, "invalid_window", "End must be after start.")

    member = None
    if member_id is not None:
        member = session.get(Member, member_id)
        if member is None:
            raise _error(404, "not_found", "Member not found.")

    _reject_if_bay_hour_taken(session, hoist.id, start_at, end_at)

    booking = Booking(
        member_id=member.id if member is not None else None,
        hoist_id=hoist.id,
        start_at=start_at,
        end_at=end_at,
        kind=BookingKind.SHOP,
        status=BookingStatus.PENDING,
        reserved_tokens=Decimal("0"),
        pricing_rule=None,
        notes=notes,
    )
    session.add(booking)
    session.flush()
    claim_booking_hours(session, booking)
    return get_booking(session, booking.id)


def confirm_booking(session: Session, booking_id: UUID) -> Booking:
    booking = get_booking(session, booking_id)
    if booking.status != BookingStatus.PENDING:
        raise _error(400, "invalid_transition", "Only pending bookings can be confirmed.")
    if booking.hoist.status in UNAVAILABLE_HOIST:
        raise _error(400, "hoist_unavailable", "That hoist is in maintenance or locked.")
    if booking.kind == BookingKind.CUSTOMER and booking.hoist.is_shop:
        raise _error(
            400,
            "shop_hoist_approval_required",
            "A shop hoist request is not a booking until a person or an AI approves it.",
        )
    _reject_if_bay_hour_taken(
        session,
        booking.hoist_id,
        booking.start_at,
        booking.end_at,
        exclude_id=booking.id,
        statuses=OVERLAP_STATUSES,
    )
    booking.status = BookingStatus.CONFIRMED
    session.add(booking)
    claim_booking_hours(session, booking)
    session.flush()
    return get_booking(session, booking.id)


def check_in_booking(session: Session, booking_id: UUID) -> Booking:
    booking = get_booking(session, booking_id)
    if booking.status != BookingStatus.CONFIRMED:
        raise _error(400, "invalid_transition", "Only confirmed bookings can be checked in.")
    if booking.hoist.status in UNAVAILABLE_HOIST:
        raise _error(400, "hoist_unavailable", "That hoist is in maintenance or locked.")
    opens_at = _stored_utc(booking.start_at) - timedelta(minutes=CHECK_IN_EARLY_MINUTES)
    if _stored_utc(shop_now()) < opens_at:
        raise _error(
            400,
            "check_in_too_early",
            f"Check-in opens {CHECK_IN_EARLY_MINUTES} minutes before the start.",
        )
    # Closed at end_at. The open window is [opens_at, end_at).
    if _stored_utc(shop_now()) >= _stored_utc(booking.end_at):
        raise _error(
            400,
            "check_in_too_late",
            "Check-in closes when the visit ends.",
        )
    booking.status = BookingStatus.ACTIVE
    booking.hoist.status = HoistStatus.OCCUPIED
    session.add(booking)
    session.add(booking.hoist)
    session.flush()
    return get_booking(session, booking.id)


def complete_booking(session: Session, booking_id: UUID) -> Booking:
    """Close an active or overdue visit. The reserve stands as the charge.

    Unused time is never refunded once a visit has started (Ben, D16), so
    completion writes no ledger row.
    """
    # Lock the booking before the status check. A second complete waits and
    # sees the new status.
    booking = _locked_booking(session, booking_id)
    if booking.status not in (BookingStatus.ACTIVE, BookingStatus.OVERDUE):
        raise _error(
            400,
            "invalid_transition",
            "Only an active or overdue booking can be completed.",
        )
    booking.reserved_tokens = Decimal("0")
    booking.status = BookingStatus.COMPLETED
    session.add(booking)
    release_booking_hours(session, booking)
    session.flush()
    _set_hoist_available_if_idle(session, booking.hoist)
    return get_booking(session, booking.id)


def _stored_utc(value: datetime) -> datetime:
    """UTC instant for a stored timestamp or an aware clock.

    Postgres returns timestamptz as aware. SQLite returns the same UTC instant
    as a naive datetime. ``as_utc`` treats naive values as shop-local, which
    would move a past end into the future.
    """
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _late_return(session: Session, booking_id: UUID) -> Incident | None:
    return session.scalars(
        select(Incident)
        .where(
            Incident.booking_id == booking_id,
            Incident.kind == IncidentKind.LATE_RETURN,
        )
        .order_by(Incident.created_at, Incident.id)
    ).first()


def _open_late_return(session: Session, booking: Booking) -> Incident:
    incident = Incident(
        member_id=booking.member_id,
        hoist_id=booking.hoist_id,
        booking_id=booking.id,
        kind=IncidentKind.LATE_RETURN,
        severity=IncidentSeverity.MINOR,
        description=(
            "Late return. The booking was still active after its end. "
            "No money was charged. The Owner reviews this incident."
        ),
        photos=[],
    )
    session.add(incident)
    return incident


def mark_overdue(session: Session, booking_id: UUID) -> tuple[Booking, bool]:
    """Flip an active booking past its end to overdue and open one late_return.

    Repeat calls are idempotent. This path does not write a token ledger row
    or a billing row, and it does not release the hour. Returns the booking
    and whether this call changed stored state (status or a new incident).
    """
    booking = _locked_booking(session, booking_id)
    existing = _late_return(session, booking.id)
    changed = False
    if booking.status != BookingStatus.OVERDUE:
        if booking.status != BookingStatus.ACTIVE:
            raise _error(400, "invalid_transition", "Only an active booking can be marked overdue.")
        if _stored_utc(booking.end_at) > _stored_utc(shop_now()):
            raise _error(
                400,
                "not_past_end",
                "An active booking can be marked overdue only after its end.",
            )
        booking.status = BookingStatus.OVERDUE
        session.add(booking)
        changed = True
    if existing is None:
        _open_late_return(session, booking)
        changed = True
    if changed:
        session.flush()
    return get_booking(session, booking.id), changed


def future_bookings_on_hoist(session: Session, hoist_id: UUID) -> list[Booking]:
    """Pending or confirmed bookings on this bay that have not ended yet."""
    now = _stored_utc(shop_now())
    rows = session.scalars(
        select(Booking)
        .where(
            Booking.hoist_id == hoist_id,
            Booking.status.in_(CLOSE_BLOCKING_STATUSES),
        )
        .order_by(Booking.start_at, Booking.id)
    ).all()
    return [row for row in rows if _stored_utc(row.end_at) > now]


def kept_share(reserved: Decimal, keep_pct: Decimal) -> Decimal:
    """Tokens the shop keeps, rounded half up to the cent."""
    return (Decimal(reserved) * keep_pct / Decimal("100")).quantize(CENTS, rounding=ROUND_HALF_UP)


def _member_cancel_terms(booking: Booking) -> tuple[Decimal, dict]:
    """Share kept and refund meta for a member cancel (Ben, D3 / D5)."""
    lead = _stored_utc(booking.start_at) - _stored_utc(shop_now())
    if lead <= timedelta(0):
        raise _error(400, "cancel_after_start", "A booking cannot be cancelled once it has started.")
    if lead >= timedelta(hours=FREE_CANCEL_HOURS):
        return Decimal("0"), {"policy": "free_cancel"}
    hours_before = (Decimal(lead.total_seconds()) / Decimal(3600)).quantize(CENTS, rounding=ROUND_HALF_UP)
    kept = kept_share(Decimal(booking.reserved_tokens), LATE_CANCEL_KEEP_PCT)
    return kept, {
        "policy": "late_cancel",
        "keep_pct": str(LATE_CANCEL_KEEP_PCT),
        "kept_tokens": str(kept),
        "hours_before": str(hours_before),
    }


REASON_MIN = 3
REASON_MAX = 500


def settle_elapsed_no_shows(session: Session) -> list[Booking]:
    """Turn a confirmed visit whose end has passed into a no-show.

    The hour is freed in this save and the reserve stays with the shop.
    A second call finds nothing new. Sweep is the same rule, kept as a
    catch-up button.
    """
    now = _stored_utc(shop_now())
    candidates = session.scalars(
        select(Booking.id)
        .where(
            Booking.status == BookingStatus.CONFIRMED,
            Booking.member_id.is_not(None),
        )
        .order_by(Booking.end_at, Booking.id)
    ).all()
    swept: list[Booking] = []
    for booking_id in candidates:
        booking = _locked_booking(session, booking_id)
        if booking.status != BookingStatus.CONFIRMED or _stored_utc(booking.end_at) > now:
            continue
        member = lock_member(session, booking.member_id)
        reserved = Decimal(booking.reserved_tokens)
        kept = kept_share(reserved, NO_SHOW_KEEP_PCT)
        if reserved - kept > 0:
            apply_ledger(
                session,
                member,
                kind=TokenTransactionKind.BOOKING_REFUND,
                amount=reserved - kept,
                booking_id=booking.id,
                note=f"No-show: refund {reserved - kept}, keep {kept}",
                meta={"policy": "no_show", "keep_pct": str(NO_SHOW_KEEP_PCT), "kept_tokens": str(kept)},
            )
        booking.reserved_tokens = Decimal("0")
        booking.status = BookingStatus.NO_SHOW
        session.add(booking)
        release_booking_hours(session, booking)
        session.flush()
        _set_hoist_available_if_idle(session, booking.hoist)
        swept.append(get_booking(session, booking.id))
    return swept


def cancel_booking(
    session: Session,
    booking_id: UUID,
    *,
    by_member: bool = False,
    refund_meta: dict | None = None,
    refund_note: str = "Refund reserve on cancel",
    reason: str | None = None,
    require_reason: bool = False,
    actor: str | None = None,
) -> Booking:
    """Cancel an open booking and refund its reserve.

    ``by_member`` applies the member cancel window. Owner cancels before the
    start refund in full and need a written reason. Once the visit is checked
    in, or the start has passed, nothing is refunded.
    """
    # A confirmed visit that already ended is a no-show before anyone can
    # cancel it back to a refund.
    settle_elapsed_no_shows(session)
    # Lock the booking, then the member, before the status check. A second
    # cancel waits, sees the new status, and does not write another refund.
    # Shop work can have no member and no reserve.
    booking = _locked_booking(session, booking_id)
    member = lock_member(session, booking.member_id) if booking.member_id is not None else None
    if booking.status not in OPEN_STATUSES:
        raise _error(400, "invalid_transition", "Completed, overdue, or cancelled bookings cannot be cancelled.")
    if booking.status == BookingStatus.ACTIVE:
        raise _error(400, "cancel_after_check_in", "A checked-in visit cannot be cancelled.")
    if _stored_utc(booking.start_at) <= _stored_utc(shop_now()):
        raise _error(400, "cancel_after_start", "A booking cannot be cancelled once it has started.")

    reserved = Decimal(booking.reserved_tokens)
    meta = {"pricing_rule": booking.pricing_rule} if booking.pricing_rule else {}
    kept = Decimal("0")
    if by_member:
        kept, terms = _member_cancel_terms(booking)
        meta.update(terms)
    elif require_reason:
        text = (reason or "").strip()
        if not REASON_MIN <= len(text) <= REASON_MAX:
            raise _error(
                422,
                "reason_required",
                f"Cancelling a visit needs a reason of {REASON_MIN}-{REASON_MAX} characters.",
            )
        meta["override"] = {"reason": text, "by": actor or "owner"}
    meta.update(refund_meta or {})
    refund = reserved - kept
    if refund > 0:
        apply_ledger(
            session,
            member,
            kind=TokenTransactionKind.BOOKING_REFUND,
            amount=refund,
            booking_id=booking.id,
            note=refund_note if kept == 0 else f"Late cancel: refund {refund}, keep {kept}",
            meta=meta or None,
        )
    booking.reserved_tokens = Decimal("0")

    booking.status = BookingStatus.CANCELLED
    session.add(booking)
    release_booking_hours(session, booking)
    session.flush()
    _set_hoist_available_if_idle(session, booking.hoist)
    return get_booking(session, booking.id)


def sweep_no_shows(session: Session) -> list[Booking]:
    """Catch-up for confirmed member visits that ended without a check-in.

    The same save as ``settle_elapsed_no_shows``. A second sweep does nothing.
    """
    return settle_elapsed_no_shows(session)
