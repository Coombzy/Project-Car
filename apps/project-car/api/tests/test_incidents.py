"""Owner files an incident and lists newest first.

On a tree with no incidents router, POST /incidents is 404 and the 201
assertion fails. The same assertions pass once the router is mounted.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import UUID, uuid4

from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import BillingTransaction, Incident, IncidentKind, IncidentSeverity, TokenTransaction
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


def _store_incidents(client: TestClient, count: int) -> list[str]:
    """Insert `count` incidents, oldest first. Notes come back newest first."""
    session = _session(client)
    try:
        base = datetime(2026, 6, 1, tzinfo=timezone.utc)
        for index in range(count):
            created = base + timedelta(minutes=index)
            session.add(
                Incident(
                    kind=IncidentKind.OTHER,
                    severity=IncidentSeverity.MINOR,
                    description=f"note-{index:03d}",
                    photos=[],
                    created_at=created,
                    updated_at=created,
                )
            )
        session.commit()
    finally:
        session.close()
    return [f"note-{index:03d}" for index in range(count - 1, -1, -1)]


def test_list_limit_defaults_to_200_and_rejects_501(client: TestClient) -> None:
    """201 stored rows: the default page is the 200 newest.

    `limit=500` is accepted and returns every row. `limit=501` is 422 and
    inserts nothing. A cap of 200 rejects `limit=500`.
    """
    newest_first = _store_incidents(client, 201)
    assert _count(client, Incident) == 201

    listed = client.get("/incidents", headers=AUTH)
    assert listed.status_code == 200, listed.text
    assert [row["note"] for row in listed.json()] == newest_first[:200]

    wide = client.get("/incidents", headers=AUTH, params={"limit": 500})
    assert wide.status_code == 200, wide.text
    assert [row["note"] for row in wide.json()] == newest_first

    rejected = client.get("/incidents", headers=AUTH, params={"limit": 501})
    assert rejected.status_code == 422, rejected.text
    assert rejected.json()["error"]["code"] == "validation_error"
    assert _count(client, Incident) == 201


def test_refused_incident_writes_nothing_and_backlog_lists_r92(client: TestClient) -> None:
    """Refusals write no incident and no ledger row.

    Blank note is 422, an unknown member or booking is 404, and no session
    is 401. Those checks already hold once the router is mounted. The backlog
    check fails while Skipped still says the desk has no router, and passes
    once that bullet is gone and R92 names POST /incidents and GET /incidents.
    """
    ledger_before = _count(client, TokenTransaction)
    billing_before = _count(client, BillingTransaction)

    for note in ("", "   "):
        blank = client.post(
            "/incidents",
            headers=AUTH,
            json={"kind": "damage", "note": note},
        )
        assert blank.status_code == 422, blank.text
        assert blank.json()["error"]["code"] == "validation_error"

    missing_member = client.post(
        "/incidents",
        headers=AUTH,
        json={"kind": "damage", "member_id": str(uuid4()), "note": "No such member"},
    )
    assert missing_member.status_code == 404, missing_member.text
    assert missing_member.json()["error"]["code"] == "not_found"
    assert missing_member.json()["error"]["message"] == "Member not found."

    missing_booking = client.post(
        "/incidents",
        headers=AUTH,
        json={"kind": "injury", "booking_id": str(uuid4()), "note": "No such booking"},
    )
    assert missing_booking.status_code == 404, missing_booking.text
    assert missing_booking.json()["error"]["code"] == "not_found"
    assert missing_booking.json()["error"]["message"] == "Booking not found."

    logged_out = client.post(
        "/incidents",
        json={"kind": "other", "note": "No session"},
    )
    assert logged_out.status_code == 401, logged_out.text
    assert logged_out.json()["error"]["code"] == "unauthorized"
    logged_out_list = client.get("/incidents")
    assert logged_out_list.status_code == 401, logged_out_list.text
    assert logged_out_list.json()["error"]["code"] == "unauthorized"

    assert _count(client, Incident) == 0
    assert _count(client, TokenTransaction) == ledger_before
    assert _count(client, BillingTransaction) == billing_before

    backlog = Path(__file__).resolve().parents[4].joinpath("Docs", "backlog.md").read_text(
        encoding="utf-8"
    )
    start = backlog.find("### R92. Incidents have a table and no API")
    assert start != -1
    section = backlog[start:]
    next_heading = section.find("\n## ")
    if next_heading != -1:
        section = section[:next_heading]
    assert "POST /incidents" in section
    assert "GET /incidents" in section
    assert "- A general incident desk. `Incident` has a model and no router." not in backlog
