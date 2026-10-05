"""A job claim stores a row and marking it done stores another row."""

from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import ChatMessage, JobEvent, JobEventKind, TokenTransaction
from tests.conftest import AUTH, create_member, login_member


def _session(client: TestClient) -> Session:
    factory = client.session_factory  # type: ignore[attr-defined]
    return factory()


def _stored(client: TestClient) -> list[JobEvent]:
    session = _session(client)
    try:
        return list(session.scalars(select(JobEvent).order_by(JobEvent.created_at, JobEvent.job_key)).all())
    finally:
        session.close()


def _count(client: TestClient, model, kind: JobEventKind | None = None) -> int:
    session = _session(client)
    try:
        stmt = select(func.count()).select_from(model)
        if kind is not None:
            stmt = stmt.where(JobEvent.kind == kind)
        return int(session.scalar(stmt) or 0)
    finally:
        session.close()


def test_claim_and_done_each_store_a_row(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com", name="Ada Reyes")
    create_member(client, email="casey@example.com", name="Casey", tier_name="basic")
    tokens_before = _count(client, TokenTransaction)
    assert _count(client, JobEvent) == 0
    assert _count(client, ChatMessage) == 0

    denied = client.post(
        "/member/jobs/claims",
        json={"job_key": "job-sweep-floor", "note": "After close"},
    )
    assert denied.status_code == 401
    assert _count(client, JobEvent) == 0

    login_member(client, "ada@example.com")
    created = client.post(
        "/member/jobs/claims",
        json={"job_key": "  Job-Sweep-Floor  ", "note": "  After the last booking  "},
    )
    assert created.status_code == 201, created.text
    claim = created.json()
    assert claim["job_key"] == "job-sweep-floor"
    assert claim["title"] == "Sweep the shop floor"
    assert claim["kind"] == "claim"
    assert claim["note"] == "After the last booking"
    assert claim["member_id"] == ada["id"]
    assert claim["member_name"] == "Ada Reyes"
    assert claim["claim_id"] is None

    stored = _stored(client)
    assert len(stored) == 1
    claim_row = stored[0]
    assert str(claim_row.id) == claim["id"]
    assert str(claim_row.member_id) == ada["id"]
    assert claim_row.job_key == "job-sweep-floor"
    assert claim_row.title == "Sweep the shop floor"
    assert claim_row.kind == JobEventKind.CLAIM
    assert claim_row.note == "After the last booking"
    assert claim_row.claim_id is None
    assert claim_row.created_at is not None
    assert _count(client, JobEvent, JobEventKind.CLAIM) == 1
    assert _count(client, JobEvent, JobEventKind.DONE) == 0
    assert _count(client, TokenTransaction) == tokens_before
    assert _count(client, ChatMessage) == 0

    client.cookies.clear()
    empty_done = client.post("/member/jobs/done", json={"job_key": "job-sweep-floor"})
    assert empty_done.status_code == 401
    assert _count(client, JobEvent) == 1

    login_member(client, "ada@example.com")
    finished = client.post(
        "/member/jobs/done",
        json={"job_key": "job-sweep-floor", "note": "  Floor is clear  "},
    )
    assert finished.status_code == 201, finished.text
    body = finished.json()
    assert body["job_key"] == "job-sweep-floor"
    assert body["title"] == "Sweep the shop floor"
    assert body["kind"] == "done"
    assert body["note"] == "Floor is clear"
    assert body["member_id"] == ada["id"]
    assert body["member_name"] == "Ada Reyes"
    assert body["claim_id"] == claim["id"]
    assert body["id"] != claim["id"]

    stored = _stored(client)
    assert len(stored) == 2
    kinds = {row.kind for row in stored}
    assert kinds == {JobEventKind.CLAIM, JobEventKind.DONE}
    still_claimed = next(row for row in stored if row.kind == JobEventKind.CLAIM)
    finished_row = next(row for row in stored if row.kind == JobEventKind.DONE)
    assert str(still_claimed.id) == claim["id"]
    assert still_claimed.kind == JobEventKind.CLAIM
    assert still_claimed.note == "After the last booking"
    assert str(finished_row.id) == body["id"]
    assert finished_row.claim_id == still_claimed.id
    assert finished_row.member_id == still_claimed.member_id
    assert finished_row.job_key == "job-sweep-floor"
    assert finished_row.title == "Sweep the shop floor"
    assert finished_row.note == "Floor is clear"
    assert _count(client, JobEvent, JobEventKind.CLAIM) == 1
    assert _count(client, JobEvent, JobEventKind.DONE) == 1
    assert _count(client, TokenTransaction) == tokens_before
    assert _count(client, ChatMessage) == 0

    listed = client.get("/member/jobs/events")
    assert listed.status_code == 200, listed.text
    assert [item["kind"] for item in listed.json()] == ["done", "claim"]

    login_member(client, "casey@example.com")
    assert client.get("/member/jobs/events").json() == []

    owner = client.get("/jobs/events", headers=AUTH)
    assert owner.status_code == 200, owner.text
    assert [item["kind"] for item in owner.json()] == ["done", "claim"]
    assert client.get("/jobs/events").status_code == 401


def test_unknown_job_and_second_claim_do_not_store_a_row(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com", name="Ada Reyes")
    create_member(client, email="casey@example.com", name="Casey", tier_name="basic")
    tokens_before = _count(client, TokenTransaction)
    login_member(client, "ada@example.com")

    tool = client.post("/member/jobs/claims", json={"job_key": "TC-FL-001"})
    assert tool.status_code == 422
    assert tool.json()["error"]["code"] == "not_a_job"

    part = client.post("/member/jobs/claims", json={"job_key": "PT-OIL-5W30-012"})
    assert part.status_code == 422
    assert part.json()["error"]["code"] == "not_a_job"

    bay = client.post("/member/jobs/claims", json={"job_key": "B2-WR-014"})
    assert bay.status_code == 422
    assert bay.json()["error"]["code"] == "not_a_job"

    junk = client.post("/member/jobs/claims", json={"job_key": "not-a-job"})
    assert junk.status_code == 422
    assert junk.json()["error"]["code"] == "unknown_job"
    assert _count(client, JobEvent) == 0

    first = client.post("/member/jobs/claims", json={"job_key": "job-empty-oil"})
    assert first.status_code == 201, first.text

    second = client.post("/member/jobs/claims", json={"job_key": "job-empty-oil", "note": "again"})
    assert second.status_code == 409
    assert second.json()["error"]["code"] == "already_claimed"
    assert _count(client, JobEvent) == 1

    other = client.post("/member/jobs/claims", json={"job_key": "job-sort-fasteners", "note": ""})
    assert other.status_code == 201, other.text
    assert other.json()["note"] is None
    assert _count(client, JobEvent, JobEventKind.CLAIM) == 2

    early = client.post("/member/jobs/done", json={"job_key": "job-restock-towels"})
    assert early.status_code == 409
    assert early.json()["error"]["code"] == "not_claimed"
    assert _count(client, JobEvent, JobEventKind.DONE) == 0

    login_member(client, "casey@example.com")
    stolen = client.post("/member/jobs/done", json={"job_key": "job-empty-oil"})
    assert stolen.status_code == 409
    assert stolen.json()["error"]["code"] == "not_your_claim"
    assert _count(client, JobEvent, JobEventKind.DONE) == 0

    client.cookies.clear()
    owner_done = client.post(
        "/member/jobs/done",
        headers=AUTH,
        json={"job_key": "job-empty-oil"},
    )
    assert owner_done.status_code == 401
    assert _count(client, JobEvent) == 2

    login_member(client, "ada@example.com")
    finished = client.post("/member/jobs/done", json={"job_key": "job-empty-oil"})
    assert finished.status_code == 201, finished.text
    assert finished.json()["member_id"] == ada["id"]
    assert finished.json()["note"] is None
    assert finished.json()["claim_id"] == first.json()["id"]

    again = client.post("/member/jobs/done", json={"job_key": "job-empty-oil"})
    assert again.status_code == 409
    assert again.json()["error"]["code"] == "not_claimed"
    assert _count(client, JobEvent, JobEventKind.DONE) == 1
    assert _count(client, JobEvent, JobEventKind.CLAIM) == 2

    reopened = client.post("/member/jobs/claims", json={"job_key": "job-empty-oil", "note": "Next night"})
    assert reopened.status_code == 201, reopened.text
    assert _count(client, JobEvent, JobEventKind.CLAIM) == 3
    assert _count(client, JobEvent, JobEventKind.DONE) == 1
    assert _count(client, TokenTransaction) == tokens_before
    assert _count(client, ChatMessage) == 0


def test_inactive_member_does_not_store_a_row(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com")
    login_member(client, "ada@example.com")
    patched = client.patch(f"/members/{ada['id']}", headers=AUTH, json={"status": "suspended"})
    assert patched.status_code == 200, patched.text

    denied = client.post("/member/jobs/claims", json={"job_key": "job-sweep-floor"})
    assert denied.status_code == 403
    assert denied.json()["error"]["code"] == "member_not_bookable"
    denied_done = client.post("/member/jobs/done", json={"job_key": "job-sweep-floor"})
    assert denied_done.status_code == 403
    assert _count(client, JobEvent) == 0
