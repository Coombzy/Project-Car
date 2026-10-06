"""A job claim stores a row and marking it done stores another row."""

from __future__ import annotations

import re
from pathlib import Path
from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

from app.models import ChatMessage, JobEvent, JobEventKind, TokenTransaction, ToolCribEvent
from app.services.jobs import POSTED_JOBS
from tests.conftest import AUTH, create_member, login_member

PLACEHOLDERS = Path(__file__).resolve().parents[2] / "web" / "lib" / "placeholders.ts"
ALEMBIC_INI = Path(__file__).resolve().parents[1] / "alembic.ini"


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
    assert stolen.status_code == 403
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
    tokens_before = _count(client, TokenTransaction)
    chats_before = _count(client, ChatMessage)
    patched = client.patch(f"/members/{ada['id']}", headers=AUTH, json={"status": "suspended"})
    assert patched.status_code == 200, patched.text

    denied = client.post("/member/jobs/claims", json={"job_key": "job-sweep-floor"})
    assert denied.status_code == 403
    assert denied.json()["error"]["code"] == "member_not_bookable"
    denied_done = client.post("/member/jobs/done", json={"job_key": "job-sweep-floor"})
    assert denied_done.status_code == 403
    assert denied_done.json()["error"]["code"] == "member_not_bookable"
    assert _count(client, JobEvent) == 0
    assert _count(client, TokenTransaction) == tokens_before
    assert _count(client, ChatMessage) == chats_before


def _side_counts(client: TestClient) -> tuple[int, int]:
    return _count(client, TokenTransaction), _count(client, ChatMessage)


def test_blank_unknown_and_sku_keys_are_rejected_on_both_routes(client: TestClient) -> None:
    create_member(client, email="ada@example.com")
    login_member(client, "ada@example.com")
    sides = _side_counts(client)

    for path in ("/member/jobs/claims", "/member/jobs/done"):
        blank = client.post(path, json={"job_key": ""})
        assert blank.status_code == 422, blank.text
        padded_blank = client.post(path, json={"job_key": "   "})
        assert padded_blank.status_code == 422, padded_blank.text

        for sku in ("  pt-oil-5w30-012  ", "tc-fl-001", "  B2-WR-014", "b6-sk-010  "):
            denied = client.post(path, json={"job_key": sku})
            assert denied.status_code == 422, (path, sku, denied.text)
            assert denied.json()["error"]["code"] == "not_a_job", (path, sku)

        unknown = client.post(path, json={"job_key": "  not-a-posted-job  "})
        assert unknown.status_code == 422, unknown.text
        assert unknown.json()["error"]["code"] == "unknown_job"

    assert _count(client, JobEvent) == 0
    assert _side_counts(client) == sides


def test_inactive_member_cannot_finish_an_open_claim(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com")
    login_member(client, "ada@example.com")
    sides = _side_counts(client)
    claimed = client.post("/member/jobs/claims", json={"job_key": "job-sort-fasteners"})
    assert claimed.status_code == 201, claimed.text
    assert _side_counts(client) == sides

    patched = client.patch(f"/members/{ada['id']}", headers=AUTH, json={"status": "suspended"})
    assert patched.status_code == 200, patched.text
    denied = client.post("/member/jobs/done", json={"job_key": "job-sort-fasteners"})
    assert denied.status_code == 403
    assert denied.json()["error"]["code"] == "member_not_bookable"
    assert _count(client, JobEvent, JobEventKind.CLAIM) == 1
    assert _count(client, JobEvent, JobEventKind.DONE) == 0
    assert _side_counts(client) == sides


def test_another_member_reclaims_after_done(client: TestClient) -> None:
    create_member(client, email="ada@example.com", name="Ada Reyes")
    casey = create_member(client, email="casey@example.com", name="Casey", tier_name="basic")
    login_member(client, "ada@example.com")
    sides = _side_counts(client)
    claimed = client.post("/member/jobs/claims", json={"job_key": "job-torque-wrenches"})
    assert claimed.status_code == 201, claimed.text
    finished = client.post("/member/jobs/done", json={"job_key": "job-torque-wrenches"})
    assert finished.status_code == 201, finished.text

    login_member(client, "casey@example.com")
    reclaimed = client.post("/member/jobs/claims", json={"job_key": "  Job-Torque-Wrenches  "})
    assert reclaimed.status_code == 201, reclaimed.text
    assert reclaimed.json()["member_id"] == casey["id"]
    assert reclaimed.json()["job_key"] == "job-torque-wrenches"
    assert _count(client, JobEvent, JobEventKind.CLAIM) == 2
    assert _count(client, JobEvent, JobEventKind.DONE) == 1

    login_member(client, "ada@example.com")
    blocked = client.post("/member/jobs/claims", json={"job_key": "job-torque-wrenches"})
    assert blocked.status_code == 409
    assert blocked.json()["error"]["code"] == "already_claimed"
    assert _count(client, JobEvent, JobEventKind.CLAIM) == 2
    assert _side_counts(client) == sides


def test_posted_jobs_match_the_sample_board() -> None:
    source = PLACEHOLDERS.read_text(encoding="utf-8")
    board = source.split("export const SAMPLE_JOBS = [", 1)[1].split("] as const;", 1)[0]
    pairs = re.findall(r'id: "([^"]+)",\s*title: "([^"]+)"', board)
    assert pairs, "SAMPLE_JOBS ids and titles not found"
    assert dict(pairs) == POSTED_JOBS


def test_job_events_migration_is_a_single_head() -> None:
    from alembic.config import Config
    from alembic.script import ScriptDirectory

    script = ScriptDirectory.from_config(Config(str(ALEMBIC_INI)))
    assert script.get_heads() == ["20261004_0011"]
    job = script.get_revision("20261004_0010")
    assert job is not None
    assert job.down_revision == "20261004_0009"


def test_seed_reset_clears_job_events_and_tool_crib_events(client: TestClient) -> None:
    from app.seed import seed

    ada = create_member(client, email="ada@example.com", name="Ada Reyes")
    login_member(client, "ada@example.com")
    claimed = client.post("/member/jobs/claims", json={"job_key": "job-sweep-floor"})
    assert claimed.status_code == 201, claimed.text
    finished = client.post("/member/jobs/done", json={"job_key": "job-sweep-floor"})
    assert finished.status_code == 201, finished.text
    checkout = client.post(
        "/tool-crib/checkouts",
        headers=AUTH,
        json={"member_id": ada["id"], "sku": "TC-FL-001"},
    )
    assert checkout.status_code == 201, checkout.text
    returned = client.post("/tool-crib/returns", headers=AUTH, json={"sku": "TC-FL-001"})
    assert returned.status_code == 201, returned.text
    assert _count(client, JobEvent) == 2
    assert _count(client, ToolCribEvent) == 2

    session = _session(client)
    try:
        session.commit()
        session.connection().exec_driver_sql("PRAGMA foreign_keys=ON")
        seed(session, reset=True)
        session.commit()
        jobs_left = int(session.scalar(select(func.count()).select_from(JobEvent)) or 0)
        crib_left = int(session.scalar(select(func.count()).select_from(ToolCribEvent)) or 0)
    finally:
        session.close()

    assert jobs_left == 0
    assert crib_left == 0


def test_claim_and_done_take_a_postgres_advisory_lock(client: TestClient, monkeypatch) -> None:
    from app.services import jobs as job_service

    ada = create_member(client, email="ada@example.com", name="Ada Reyes")
    locks: list[tuple[str, dict[str, object] | None]] = []
    original_execute = Session.execute

    def execute(self, statement, params=None, **kwargs):
        sql = getattr(statement, "text", None)
        if isinstance(sql, str) and "pg_advisory_xact_lock" in sql:
            locks.append((sql, dict(params) if isinstance(params, dict) else None))
            return original_execute(self, text("SELECT 1"))
        if params is None:
            return original_execute(self, statement, **kwargs)
        return original_execute(self, statement, params, **kwargs)

    monkeypatch.setattr(Session, "execute", execute)
    monkeypatch.setattr(job_service, "_uses_postgres_lock", lambda _session: True, raising=False)

    opens: list[tuple[str, int]] = []
    real_open = job_service.open_claim

    def open_claim(session, job_key: str):
        opens.append((job_key, len(locks)))
        return real_open(session, job_key)

    monkeypatch.setattr(job_service, "open_claim", open_claim)

    session = _session(client)
    try:
        job_service.claim_job(
            session,
            member_id=UUID(ada["id"]),
            job_key="  Job-Empty-Oil  ",
            note=None,
        )
        job_service.mark_job_done(
            session,
            member_id=UUID(ada["id"]),
            job_key="job-empty-oil",
            note=None,
        )
    finally:
        session.close()

    assert opens == [("job-empty-oil", 1), ("job-empty-oil", 2)]
    assert len(locks) == 2
    for sql, params in locks:
        assert "pg_advisory_xact_lock" in sql
        assert "hashtextextended" in sql
        assert params == {"job_key": "job-empty-oil"}
