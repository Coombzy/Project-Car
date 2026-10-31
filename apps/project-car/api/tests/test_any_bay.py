"""Any bay is the lowest-numbered free member bay for the whole visit.

Bay 6 is never chosen. The choice is saved with the hours. If the first bay
loses the hour, the next bay is tried. The response names the bay.
"""

from datetime import datetime, timedelta
from decimal import Decimal

from fastapi.testclient import TestClient

from app.shop_time import PRICING_TZ
from tests.conftest import AUTH, create_hoist, create_member, freeze_shop_clock, next_hour


def _book(client: TestClient, member_id: str, start, end, **extra) -> object:
    body = {
        "member_id": member_id,
        "start_at": start.isoformat(),
        "end_at": end.isoformat(),
        **extra,
    }
    return client.post("/bookings", headers=AUTH, json=body)


def test_any_bay_skips_a_bay_that_is_busy_for_part_of_the_visit(client: TestClient) -> None:
    member = create_member(client, email="any@example.com", tier_name="premium")
    bay1 = create_hoist(client, name="Bay 1")
    create_hoist(client, name="Bay 2")
    create_hoist(client, name="Bay 6", is_shop=True)
    start = next_hour(48)
    busy = _book(
        client,
        member["id"],
        start,
        start + timedelta(hours=1),
        hoist_id=bay1["id"],
    )
    assert busy.status_code == 201, busy.text

    chosen = _book(client, member["id"], start, start + timedelta(hours=2))
    assert chosen.status_code == 201, chosen.text
    assert chosen.json()["hoist_name"] == "Bay 2"
    assert chosen.json()["hoist_id"] != bay1["id"]


def test_two_any_bay_requests_take_different_bays(client: TestClient) -> None:
    patched = client.patch(
        "/tiers/premium",
        headers=AUTH,
        json={"max_simultaneous_bookings": 3},
    )
    assert patched.status_code == 200, patched.text
    member = create_member(client, email="race@example.com", tier_name="premium")
    create_hoist(client, name="Bay 1")
    create_hoist(client, name="Bay 2")
    start = next_hour(60)
    end = start + timedelta(hours=1)
    before = Decimal(str(client.get(f"/members/{member['id']}", headers=AUTH).json()["token_balance"]))

    first = _book(client, member["id"], start, end)
    second = _book(client, member["id"], start, end)
    assert first.status_code == 201, first.text
    assert second.status_code == 201, second.text
    assert first.json()["hoist_name"] == "Bay 1"
    assert second.json()["hoist_name"] == "Bay 2"

    refused = _book(client, member["id"], start, end)
    assert refused.status_code == 409, refused.text
    assert refused.json()["error"]["code"] == "no_bay"
    names = {row["hoist_name"] for row in client.get("/bookings", headers=AUTH).json()}
    assert names == {"Bay 1", "Bay 2"}
    balance = Decimal(str(client.get(f"/members/{member['id']}", headers=AUTH).json()["token_balance"]))
    spent = Decimal(str(first.json()["reserved_tokens"])) + Decimal(str(second.json()["reserved_tokens"]))
    assert balance == before - spent


def test_any_bay_uses_an_occupied_bay_when_the_hour_is_free(client: TestClient) -> None:
    freeze_shop_clock(datetime(2026, 11, 2, 9, 50, tzinfo=PRICING_TZ))
    here = create_member(client, email="here@example.com")
    later = create_member(client, email="later@example.com")
    bay1 = create_hoist(client, name="Bay 1")
    create_hoist(client, name="Bay 2")
    start = datetime(2026, 11, 2, 10, tzinfo=PRICING_TZ)
    current = _book(client, here["id"], start, start + timedelta(hours=1), hoist_id=bay1["id"])
    assert current.status_code == 201, current.text
    booking_id = current.json()["id"]
    assert client.post(f"/bookings/{booking_id}/confirm", headers=AUTH).status_code == 200
    checked = client.post(f"/bookings/{booking_id}/check-in", headers=AUTH)
    assert checked.status_code == 200, checked.text

    future = datetime(2026, 11, 2, 12, tzinfo=PRICING_TZ)
    chosen = _book(client, later["id"], future, future + timedelta(hours=1))
    assert chosen.status_code == 201, chosen.text
    assert chosen.json()["hoist_name"] == "Bay 1"


def test_any_bay_skips_a_maintenance_bay(client: TestClient) -> None:
    member = create_member(client, email="maint@example.com")
    create_hoist(client, name="Bay 1", status="maintenance")
    create_hoist(client, name="Bay 2")
    start = next_hour(48)
    chosen = _book(client, member["id"], start, start + timedelta(hours=1))
    assert chosen.status_code == 201, chosen.text
    assert chosen.json()["hoist_name"] == "Bay 2"
