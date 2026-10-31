"""Two members book Any bay for one hour at the same time, on real Postgres.

SQLite runs one statement at a time, so the rest of the suite cannot show this
race. The test is skipped unless ANY_BAY_POSTGRES=1. Point
ANY_BAY_POSTGRES_URL at a database you can wipe, or accept the local default.
Both requests read the first bay as free, then both try to take that hour.
One booking owns it. The other takes the next member bay, or 409 no_bay when
no bay is left. The shop hoist is never used.
"""

from __future__ import annotations

import os
import threading
import time
from datetime import datetime

import httpx
import pytest
import uvicorn
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
from tests.conftest import AUTH, freeze_shop_clock, seed_placeholder_tiers

pytestmark = pytest.mark.skipif(
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
    finally:
        session.close()


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
    finally:
        session.close()
