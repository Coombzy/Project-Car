"""Dashboard waitlist_count drops people who already became members."""

from __future__ import annotations

from fastapi.testclient import TestClient

from tests.conftest import AUTH

# Other waitlist tests already spend the eight creates on TestClient's default
# host. This proof uses its own address so it does not take those slots.
_WAITLIST_CLIENT = ("203.0.113.54", 50000)


def _create_waitlist(client: TestClient, name: str, email: str) -> dict:
    transport = client._transport
    previous = transport.client
    transport.client = _WAITLIST_CLIENT
    try:
        created = client.post("/waitlist", json={"name": name, "email": email})
    finally:
        transport.client = previous
    assert created.status_code == 201, created.text
    return created.json()


def test_dashboard_waitlist_count_skips_converted_entries(client: TestClient) -> None:
    """3 entries, 1 converted: count 2. A contacted unconverted entry still counts. None left: 0."""
    priya = _create_waitlist(client, "Priya Shah", "priya.r54@example.com")
    luis = _create_waitlist(client, "Luis Ortega", "luis.r54@example.com")
    harper = _create_waitlist(client, "Harper Quinn", "harper.r54@example.com")

    waiting = client.get("/dashboard", headers=AUTH)
    assert waiting.status_code == 200, waiting.text
    body = waiting.json()
    assert isinstance(body["waitlist_count"], int)
    assert "today_bookings" in body
    assert "token_at_risk" in body
    assert "todos" in body
    assert "parts_orders" in body
    assert "hoists" in body
    assert body["tz"] == "America/Regina"
    assert body["waitlist_count"] == 3

    converted = client.post(
        f"/waitlist/{priya['id']}/convert",
        headers=AUTH,
        json={"tier_name": "basic"},
    )
    assert converted.status_code == 200, converted.text
    assert converted.json()["member_id"]

    listed = client.get("/waitlist", headers=AUTH)
    assert listed.status_code == 200, listed.text
    rows = listed.json()
    assert len(rows) == 3
    assert sum(1 for row in rows if row["member_id"] is not None) == 1

    one_converted = client.get("/dashboard", headers=AUTH)
    assert one_converted.status_code == 200, one_converted.text
    # The converted row is still stored. It is not someone waiting.
    assert one_converted.json()["waitlist_count"] == 2
    assert set(one_converted.json()) == set(body)

    marked = client.post(f"/waitlist/{luis['id']}/contacted", headers=AUTH)
    assert marked.status_code == 200, marked.text
    assert marked.json()["contacted_at"] is not None
    assert marked.json()["member_id"] is None

    contacted = client.get("/dashboard", headers=AUTH)
    assert contacted.status_code == 200, contacted.text
    # Contacted, not converted: still waiting. Only member_id drops the count.
    assert contacted.json()["waitlist_count"] == 2

    for entry in (luis, harper):
        done = client.post(
            f"/waitlist/{entry['id']}/convert",
            headers=AUTH,
            json={"tier_name": "basic"},
        )
        assert done.status_code == 200, done.text
        assert done.json()["member_id"]

    still_listed = client.get("/waitlist", headers=AUTH)
    assert still_listed.status_code == 200, still_listed.text
    assert len(still_listed.json()) == 3
    assert all(row["member_id"] is not None for row in still_listed.json())

    none_left = client.get("/dashboard", headers=AUTH)
    assert none_left.status_code == 200, none_left.text
    assert none_left.json()["waitlist_count"] == 0
    assert set(none_left.json()) == set(body)
