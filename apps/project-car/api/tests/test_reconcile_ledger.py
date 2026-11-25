from __future__ import annotations

import importlib.util
from contextlib import redirect_stdout
from decimal import Decimal
from io import StringIO
from pathlib import Path
from uuid import UUID

from fastapi.testclient import TestClient

from app.models import Member, TokenTransaction, TokenTransactionKind
from tests.conftest import create_member

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "reconcile_ledger.py"


def _load():
    spec = importlib.util.spec_from_file_location("reconcile_ledger", _SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run(session) -> tuple[int, str]:
    buf = StringIO()
    with redirect_stdout(buf):
        code = _load().main(session)
    return code, buf.getvalue()


def test_drifted_cached_balance_is_listed(client: TestClient) -> None:
    member = create_member(client, email="reconcile@example.com", allocate_tokens=False)
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        row = session.get(Member, UUID(member["id"]))
        assert row is not None
        row.allowance_balance = Decimal("10.00")
        row.purchased_balance = Decimal("5.00")
        row.token_balance = Decimal("15.00")
        session.add(TokenTransaction(
            member_id=row.id, kind=TokenTransactionKind.ADMIN_ADJUSTMENT,
            amount=Decimal("15.00"), allowance_amount=Decimal("10.00"),
            purchased_amount=Decimal("5.00"),
        ))
        session.commit()
        code, out = _run(session)
        assert code == 0 and out.strip() == "ok"
        row.token_balance = Decimal("99.00")
        session.commit()
        assert _load().mismatched_members(session) == [member["id"]]
        code, out = _run(session)
        assert code == 1 and member["id"] in out and out.strip() != "ok"
    finally:
        session.close()
