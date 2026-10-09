"""Shop hoist requests.

A request is not a booking. It does not hold the hour and does not move tokens.
Approval is a later step. This module does not approve.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.auth import Principal
from app.models import (
    ActorKind,
    Booking,
    BookingKind,
    BookingStatus,
    Hoist,
    Member,
    MemberStatus,
    ShopHoistRequest,
    ShopHoistRequestStatus,
    StaffAction,
    StaffSubject,
    TokenTransactionKind,
)
from app.services.bookings import (
    HOLDING_STATUSES,
    UNAVAILABLE_HOIST,
    hoist_has_overlap,
    open_booking_count,
    preview_reserve,
)
from app.services.staff import actor_of, record_action, reject_own_request
from app.services.tokens import apply_ledger
from app.shop_time import as_utc, shop_now


def _error(status: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status, detail={"code": code, "message": message})


def get_shop_hoist_request(session: Session, request_id: UUID) -> ShopHoistRequest:
    row = session.scalars(
        select(ShopHoistRequest)
        .options(selectinload(ShopHoistRequest.member), selectinload(ShopHoistRequest.hoist))
        .where(ShopHoistRequest.id == request_id)
    ).first()
    if row is None:
        raise _error(404, "not_found", "Shop hoist request not found.")
    return row


def get_shop_hoist(session: Session) -> Hoist:
    row = session.scalars(select(Hoist).where(Hoist.is_shop.is_(True)).order_by(Hoist.name)).first()
    if row is None:
        raise _error(404, "not_found", "Shop hoist is not configured.")
    return row


def list_shop_hoist_requests(
    session: Session,
    *,
    member_id: UUID | None = None,
    status: ShopHoistRequestStatus | None = None,
) -> list[ShopHoistRequest]:
    stmt = (
        select(ShopHoistRequest)
        .options(selectinload(ShopHoistRequest.member), selectinload(ShopHoistRequest.hoist))
        .order_by(ShopHoistRequest.start_at)
    )
    if member_id is not None:
        stmt = stmt.where(ShopHoistRequest.member_id == member_id)
    if status is not None:
        stmt = stmt.where(ShopHoistRequest.status == status)
    return list(session.scalars(stmt).all())


def create_shop_hoist_request(
    session: Session,
    *,
    member_id: UUID,
    hoist_id: UUID,
    start_at: datetime,
    end_at: datetime,
    notes: str | None,
    created_by_kind: ActorKind,
    created_by_id: str,
) -> ShopHoistRequest:
    """Store a pending request. Does not create a booking and does not touch the ledger."""
    start_at = as_utc(start_at)
    end_at = as_utc(end_at)

    hoist = session.get(Hoist, hoist_id)
    if hoist is None:
        raise _error(404, "not_found", "Hoist not found.")
    if not hoist.is_shop:
        raise _error(
            400,
            "not_shop_hoist",
            "Only the shop hoist takes a request. Bays 1-5 are a direct booking.",
        )
    if hoist.status in UNAVAILABLE_HOIST:
        raise _error(400, "hoist_unavailable", "That hoist is in maintenance or locked.")

    member = session.scalars(
        select(Member).options(selectinload(Member.tier)).where(Member.id == member_id)
    ).first()
    if member is None:
        raise _error(404, "not_found", "Member not found.")
    if member.status != MemberStatus.ACTIVE:
        raise _error(400, "member_not_bookable", "Only active members can request the shop hoist.")

    quote, _balance, _after = preview_reserve(
        session,
        start_at=start_at,
        end_at=end_at,
        member_id=member.id,
    )
    window = timedelta(days=member.tier.booking_window_days)
    if start_at > as_utc(shop_now()) + window:
        raise _error(
            400,
            "booking_window",
            f"Start is outside this member's {member.tier.booking_window_days}-day booking window.",
        )

    row = ShopHoistRequest(
        member_id=member.id,
        hoist_id=hoist.id,
        start_at=start_at,
        end_at=end_at,
        status=ShopHoistRequestStatus.PENDING,
        token_quote=quote.final_reserve_cost,
        pricing_rule=quote.as_rule(),
        notes=notes,
        created_by_kind=created_by_kind,
        created_by_id=created_by_id,
    )
    session.add(row)
    session.flush()
    return get_shop_hoist_request(session, row.id)


def _decide(row: ShopHoistRequest, principal: Principal, *, status: ShopHoistRequestStatus) -> None:
    kind, actor_id = actor_of(principal)
    row.status = status
    row.decided_by_kind = kind
    row.decided_by_id = actor_id
    row.decided_at = datetime.now(timezone.utc)


def approve_shop_hoist_request(
    session: Session, request_id: UUID, principal: Principal
) -> tuple[ShopHoistRequest, StaffAction]:
    """Turn a pending request into a confirmed booking and reserve tokens."""
    row = get_shop_hoist_request(session, request_id)
    if row.status != ShopHoistRequestStatus.PENDING:
        raise _error(400, "invalid_transition", "Only a pending shop hoist request can be approved.")
    reject_own_request(principal, row.created_by_kind, row.created_by_id)
    if row.hoist.status in UNAVAILABLE_HOIST:
        raise _error(400, "hoist_unavailable", "That hoist is in maintenance or locked.")
    member = row.member
    if member.status != MemberStatus.ACTIVE:
        raise _error(400, "member_not_bookable", "Only active members can hold an approved shop hoist hour.")
    quote = Decimal(row.token_quote)
    if open_booking_count(session, member.id) >= member.tier.max_simultaneous_bookings:
        raise _error(
            400,
            "max_simultaneous_bookings",
            "Member is already at the tier's simultaneous booking limit.",
        )
    if Decimal(member.token_balance) < quote:
        raise _error(400, "insufficient_tokens", "Member does not have enough tokens to reserve.")
    if hoist_has_overlap(
        session,
        row.hoist_id,
        row.start_at,
        row.end_at,
        statuses=HOLDING_STATUSES,
    ):
        raise _error(
            409,
            "hoist_overlap",
            "That hour is already booked. This approval did not take tokens.",
        )

    booking = Booking(
        member_id=member.id,
        hoist_id=row.hoist_id,
        start_at=row.start_at,
        end_at=row.end_at,
        kind=BookingKind.CUSTOMER,
        status=BookingStatus.CONFIRMED,
        reserved_tokens=quote,
        pricing_rule=row.pricing_rule,
        notes=row.notes,
    )
    session.add(booking)
    session.flush()
    apply_ledger(
        session,
        member,
        kind=TokenTransactionKind.BOOKING_RESERVE,
        amount=-quote,
        booking_id=booking.id,
        note="Reserve tokens for an approved shop hoist request",
        meta={"pricing_rule": row.pricing_rule} if row.pricing_rule else None,
    )
    row.booking_id = booking.id
    _decide(row, principal, status=ShopHoistRequestStatus.APPROVED)
    session.add(row)
    action = record_action(
        session,
        principal=principal,
        action="approve",
        request_id=row.id,
        subject=StaffSubject.SHOP_HOIST,
    )
    session.flush()
    return get_shop_hoist_request(session, row.id), action


def deny_shop_hoist_request(
    session: Session, request_id: UUID, principal: Principal
) -> tuple[ShopHoistRequest, StaffAction]:
    """Refuse a pending request. Tokens stay where they are."""
    row = get_shop_hoist_request(session, request_id)
    if row.status != ShopHoistRequestStatus.PENDING:
        raise _error(400, "invalid_transition", "Only a pending shop hoist request can be denied.")
    _decide(row, principal, status=ShopHoistRequestStatus.DENIED)
    session.add(row)
    action = record_action(
        session,
        principal=principal,
        action="deny",
        request_id=row.id,
        subject=StaffSubject.SHOP_HOIST,
    )
    session.flush()
    return get_shop_hoist_request(session, row.id), action
