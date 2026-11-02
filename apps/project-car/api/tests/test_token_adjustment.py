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
        json={"amount": amount, "reason": "Owner correction"},
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
            json={"amount": amount, "reason": "Owner correction"},
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
        json={"amount": "0.0001", "reason": "Owner correction"},
    )
    assert response.status_code == 403, response.text
    assert response.json()["error"]["code"] == "token_change_requires_human"
    assert sorted(row["id"] for row in _ledger(client, member_id)) == before_ids
    assert _balance(client, member_id) == before_balance


def _record_scalars(monkeypatch, reads: list[tuple[str, bool]]) -> None:
    """Compile each ORM read on the postgresql dialect.

    SQLite drops FOR UPDATE at execution. The statement still carries the
    lock, which is what Postgres will take. Same spy as test_allocation.py.
    """
    from sqlalchemy.dialects import postgresql
    from sqlalchemy.orm import Session

    original = Session.scalars

    def spy(self, statement, *args, **kwargs):
        sql = str(statement.compile(dialect=postgresql.dialect()))
        locked = getattr(statement, "_for_update_arg", None) is not None
        reads.append((sql, locked))
        return original(self, statement, *args, **kwargs)

    monkeypatch.setattr(Session, "scalars", spy)


def _member_for_update_sql(reads: list[tuple[str, bool]]) -> list[str]:
    return [
        sql
        for sql, locked in reads
        if locked and "FOR UPDATE" in sql and "FROM members" in sql and "WHERE members.id" in sql
    ]


def test_adjust_member_tokens_locks_the_member_for_update(client: TestClient, monkeypatch) -> None:
    """The adjust route selects that member FOR UPDATE before it reads the cache.

    Red on main: adjust_member_tokens loads through session.get, so this select
    has no FOR UPDATE. Two overlapping adjustments can both add to the old
    token_balance and the second write drops the first from the cache.
    """
    member = create_member(client, email="adjust-lock@example.com")
    reads: list[tuple[str, bool]] = []
    _record_scalars(monkeypatch, reads)

    response = client.post(
        f"/members/{member['id']}/tokens",
        headers=AUTH,
        json={"amount": "10.00", "note": "lock check", "reason": "lock check"},
    )
    assert response.status_code == 201, response.text
    assert response.json()["kind"] == "admin_adjustment"
    locked = _member_for_update_sql(reads)
    assert locked, "adjust_member_tokens member select has no FOR UPDATE on the postgresql dialect"


def test_two_adjustments_in_a_row_match_the_ledger_sum(client: TestClient) -> None:
    """Two sequential adjustments both land, and the cache equals the ledger sum."""
    member = create_member(client, email="adjust-sum@example.com")
    member_id = member["id"]
    opening = _balance(client, member_id)
    posted = (Decimal("40.25"), Decimal("-15.00"))

    for amount in posted:
        response = client.post(
            f"/members/{member_id}/tokens",
            headers=AUTH,
            json={"amount": format(amount, "f"), "note": "sequential", "reason": "sequential"},
        )
        assert response.status_code == 201, response.text
        assert response.json()["kind"] == "admin_adjustment"
        assert Decimal(str(response.json()["amount"])) == amount

    rows = _ledger(client, member_id)
    ledger_sum = sum((Decimal(str(row["amount"])) for row in rows), Decimal("0"))
    adjustments = [
        Decimal(str(row["amount"])) for row in rows if row["kind"] == "admin_adjustment"
    ]
    assert sorted(adjustments) == sorted(posted)
    assert _balance(client, member_id) == opening + sum(posted, Decimal("0"))
    assert _balance(client, member_id) == ledger_sum


def test_unknown_member_adjustment_is_still_404(client: TestClient) -> None:
    """A missing member is 404 not_found. The lock does not change that answer."""
    missing = "00000000-0000-4000-8000-000000000065"
    response = client.post(
        f"/members/{missing}/tokens",
        headers=AUTH,
        json={"amount": "1.00", "note": "missing", "reason": "missing"},
    )
    assert response.status_code == 404, response.text
    body = response.json()
    assert body["error"]["code"] == "not_found"
    assert body["error"]["message"] == "Member not found."
