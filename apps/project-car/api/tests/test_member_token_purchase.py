"""A member buys tokens through the payment adapter. The stand-in is the v1 processor."""

from decimal import Decimal

from fastapi.testclient import TestClient

from tests.conftest import create_member, login_member


def test_member_purchase_records_gst_through_the_stand_in(client: TestClient) -> None:
    member = create_member(client, email="buyer@example.com", tier_name="basic")
    login_member(client, member["email"])
    bought = client.post(
        "/member/token-purchases",
        json={"payment_id": "STANDIN-PAYPAL-BUY", "tokens": "200.00", "subtotal_cad": "40.00"},
    )
    assert bought.status_code == 201, bought.text
    purchase = bought.json()["meta"]["purchase"]
    assert purchase["processor"] == "stand-in"
    assert purchase["payment_id"] == "STANDIN-PAYPAL-BUY"
    assert Decimal(purchase["gst_cad"]) == Decimal("2.00")
    assert Decimal(purchase["total_cad"]) == Decimal("42.00")
    me = client.get("/member/me")
    assert Decimal(me.json()["purchased_balance"]) == Decimal("200.00")

    refused = client.post(
        "/member/token-purchases",
        json={"payment_id": "PAYPAL-LIVE-1", "tokens": "10.00", "subtotal_cad": "5.00"},
    )
    assert refused.status_code == 422, refused.text
    assert refused.json()["error"]["code"] == "standin_only"

    again = client.post(
        "/member/token-purchases",
        json={"payment_id": "STANDIN-PAYPAL-BUY", "tokens": "200.00", "subtotal_cad": "40.00"},
    )
    assert again.status_code == 409, again.text
