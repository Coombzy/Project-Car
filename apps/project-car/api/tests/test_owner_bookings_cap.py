"""Owner GET /bookings is capped (PC-new-2).

`limit` defaults to 500 and must be 1..1000 (422 outside that); `offset` >= 0.
Order stays start_at ascending.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from uuid import UUID

from fastapi.testclient import TestClient

from app.models import Booking, BookingKind, BookingStatus
from app.shop_time import as_utc
from tests.conftest import AUTH, create_hoist, create_member

TOTAL = 505
_BASE = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _seed(client: TestClient, member_id: str, hoist_id: str) -> None:
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        for index in range(TOTAL):
            start = as_utc(_BASE + timedelta(hours=index))
            session.add(
                Booking(
                    member_id=UUID(member_id),
                    hoist_id=UUID(hoist_id),
                    start_at=start,
                    end_at=as_utc(start + timedelta(hours=1)),
                    kind=BookingKind.CUSTOMER,
                    status=BookingStatus.CONFIRMED,
                    reserved_tokens=Decimal("0"),
                    notes=f"visit-{index:03d}",
                )
            )
        session.commit()
    finally:
        session.close()


def _notes(response) -> list[str]:
    assert response.status_code == 200, response.text
    return [row["notes"] for row in response.json()]


def test_owner_bookings_list_caps_rows(client: TestClient) -> None:
    member = create_member(
        client, name="Ada Reyes", email="owner-cap@example.com", tier_name="premium", allocate_tokens=False
    )
    hoist = create_hoist(client, name="Bay 1")
    _seed(client, member["id"], hoist["id"])

    default = _notes(client.get("/bookings", headers=AUTH))
    assert default == [f"visit-{i:03d}" for i in range(500)]

    tail = _notes(client.get("/bookings", headers=AUTH, params={"limit": 10, "offset": 500}))
    assert tail == [f"visit-{i:03d}" for i in range(500, TOTAL)]

    everything = _notes(client.get("/bookings", headers=AUTH, params={"limit": 1000}))
    assert len(everything) == TOTAL

    for params in ({"limit": 0}, {"limit": 1001}, {"offset": -1}):
        response = client.get("/bookings", headers=AUTH, params=params)
        assert response.status_code == 422, (params, response.text)
