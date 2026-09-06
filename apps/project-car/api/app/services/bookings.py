"""Booking lifecycle and token reserve / debit / refund rules (spec §5)."""

from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import (
    Booking,
    BookingKind,
    BookingStatus,
    Hoist,
    HoistStatus,
    Member,
    MemberStatus,
    TokenTransactionKind,
)
from app.services.fill import resolve_fill_for_slot
from app.services.pricing import PricingError, quote_reserve
from app.services.tokens import apply_ledger
from app.shop_time import as_utc, shop_now

OPEN_STATUSES = (BookingStatus.PENDING, BookingStatus.CONFIRMED, BookingStatus.ACTIVE)
OVERLAP_STATUSES = (BookingStatus.CONFIRMED, BookingStatus.ACTIVE)
UNAVAILABLE_HOIST = (HoistStatus.MAINTENANCE, HoistStatus.LOCKED)


def _error(status: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status, detail={"code": code, "message": message})


def get_booking(session: Session, booking_id: UUID) -> Booking:
    booking = session.scalars(
        select(Booking)
        .options(selectinload(Booking.member), selectinload(Booking.hoist))
        .where(Booking.id == booking_id)
    ).first()
    if booking is None:
        raise _error(404, "not_found", "Booking not found.")
    return booking


def hoist_has_overlap(
    session: Session,
    hoist_id: UUID,
    start_at: datetime,
    end_at: datetime,
    *,
    exclude_id: UUID | None = None,
) -> bool:
    stmt = select(Booking.id).where(
        Booking.hoist_id == hoist_id,
        Booking.status.in_(OVERLAP_STATUSES),
        Booking.start_at < end_at,
        Booking.end_at > start_at,
    )
    if exclude_id is not None:
        stmt = stmt.where(Booking.id != exclude_id)
    return session.scalars(stmt).first() is not None


def _open_booking_count(session: Session, member_id: UUID) -> int:
    rows = session.scalars(
        select(Booking.id).where(
            Booking.member_id == member_id,
            Booking.status.in_(OPEN_STATUSES),
        )
    ).all()
    return len(rows)


def _set_hoist_available_if_idle(session: Session, hoist: Hoist) -> None:
    active = session.scalars(
        select(Booking.id).where(
            Booking.hoist_id == hoist.id,
            Booking.status == BookingStatus.ACTIVE,
        )
    ).first()
    if active is None and hoist.status == HoistStatus.OCCUPIED:
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
    fill = resolve_fill_for_slot(session, start_at, end_at)
    try:
        quote = quote_reserve(start_at, end_at, fill=fill)
    except PricingError as exc:
        raise _error(400, exc.code, exc.message) from exc
    if member_id is None:
        return quote, None, None
    member = session.get(Member, member_id)
    if member is None:
        raise _error(404, "not_found", "Member not found.")
    balance = Decimal(member.token_balance)
    return quote, balance, balance - quote.final_reserve_cost


def create_booking(
    session: Session,
    *,
    member_id: UUID | None,
    hoist_id: UUID,
    start_at: datetime,
    end_at: datetime,
    notes: str | None,
    kind: BookingKind = BookingKind.CUSTOMER,
) -> Booking:
    start_at = as_utc(start_at)
    end_at = as_utc(end_at)

    hoist = session.get(Hoist, hoist_id)
    if hoist is None:
        raise _error(404, "not_found", "Hoist not found.")
    if hoist.status in UNAVAILABLE_HOIST:
        raise _error(400, "hoist_unavailable", "That hoist is in maintenance or locked.")

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
        quote = quote_reserve(start_at, end_at, fill=fill)
    except PricingError as exc:
        raise _error(400, exc.code, exc.message) from exc
    tokens = quote.final_reserve_cost
    rule = quote.as_rule()
    meta = quote.ledger_meta()

    member = session.scalars(
        select(Member).options(selectinload(Member.tier)).where(Member.id == member_id)
    ).first()
    if member is None:
        raise _error(404, "not_found", "Member not found.")

    if member.status != MemberStatus.ACTIVE:
        raise _error(400, "member_not_bookable", "Only active members can book a hoist.")

    if hoist.is_shop:
        raise _error(
            400,
            "shop_hoist_owner_only",
            "The shop hoist is Owner-only. Customer bookings use the five customer bays.",
        )

    window = timedelta(days=member.tier.booking_window_days)
    if start_at > as_utc(shop_now()) + window:
        raise _error(
            400,
            "booking_window",
            f"Start is outside this member's {member.tier.booking_window_days}-day booking window.",
        )

    if _open_booking_count(session, member.id) >= member.tier.max_simultaneous_bookings:
        raise _error(
            400,
            "max_simultaneous_bookings",
            "Member is already at the tier's simultaneous booking limit.",
        )

    if Decimal(member.token_balance) < tokens:
        raise _error(400, "insufficient_tokens", "Member does not have enough tokens to reserve.")

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

    if hoist_has_overlap(session, hoist.id, start_at, end_at):
        raise _error(
            409,
            "hoist_overlap",
            "That hoist already has a confirmed or active booking in this window.",
        )

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
            "shop_hoist_owner_only",
            "The shop hoist is Owner-only. Customer bookings use the five customer bays.",
        )
    if hoist_has_overlap(
        session,
        booking.hoist_id,
        booking.start_at,
        booking.end_at,
        exclude_id=booking.id,
    ):
        raise _error(409, "hoist_overlap", "That hoist already has a confirmed or active booking in this window.")
    booking.status = BookingStatus.CONFIRMED
    session.add(booking)
    session.flush()
    return get_booking(session, booking.id)


def check_in_booking(session: Session, booking_id: UUID) -> Booking:
    booking = get_booking(session, booking_id)
    if booking.status != BookingStatus.CONFIRMED:
        raise _error(400, "invalid_transition", "Only confirmed bookings can be checked in.")
    if booking.hoist.status in UNAVAILABLE_HOIST:
        raise _error(400, "hoist_unavailable", "That hoist is in maintenance or locked.")
    booking.status = BookingStatus.ACTIVE
    booking.hoist.status = HoistStatus.OCCUPIED
    session.add(booking)
    session.add(booking.hoist)
    session.flush()
    return get_booking(session, booking.id)


def complete_booking(
    session: Session,
    booking_id: UUID,
    *,
    unused_tokens: Decimal = Decimal("0"),
) -> Booking:
    booking = get_booking(session, booking_id)
    if booking.status != BookingStatus.ACTIVE:
        raise _error(400, "invalid_transition", "Only active bookings can be completed.")

    unused = Decimal(unused_tokens)
    reserved = Decimal(booking.reserved_tokens)
    if unused < 0 or unused > reserved:
        raise _error(400, "invalid_refund", "Unused tokens must be between 0 and the reserved amount.")

    used = reserved - unused
    member = booking.member
    meta = {"pricing_rule": booking.pricing_rule} if booking.pricing_rule else None
    if reserved > 0:
        apply_ledger(
            session,
            member,
            kind=TokenTransactionKind.BOOKING_REFUND,
            amount=reserved,
            booking_id=booking.id,
            note="Release reserved tokens",
            meta=meta,
        )
        if used > 0:
            apply_ledger(
                session,
                member,
                kind=TokenTransactionKind.BOOKING_DEBIT,
                amount=-used,
                booking_id=booking.id,
                note="Debit used tokens",
                meta=meta,
            )

    booking.reserved_tokens = Decimal("0")
    booking.status = BookingStatus.COMPLETED
    session.add(booking)
    session.flush()
    _set_hoist_available_if_idle(session, booking.hoist)
    return get_booking(session, booking.id)


def cancel_booking(session: Session, booking_id: UUID) -> Booking:
    booking = get_booking(session, booking_id)
    if booking.status not in OPEN_STATUSES:
        raise _error(400, "invalid_transition", "Completed, overdue, or cancelled bookings cannot be cancelled.")

    reserved = Decimal(booking.reserved_tokens)
    meta = {"pricing_rule": booking.pricing_rule} if booking.pricing_rule else None
    if reserved > 0:
        apply_ledger(
            session,
            booking.member,
            kind=TokenTransactionKind.BOOKING_REFUND,
            amount=reserved,
            booking_id=booking.id,
            note="Refund reserve on cancel",
            meta=meta,
        )
        booking.reserved_tokens = Decimal("0")

    booking.status = BookingStatus.CANCELLED
    session.add(booking)
    session.flush()
    _set_hoist_available_if_idle(session, booking.hoist)
    return get_booking(session, booking.id)
