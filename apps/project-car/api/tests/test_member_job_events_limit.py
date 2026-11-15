"""Member GET /member/jobs/events is capped (PC-R76).

limit defaults to 200 and must be 1..500 (422 outside). Newest first.
Other members' rows never appear. Cap is applied in the router.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi.testclient import TestClient

from app.models import JobEvent, JobEventKind
from tests.conftest import create_member, login_member

TOTAL = 205
_BASE = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _seed(client: TestClient, member_id: str, count: int, prefix: str) -> None:
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        for index in range(count):
            session.add(
                JobEvent(
                    member_id=UUID(member_id),
                    job_key=f"job-sweep-floor",
                    title="Sweep the shop floor",
                    kind=JobEventKind.CLAIM,
                    note=f"{prefix}-{index:03d}",
                    created_at=_BASE + timedelta(seconds=index),
                )
            )
        session.commit()
    finally:
        session.close()


def _notes(response) -> list[str]:
    assert response.status_code == 200, response.text
    return [row["note"] for row in response.json()]


def test_member_job_events_list_caps_rows(client: TestClient) -> None:
    ada = create_member(client, email="ada-r76@example.com", name="Ada Reyes")
    casey = create_member(client, email="casey-r76@example.com", name="Casey", tier_name="basic")
    _seed(client, ada["id"], TOTAL, "ada")
    _seed(client, casey["id"], 10, "casey")

    login_member(client, "ada-r76@example.com")
    default = _notes(client.get("/member/jobs/events"))
    # newest first: index 204 .. 5 (200 rows)
    assert len(default) == 200
    assert default[0] == "ada-204"
    assert default[-1] == "ada-005"
    assert all(n.startswith("ada-") for n in default)

    short = _notes(client.get("/member/jobs/events", params={"limit": 3}))
    assert short == ["ada-204", "ada-203", "ada-202"]

    for params in ({"limit": 0}, {"limit": 501}):
        response = client.get("/member/jobs/events", params=params)
        assert response.status_code == 422, (params, response.text)

    login_member(client, "casey-r76@example.com")
    casey_notes = _notes(client.get("/member/jobs/events"))
    assert len(casey_notes) == 10
    assert all(n.startswith("casey-") for n in casey_notes)
