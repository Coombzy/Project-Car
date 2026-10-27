"""PATCH /hoists/{id} will not free a bay under a visit, or drop the shop flag.

An Owner (or AI bearer) setting status available while a booking on that hoist
is active or overdue is 409 hoist_occupied. Clearing is_shop on the only shop
hoist is 409 last_shop_hoist. A second is_shop stays 409 duplicate_shop_hoist.
"""

from __future__ import annotations

from datetime import timedelta
from uuid import UUID

from fastapi.testclient import TestClient

from app.models import Booking
from app.shop_time import as_utc, shop_now
from tests.conftest import AUTH, create_hoist, create_member

_HOIST_FIELDS = ("id", "name", "location_label", "status", "is_shop", "created_at", "updated_at")


def _stored(client: TestClient, hoist_id: str) -> dict:
    listed = client.get("/hoists", headers=AUTH)
    assert listed.status_code == 200, listed.text
    return next(row for row in listed.json() if row["id"] == hoist_id)


def _window_inside_check_in() -> tuple[str, str]:
    start = shop_now() + timedelta(minutes=10)
    end = start + timedelta(hours=2)
    return start.isoformat(), end.isoformat()


def _checked_in(client: TestClient, *, hoist_name: str = "Bay 1") -> tuple[dict, dict]:
    member = create_member(client)
    hoist = create_hoist(client, name=hoist_name)
    start, end = _window_inside_check_in()
    created = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": start,
            "end_at": end,
        },
    )
    assert created.status_code == 201, created.text
    booking_id = created.json()["id"]
    assert client.post(f"/bookings/{booking_id}/confirm", headers=AUTH).status_code == 200
    checked = client.post(f"/bookings/{booking_id}/check-in", headers=AUTH)
    assert checked.status_code == 200, checked.text
    assert checked.json()["status"] == "active"
    stored = _stored(client, hoist["id"])
    assert stored["status"] == "occupied"
    return stored, created.json()


def _move_into_the_past(client: TestClient, booking_id: str) -> None:
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        row = session.get(Booking, UUID(booking_id))
        assert row is not None
        end = as_utc(shop_now() - timedelta(minutes=1))
        row.start_at = end - timedelta(hours=1)
        row.end_at = end
        session.commit()
    finally:
        session.close()


def test_patch_available_while_active_is_409_then_complete_is_200(client: TestClient) -> None:
    hoist, booking = _checked_in(client)
    before = _stored(client, hoist["id"])

    blocked = client.patch(
        f"/hoists/{hoist['id']}",
        headers=AUTH,
        json={"status": "available", "name": "Bay 9"},
    )

    assert blocked.status_code == 409, blocked.text
    assert blocked.json()["error"]["code"] == "hoist_occupied"
    assert _stored(client, hoist["id"]) == before
    assert before["status"] == "occupied"
    assert before["name"] == "Bay 1"

    completed = client.post(
        f"/bookings/{booking['id']}/complete",
        headers=AUTH,
        json={"unused_tokens": "0"},
    )
    assert completed.status_code == 200, completed.text
    assert completed.json()["status"] == "completed"

    freed = client.patch(
        f"/hoists/{hoist['id']}",
        headers=AUTH,
        json={"status": "available"},
    )
    assert freed.status_code == 200, freed.text
    body = freed.json()
    assert set(body) == set(_HOIST_FIELDS)
    assert body["status"] == "available"
    assert _stored(client, hoist["id"])["status"] == "available"


def test_patch_available_while_overdue_is_409(client: TestClient) -> None:
    hoist, booking = _checked_in(client, hoist_name="Bay 2")
    _move_into_the_past(client, booking["id"])
    overdue = client.post(f"/bookings/{booking['id']}/overdue", headers=AUTH)
    assert overdue.status_code == 200, overdue.text
    assert overdue.json()["status"] == "overdue"
    before = _stored(client, hoist["id"])
    assert before["status"] == "occupied"

    blocked = client.patch(
        f"/hoists/{hoist['id']}",
        headers=AUTH,
        json={"status": "available"},
    )

    assert blocked.status_code == 409, blocked.text
    assert blocked.json()["error"]["code"] == "hoist_occupied"
    assert _stored(client, hoist["id"]) == before


def test_clearing_the_only_shop_hoist_is_409_last_shop_hoist(client: TestClient) -> None:
    shop = create_hoist(client, name="Bay 6", location_label="Internal", is_shop=True)
    bay = create_hoist(client, name="Bay 1")
    before = _stored(client, shop["id"])
    assert before["is_shop"] is True

    blocked = client.patch(
        f"/hoists/{shop['id']}",
        headers=AUTH,
        json={"is_shop": False},
    )

    assert blocked.status_code == 409, blocked.text
    assert blocked.json()["error"]["code"] == "last_shop_hoist"
    assert _stored(client, shop["id"]) == before
    assert _stored(client, shop["id"])["is_shop"] is True
    assert _stored(client, bay["id"])["is_shop"] is False


def test_second_shop_hoist_is_still_409_duplicate_shop_hoist(client: TestClient) -> None:
    shop = create_hoist(client, name="Bay 6", is_shop=True)
    bay = create_hoist(client, name="Bay 1")
    before = _stored(client, bay["id"])

    blocked = client.patch(
        f"/hoists/{bay['id']}",
        headers=AUTH,
        json={"is_shop": True},
    )

    assert blocked.status_code == 409, blocked.text
    assert blocked.json()["error"]["code"] == "duplicate_shop_hoist"
    assert _stored(client, bay["id"]) == before
    assert _stored(client, shop["id"])["is_shop"] is True


def test_non_shop_hoist_can_still_be_edited(client: TestClient) -> None:
    hoist = create_hoist(client, name="Bay 1", location_label="North wall")

    patched = client.patch(
        f"/hoists/{hoist['id']}",
        headers=AUTH,
        json={"name": "Bay 3", "location_label": "East wall", "status": "maintenance"},
    )
    assert patched.status_code == 200, patched.text
    body = patched.json()
    assert set(body) == set(_HOIST_FIELDS)
    assert body["name"] == "Bay 3"
    assert body["location_label"] == "East wall"
    assert body["status"] == "maintenance"
    assert body["is_shop"] is False

    locked = client.patch(
        f"/hoists/{hoist['id']}",
        headers=AUTH,
        json={"status": "locked"},
    )
    assert locked.status_code == 200, locked.text
    assert locked.json()["status"] == "locked"
    assert _stored(client, hoist["id"])["status"] == "locked"

    available = client.patch(
        f"/hoists/{hoist['id']}",
        headers=AUTH,
        json={"status": "available"},
    )
    assert available.status_code == 200, available.text
    assert available.json()["status"] == "available"

    still_not_shop = client.patch(
        f"/hoists/{hoist['id']}",
        headers=AUTH,
        json={"is_shop": False},
    )
    assert still_not_shop.status_code == 200, still_not_shop.text
    assert still_not_shop.json()["is_shop"] is False
    assert _stored(client, hoist["id"])["is_shop"] is False
