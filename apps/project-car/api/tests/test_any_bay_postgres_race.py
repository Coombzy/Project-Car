"""Two members book Any bay for one hour at the same time.

SQLite runs one statement at a time, so the live race is skipped unless
ANY_BAY_POSTGRES=1. Point ANY_BAY_POSTGRES_URL at a database you can wipe, or
accept the local default. Both requests read the first bay as free, then both
try to take that hour. One booking owns it. The other takes the next member
bay, or 409 no_bay when no bay is left. The shop hoist is never used.

CI stays on SQLite. It still forces the overlap check clear so the unique
hour row is what loses Bay 1, and the visit has to land on the next bay.
"""

from __future__ import annotations

import os
import threading
import time
from datetime import datetime, timedelta
from unittest.mock import patch

import httpx
import pytest
import uvicorn
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.config import settings
from app.db import get_db
from app.main import app
from app.models import Base
from app.services import bookings as booking_service
from app.services.pricing import ensure_pricing_settings
from app.shop_time import PRICING_TZ
from tests.conftest import AUTH, create_hoist, create_member, freeze_shop_clock, next_hour, seed_placeholder_tiers

_needs_postgres = pytest.mark.skipif(
    os.environ.get("ANY_BAY_POSTGRES") != "1",
    reason="Opt-in Postgres race. Set ANY_BAY_POSTGRES=1. CI stays on SQLite.",
)

_DEFAULT_URL = "postgresql+psycopg://projectcar:projectcar@127.0.0.1:5432/projectcar_any_bay"
_PORT = 18766
_PASSWORD = "long-enough-pw"
_HOLDING_SQL = "('pending', 'confirmed', 'active', 'overdue')"


def _database_url() -> str:
    return os.environ.get("ANY_BAY_POSTGRES_URL", _DEFAULT_URL)


@pytest.fixture
def race_server():
    """A live API on a wiped Postgres database. Schema comes from the models."""
    engine = create_engine(_database_url(), poolclass=NullPool)
    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
    Base.metadata.create_all(engine)
    with engine.connect() as conn:
        row = conn.execute(
            text(
                "SELECT condeferrable FROM pg_constraint "
                "WHERE conname = 'uq_booking_hours_hoist_hour'"
            )
        ).one()
    assert row.condeferrable is False

    Session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    setup = Session()
    seed_placeholder_tiers(setup)
    ensure_pricing_settings(setup)
    setup.commit()
    setup.close()

    def override_db():
        session = Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_db
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=_PORT,
        log_level="warning",
        access_log=False,
    )
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, name="any-bay-race-api", daemon=True)
    thread.start()
    deadline = time.monotonic() + 10
    while not server.started:
        if time.monotonic() > deadline:
            raise RuntimeError("The race API did not start.")
        time.sleep(0.05)
    try:
        yield {"base": f"http://127.0.0.1:{_PORT}", "Session": Session}
    finally:
        server.should_exit = True
        thread.join(timeout=5)
        app.dependency_overrides.clear()
        engine.dispose()


def _post(client: httpx.Client, path: str, **kwargs) -> httpx.Response:
    response = client.post(path, **kwargs)
    assert response.status_code < 500, response.text
    return response


def _member_cookie(client: httpx.Client, email: str) -> str:
    created = _post(
        client,
        "/members",
        headers=AUTH,
        json={"name": email, "email": email, "tier_name": "premium"},
    )
    assert created.status_code == 201, created.text
    member_id = created.json()["id"]
    password = _post(
        client,
        f"/members/{member_id}/password",
        headers=AUTH,
        json={"password": _PASSWORD},
    )
    assert password.status_code == 200, password.text
    logged_in = _post(
        client,
        "/auth/member/login",
        json={"email": email, "password": _PASSWORD},
    )
    assert logged_in.status_code == 200, logged_in.text
    token = logged_in.cookies.get(settings.member_cookie_name)
    assert token
    return token


def _holding_names(session) -> list[str]:
    rows = session.execute(
        text(
            """
            SELECT h.name
            FROM bookings b
            JOIN hoists h ON h.id = b.hoist_id
            WHERE b.status IN """
            + _HOLDING_SQL
            + """
            ORDER BY h.name
            """
        )
    ).scalars()
    return list(rows)


def _overlapping_pairs(session) -> list[tuple]:
    rows = session.execute(
        text(
            """
            SELECT b1.id, b2.id
            FROM bookings b1
            JOIN bookings b2
              ON b1.hoist_id = b2.hoist_id
             AND b1.id < b2.id
            WHERE b1.status IN """
            + _HOLDING_SQL
            + """
              AND b2.status IN """
            + _HOLDING_SQL
            + """
              AND b1.start_at < b2.end_at
              AND b2.start_at < b1.end_at
            """
        )
    ).all()
    return list(rows)


def _reserve_counts(session) -> dict[str, int]:
    rows = session.execute(
        text(
            """
            SELECT m.email, count(t.id)
            FROM members m
            LEFT JOIN token_transactions t
              ON t.member_id = m.id
             AND t.kind = 'booking_reserve'
            GROUP BY m.email
            ORDER BY m.email
            """
        )
    ).all()
    return {email: count for email, count in rows}


def _duplicate_hours(session) -> list[tuple]:
    rows = session.execute(
        text(
            """
            SELECT hoist_id, hour_start, count(*)
            FROM booking_hours
            GROUP BY hoist_id, hour_start
            HAVING count(*) > 1
            """
        )
    ).all()
    return list(rows)


def _book_together(base: str, cookies: list[str], start: datetime, end: datetime) -> list[httpx.Response]:
    """Both requests read Bay 1 as free, then both try to take it.

    The wait sits after that read and before the hour insert. One request
    cannot commit the hour until the other has already decided the bay is free.
    """
    barrier = threading.Barrier(2)
    seen = threading.local()
    overlaps = booking_service.hoist_has_overlap

    def overlap_then_wait(session, hoist_id, start_at, end_at, **kwargs):
        found = overlaps(session, hoist_id, start_at, end_at, **kwargs)
        if not getattr(seen, "waited", False):
            seen.waited = True
            barrier.wait(timeout=8)
        return found

    booking_service.hoist_has_overlap = overlap_then_wait
    body = {"start_at": start.isoformat(), "end_at": end.isoformat()}
    responses: list[httpx.Response] = []
    errors: list[BaseException] = []
    lock = threading.Lock()

    def shoot(token: str) -> None:
        try:
            with httpx.Client(base_url=base, timeout=20) as client:
                response = client.post(
                    "/member/bookings",
                    headers={"Cookie": f"{settings.member_cookie_name}={token}"},
                    json=body,
                )
            with lock:
                responses.append(response)
        except BaseException as exc:
            with lock:
                errors.append(exc)

    threads = [threading.Thread(target=shoot, args=(token,)) for token in cookies]
    try:
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=20)
    finally:
        booking_service.hoist_has_overlap = overlaps
    still_running = [thread for thread in threads if thread.is_alive()]
    assert not still_running, "A booking request was still running."
    assert not errors, errors
    assert len(responses) == 2
    return responses


def _prepare(base: str, bay_count: int) -> tuple[list[str], datetime, datetime]:
    freeze_shop_clock(datetime(2026, 11, 2, 8, 0, tzinfo=PRICING_TZ))
    start = datetime(2026, 11, 2, 10, 0, tzinfo=PRICING_TZ)
    end = datetime(2026, 11, 2, 11, 0, tzinfo=PRICING_TZ)
    with httpx.Client(base_url=base, timeout=20) as client:
        for number in range(1, bay_count + 1):
            bay = _post(
                client,
                "/hoists",
                headers=AUTH,
                json={"name": f"Bay {number}", "location_label": "North wall"},
            )
            assert bay.status_code == 201, bay.text
        shop = _post(
            client,
            "/hoists",
            headers=AUTH,
            json={"name": "Bay 6", "location_label": "Shop", "is_shop": True},
        )
        assert shop.status_code == 201, shop.text
        cookies = [
            _member_cookie(client, "race-one@example.com"),
            _member_cookie(client, "race-two@example.com"),
        ]
    return cookies, start, end


def _book(client: TestClient, member_id: str, start, end, **extra) -> httpx.Response:
    body = {
        "member_id": member_id,
        "start_at": start.isoformat(),
        "end_at": end.isoformat(),
        **extra,
    }
    return client.post("/bookings", headers=AUTH, json=body)


def test_any_bay_takes_the_next_bay_when_the_hour_insert_loses(client: TestClient) -> None:
    """The overlap read already said Bay 1 was free. The hour insert loses it.

    CI can show this without two transactions. A held hour plus a forced-clear
    overlap check is the same conflict the Postgres race hits. The savepoint
    must roll that attempt back and use Bay 2. With both bays lost, the answer
    is 409 no_bay, and Bay 6 stays unused.
    """
    patched = client.patch(
        "/tiers/premium",
        headers=AUTH,
        json={"max_simultaneous_bookings": 3},
    )
    assert patched.status_code == 200, patched.text
    holder = create_member(client, email="holds@example.com", tier_name="premium")
    loser = create_member(client, email="loses@example.com", tier_name="premium")
    alone = create_member(client, email="alone@example.com", tier_name="premium")
    later = create_member(client, email="later@example.com", tier_name="premium")
    bay1 = create_hoist(client, name="Bay 1")
    create_hoist(client, name="Bay 2")
    create_hoist(client, name="Bay 6", is_shop=True)
    start = next_hour(48)
    end = start + timedelta(hours=1)
    held = _book(client, holder["id"], start, end, hoist_id=bay1["id"])
    assert held.status_code == 201, held.text

    with patch("app.services.bookings.hoist_has_overlap", return_value=False):
        chosen = _book(client, loser["id"], start, end)
    assert chosen.status_code == 201, chosen.text
    assert chosen.json()["hoist_name"] == "Bay 2"
    assert chosen.json()["status"] == "pending"

    with patch("app.services.bookings.hoist_has_overlap", return_value=False):
        refused = _book(client, alone["id"], start, end)
    assert refused.status_code == 409, refused.text
    assert refused.json()["error"]["code"] == "no_bay"
    names = {row["hoist_name"] for row in client.get("/bookings", headers=AUTH).json()}
    assert names == {"Bay 1", "Bay 2"}

    # A later day: Bay 1 is free for the first hour and taken for the second.
    # The overlap read is forced clear. The first hour must not stay on Bay 1
    # after the second hour loses, and the whole visit lands on Bay 2.
    far = next_hour(80)
    partial = _book(
        client,
        holder["id"],
        far + timedelta(hours=1),
        far + timedelta(hours=2),
        hoist_id=bay1["id"],
    )
    assert partial.status_code == 201, partial.text
    before = len(client.get("/bookings", headers=AUTH).json())
    with patch("app.services.bookings.hoist_has_overlap", return_value=False):
        moved = _book(client, later["id"], far, far + timedelta(hours=2))
    assert moved.status_code == 201, moved.text
    assert moved.json()["hoist_name"] == "Bay 2"
    assert len(client.get("/bookings", headers=AUTH).json()) == before + 1


@_needs_postgres
def test_two_concurrent_any_bay_bookings_take_different_bays(race_server) -> None:
    cookies, start, end = _prepare(race_server["base"], bay_count=2)
    responses = _book_together(race_server["base"], cookies, start, end)
    codes = sorted(response.status_code for response in responses)
    detail = [(response.status_code, response.text) for response in responses]
    assert codes == [201, 201], detail
    names = {response.json()["hoist_name"] for response in responses}
    assert names == {"Bay 1", "Bay 2"}
    assert all(response.json()["status"] == "confirmed" for response in responses)

    session = race_server["Session"]()
    try:
        assert _holding_names(session) == ["Bay 1", "Bay 2"]
        assert _overlapping_pairs(session) == []
        assert _duplicate_hours(session) == []
        assert _reserve_counts(session) == {
            "race-one@example.com": 1,
            "race-two@example.com": 1,
        }
    finally:
        session.close()


@_needs_postgres
def test_two_concurrent_any_bay_bookings_on_one_bay_return_no_bay(race_server) -> None:
    cookies, start, end = _prepare(race_server["base"], bay_count=1)
    responses = _book_together(race_server["base"], cookies, start, end)
    by_code = {response.status_code: response for response in responses}
    detail = [(response.status_code, response.text) for response in responses]
    assert set(by_code) == {201, 409}, detail
    assert by_code[201].json()["hoist_name"] == "Bay 1"
    assert by_code[409].json()["error"]["code"] == "no_bay"

    session = race_server["Session"]()
    try:
        assert _holding_names(session) == ["Bay 1"]
        assert _overlapping_pairs(session) == []
        assert _duplicate_hours(session) == []
        counts = _reserve_counts(session)
        assert set(counts) == {"race-one@example.com", "race-two@example.com"}
        assert sorted(counts.values()) == [0, 1]
        assert counts[by_code[201].json()["member_name"]] == 1
    finally:
        session.close()
