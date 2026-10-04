"""Shop hoist requests.

A request is not a booking. It does not hold the hour and does not move tokens.
Approval is a later step. This module does not approve.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import (
    ActorKind,
    Hoist,
    Member,
    MemberStatus,
    ShopHoistRequest,
    ShopHoistRequestStatus,
)
from app.services.bookings import UNAVAILABLE_HOIST, preview_reserve
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
