"""Owner files an incident and lists newest first.

On a tree with no incidents router, POST /incidents is 404 and the 201
assertion fails. The same assertions pass once the router is mounted.
"""

from __future__ import annotations

from datetime import timedelta
from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import BillingTransaction, Incident, TokenTransaction
from app.shop_time import shop_now
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


def _rewind(client: TestClient, incident_id: str) -> None:
    session = _session(client)
    try:
        row = session.get(Incident, UUID(incident_id))
        assert row is not None
        row.created_at = row.created_at - timedelta(minutes=5)
        session.commit()
    finally:
        session.close()


def _window(hours_from_now: int, length_hours: float = 2) -> tuple[str, str]:
    start = shop_now() + timedelta(hours=hours_from_now)
    end = start + timedelta(hours=length_hours)
    return start.isoformat(), end.isoformat()


def test_owner_creates_an_incident_and_lists_newest_first(client: TestClient) -> None:
    member = create_member(client)
    hoist = create_hoist(client)
    start, end = _window(4)
    booking = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": start,
            "end_at": end,
            "notes": "Door work",
        },
    )
    assert booking.status_code == 201, booking.text
    booking_id = booking.json()["id"]

    ledger_before = _count(client, TokenTransaction)
    billing_before = _count(client, BillingTransaction)

    damage = client.post(
        "/incidents",
        headers=AUTH,
        json={
            "kind": "damage",
            "member_id": member["id"],
            "booking_id": booking_id,
            "note": "Scratched the door",
        },
    )
    assert damage.status_code == 201, damage.text
    damage_body = damage.json()
    assert damage_body["kind"] == "damage"
    assert damage_body["member_id"] == member["id"]
    assert damage_body["booking_id"] == booking_id
    assert damage_body["note"] == "Scratched the door"
    _rewind(client, damage_body["id"])

    injury = client.post(
        "/incidents",
        headers=AUTH,
        json={"kind": "injury", "note": "Cut on the bay"},
    )
    assert injury.status_code == 201, injury.text
    injury_body = injury.json()
    assert injury_body["kind"] == "injury"
    assert injury_body["member_id"] is None
    assert injury_body["booking_id"] is None
    assert injury_body["note"] == "Cut on the bay"

    assert _count(client, TokenTransaction) == ledger_before
    assert _count(client, BillingTransaction) == billing_before
    assert _count(client, Incident) == 2

    listed = client.get("/incidents", headers=AUTH)
    assert listed.status_code == 200, listed.text
    assert [row["id"] for row in listed.json()] == [injury_body["id"], damage_body["id"]]

    newest = client.get("/incidents", headers=AUTH, params={"limit": 1, "offset": 0})
    assert newest.status_code == 200, newest.text
    assert [row["id"] for row in newest.json()] == [injury_body["id"]]

    older = client.get("/incidents", headers=AUTH, params={"limit": 1, "offset": 1})
    assert older.status_code == 200, older.text
    assert [row["id"] for row in older.json()] == [damage_body["id"]]

    unknown = client.post(
        "/incidents",
        headers=AUTH,
        json={"kind": "volcano", "note": "Not a kind"},
    )
    assert unknown.status_code == 422, unknown.text
    assert unknown.json()["error"]["code"] == "validation_error"
    assert _count(client, Incident) == 2
    assert _count(client, TokenTransaction) == ledger_before
    assert _count(client, BillingTransaction) == billing_before

    login_member(client, member["email"])
    denied = client.post(
        "/incidents",
        json={"kind": "damage", "note": "Member cannot file"},
    )
    assert denied.status_code == 403, denied.text
    assert denied.json()["error"]["code"] == "forbidden"
    denied_list = client.get("/incidents")
    assert denied_list.status_code == 403, denied_list.text
    assert denied_list.json()["error"]["code"] == "forbidden"
    assert _count(client, Incident) == 2
    assert _count(client, TokenTransaction) == ledger_before
    assert _count(client, BillingTransaction) == billing_before
