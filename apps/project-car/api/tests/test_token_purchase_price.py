"""AUD-001: a member cannot name the token price.

The server prices the purchase. The repro is 999,999 tokens for 0.01 CAD.
Outside dev mode the route is not configured.
"""

from __future__ import annotations

from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy import func, select

from app.config import get_settings
from app.models import BillingTransaction, TokenTransaction, TokenTransactionKind
from tests.conftest import create_member, login_member

REPRO = {"tokens": "999999", "amount_cad": "0.01", "payment_id": "STANDIN-REPRO"}


def _buyer(client: TestClient, email: str) -> dict:
    member = create_member(client, email=email, tier_name="basic")
    login_member(client, member["email"])
    return member


def _purchase_counts(client: TestClient, member_id: str) -> tuple[int, int]:
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        mid = UUID(member_id)
        billing = session.scalar(
            select(func.count())
            .select_from(BillingTransaction)
            .where(BillingTransaction.member_id == mid)
        )
        ledger = session.scalar(
            select(func.count())
            .select_from(TokenTransaction)
            .where(
                TokenTransaction.member_id == mid,
                TokenTransaction.kind == TokenTransactionKind.TOKEN_PURCHASE,
            )
        )
    finally:
        session.close()
    return int(billing or 0), int(ledger or 0)


def test_client_chosen_amount_is_rejected(client: TestClient) -> None:
    """999,999 tokens for $0.01 is accepted today. The client amount is not the price."""
    member = _buyer(client, "price-client@example.com")
    bought = client.post("/member/token-purchases", json=REPRO)
    assert bought.status_code == 422, bought.text
    assert bought.json()["error"]["code"] == "amount_mismatch"
    assert _purchase_counts(client, member["id"]) == (0, 0)


def test_purchase_not_configured_outside_dev_mode(client: TestClient, monkeypatch) -> None:
    member = _buyer(client, "price-prod@example.com")
    monkeypatch.delenv("SHOP_DEV_MODE", raising=False)
    get_settings.cache_clear()
    try:
        bought = client.post("/member/token-purchases", json=REPRO)
        assert bought.status_code == 503, bought.text
        assert bought.json()["error"]["code"] == "purchase_not_configured"
        assert _purchase_counts(client, member["id"]) == (0, 0)
    finally:
        get_settings.cache_clear()
