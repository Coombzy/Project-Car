"""AUD-026: completing a claimed shop job does not credit the token ledger."""

from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy import func, select

from app.models import TokenTransaction
from tests.conftest import AUTH, create_member, login_member


def _tx_count(client: TestClient, member_id: str) -> int:
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        return int(
            session.scalar(
                select(func.count())
                .select_from(TokenTransaction)
                .where(TokenTransaction.member_id == UUID(member_id))
            )
            or 0
        )
    finally:
        session.close()


def test_completing_a_claimed_job_does_not_credit_the_ledger(client: TestClient) -> None:
    member = create_member(client, email="ada.bounty@example.com")
    member_id = member["id"]
    created = client.post(
        "/jobs",
        headers=AUTH,
        json={"title": "Sweep the bay", "token_bounty": "25"},
    )
    assert created.status_code == 201, created.text
    job_id = created.json()["id"]

    login_member(client, "ada.bounty@example.com")
    claimed = client.post(f"/member/jobs/{job_id}/claim")
    assert claimed.status_code == 200, claimed.text

    before = client.get(f"/members/{member_id}", headers=AUTH)
    assert before.status_code == 200, before.text
    balance = before.json()["token_balance"]
    tx_before = _tx_count(client, member_id)

    done = client.post(f"/jobs/{job_id}/done", headers=AUTH)
    assert done.status_code == 200, done.text
    assert done.json()["status"] == "done"

    after = client.get(f"/members/{member_id}", headers=AUTH)
    assert after.status_code == 200, after.text
    assert after.json()["token_balance"] == balance
    assert _tx_count(client, member_id) == tx_before

    again = client.post(f"/jobs/{job_id}/done", headers=AUTH)
    assert again.status_code == 409, again.text
    assert again.json()["error"]["code"] == "job_already_decided"
