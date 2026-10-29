"""Owner incident log. Create stores a row. List is newest first. No token ledger row."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from uuid import UUID, uuid4

from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import (
    BillingTransaction,
    Booking,
    BookingKind,
    BookingStatus,
    Incident,
    IncidentKind,
    IncidentSeverity,
    TokenTransaction,
)
from tests.conftest import AUTH, create_hoist, create_member, login_member


def _session(client: TestClient) -> Session:
    factory = client.session_factory  # type: ignore[attr-defined]
    return factory()


def _count(client: TestClient, model) -> int:
    session = _session(client)
    try:
        return int(session.scalar(select(func.count()).select_from(model)) or 0)
    finally:
        session.close()


def _incident(client: TestClient, incident_id: str) -> Incident:
    session = _session(client)
    try:
        row = session.get(Incident, UUID(incident_id))
        assert row is not None
        return row
    finally:
        session.close()


def _booking(client: TestClient, member_id: str, hoist_id: str) -> str:
    session = _session(client)
    try:
        start = datetime.now(timezone.utc) + timedelta(days=2)
        row = Booking(
            member_id=UUID(member_id),
            hoist_id=UUID(hoist_id),
            start_at=start,
            end_at=start + timedelta(hours=2),
            kind=BookingKind.CUSTOMER,
            status=BookingStatus.PENDING,
            reserved_tokens=Decimal("0"),
        )
        session.add(row)
        session.commit()
        return str(row.id)
    finally:
        session.close()


def test_owner_creates_an_incident_and_lists_newest_first(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com", name="Ada Reyes")
    hoist = create_hoist(client, name="Bay 1")
    booking_id = _booking(client, ada["id"], hoist["id"])
    tokens_before = _count(client, TokenTransaction)
    billing_before = _count(client, BillingTransaction)
    assert _count(client, Incident) == 0

    client.cookies.clear()
    created = client.post(
        "/incidents",
        headers=AUTH,
        json={
            "kind": "damage",
            "member_id": ada["id"],
            "booking_id": booking_id,
            "note": "  Scratched the door  ",
        },
    )
    assert created.status_code == 201, created.text
    damage = created.json()
    assert damage["kind"] == "damage"
    assert damage["note"] == "Scratched the door"
    assert damage["member_id"] == ada["id"]
    assert damage["booking_id"] == booking_id

    stored = _incident(client, damage["id"])
    assert stored.kind == IncidentKind.DAMAGE
    assert stored.description == "Scratched the door"
    assert str(stored.member_id) == ada["id"]
    assert str(stored.booking_id) == booking_id
    assert stored.severity == IncidentSeverity.MINOR
    assert stored.photos == []
    assert _count(client, Incident) == 1
    assert _count(client, TokenTransaction) == tokens_before
    assert _count(client, BillingTransaction) == billing_before

    injury = client.post(
        "/incidents",
        headers=AUTH,
        json={"kind": "injury", "note": "Cut on the grinder"},
    )
    assert injury.status_code == 201, injury.text
    assert injury.json()["kind"] == "injury"
    assert injury.json()["member_id"] is None
    assert injury.json()["booking_id"] is None
    assert injury.json()["note"] == "Cut on the grinder"

    late = client.post(
        "/incidents",
        headers=AUTH,
        json={"kind": "late_return", "member_id": ada["id"], "note": "Bay held past the end"},
    )
    assert late.status_code == 201, late.text
    assert late.json()["booking_id"] is None

    other = client.post(
        "/incidents",
        headers=AUTH,
        json={"kind": "other", "note": "Oil on the floor"},
    )
    assert other.status_code == 201, other.text

    listed = client.get("/incidents", headers=AUTH)
    assert listed.status_code == 200, listed.text
    notes = [row["note"] for row in listed.json()]
    assert notes == [
        "Oil on the floor",
        "Bay held past the end",
        "Cut on the grinder",
        "Scratched the door",
    ]
    assert [row["kind"] for row in listed.json()] == ["other", "late_return", "injury", "damage"]

    page = client.get("/incidents", headers=AUTH, params={"limit": 1, "offset": 0})
    assert page.status_code == 200, page.text
    assert [row["id"] for row in page.json()] == [other.json()["id"]]

    skipped = client.get("/incidents", headers=AUTH, params={"limit": 2, "offset": 1})
    assert [row["id"] for row in skipped.json()] == [late.json()["id"], injury.json()["id"]]

    empty = client.get("/incidents", headers=AUTH, params={"limit": 1, "offset": 4})
    assert empty.json() == []

    unknown = client.post(
        "/incidents",
        headers=AUTH,
        json={"kind": "flood", "note": "Bay flooded"},
    )
    assert unknown.status_code == 422, unknown.text
    assert unknown.json()["error"]["code"] == "validation_error"

    blank = client.post(
        "/incidents",
        headers=AUTH,
        json={"kind": "damage", "note": "   "},
    )
    assert blank.status_code == 422, blank.text
    assert _count(client, Incident) == 4

    missing_member = client.post(
        "/incidents",
        headers=AUTH,
        json={"kind": "damage", "member_id": str(uuid4()), "note": "No such member"},
    )
    assert missing_member.status_code == 404, missing_member.text
    assert missing_member.json()["error"]["code"] == "not_found"

    missing_booking = client.post(
        "/incidents",
        headers=AUTH,
        json={"kind": "damage", "booking_id": str(uuid4()), "note": "No such booking"},
    )
    assert missing_booking.status_code == 404, missing_booking.text
    assert _count(client, Incident) == 4

    login_member(client, "ada@example.com")
    member_post = client.post(
        "/incidents",
        json={"kind": "damage", "note": "Member must not file this"},
    )
    assert member_post.status_code == 403, member_post.text
    assert member_post.json()["error"]["code"] == "forbidden"
    member_list = client.get("/incidents")
    assert member_list.status_code == 403, member_list.text
    assert _count(client, Incident) == 4

    client.cookies.clear()
    anon = client.post("/incidents", json={"kind": "other", "note": "Nobody"})
    assert anon.status_code == 401, anon.text
    anon_list = client.get("/incidents")
    assert anon_list.status_code == 401, anon_list.text

    assert _count(client, Incident) == 4
    assert _count(client, TokenTransaction) == tokens_before
    assert _count(client, BillingTransaction) == billing_before
