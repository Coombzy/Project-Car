"""Member self-serve: own balance, quote, book / confirm / cancel.

Reuses Owner booking services (duration × band × overlay + ledger). Members
act only on their own rows, kind=customer, and cannot book the shop hoist.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.deps import DbSession, MemberUser
from app.models import Booking, BookingKind, Hoist, Member, TokenTransaction
from app.schemas import (
    BookingOut,
    BookingQuoteOut,
    FillPreviewOut,
    HoistOut,
    MemberBookingCreate,
    MemberBookingQuoteRequest,
    MemberDashboardOut,
    MemberScheduleOut,
    MemberSelfOut,
    OccupancyOut,
    PricingRuleOut,
    TokenTransactionOut,
)
from app.routers.dashboard import member_dashboard_payload
from app.services import bookings as booking_service
from app.services.fill import snapshot_next_day
from app.shop_time import as_utc

router = APIRouter(prefix="/member", tags=["member"])


def _forbidden(message: str = "Members can only act on their own bookings.") -> HTTPException:
    return HTTPException(status_code=403, detail={"code": "forbidden", "message": message})


def _own_member(session, principal: MemberUser) -> Member:
    member = session.scalars(
        select(Member).options(selectinload(Member.tier)).where(Member.id == principal.member_id)
    ).first()
    if member is None:
        raise HTTPException(
            status_code=401,
            detail={"code": "unauthorized", "message": "Member authentication required."},
        )
    return member


def _own_booking(session, principal: MemberUser, booking_id: UUID) -> Booking:
    booking = booking_service.get_booking(session, booking_id)
    if booking.member_id != principal.member_id:
        raise _forbidden()
    return booking


def _customer_hoists(session) -> list[Hoist]:
    return list(
        session.scalars(select(Hoist).where(Hoist.is_shop.is_(False)).order_by(Hoist.name)).all()
    )


@router.get("/me", response_model=MemberSelfOut)
def member_me(session: DbSession, principal: MemberUser) -> MemberSelfOut:
    member = session.scalars(
        select(Member)
        .options(
            selectinload(Member.tier),
            selectinload(Member.bookings).selectinload(Booking.hoist),
            selectinload(Member.bookings).selectinload(Booking.member),
            selectinload(Member.token_transactions),
        )
        .where(Member.id == principal.member_id)
    ).first()
    if member is None:
        raise HTTPException(
            status_code=401,
            detail={"code": "unauthorized", "message": "Member authentication required."},
        )
    bookings = sorted(member.bookings, key=lambda row: row.start_at, reverse=True)
    tokens = sorted(member.token_transactions, key=lambda row: row.created_at, reverse=True)
    return MemberSelfOut(
        id=member.id,
        name=member.name,
        email=member.email,
        phone=member.phone,
        tier_name=member.tier_name,
        status=member.status,
        waiver_signed_at=member.waiver_signed_at,
        waiver_version=member.waiver_version,
        emergency_contact_name=member.emergency_contact_name,
        emergency_contact_phone=member.emergency_contact_phone,
        token_balance=member.token_balance,
        deposit_balance=member.deposit_balance,
        created_at=member.created_at,
        updated_at=member.updated_at,
        booking_window_days=member.tier.booking_window_days,
        max_simultaneous_bookings=member.tier.max_simultaneous_bookings,
        included_tokens=member.tier.included_tokens,
        bookings=[BookingOut.from_booking(row) for row in bookings],
        tokens=[TokenTransactionOut.model_validate(row) for row in tokens],
    )


@router.get("/dashboard", response_model=MemberDashboardOut)
def member_dashboard(session: DbSession, principal: MemberUser) -> MemberDashboardOut:
    return member_dashboard_payload(session, principal)


@router.get("/tokens", response_model=list[TokenTransactionOut])
def member_tokens(session: DbSession, principal: MemberUser) -> list[TokenTransactionOut]:
    rows = session.scalars(
        select(TokenTransaction)
        .where(TokenTransaction.member_id == principal.member_id)
        .order_by(TokenTransaction.created_at.desc())
    ).all()
    return [TokenTransactionOut.model_validate(row) for row in rows]


@router.get("/hoists", response_model=list[HoistOut])
def member_hoists(session: DbSession, _principal: MemberUser) -> list[HoistOut]:
    return [HoistOut.model_validate(row) for row in _customer_hoists(session)]


@router.get("/bookings", response_model=list[BookingOut])
def member_bookings(
    session: DbSession,
    principal: MemberUser,
    hoist_id: UUID | None = None,
    window_start: datetime | None = Query(default=None),
    window_end: datetime | None = Query(default=None),
) -> list[BookingOut]:
    stmt = (
        select(Booking)
        .options(selectinload(Booking.member), selectinload(Booking.hoist))
        .where(Booking.member_id == principal.member_id)
        .order_by(Booking.start_at)
    )
    if hoist_id is not None:
        stmt = stmt.where(Booking.hoist_id == hoist_id)
    if window_start is not None:
        stmt = stmt.where(Booking.end_at > as_utc(window_start))
    if window_end is not None:
        stmt = stmt.where(Booking.start_at < as_utc(window_end))
    return [BookingOut.from_booking(row) for row in session.scalars(stmt).all()]


@router.get("/schedule", response_model=MemberScheduleOut)
def member_schedule(
    session: DbSession,
    principal: MemberUser,
    window_start: datetime | None = Query(default=None),
    window_end: datetime | None = Query(default=None),
) -> MemberScheduleOut:
    hoists = _customer_hoists(session)
    hoist_ids = [row.id for row in hoists]
    stmt = (
        select(Booking)
        .options(selectinload(Booking.member), selectinload(Booking.hoist))
        .where(
            Booking.hoist_id.in_(hoist_ids),
            Booking.kind == BookingKind.CUSTOMER,
            Booking.status.in_(booking_service.OPEN_STATUSES),
        )
        .order_by(Booking.start_at)
    )
    if window_start is not None:
        stmt = stmt.where(Booking.end_at > as_utc(window_start))
    if window_end is not None:
        stmt = stmt.where(Booking.start_at < as_utc(window_end))
    rows = session.scalars(stmt).all()
    own: list[BookingOut] = []
    occupancy: list[OccupancyOut] = []
    for row in rows:
        occupancy.append(
            OccupancyOut(
                booking_id=row.id,
                hoist_id=row.hoist_id,
                hoist_name=row.hoist.name,
                start_at=row.start_at,
                end_at=row.end_at,
                status=row.status,
                own=row.member_id == principal.member_id,
            )
        )
        if row.member_id == principal.member_id:
            own.append(BookingOut.from_booking(row))
    return MemberScheduleOut(
        hoists=[HoistOut.model_validate(row) for row in hoists],
        bookings=own,
        occupancy=occupancy,
    )


@router.get("/fill", response_model=FillPreviewOut)
def member_fill(session: DbSession, _principal: MemberUser) -> FillPreviewOut:
    return FillPreviewOut.from_snapshot(snapshot_next_day(session))


@router.post("/bookings/quote", response_model=BookingQuoteOut)
def member_quote(
    body: MemberBookingQuoteRequest,
    session: DbSession,
    principal: MemberUser,
) -> BookingQuoteOut:
    quote, balance, after = booking_service.preview_reserve(
        session,
        start_at=body.start_at,
        end_at=body.end_at,
        member_id=principal.member_id,
    )
    return BookingQuoteOut(
        pricing_rule=PricingRuleOut.model_validate(quote.as_rule()),
        reserved_tokens=quote.final_reserve_cost,
        token_balance=balance,
        token_balance_after=after,
    )


@router.post("/bookings", response_model=BookingOut, status_code=201)
def member_create_booking(
    body: MemberBookingCreate,
    session: DbSession,
    principal: MemberUser,
) -> BookingOut:
    _own_member(session, principal)
    booking = booking_service.create_booking(
        session,
        member_id=principal.member_id,
        hoist_id=body.hoist_id,
        start_at=body.start_at,
        end_at=body.end_at,
        notes=body.notes,
        kind=BookingKind.CUSTOMER,
    )
    return BookingOut.from_booking(booking)


@router.post("/bookings/{booking_id}/confirm", response_model=BookingOut)
def member_confirm_booking(
    booking_id: UUID,
    session: DbSession,
    principal: MemberUser,
) -> BookingOut:
    _own_booking(session, principal, booking_id)
    return BookingOut.from_booking(booking_service.confirm_booking(session, booking_id))


@router.post("/bookings/{booking_id}/cancel", response_model=BookingOut)
def member_cancel_booking(
    booking_id: UUID,
    session: DbSession,
    principal: MemberUser,
) -> BookingOut:
    _own_booking(session, principal, booking_id)
    return BookingOut.from_booking(booking_service.cancel_booking(session, booking_id))
