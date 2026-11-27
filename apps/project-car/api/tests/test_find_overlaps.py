from __future__ import annotations

import importlib.util
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from io import StringIO
from pathlib import Path
from uuid import UUID

from fastapi.testclient import TestClient

from app.models import Booking, BookingKind, BookingStatus
from tests.conftest import create_hoist, create_member

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "find_overlaps.py"


def _load():
    spec = importlib.util.spec_from_file_location("find_overlaps", _SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run(session) -> tuple[int, str]:
    buf = StringIO()
    with redirect_stdout(buf):
        code = _load().main(session)
    return code, buf.getvalue()


def _add(session, member_id, hoist_id, start, hours, status) -> str:
    booking = Booking(
        member_id=UUID(member_id), hoist_id=UUID(hoist_id),
        start_at=start, end_at=start + timedelta(hours=hours),
        kind=BookingKind.CUSTOMER, status=status, reserved_tokens=Decimal("0"),
    )
    session.add(booking)
    session.commit()
    return str(booking.id)


def test_overlapping_bookings_list_both_ids(client: TestClient) -> None:
    member = create_member(client)
    hoist = create_hoist(client)
    start = datetime(2026, 11, 24, 16, 0, tzinfo=timezone.utc)
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        first = _add(session, member["id"], hoist["id"], start, 2, BookingStatus.PENDING)
        second = _add(
            session, member["id"], hoist["id"], start + timedelta(hours=1), 2, BookingStatus.CONFIRMED,
        )
        code, out = _run(session)
    finally:
        session.close()
    assert code == 0 and first in out and second in out


def test_no_overlaps_exits_zero(client: TestClient) -> None:
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        code, out = _run(session)
    finally:
        session.close()
    assert code == 0 and out.strip() == "no overlaps"
