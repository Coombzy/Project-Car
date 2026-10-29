"""GET /jobs and GET /member/jobs list stored shop jobs.

Owner sees every job, newest first, with status, bounty, claimer id, and
timestamps. A member sees open and sent_back jobs, plus jobs they claimed.
Another member's claimed or finished job is absent. `limit` defaults to 50
and maxes at 200 (201 is 422). Logged out is 401.

Red on main: GET /jobs is 405 (POST /jobs already exists) and GET /member/jobs is 404.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from uuid import UUID

from fastapi.testclient import TestClient

from app.models import ShopJob, ShopJobStatus
from tests.conftest import AUTH, create_member, login_member

SWEEP = "Sweep the shop floor"
EMPTY = "Empty the used-oil drum"
RESTOCK = "Restock shop towels"
_BASE = datetime(2026, 5, 1, tzinfo=timezone.utc)


def _titles(response) -> list[str]:
    assert response.status_code == 200, response.text
    return [row["title"] for row in response.json()]


def _bounty(row: dict) -> Decimal:
    return Decimal(str(row["token_bounty"]))


def _stamp(client: TestClient, job_id: str, created_at: datetime) -> None:
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        row = session.get(ShopJob, UUID(job_id))
        assert row is not None
        row.created_at = created_at
        row.updated_at = created_at
        session.commit()
    finally:
        session.close()


def _post_job(client: TestClient, title: str, bounty: str) -> dict:
    response = client.post(
        "/jobs",
        headers=AUTH,
        json={"title": title, "token_bounty": bounty},
    )
    assert response.status_code == 201, response.text
    return response.json()


def _seed_three(client: TestClient) -> tuple[dict, dict, dict]:
    """Three posted jobs: open, claimed by Casey, claimed by Ada. Newest is Ada's."""
    ada = create_member(client, name="Ada Reyes", email="ada.jobs@example.com")
    casey = create_member(client, name="Casey Ng", email="casey.jobs@example.com")
    sweep = _post_job(client, SWEEP, "25")
    empty = _post_job(client, EMPTY, "40")
    restock = _post_job(client, RESTOCK, "15")
    login_member(client, "ada.jobs@example.com")
    claimed = client.post(f"/member/jobs/{restock['id']}/claim")
    assert claimed.status_code == 200, claimed.text
    login_member(client, "casey.jobs@example.com")
    other = client.post(f"/member/jobs/{empty['id']}/claim")
    assert other.status_code == 200, other.text
    _stamp(client, sweep["id"], _BASE)
    _stamp(client, empty["id"], _BASE + timedelta(hours=1))
    _stamp(client, restock["id"], _BASE + timedelta(hours=2))
    return ada, casey, restock


def test_owner_sees_three_seeded_jobs_newest_first(client: TestClient) -> None:
    ada, casey, _restock = _seed_three(client)

    listed = client.get("/jobs", headers=AUTH)
    assert listed.status_code == 200, listed.text
    body = listed.json()
    assert [row["title"] for row in body] == [RESTOCK, EMPTY, SWEEP]
    assert [row["status"] for row in body] == ["claimed", "claimed", "open"]
    assert body[0]["claimed_by_member_id"] == ada["id"]
    assert body[1]["claimed_by_member_id"] == casey["id"]
    assert body[2]["claimed_by_member_id"] is None
    assert _bounty(body[0]) == Decimal("15")
    assert _bounty(body[1]) == Decimal("40")
    assert _bounty(body[2]) == Decimal("25")
    created = [row["created_at"] for row in body]
    updated = [row["updated_at"] for row in body]
    assert created == sorted(created, reverse=True)
    assert len(set(created)) == 3
    assert all(updated)

    middle = client.get("/jobs", headers=AUTH, params={"limit": 1, "offset": 1})
    assert _titles(middle) == [EMPTY]
    assert middle.json()[0]["claimed_by_member_id"] == casey["id"]

    capped = client.get("/jobs", headers=AUTH, params={"limit": 200})
    assert _titles(capped) == [RESTOCK, EMPTY, SWEEP]


def test_member_sees_open_and_own_claim_not_another_members(client: TestClient) -> None:
    ada, casey, restock = _seed_three(client)

    login_member(client, "ada.jobs@example.com")
    listed = client.get("/member/jobs")
    assert listed.status_code == 200, listed.text
    body = listed.json()
    assert [row["title"] for row in body] == [RESTOCK, SWEEP]
    assert [row["status"] for row in body] == ["claimed", "open"]
    assert body[0]["claimed_by_member_id"] == ada["id"]
    assert _bounty(body[0]) == Decimal("15")
    assert body[0]["created_at"]
    assert body[0]["updated_at"]
    assert body[1]["claimed_by_member_id"] is None
    assert _bounty(body[1]) == Decimal("25")
    assert EMPTY not in listed.text
    assert casey["id"] not in listed.text

    page = client.get("/member/jobs", params={"offset": 1})
    assert _titles(page) == [SWEEP]

    done = client.post(f"/jobs/{restock['id']}/done", headers=AUTH)
    assert done.status_code == 200, done.text
    after = client.get("/member/jobs")
    finished = next(row for row in after.json() if row["id"] == restock["id"])
    assert finished["status"] == "done"
    assert finished["claimed_by_member_id"] == ada["id"]
    assert finished["title"] == RESTOCK

    login_member(client, "casey.jobs@example.com")
    other = client.get("/member/jobs")
    assert _titles(other) == [EMPTY, SWEEP]
    assert RESTOCK not in other.text
    assert ada["id"] not in other.text


TORQUE = "Torque the hoist bolts"
RESET = "Reset the hoist pins"
BLEED = "Bleed the lift brakes"
BAG = "Bag the shop rags"


def test_member_sees_sent_back_with_null_or_other_claimer(client: TestClient) -> None:
    """sent_back is claimable, so a member sees it when the claimer is null or someone else.

    Another member's claimed and done rows stay out: their titles are absent, and
    that member's id is not the claimer on any claimed or done row in the list.
    Red before the member filter includes sent_back: both sent_back titles are missing.
    """
    create_member(client, name="Ada Reyes", email="ada.sentback@example.com")
    casey = create_member(client, name="Casey Ng", email="casey.sentback@example.com")
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        seeded = (
            (TORQUE, ShopJobStatus.SENT_BACK, None, 4),
            (RESET, ShopJobStatus.SENT_BACK, UUID(casey["id"]), 3),
            (BLEED, ShopJobStatus.CLAIMED, UUID(casey["id"]), 2),
            (BAG, ShopJobStatus.DONE, UUID(casey["id"]), 1),
        )
        for title, status, claimer, hours in seeded:
            created = _BASE + timedelta(hours=hours)
            session.add(
                ShopJob(
                    title=title,
                    token_bounty=Decimal("10"),
                    status=status,
                    claimed_by_member_id=claimer,
                    created_at=created,
                    updated_at=created,
                )
            )
        session.commit()
    finally:
        session.close()

    login_member(client, "ada.sentback@example.com")
    listed = client.get("/member/jobs")
    assert listed.status_code == 200, listed.text
    body = listed.json()
    assert [row["title"] for row in body] == [TORQUE, RESET]
    by_title = {row["title"]: row for row in body}
    assert by_title[TORQUE]["status"] == "sent_back"
    assert by_title[TORQUE]["claimed_by_member_id"] is None
    assert _bounty(by_title[TORQUE]) == Decimal("10")
    assert by_title[RESET]["status"] == "sent_back"
    assert by_title[RESET]["claimed_by_member_id"] == casey["id"]
    assert BLEED not in listed.text
    assert BAG not in listed.text
    assert casey["id"] not in [
        row["claimed_by_member_id"]
        for row in body
        if row["status"] in ("claimed", "done")
    ]

    login_member(client, "casey.sentback@example.com")
    own = client.get("/member/jobs")
    assert _titles(own) == [TORQUE, RESET, BLEED, BAG]
    own_body = {row["title"]: row for row in own.json()}
    assert own_body[BLEED]["status"] == "claimed"
    assert own_body[BLEED]["claimed_by_member_id"] == casey["id"]
    assert own_body[BAG]["status"] == "done"
    assert own_body[BAG]["claimed_by_member_id"] == casey["id"]


def test_limit_201_is_422(client: TestClient) -> None:
    create_member(client, email="ada.limit@example.com")
    login_member(client, "ada.limit@example.com")

    owner = client.get("/jobs", headers=AUTH, params={"limit": 201})
    member = client.get("/member/jobs", params={"limit": 201})
    for response in (owner, member):
        assert response.status_code == 422, response.text
        assert response.json()["error"]["code"] == "validation_error"


def test_default_limit_is_50_newest(client: TestClient) -> None:
    create_member(client, email="ada.page@example.com")
    login_member(client, "ada.page@example.com")
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        for index in range(51):
            created = _BASE + timedelta(minutes=index)
            session.add(
                ShopJob(
                    title=f"job-{index:03d}",
                    token_bounty=Decimal("10"),
                    status=ShopJobStatus.OPEN,
                    created_at=created,
                    updated_at=created,
                )
            )
        session.commit()
    finally:
        session.close()

    newest_50 = [f"job-{index:03d}" for index in range(50, 0, -1)]
    all_51 = [f"job-{index:03d}" for index in range(50, -1, -1)]
    assert _titles(client.get("/jobs", headers=AUTH)) == newest_50
    assert _titles(client.get("/member/jobs")) == newest_50
    assert _titles(client.get("/jobs", headers=AUTH, params={"limit": 50})) == newest_50
    assert _titles(client.get("/jobs", headers=AUTH, params={"limit": 200})) == all_51
    assert _titles(client.get("/member/jobs", params={"offset": 50})) == ["job-000"]


def test_logged_out_job_lists_are_401(client: TestClient) -> None:
    owner = client.get("/jobs")
    member = client.get("/member/jobs")
    assert owner.status_code == 401, owner.text
    assert member.status_code == 401, member.text
    assert owner.json()["error"]["code"] == "unauthorized"
    assert member.json()["error"]["code"] == "unauthorized"
    assert owner.json()["error"]["message"] == "Owner authentication required."
    assert member.json()["error"]["message"] == "Member authentication required."
