from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.deps import DbSession, Owner
from app.models import Booking, BookingStatus, Hoist, Member, MemberStatus, WaitlistEntry
from app.schemas import BookingOut, DashboardOut, HoistSnapshotOut, MemberAtRiskOut
from app.shop_time import day_bounds, shop_now

router = APIRouter(tags=["dashboard"])

TOKEN_AT_RISK_BELOW = Decimal("2")


@router.get("/dashboard", response_model=DashboardOut)
def get_dashboard(session: DbSession, _owner: Owner) -> DashboardOut:
    start, end = day_bounds(shop_now().date())
    hoists = session.scalars(select(Hoist).order_by(Hoist.name)).all()
    today_rows = session.scalars(
        select(Booking)
        .options(selectinload(Booking.member), selectinload(Booking.hoist))
        .where(
            Booking.start_at < end,
            Booking.end_at > start,
            Booking.status != BookingStatus.CANCELLED,
        )
        .order_by(Booking.start_at)
    ).all()
    today = [BookingOut.from_booking(row) for row in today_rows]
    by_hoist = {
        row.hoist_id: BookingOut.from_booking(row)
        for row in today_rows
        if row.status == BookingStatus.ACTIVE
    }

    waitlist_count = session.scalar(select(func.count()).select_from(WaitlistEntry)) or 0
    at_risk_rows = session.scalars(
        select(Member)
        .where(
            Member.status == MemberStatus.ACTIVE,
            Member.token_balance < TOKEN_AT_RISK_BELOW,
        )
        .order_by(Member.token_balance, Member.name)
    ).all()

    return DashboardOut(
        hoists=[
            HoistSnapshotOut(
                id=hoist.id,
                name=hoist.name,
                location_label=hoist.location_label,
                status=hoist.status,
                created_at=hoist.created_at,
                updated_at=hoist.updated_at,
                current_booking=by_hoist.get(hoist.id),
            )
            for hoist in hoists
        ],
        today_bookings=today,
        waitlist_count=int(waitlist_count),
        token_at_risk=[
            MemberAtRiskOut(
                id=row.id,
                name=row.name,
                email=row.email,
                tier_name=row.tier_name,
                token_balance=row.token_balance,
            )
            for row in at_risk_rows
        ],
    )
