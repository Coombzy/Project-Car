"""Owner GET /members/{id}/tokens is capped (PC-new-4).

Same contract as the member's own /member/tokens (R60): `limit` defaults to
200 and must be 1..500 (422 outside), newest first.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from uuid import UUID

from fastapi.testclient import TestClient

from app.models import TokenTransaction, TokenTransactionKind
from tests.conftest import AUTH, create_member

TOTAL = 205
_BASE = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _seed(client: TestClient, member_id: str) -> None:
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        for index in range(TOTAL):
            session.add(
                TokenTransaction(
                    member_id=UUID(member_id),
                    kind=TokenTransactionKind.ADMIN_ADJUSTMENT,
                    amount=Decimal(index),
                    note=f"ledger-{index:03d}",
                    created_at=_BASE + timedelta(minutes=index),
                )
            )
        session.commit()
    finally:
        session.close()


def _notes(response) -> list[str]:
    assert response.status_code == 200, response.text
    return [row["note"] for row in response.json()]


def test_owner_member_tokens_list_caps_rows(client: TestClient) -> None:
    member = create_member(
        client, name="Ada Reyes", email="ledger-cap@example.com", tier_name="premium", allocate_tokens=False
    )
    _seed(client, member["id"])
    path = f"/members/{member['id']}/tokens"
    newest = [f"ledger-{i:03d}" for i in range(TOTAL - 1, -1, -1)]

    assert _notes(client.get(path, headers=AUTH)) == newest[:200]
    assert _notes(client.get(path, headers=AUTH, params={"limit": 2})) == newest[:2]
    assert _notes(client.get(path, headers=AUTH, params={"limit": 500})) == newest

    for limit in (0, 501):
        response = client.get(path, headers=AUTH, params={"limit": limit})
        assert response.status_code == 422, response.text
