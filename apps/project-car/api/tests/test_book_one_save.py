"""Member Book creates and confirms in one save.

A refused Book leaves no pending hold. The balance and the hours stay as they were.
"""

from datetime import timedelta
from decimal import Decimal
from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy import func, select

from app.models import BookingHour
from tests.conftest import AUTH, create_hoist, create_member, login_member, next_hour


def _hours(client: TestClient) -> int:
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        return int(session.scalar(select(func.count()).select_from(BookingHour)) or 0)
    finally:
        session.close()


def _hours_for(client: TestClient, booking_id: str) -> int:
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        return int(
            session.scalar(
                select(func.count())
                .select_from(BookingHour)
                .where(BookingHour.booking_id == UUID(booking_id))
            )
            or 0
        )
    finally:
        session.close()


def _balance(client: TestClient, member_id: str) -> Decimal:
    body = client.get(f"/members/{member_id}", headers=AUTH).json()
    return Decimal(str(body["token_balance"]))


def test_member_book_is_confirmed_in_the_same_save(client: TestClient) -> None:
    member = create_member(client, email="book@example.com", tier_name="premium")
    hoist = create_hoist(client, name="Bay 1")
    start = next_hour(30)
    end = start + timedelta(hours=1)
    login_member(client, member["email"])
    quoted = client.post(
        "/member/bookings/quote",
        json={"start_at": start.isoformat(), "end_at": end.isoformat()},
    )
    assert quoted.status_code == 200, quoted.text
    created = client.post(
        "/member/bookings",
        json={
            "hoist_id": hoist["id"],
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
            "tokens": str(quoted.json()["reserved_tokens"]),
        },
    )
    assert created.status_code == 201, created.text
    assert created.json()["status"] == "confirmed"
    rows = client.get("/bookings", headers=AUTH).json()
    assert [row["status"] for row in rows] == ["confirmed"]
    assert _hours_for(client, created.json()["id"]) == 1


def test_refused_book_leaves_the_balance_and_the_hours(client: TestClient) -> None:
    broke = create_member(client, email="broke@example.com", tier_name="basic", allocate_tokens=False)
    holder = create_member(client, email="holder@example.com", tier_name="premium")
    hoist = create_hoist(client, name="Bay 1")
    start = next_hour(36)
    end = start + timedelta(hours=1)
    before = _balance(client, broke["id"])
    login_member(client, broke["email"])
    refused = client.post(
        "/member/bookings",
        json={"hoist_id": hoist["id"], "start_at": start.isoformat(), "end_at": end.isoformat()},
    )
    assert refused.status_code == 400, refused.text
    assert refused.json()["error"]["code"] == "insufficient_tokens"
    assert client.get("/bookings", headers=AUTH).json() == []
    assert _hours(client) == 0
    assert _balance(client, broke["id"]) == before

    login_member(client, holder["email"])
    quoted = client.post(
        "/member/bookings/quote",
        json={"start_at": start.isoformat(), "end_at": end.isoformat()},
    )
    assert quoted.status_code == 200, quoted.text
    taken = client.post(
        "/member/bookings",
        json={
            "hoist_id": hoist["id"],
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
            "tokens": str(quoted.json()["reserved_tokens"]),
        },
    )
    assert taken.status_code == 201, taken.text
    assert taken.json()["status"] == "confirmed"
    held_balance = _balance(client, holder["id"])
    held_hours = _hours(client)

    login_member(client, broke["email"])
    client.post(
        f"/members/{broke['id']}/tokens",
        headers=AUTH,
        json={"amount": "500", "reason": "Owner added tokens for a second try"},
    )
    funded = _balance(client, broke["id"])
    overlap = client.post(
        "/member/bookings",
        json={
            "hoist_id": hoist["id"],
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
            "tokens": str(quoted.json()["reserved_tokens"]),
        },
    )
    assert overlap.status_code == 409, overlap.text
    assert overlap.json()["error"]["code"] == "hoist_overlap"
    rows = client.get("/bookings", headers=AUTH).json()
    assert [row["id"] for row in rows] == [taken.json()["id"]]
    assert rows[0]["status"] == "confirmed"
    assert _hours(client) == held_hours
    assert _balance(client, holder["id"]) == held_balance
    assert _balance(client, broke["id"]) == funded
