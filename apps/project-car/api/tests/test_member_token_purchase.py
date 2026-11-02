"""A member cannot credit a client-chosen token count through the stand-in.

The owner purchase route is the manual stand-in. The member route must not
raise purchased_balance from body.tokens, a blank payment id, or a tiny subtotal.
"""

from decimal import Decimal
from uuid import uuid4

from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.services.payments import StandInPaymentProcessor
from tests.conftest import AUTH, create_member, login_member


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


def test_member_cannot_credit_a_client_chosen_token_count(client: TestClient) -> None:
    member = create_member(client, email="chooser@example.com", tier_name="basic")
    login_member(client, member["email"])
    before = client.get("/member/me").json()

    bought = client.post(
        "/member/token-purchases",
        json={"tokens": "999999.99", "subtotal_cad": "0.01"},
    )
    assert bought.status_code == 403, bought.text
    assert bought.json()["error"]["code"] == "owner_records_purchases"
    me = client.get("/member/me").json()
    assert Decimal(me["purchased_balance"]) == Decimal(str(before["purchased_balance"]))
    assert Decimal(me["token_balance"]) == Decimal(str(before["token_balance"]))
    ledger = client.get("/member/tokens").json()
    assert [row for row in ledger if row["kind"] == "token_purchase"] == []

    owner = client.get(f"/members/{member['id']}/tokens", headers=AUTH)
    assert owner.status_code == 200, owner.text
    assert [row for row in owner.json() if row["kind"] == "token_purchase"] == []


def test_stand_in_does_not_mint_a_receipt_for_a_client_token_count() -> None:
    processor = StandInPaymentProcessor()
    try:
        processor.collect(
            member_id=uuid4(),
            tokens=Decimal("999999.99"),
            subtotal_cad=Decimal("0.01"),
            payment_id=None,
        )
    except HTTPException as exc:
        assert exc.status_code == 403
        assert exc.detail["code"] == "owner_records_purchases"
        return
    raise AssertionError("stand-in collect minted a receipt for a client token count")
