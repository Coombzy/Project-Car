"""Read-only printer of holding bookings that overlap on one hoist.

Half-open [start_at, end_at). No writes, no commits, no alembic.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Booking
from app.services.bookings import HOLDING_STATUSES


def overlapping_booking_ids(session: Session) -> list[str]:
    rows = session.scalars(select(Booking).where(Booking.status.in_(HOLDING_STATUSES))).all()
    groups: dict = {}
    for row in rows:
        groups.setdefault(row.hoist_id, []).append(row)
    seen: list[str] = []
    for group in groups.values():
        ordered = sorted(group, key=lambda row: (row.start_at, str(row.id)))
        for index, left in enumerate(ordered):
            for right in ordered[index + 1 :]:
                if right.start_at >= left.end_at:
                    break
                for item in (left, right):
                    text = str(item.id)
                    if text not in seen:
                        seen.append(text)
    return seen


def main(session: Session | None = None) -> int:
    owns = session is None
    if session is None:
        session = SessionLocal()
    try:
        ids = overlapping_booking_ids(session)
        print("no overlaps" if not ids else "\n".join(ids))
        return 0
    finally:
        if owns:
            session.close()


if __name__ == "__main__":
    sys.exit(main())
