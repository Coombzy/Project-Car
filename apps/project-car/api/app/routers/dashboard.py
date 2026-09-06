from __future__ import annotations

from collections import defaultdict
from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.config import get_settings
from app.deps import AnyPrincipal, DbSession, Owner
from app.models import (
    Booking,
    BookingStatus,
    Hoist,
    Member,
    MemberStatus,
    PartsOrder,
    PartsOrderStatus,
    WaitlistEntry,
)
from app.schemas import (
    BookedHourOut,
    BookingOut,
    CalendarStatusOut,
    DashboardOut,
    HoistSnapshotOut,
    MemberAtRiskOut,
    MemberDashboardOut,
    PartsOrderOut,
    TodoOut,
)
from app.services.calendar_oauth import calendar_payload
from app.services.hours import expand_booked_hours
from app.services.todos import list_todos
from app.shop_time import PRICING_TZ, day_bounds, next_24h_bounds, shop_now

router = APIRouter(tags=["dashboard"])

TOKEN_AT_RISK_BELOW = Decimal("2")
OPEN_HOUR_STATUSES = (
    BookingStatus.PENDING,
    BookingStatus.CONFIRMED,
    BookingStatus.ACTIVE,
    BookingStatus.OVERDUE,
)
CURRENT_PO_STATUSES = (
    PartsOrderStatus.ORDERED,
    PartsOrderStatus.SHIPPED,
    PartsOrderStatus.IN_TRANSIT,
)


def _booked_hour(row: dict) -> BookedHourOut:
    return BookedHourOut.model_validate(row)


def _hoist_snapshots(
    hoists: list[Hoist],
    hour_rows: list[dict],
    current_by_hoist: dict[UUID, Booking],
) -> list[HoistSnapshotOut]:
    hours_by_hoist: dict[UUID, list[BookedHourOut]] = defaultdict(list)
    for row in hour_rows:
        hours_by_hoist[row["hoist_id"]].append(_booked_hour(row))
    return [
        HoistSnapshotOut(
            id=hoist.id,
            name=hoist.name,
            location_label=hoist.location_label,
            status=hoist.status,
            is_shop=hoist.is_shop,
            created_at=hoist.created_at,
            updated_at=hoist.updated_at,
            current_booking=(
                BookingOut.from_booking(current_by_hoist[hoist.id])
                if hoist.id in current_by_hoist
                else None
            ),
            next_hours=hours_by_hoist.get(hoist.id, []),
        )
        for hoist in hoists
    ]


def _window_bookings(session, window_start, window_end) -> list[Booking]:
    return list(
        session.scalars(
            select(Booking)
            .options(selectinload(Booking.member), selectinload(Booking.hoist))
            .where(
                Booking.start_at < window_end,
                Booking.end_at > window_start,
                Booking.status.in_(OPEN_HOUR_STATUSES),
            )
            .order_by(Booking.start_at)
        ).all()
    )


def _current_parts_orders(session) -> list[PartsOrder]:
    open_rows = list(
        session.scalars(
            select(PartsOrder)
            .where(PartsOrder.status.in_(CURRENT_PO_STATUSES))
            .order_by(PartsOrder.ordered_at.desc())
        ).all()
    )
    if len(open_rows) >= 6:
        return open_rows[:6]
    extra = list(
        session.scalars(
            select(PartsOrder)
            .where(PartsOrder.status == PartsOrderStatus.RECEIVED)
            .order_by(PartsOrder.received_at.desc())
            .limit(6 - len(open_rows))
        ).all()
    )
    return open_rows + extra


@router.get("/dashboard", response_model=DashboardOut)
def get_dashboard(session: DbSession, owner: Owner) -> DashboardOut:
    start, end = day_bounds(shop_now().date())
    window_start, window_end = next_24h_bounds()
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
        row.hoist_id: row
        for row in today_rows
        if row.status == BookingStatus.ACTIVE
    }
    hour_rows = expand_booked_hours(_window_bookings(session, window_start, window_end), window_start, window_end)

    waitlist_count = session.scalar(select(func.count()).select_from(WaitlistEntry)) or 0
    at_risk_rows = session.scalars(
        select(Member)
        .where(
            Member.status == MemberStatus.ACTIVE,
            Member.token_balance < TOKEN_AT_RISK_BELOW,
        )
        .order_by(Member.token_balance, Member.name)
    ).all()
    calendar = CalendarStatusOut.model_validate(calendar_payload(session, owner, get_settings()))

    return DashboardOut(
        tz=str(PRICING_TZ),
        window_start=window_start,
        window_end=window_end,
        hoists=_hoist_snapshots(list(hoists), hour_rows, by_hoist),
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
        todos=[TodoOut.model_validate(row) for row in list_todos(session, owner)],
        parts_orders=[PartsOrderOut.model_validate(row) for row in _current_parts_orders(session)],
        calendar=calendar,
    )


def member_dashboard_payload(session, principal: AnyPrincipal) -> MemberDashboardOut:
    window_start, window_end = next_24h_bounds()
    bookings = _window_bookings(session, window_start, window_end)
    hour_rows = expand_booked_hours(bookings, window_start, window_end, member_id=principal.member_id)
    hoist_ids = {row["hoist_id"] for row in hour_rows}
    hoists = []
    if hoist_ids:
        hoists = list(
            session.scalars(
                select(Hoist)
                .where(Hoist.id.in_(hoist_ids), Hoist.is_shop.is_(False))
                .order_by(Hoist.name)
            ).all()
        )
    calendar = CalendarStatusOut.model_validate(calendar_payload(session, principal, get_settings()))
    return MemberDashboardOut(
        tz=str(PRICING_TZ),
        window_start=window_start,
        window_end=window_end,
        hoists=_hoist_snapshots(hoists, hour_rows, {}),
        todos=[TodoOut.model_validate(row) for row in list_todos(session, principal)],
        calendar=calendar,
    )

