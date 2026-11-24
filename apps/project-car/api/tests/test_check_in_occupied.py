"""Check-in is 409 hoist_occupied while another visit is active or overdue.

A (10:00-11:00) and B (11:00-12:00) on one bay, both confirmed. At 10:50 both
windows are open, so check-in must not put two members on the same hoist.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from tests.conftest import AUTH, create_hoist, create_member

DAY = "2026-11-24"
DETAIL = "Another visit is still on this bay. Complete it first."


def _clock(monkeypatch, hm: str) -> None:
    monkeypatch.setenv("SHOP_DEV_MODE", "1")
    monkeypatch.setenv("SHOP_NOW", f"{DAY}T{hm}:00")


def _stored(client: TestClient, booking_id: str) -> dict:
    rows = client.get("/bookings", headers=AUTH).json()
    return next(row for row in rows if row["id"] == booking_id)


def _hoist_status(client: TestClient, hoist_id: str) -> str:
    rows = client.get("/hoists", headers=AUTH).json()
    return next(row for row in rows if row["id"] == hoist_id)["status"]


def _confirmed(client: TestClient, *, member: dict, hoist_id: str, hour: int) -> str:
    created = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist_id,
            "start_at": f"{DAY}T{hour:02d}:00:00",
            "end_at": f"{DAY}T{hour + 1:02d}:00:00",
        },
    )
    assert created.status_code == 201, created.text
    booking_id = created.json()["id"]
    assert client.post(f"/bookings/{booking_id}/confirm", headers=AUTH).status_code == 200
    return booking_id


def _pair(client: TestClient, monkeypatch, bay: str) -> tuple[str, str, str]:
    """Two confirmed back-to-back visits, created while the clock is still 09:00."""
    _clock(monkeypatch, "09:00")
    slug = bay.lower().replace(" ", "")
    ada = create_member(client, name="Ada Reyes", email=f"ada.{slug}@example.com")
    casey = create_member(client, name="Casey", email=f"casey.{slug}@example.com")
    hoist = create_hoist(client, name=bay)
    first = _confirmed(client, member=ada, hoist_id=hoist["id"], hour=10)
    second = _confirmed(client, member=casey, hoist_id=hoist["id"], hour=11)
    return hoist["id"], first, second


def _check_in(client: TestClient, booking_id: str):
    return client.post(f"/bookings/{booking_id}/check-in", headers=AUTH)


def _refused(client: TestClient, booking_id: str, hoist_id: str) -> None:
    before = _hoist_status(client, hoist_id)
    blocked = _check_in(client, booking_id)
    assert blocked.status_code == 409, blocked.text
    assert blocked.json()["error"] == {"code": "hoist_occupied", "message": DETAIL}
    assert _stored(client, booking_id)["status"] == "confirmed"
    assert _hoist_status(client, hoist_id) == before


def test_active_visit_blocks_check_in_until_complete(client: TestClient, monkeypatch) -> None:
    hoist_id, first, second = _pair(client, monkeypatch, "Bay 1")
    _clock(monkeypatch, "10:50")
    checked = _check_in(client, first)
    assert checked.status_code == 200, checked.text
    assert checked.json()["status"] == "active"
    _refused(client, second, hoist_id)
    done = client.post(
        f"/bookings/{first}/complete",
        headers=AUTH,
        json={"unused_tokens": "0"},
    )
    assert done.status_code == 200, done.text
    assert done.json()["status"] == "completed"
    followed = _check_in(client, second)
    assert followed.status_code == 200, followed.text
    assert followed.json()["status"] == "active"
    assert _stored(client, second)["status"] == "active"


def test_overdue_visit_blocks_check_in(client: TestClient, monkeypatch) -> None:
    hoist_id, first, second = _pair(client, monkeypatch, "Bay 2")
    _clock(monkeypatch, "10:50")
    assert _check_in(client, first).status_code == 200
    _clock(monkeypatch, "11:05")
    overdue = client.post(f"/bookings/{first}/overdue", headers=AUTH)
    assert overdue.status_code == 200, overdue.text
    assert overdue.json()["status"] == "overdue"
    _refused(client, second, hoist_id)


def test_free_bay_still_checks_in(client: TestClient, monkeypatch) -> None:
    _clock(monkeypatch, "09:00")
    member = create_member(client, name="Riley", email="riley@example.com")
    hoist = create_hoist(client, name="Bay 3")
    booking_id = _confirmed(client, member=member, hoist_id=hoist["id"], hour=10)
    _clock(monkeypatch, "10:50")
    checked = _check_in(client, booking_id)
    assert checked.status_code == 200, checked.text
    assert checked.json()["status"] == "active"
    assert _hoist_status(client, hoist["id"]) == "occupied"


def test_second_check_in_of_the_same_booking_still_errors(
    client: TestClient, monkeypatch
) -> None:
    hoist_id, first, _second = _pair(client, monkeypatch, "Bay 4")
    _clock(monkeypatch, "10:50")
    assert _check_in(client, first).status_code == 200
    again = _check_in(client, first)
    assert again.status_code == 400, again.text
    assert again.json()["error"]["code"] == "invalid_transition"
    assert _stored(client, first)["status"] == "active"
    assert _hoist_status(client, hoist_id) == "occupied"
