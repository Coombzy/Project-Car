"""Owner and member job event lists cap rows in SQL (AUD-051).

Owner GET /jobs/events accepts limit. Member GET /member/jobs/events
already accepts limit; the list query itself must contain LIMIT.
"""

from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import Session

from tests.conftest import AUTH, create_member, login_member
from tests.test_member_job_events_limit import _notes, _seed

MORE_THAN_FIVE = 8
REQUESTED = 3


def test_owner_job_events_honors_limit(client: TestClient) -> None:
    ada = create_member(client, email="ada-aud051@example.com", name="Ada Reyes")
    _seed(client, ada["id"], MORE_THAN_FIVE, "ada")

    listed = _notes(client.get("/jobs/events", headers=AUTH, params={"limit": 5}))
    assert len(listed) == 5
    assert listed == ["ada-007", "ada-006", "ada-005", "ada-004", "ada-003"]


def _job_event_selects(statements: list) -> list[str]:
    compiled: list[str] = []
    for statement in statements:
        sql = str(statement.compile(dialect=sqlite.dialect()))
        if "FROM job_events" not in sql:
            continue
        compiled.append(sql)
    return compiled


def test_member_job_events_sql_uses_limit(client: TestClient, monkeypatch) -> None:
    ada = create_member(client, email="ada-aud051-sql@example.com", name="Ada Reyes")
    _seed(client, ada["id"], MORE_THAN_FIVE, "ada")
    login_member(client, "ada-aud051-sql@example.com")

    seen: list = []
    original = Session.scalars

    def spy(self, statement, *args, **kwargs):
        seen.append(statement)
        return original(self, statement, *args, **kwargs)

    monkeypatch.setattr(Session, "scalars", spy)
    short = _notes(client.get("/member/jobs/events", params={"limit": REQUESTED}))
    assert short == ["ada-007", "ada-006", "ada-005"]

    selects = _job_event_selects(seen)
    assert selects, "expected a job_events SELECT"
    limited = [sql for sql in selects if "LIMIT" in sql]
    assert limited, f"the member list query's SQL contains no LIMIT: {selects}"
