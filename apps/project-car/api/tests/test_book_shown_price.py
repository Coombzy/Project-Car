"""A published deal discounts only the hours inside the deal window.

Book must send the total it showed. A different total is refused and writes
nothing. A day with no published deal charges the plain band price.
"""

from datetime import datetime, timedelta
from decimal import Decimal

from fastapi.testclient import TestClient

from app.shop_time import PRICING_TZ
from tests.conftest import AUTH, create_hoist, create_member, freeze_shop_clock

# Wednesday 10:00, so tomorrow is Thursday 5 Nov 2026.
WEDNESDAY = datetime(2026, 11, 4, 10, 0, tzinfo=PRICING_TZ)


def _thursday_evening() -> tuple[datetime, datetime]:
    start = datetime(2026, 11, 5, 19, 0, tzinfo=PRICING_TZ)
    return start, start + timedelta(hours=4)


def _publish(client: TestClient) -> None:
    notified = client.post(
        "/fill/notify",
        headers=AUTH,
        json={"dry_run": False, "discount_pct": "25", "channels": ["email"]},
    )
    assert notified.status_code == 200, notified.text
    assert notified.json()["published"] is True


def test_published_deal_discounts_only_hours_inside_the_window(client: TestClient) -> None:
    freeze_shop_clock(WEDNESDAY)
    member = create_member(client, email="ada@example.com", tier_name="premium")
    hoist = create_hoist(client, name="Bay 1")
    _publish(client)
    start, end = _thursday_evening()

    quoted = client.post(
        "/bookings/quote",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
        },
    )
    assert quoted.status_code == 200, quoted.text
    # 19:00 and 20:00 are evening 125 at 25% off. 21:00 and 22:00 stay off-peak 75.
    assert Decimal(str(quoted.json()["reserved_tokens"])) == Decimal("337.50")


def test_stale_total_is_refused_and_writes_nothing(client: TestClient) -> None:
    freeze_shop_clock(WEDNESDAY)
    member = create_member(client, email="ada@example.com", tier_name="premium")
    hoist = create_hoist(client, name="Bay 1")
    _publish(client)
    start, end = _thursday_evening()
    before = Decimal(str(client.get(f"/members/{member['id']}", headers=AUTH).json()["token_balance"]))

    stale = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
            "tokens": "300.00",
        },
    )
    assert stale.status_code == 409, stale.text
    assert stale.json()["error"]["code"] == "price_changed"
    assert Decimal(str(stale.json()["error"]["reserved_tokens"])) == Decimal("337.50")
    assert client.get("/bookings", headers=AUTH).json() == []
    balance = Decimal(str(client.get(f"/members/{member['id']}", headers=AUTH).json()["token_balance"]))
    assert balance == before


def test_no_published_deal_charges_the_plain_band_price(client: TestClient) -> None:
    freeze_shop_clock(WEDNESDAY)
    member = create_member(client, email="ada@example.com", tier_name="premium")
    create_hoist(client, name="Bay 1")
    start, end = _thursday_evening()
    quoted = client.post(
        "/bookings/quote",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
        },
    )
    assert quoted.status_code == 200, quoted.text
    assert quoted.json()["pricing_rule"]["fill_id"] == "none"
    assert Decimal(str(quoted.json()["reserved_tokens"])) == Decimal("400.00")
