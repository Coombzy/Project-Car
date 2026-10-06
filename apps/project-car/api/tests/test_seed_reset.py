"""Reset clears migration 20261004_0011 rows whose foreign keys are ON DELETE RESTRICT.

Those tables are shop_hoist_requests (member and hoist), staff_parts_requests
(member), tool_crib_exceptions (member), and refund_requests (booking).
shop_jobs and staff_drafts in that migration are ON DELETE SET NULL.
parts_requests.member_id is ON DELETE CASCADE. tool_crib_events from
20261004_0009 is already cleared with job_events.
"""

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import (
    ActorKind,
    Booking,
    Hoist,
    Member,
    RefundRequest,
    ShopHoistRequest,
    ShopHoistRequestStatus,
    StaffPartsRequest,
    ToolCribException,
)
from app.seed import seed, seed_id
from app.shop_time import shop_now

RESTRICT_CHILDREN = (
    ShopHoistRequest,
    StaffPartsRequest,
    ToolCribException,
    RefundRequest,
)


def _session(client: TestClient) -> Session:
    factory = client.session_factory  # type: ignore[attr-defined]
    return factory()


def _count(session: Session, model: type) -> int:
    return int(session.scalar(select(func.count()).select_from(model)) or 0)


def test_seed_reset_clears_restrict_children(client: TestClient) -> None:
    session = _session(client)
    try:
        seed(session)
        member_id = seed_id("member", "ada")
        hoist_id = seed_id("hoist", "bay-3")
        booking_id = seed_id("booking", "wed-ada")
        assert session.get(Member, member_id) is not None
        assert session.get(Hoist, hoist_id) is not None
        assert session.get(Booking, booking_id) is not None

        start = shop_now()
        session.add(
            ShopHoistRequest(
                member_id=member_id,
                hoist_id=hoist_id,
                start_at=start,
                end_at=start + timedelta(hours=1),
                status=ShopHoistRequestStatus.PENDING,
                token_quote=Decimal("100.00"),
                created_by_kind=ActorKind.HUMAN,
                created_by_id="owner@projectcar.ca",
            )
        )
        session.add(
            StaffPartsRequest(
                member_id=member_id,
                sku="PT-PAD-001",
                status=ShopHoistRequestStatus.PENDING,
                created_by_kind=ActorKind.HUMAN,
                created_by_id="owner@projectcar.ca",
            )
        )
        session.add(
            ToolCribException(
                member_id=member_id,
                tool_code="TC-FL-001",
                status=ShopHoistRequestStatus.PENDING,
                created_by_kind=ActorKind.HUMAN,
                created_by_id="owner@projectcar.ca",
            )
        )
        session.add(
            RefundRequest(
                booking_id=booking_id,
                status=ShopHoistRequestStatus.PENDING,
                created_by_kind=ActorKind.HUMAN,
                created_by_id="owner@projectcar.ca",
            )
        )
        session.commit()
        assert [_count(session, model) for model in RESTRICT_CHILDREN] == [1, 1, 1, 1]

        session.connection().exec_driver_sql("PRAGMA foreign_keys=ON")
        seed(session, reset=True)
        session.commit()
        assert [_count(session, model) for model in RESTRICT_CHILDREN] == [0, 0, 0, 0]
    finally:
        session.close()
