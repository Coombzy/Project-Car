"""Owner period allotment: one monthly_allocation per active member per Regina month."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy import select

from app.models import TokenTransaction
from app.shop_time import PRICING_TZ, pricing_now
from tests.conftest import AUTH, create_member


def _period_now() -> str:
    local = pricing_now().astimezone(PRICING_TZ)
    return f"{local.year:04d}-{local.month:02d}"


def _previous_month_naive_utc() -> datetime:
    local = pricing_now().astimezone(PRICING_TZ)
    year = local.year
    month = local.month - 1
    if month == 0:
        year -= 1
        month = 12
    wall = datetime(year, month, 15, 12, 0, tzinfo=PRICING_TZ)
    return wall.astimezone(timezone.utc).replace(tzinfo=None)


def _month_open_still_previous_regina_month() -> datetime:
    """02:00 UTC on the 1st is still the previous America/Regina calendar day.

    Regina is UTC−6 all year, so the Regina month opens at 06:00 UTC.
    """
    local = pricing_now().astimezone(PRICING_TZ)
    return datetime(local.year, local.month, 1, 2, 0)


def _ledger(client: TestClient, member_id: str) -> list[dict]:
    response = client.get(f"/members/{member_id}/tokens", headers=AUTH)
    assert response.status_code == 200, response.text
    return response.json()


def _balance(client: TestClient, member_id: str) -> Decimal:
    response = client.get(f"/members/{member_id}", headers=AUTH)
    assert response.status_code == 200, response.text
    return Decimal(str(response.json()["token_balance"]))


def _monthly(rows: list[dict]) -> list[dict]:
    return [row for row in rows if row["kind"] == "monthly_allocation"]


def _period_rows(rows: list[dict], period: str) -> list[dict]:
    found = []
    for row in _monthly(rows):
        meta = row.get("meta") or {}
        if meta.get("period") == period and meta.get("tz") == "America/Regina":
            found.append(row)
    return found


def _set_created_at(client: TestClient, member_id: str, created_at: datetime) -> None:
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        rows = list(
            session.scalars(
                select(TokenTransaction).where(TokenTransaction.member_id == UUID(member_id))
            ).all()
        )
        assert len(rows) == 1
        rows[0].created_at = created_at
        session.commit()
    finally:
        session.close()


def test_period_allocation_grants_included_tokens_once(client: TestClient) -> None:
    """POST /tiers/period-allocation/grant grants tier included_tokens once per Regina month.

    The initial monthly_allocation counts for the month it was written. A second
    call inserts no ledger row. Suspended members are not granted.
    """
    period = _period_now()
    previous = _previous_month_naive_utc().strftime("%Y-%m")
    current = create_member(client, name="Ada Current", email="ada.current@example.com", tier_name="premium")
    prior = create_member(client, name="Bea Prior", email="bea.prior@example.com", tier_name="premium")
    boundary = create_member(client, name="Cam Boundary", email="cam.boundary@example.com", tier_name="premium")
    fresh = create_member(
        client,
        name="Cal Fresh",
        email="cal.fresh@example.com",
        tier_name="basic",
        allocate_tokens=False,
    )
    suspended = create_member(
        client,
        name="Dee Suspended",
        email="dee.suspended@example.com",
        tier_name="basic",
        status="suspended",
        allocate_tokens=False,
    )
    _set_created_at(client, prior["id"], _previous_month_naive_utc())
    boundary_at = _month_open_still_previous_regina_month()
    _set_created_at(client, boundary["id"], boundary_at)

    assert _monthly(_ledger(client, fresh["id"])) == []
    assert _monthly(_ledger(client, suspended["id"])) == []
    assert len(_monthly(_ledger(client, current["id"]))) == 1
    assert _period_rows(_ledger(client, current["id"]), period) == []
    prior_before = _monthly(_ledger(client, prior["id"]))
    assert len(prior_before) == 1
    assert str(prior_before[0]["created_at"]).startswith(previous)
    boundary_before = _monthly(_ledger(client, boundary["id"]))
    assert len(boundary_before) == 1
    assert str(boundary_before[0]["created_at"]).startswith(boundary_at.strftime("%Y-%m-%dT%H:%M"))

    first = client.post("/tiers/period-allocation/grant", headers=AUTH)
    assert first.status_code == 200, first.text
    body = first.json()
    assert body["period"] == period
    assert body["tz"] == "America/Regina"
    assert body["skipped"] == 1
    amounts = {row["member_id"]: Decimal(str(row["amount"])) for row in body["granted"]}
    assert amounts == {
        fresh["id"]: Decimal("1000"),
        prior["id"]: Decimal("1500"),
        boundary["id"]: Decimal("1500"),
    }

    fresh_rows = _monthly(_ledger(client, fresh["id"]))
    assert len(fresh_rows) == 1
    assert _period_rows(fresh_rows, period) == fresh_rows
    assert Decimal(str(fresh_rows[0]["amount"])) == Decimal("1000")
    assert _balance(client, fresh["id"]) == Decimal("1000")

    prior_rows = _monthly(_ledger(client, prior["id"]))
    assert len(prior_rows) == 2
    assert len(_period_rows(prior_rows, period)) == 1
    assert Decimal(str(_period_rows(prior_rows, period)[0]["amount"])) == Decimal("1500")
    assert _balance(client, prior["id"]) == Decimal("3000")

    boundary_rows = _monthly(_ledger(client, boundary["id"]))
    assert len(boundary_rows) == 2
    assert len(_period_rows(boundary_rows, period)) == 1
    assert _balance(client, boundary["id"]) == Decimal("3000")

    current_rows = _monthly(_ledger(client, current["id"]))
    assert len(current_rows) == 1
    assert _period_rows(current_rows, period) == []
    assert Decimal(str(current_rows[0]["amount"])) == Decimal("1500")
    assert _balance(client, current["id"]) == Decimal("1500")

    assert _monthly(_ledger(client, suspended["id"])) == []
    assert _balance(client, suspended["id"]) == Decimal("0")

    ids = [current["id"], prior["id"], boundary["id"], fresh["id"], suspended["id"]]
    ledger_ids = {member_id: [row["id"] for row in _ledger(client, member_id)] for member_id in ids}
    balances = {member_id: _balance(client, member_id) for member_id in ids}

    second = client.post("/tiers/period-allocation/grant", headers=AUTH)
    assert second.status_code == 200, second.text
    assert second.json()["granted"] == []
    assert second.json()["skipped"] == 4
    assert second.json()["period"] == period
    for member_id in ids:
        assert [row["id"] for row in _ledger(client, member_id)] == ledger_ids[member_id]
        assert _balance(client, member_id) == balances[member_id]

    denied = client.post("/tiers/period-allocation/grant")
    assert denied.status_code == 401, denied.text
    ai = client.post(
        "/tiers/period-allocation/grant",
        headers={"Authorization": "Bearer dev-ai-secret"},
    )
    assert ai.status_code == 403, ai.text
    assert ai.json()["error"]["code"] == "allocation_requires_human"
    for member_id in ids:
        assert [row["id"] for row in _ledger(client, member_id)] == ledger_ids[member_id]
