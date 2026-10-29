"""GET /member/bookings/{id}/ics for the member's own visit."""

from __future__ import annotations

from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from app.shop_time import as_utc, shop_now
from tests.conftest import create_hoist, create_member, login_member


def _window(hours_from_now: int, length_hours: float = 2) -> tuple[str, str]:
    start = shop_now() + timedelta(hours=hours_from_now)
    end = start + timedelta(hours=length_hours)
    return start.isoformat(), end.isoformat()


def _ics_utc(value: str) -> str:
    return as_utc(datetime.fromisoformat(value)).strftime("%Y%m%dT%H%M%SZ")


def test_member_booking_ics_own_other_and_cancelled(client: TestClient) -> None:
    create_member(client, email="ada@example.com", tier_name="premium")
    create_member(client, name="Casey", email="casey@example.com", tier_name="basic")
    hoist = create_hoist(client, name="Bay 1")
    start, end = _window(8)

    login_member(client, "ada@example.com")
    created = client.post(
        "/member/bookings",
        json={"hoist_id": hoist["id"], "start_at": start, "end_at": end, "notes": "Miata"},
    )
    assert created.status_code == 201, created.text
    booking = created.json()

    ics = client.get(f"/member/bookings/{booking['id']}/ics")
    assert ics.status_code == 200, ics.text
    assert ics.headers["content-type"].startswith("text/calendar")
    body = ics.text
    assert body.count("BEGIN:VEVENT") == 1
    assert body.count("END:VEVENT") == 1
    assert f"DTSTART:{_ics_utc(booking['start_at'])}\r\n" in body
    assert f"DTEND:{_ics_utc(booking['end_at'])}\r\n" in body
    assert f"UID:{booking['id']}\r\n" in body
    assert f"SUMMARY:{hoist['name']}\r\n" in body
    assert "America/Regina" in body
    assert "DTSTART;TZID=" not in body

    login_member(client, "casey@example.com")
    other = client.get(f"/member/bookings/{booking['id']}/ics")
    assert other.status_code == 404, other.text
    assert other.json()["error"]["code"] == "not_found"

    login_member(client, "ada@example.com")
    cancelled = client.post(f"/member/bookings/{booking['id']}/cancel")
    assert cancelled.status_code == 200, cancelled.text
    blocked = client.get(f"/member/bookings/{booking['id']}/ics")
    assert blocked.status_code == 409, blocked.text
    assert blocked.json()["error"]["code"] == "booking_cancelled"
