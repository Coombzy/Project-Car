"""Every dollar amount is a row: before tax, GST, total, and a payment id.

Token purchases write that row, then credit tokens. A deposit taken and
returned writes no GST and no token line. A deposit kept writes GST.
Payment ids here are stand-ins until Ben supplies a processor.
"""

from decimal import Decimal

from fastapi.testclient import TestClient

from tests.conftest import AUTH, create_member


def _charges(client: TestClient, member_id: str) -> list[dict]:
    response = client.get(f"/members/{member_id}/dollar-charges", headers=AUTH)
    assert response.status_code == 200, response.text
    return response.json()


def _tokens(client: TestClient, member_id: str) -> Decimal:
    return Decimal(str(client.get(f"/members/{member_id}", headers=AUTH).json()["token_balance"]))


def _deposit(client: TestClient, member_id: str) -> Decimal:
    return Decimal(str(client.get(f"/members/{member_id}", headers=AUTH).json()["deposit_balance"]))


def test_purchase_writes_a_dollar_row_before_crediting_tokens(client: TestClient) -> None:
    member = create_member(client, email="gst-row@example.com", allocate_tokens=False)
    response = client.post(
        f"/members/{member['id']}/token-purchases",
        headers=AUTH,
        json={"payment_id": "STANDIN-PAYPAL-1230", "tokens": "100", "subtotal_cad": "12.30"},
    )
    assert response.status_code == 201, response.text
    assert _tokens(client, member["id"]) == Decimal("100")
    rows = _charges(client, member["id"])
    assert len(rows) == 1
    row = rows[0]
    assert row["purpose"] == "pack"
    assert row["payment_id"] == "STANDIN-PAYPAL-1230"
    assert Decimal(str(row["subtotal_cad"])) == Decimal("12.30")
    assert Decimal(str(row["gst_cad"])) == Decimal("0.62")
    assert Decimal(str(row["total_cad"])) == Decimal("12.92")
    assert Decimal(str(row["gst_rate"])) == Decimal("0.05")


def test_deposit_round_trip_moves_no_tokens_and_no_gst(client: TestClient) -> None:
    member = create_member(client, email="deposit@example.com", allocate_tokens=False)
    before = _tokens(client, member["id"])
    taken = client.post(
        f"/members/{member['id']}/deposits",
        headers=AUTH,
        json={"action": "take", "amount": "100.00", "payment_id": "STANDIN-DEP-TAKE"},
    )
    assert taken.status_code == 201, taken.text
    assert _deposit(client, member["id"]) == Decimal("100.00")
    assert _tokens(client, member["id"]) == before

    returned = client.post(
        f"/members/{member['id']}/deposits",
        headers=AUTH,
        json={"action": "return", "amount": "100.00", "payment_id": "STANDIN-DEP-RETURN"},
    )
    assert returned.status_code == 201, returned.text
    assert _deposit(client, member["id"]) == Decimal("0.00")
    assert _tokens(client, member["id"]) == before
    rows = {row["purpose"]: row for row in _charges(client, member["id"])}
    assert Decimal(str(rows["deposit_taken"]["gst_cad"])) == Decimal("0.00")
    assert Decimal(str(rows["deposit_returned"]["gst_cad"])) == Decimal("0.00")
    assert _tokens(client, member["id"]) == before


def test_kept_deposit_writes_five_percent_gst(client: TestClient) -> None:
    member = create_member(client, email="kept@example.com", allocate_tokens=False)
    before = _tokens(client, member["id"])
    taken = client.post(
        f"/members/{member['id']}/deposits",
        headers=AUTH,
        json={"action": "take", "amount": "100.00", "payment_id": "STANDIN-DEP-HOLD"},
    )
    assert taken.status_code == 201, taken.text
    kept = client.post(
        f"/members/{member['id']}/deposits",
        headers=AUTH,
        json={"action": "keep", "amount": "100.00", "payment_id": "STANDIN-DEP-KEEP"},
    )
    assert kept.status_code == 201, kept.text
    assert _deposit(client, member["id"]) == Decimal("0.00")
    assert _tokens(client, member["id"]) == before
    row = next(item for item in _charges(client, member["id"]) if item["purpose"] == "deposit_kept")
    assert Decimal(str(row["subtotal_cad"])) == Decimal("100.00")
    assert Decimal(str(row["gst_cad"])) == Decimal("5.00")
    assert Decimal(str(row["total_cad"])) == Decimal("105.00")
