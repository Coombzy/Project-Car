"""Windowed schedule query for staff."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.auth import Principal
from app.models import Booking, StaffSubject
from app.services.staff import record_action


def read_schedule_window(
    session: Session,
    principal: Principal,
    *,
    window_start: datetime,
    window_end: datetime,
    limit: int,
) -> list[Booking]:
    rows = list(
        session.scalars(
            select(Booking)
            .options(selectinload(Booking.member), selectinload(Booking.hoist))
            .where(Booking.start_at >= window_start, Booking.start_at < window_end)
            .order_by(Booking.start_at)
            .limit(limit)
        ).all()
    )
    record_action(
        session,
        principal=principal,
        action="read",
        request_id=None,
        subject=StaffSubject.SCHEDULE,
    )
    return rows
