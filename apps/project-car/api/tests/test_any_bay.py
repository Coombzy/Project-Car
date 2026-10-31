"""Any bay is the lowest-numbered free member bay for the whole visit.

Bay 6 is never chosen. The choice is saved with the hours. If the first bay
loses the hour, the next bay is tried. The response names the bay.
"""

from datetime import timedelta
from decimal import Decimal

from fastapi.testclient import TestClient

from tests.conftest import AUTH, create_hoist, create_member, next_hour


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
