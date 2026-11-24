"""POST /incidents links a booking to the member it belongs to."""

from __future__ import annotations

from datetime import timedelta

from fastapi.testclient import TestClient

from app.shop_time import shop_now
from tests.conftest import AUTH, create_hoist, create_member


def _booking(client: TestClient, member_id: str) -> str:
    start = shop_now() + timedelta(hours=4)
    body = {
        "member_id": member_id,
        "hoist_id": create_hoist(client)["id"],
        "start_at": start.isoformat(),
        "end_at": (start + timedelta(hours=2)).isoformat(),
        "notes": "Door work",
    }
    response = client.post("/bookings", headers=AUTH, json=body)
    assert response.status_code == 201, response.text
    return response.json()["id"]


def _incident(client: TestClient, member: str, booking: str, note: str):
    body = {"kind": "damage", "member_id": member, "booking_id": booking, "note": note}
    return client.post("/incidents", headers=AUTH, json=body)


def test_booking_of_another_member_is_rejected(client: TestClient) -> None:
    owner = create_member(client, email="owner-a@example.com")
    stranger = create_member(client, email="stranger-a@example.com")
    booking_id = _booking(client, owner["id"])
    mismatch = _incident(client, stranger["id"], booking_id, "Wrong member")
    assert mismatch.status_code == 422, mismatch.text
    assert mismatch.json()["error"]["code"] == "booking_member_mismatch"
    assert client.get("/incidents", headers=AUTH).json() == []


def test_booking_of_the_named_member_is_accepted(client: TestClient) -> None:
    member = create_member(client, email="member-b@example.com")
    booking_id = _booking(client, member["id"])
    accepted = _incident(client, member["id"], booking_id, "Scratched the door")
    assert accepted.status_code == 201, accepted.text
    assert accepted.json()["booking_id"] == booking_id
    assert client.get("/incidents", headers=AUTH).json()[0]["note"] == "Scratched the door"
