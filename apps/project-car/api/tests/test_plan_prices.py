"""Membership dollar prices are stored settings, with GST on top.

Basic is a stand-in of 500 CAD per month. Premium stays a marked stand-in
of 750 CAD per month until Ben confirms it. Signup reads the same rows
the owner edits.
"""

from decimal import Decimal

from fastapi.testclient import TestClient

from tests.conftest import AUTH

PREMIUM_MARK = "Stand-in until Ben confirms"


def _plan(client: TestClient, name: str) -> dict:
    listed = client.get("/plans")
    assert listed.status_code == 200, listed.text
    row = next((item for item in listed.json() if item["name"] == name), None)
    assert row is not None, name
    return row


def test_basic_stand_in_is_500_cad_per_month_plus_gst(client: TestClient) -> None:
    basic = _plan(client, "basic")
    assert Decimal(basic["price"]) == Decimal("500.00")
    assert basic["currency"] == "CAD"
    assert basic["billing_period"] == "month"
    assert Decimal(basic["gst_rate"]) == Decimal("0.05")
    assert Decimal(basic["gst_cad"]) == Decimal("25.00")
    assert Decimal(basic["total_cad"]) == Decimal("525.00")


def test_premium_is_a_marked_750_stand_in(client: TestClient) -> None:
    premium = _plan(client, "premium")
    assert Decimal(premium["price"]) == Decimal("750.00")
    assert Decimal(premium["gst_cad"]) == Decimal("37.50")
    assert Decimal(premium["total_cad"]) == Decimal("787.50")
    assert premium["price_mark"] == PREMIUM_MARK


def test_owner_edit_is_what_signup_and_the_plan_screen_read(client: TestClient) -> None:
    patched = client.patch("/tiers/basic", headers=AUTH, json={"price": "480.00"})
    assert patched.status_code == 200, patched.text
    assert Decimal(patched.json()["gst_cad"]) == Decimal("24.00")
    assert Decimal(patched.json()["total_cad"]) == Decimal("504.00")

    basic = _plan(client, "basic")
    assert Decimal(basic["price"]) == Decimal("480.00")
    assert Decimal(basic["gst_cad"]) == Decimal("24.00")

    owner = client.get("/tiers", headers=AUTH)
    assert owner.status_code == 200, owner.text
    plan = next(item for item in owner.json() if item["name"] == "basic")
    assert Decimal(plan["price"]) == Decimal("480.00")
    assert Decimal(plan["gst_cad"]) == Decimal("24.00")
    assert plan["price_mark"] is None
