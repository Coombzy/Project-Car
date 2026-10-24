"""Owner token adjustments must match the ledger's 2-decimal scale and the stand-in cap.

More than 2 decimal places, or an absolute value of 1,000,000 tokens or more, is
400 invalid_tokens and inserts no ledger row. Cents and whole tokens still post.
An AI is refused before the amount is checked.
"""

from __future__ import annotations

from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from tests.conftest import AUTH, create_member

AI = {"Authorization": "Bearer dev-ai-secret"}

# The row's proof amounts. Over-scale and at-cap must not land; cents and wholes must.
REFUSED = ("0.0001", "1.005", "1000000", "-1000000")
ACCEPTED = ("-1.50", "100")


def _ledger(client: TestClient, member_id: str) -> list[dict]:
    response = client.get(f"/members/{member_id}/tokens", headers=AUTH)
    assert response.status_code == 200, response.text
    return response.json()


def _balance(client: TestClient, member_id: str) -> Decimal:
    response = client.get(f"/members/{member_id}", headers=AUTH)
    assert response.status_code == 200, response.text
    return Decimal(str(response.json()["token_balance"]))


@pytest.mark.parametrize("amount", REFUSED)
def test_over_scale_or_capped_adjustment_is_400_and_writes_no_row(
    client: TestClient, amount: str
) -> None:
    member = create_member(client, email="adjust-refused@example.com")
    member_id = member["id"]
    before_ids = sorted(row["id"] for row in _ledger(client, member_id))
    before_balance = _balance(client, member_id)

    response = client.post(
        f"/members/{member_id}/tokens",
        headers=AUTH,
        json={"amount": amount},
    )
    assert response.status_code == 400, (
        f"{amount} -> {response.status_code} "
        f"kind={response.json().get('kind')} amount={response.json().get('amount')}"
    )
    assert response.json()["error"]["code"] == "invalid_tokens", response.text
    assert sorted(row["id"] for row in _ledger(client, member_id)) == before_ids
    assert _balance(client, member_id) == before_balance


def test_cent_and_whole_adjustments_are_201(client: TestClient) -> None:
    member = create_member(client, email="adjust-ok@example.com")
    member_id = member["id"]
    before_ids = {row["id"] for row in _ledger(client, member_id)}
    balance = _balance(client, member_id)

    for amount in ACCEPTED:
        response = client.post(
            f"/members/{member_id}/tokens",
            headers=AUTH,
            json={"amount": amount},
        )
        assert response.status_code == 201, response.text
        body = response.json()
        assert body["kind"] == "admin_adjustment"
        assert Decimal(str(body["amount"])) == Decimal(amount)
        balance += Decimal(amount)
        assert _balance(client, member_id) == balance

    after = _ledger(client, member_id)
    added = [row for row in after if row["id"] not in before_ids]
    assert len(added) == len(ACCEPTED)
    assert {row["kind"] for row in added} == {"admin_adjustment"}
    assert {Decimal(str(row["amount"])) for row in added} == {Decimal(amount) for amount in ACCEPTED}
    assert before_ids <= {row["id"] for row in after}


def test_ai_refusal_precedes_invalid_token_amount(client: TestClient) -> None:
    """token_change_requires_human still wins over invalid_tokens."""
    member = create_member(client, email="adjust-ai@example.com")
    member_id = member["id"]
    before_ids = sorted(row["id"] for row in _ledger(client, member_id))
    before_balance = _balance(client, member_id)

    response = client.post(
        f"/members/{member_id}/tokens",
        headers=AI,
        json={"amount": "0.0001"},
    )
    assert response.status_code == 403, response.text
    assert response.json()["error"]["code"] == "token_change_requires_human"
    assert sorted(row["id"] for row in _ledger(client, member_id)) == before_ids
    assert _balance(client, member_id) == before_balance
