from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Query
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.deps import DbSession, Owner
from app.models import Booking, BookingStatus
from app.schemas import BookingComplete, BookingCreate, BookingOut
from app.services import bookings as booking_service
from app.shop_time import as_utc

router = APIRouter(tags=["bookings"])


def _list_query(
    *,
    hoist_id: UUID | None,
    member_id: UUID | None,
    status: BookingStatus | None,
    window_start: datetime | None,
    window_end: datetime | None,
):
    stmt = (
        select(Booking)
        .options(selectinload(Booking.member), selectinload(Booking.hoist))
        .order_by(Booking.start_at)
    )
    if hoist_id is not None:
        stmt = stmt.where(Booking.hoist_id == hoist_id)
    if member_id is not None:
        stmt = stmt.where(Booking.member_id == member_id)
    if status is not None:
        stmt = stmt.where(Booking.status == status)
    if window_start is not None:
        stmt = stmt.where(Booking.end_at > as_utc(window_start))
    if window_end is not None:
        stmt = stmt.where(Booking.start_at < as_utc(window_end))
    return stmt


@router.get("/bookings", response_model=list[BookingOut])
def list_bookings(
    session: DbSession,
    _owner: Owner,
    hoist_id: UUID | None = None,
    member_id: UUID | None = None,
    status: BookingStatus | None = None,
    window_start: datetime | None = Query(default=None),
    window_end: datetime | None = Query(default=None),
) -> list[BookingOut]:
    rows = session.scalars(
        _list_query(
            hoist_id=hoist_id,
            member_id=member_id,
            status=status,
            window_start=window_start,
            window_end=window_end,
        )
    ).all()
    return [BookingOut.from_booking(row) for row in rows]


@router.post("/bookings", response_model=BookingOut, status_code=201)
def create_booking(body: BookingCreate, session: DbSession, _owner: Owner) -> BookingOut:
    booking = booking_service.create_booking(
        session,
        member_id=body.member_id,
        hoist_id=body.hoist_id,
        start_at=body.start_at,
        end_at=body.end_at,
        tokens=body.tokens,
        notes=body.notes,
    )
    return BookingOut.from_booking(booking)


@router.post("/bookings/{booking_id}/confirm", response_model=BookingOut)
def confirm_booking(booking_id: UUID, session: DbSession, _owner: Owner) -> BookingOut:
    return BookingOut.from_booking(booking_service.confirm_booking(session, booking_id))


@router.post("/bookings/{booking_id}/check-in", response_model=BookingOut)
def check_in_booking(booking_id: UUID, session: DbSession, _owner: Owner) -> BookingOut:
    return BookingOut.from_booking(booking_service.check_in_booking(session, booking_id))


@router.post("/bookings/{booking_id}/complete", response_model=BookingOut)
def complete_booking(
    booking_id: UUID,
    session: DbSession,
    _owner: Owner,
    body: BookingComplete | None = None,
) -> BookingOut:
    unused = body.unused_tokens if body is not None else Decimal("0")
    return BookingOut.from_booking(
        booking_service.complete_booking(session, booking_id, unused_tokens=unused)
    )


@router.post("/bookings/{booking_id}/cancel", response_model=BookingOut)
def cancel_booking(booking_id: UUID, session: DbSession, _owner: Owner) -> BookingOut:
    return BookingOut.from_booking(booking_service.cancel_booking(session, booking_id))
