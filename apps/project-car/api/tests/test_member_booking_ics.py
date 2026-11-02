"""GET /member/bookings/{id}/ics for the member's own visit."""

from __future__ import annotations

from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from app.shop_time import as_utc
from tests.conftest import create_hoist, create_member, login_member, next_hour


def _window(hours_from_now: int, length_hours: float = 2) -> tuple[str, str]:
    start = next_hour(hours_from_now)
    end = start + timedelta(hours=length_hours)
    return start.isoformat(), end.isoformat()


def _ics_utc(value: str) -> str:
    return as_utc(datetime.fromisoformat(value)).strftime("%Y%m%dT%H%M%SZ")


def _ics_escape(value: str) -> str:
    """Same escapes as member._ics_escape, written out so the test does not call it."""
    normalized = value.replace("\r\n", "\n").replace("\r", "\n")
    return (
        normalized.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def _physical_lines(body: str) -> list[bytes]:
    raw = body.encode("utf-8")
    assert raw.decode("utf-8") == body
    assert raw.endswith(b"\r\n")
    lines = raw.split(b"\r\n")[:-1]
    assert lines
    assert all(b"\r" not in line for line in lines)
    return lines


def _unfolded_value(body: str, name: str) -> str:
    """RFC 5545 unfold: drop CRLF + one WSP. Value is the text after NAME:."""
    start = body.index(f"{name}:")
    i = start
    while i < len(body):
        if body.startswith("\r\n", i):
            nxt = i + 2
            if nxt < len(body) and body[nxt] in " \t":
                i = nxt + 1
                continue
            chunk = body[start:i]
            break
        i += 1
    else:
        raise AssertionError(f"{name} property did not end with CRLF")
    unfolded = chunk.replace("\r\n ", "").replace("\r\n\t", "")
    marker = f"{name}:"
    assert unfolded.startswith(marker)
    return unfolded[len(marker):]


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
    assert "Mountain Time" in body
    assert "America/Regina" not in body
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

    login_member(client, "casey@example.com")
    other_cancelled = client.get(f"/member/bookings/{booking['id']}/ics")
    assert other_cancelled.status_code == 404, other_cancelled.text
    assert other_cancelled.json()["error"]["code"] == "not_found"


@pytest.mark.parametrize(
    "name",
    [
        pytest.param("A" * 120, id="ascii-120"),
        pytest.param("," * 40, id="forty-commas"),
        pytest.param("é" * 40, id="forty-eacute"),
    ],
)
def test_member_booking_ics_folds_summary_to_75_octets(
    client: TestClient, name: str
) -> None:
    """A legal hoist name must not emit a SUMMARY line longer than 75 octets.

    Hoist.name is String(120). SUMMARY: is 8 octets, so 68 ASCII characters
    are already 76. Escaping a comma to backslash-comma grows the line further.
    """
    escaped = _ics_escape(name)
    assert len(f"SUMMARY:{escaped}".encode("utf-8")) > 75

    create_member(client, email="ada@example.com", tier_name="premium")
    hoist = create_hoist(client, name=name)
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
    body = ics.text
    for line in _physical_lines(body):
        assert len(line) <= 75, len(line)
        assert line.decode("utf-8").encode("utf-8") == line
    assert _unfolded_value(body, "SUMMARY") == escaped
    assert body.count("BEGIN:VEVENT") == 1
    assert "DTSTART;TZID=" not in body
