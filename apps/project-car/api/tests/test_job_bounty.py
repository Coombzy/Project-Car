"""Cap a shop-job token bounty at 10 000 with at most two decimals."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.models import ShopJob
from tests.conftest import AUTH

MESSAGE = "A job bounty is 0 to 10,000 tokens, with at most two decimals."


def _create_job(client: TestClient, token_bounty: str):
    return client.post(
        "/jobs",
        headers=AUTH,
        json={"title": f"Bounty {token_bounty}", "token_bounty": token_bounty},
    )


def _job_count(session_factory) -> int:
    session = session_factory()
    try:
        return session.query(ShopJob).count()
    finally:
        session.close()


@pytest.mark.parametrize("bounty", ["0", "2.50", "10000"])
def test_valid_bounty_accepted(client: TestClient, bounty: str) -> None:
    resp = _create_job(client, bounty)
    assert resp.status_code == 201, resp.text
    assert resp.json()["token_bounty"] == bounty


@pytest.mark.parametrize(
    "bounty",
    ["10000.01", "99999999999", "1e30", "1.234", "1.0000000000000000000000000000001"],
)
def test_invalid_bounty_rejected_without_row(client: TestClient, bounty: str) -> None:
    before = _job_count(client.session_factory)
    resp = _create_job(client, bounty)
    assert resp.status_code == 422, resp.text
    error = resp.json()["error"]
    assert (error["code"], error["message"]) == ("invalid_bounty", MESSAGE)
    assert _job_count(client.session_factory) == before
