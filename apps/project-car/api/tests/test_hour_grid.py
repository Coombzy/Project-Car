"""Bookings land on the hour and last at least one hour (Ben, D2).

A span that starts or ends off the Regina hour is 400 ``not_on_the_hour``
on quote and create and writes nothing, so a 2-minute booking can no longer
hold two whole hours. A span shorter than ``BOOKING_MIN_HOURS`` is 400
``below_minimum_length``. Whole-hour bookings hold exactly the hours they
cover.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.services import bookings as booking_service
from tests.conftest import AUTH, create_hoist, create_member, login_member

FROZEN_NOW = "2026-11-02T09:00:00-06:00"


@pytest.fixture(autouse=True)
def frozen(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SHOP_NOW", FROZEN_NOW)


def _ledger(client: TestClient, member_id: str) -> list[dict]:
    response = client.get(f"/members/{member_id}/tokens", headers=AUTH)
    assert response.status_code == 200, response.text
    return response.json()


def _create(client: TestClient, member: dict, bay: dict, start: str, end: str):
    return client.post(
        "/bookings",
        headers=AUTH,
        json={"member_id": member["id"], "hoist_id": bay["id"], "start_at": start, "end_at": end},
    )


@pytest.mark.parametrize(
    ("start", "end"),
    [
        ("2026-11-06T16:59:00-06:00", "2026-11-06T17:01:00-06:00"),
        ("2026-11-06T16:30:00-06:00", "2026-11-06T18:00:00-06:00"),
        ("2026-11-06T16:00:00-06:00", "2026-11-06T17:30:00-06:00"),
    ],
)
def test_off_the_hour_create_is_400_and_writes_nothing(
    client: TestClient, start: str, end: str
) -> None:
    member = create_member(client, email="grid@example.com")
    bay = create_hoist(client, name="Bay 1")
    before = _ledger(client, member["id"])

    response = _create(client, member, bay, start, end)
    assert response.status_code == 400, response.text
    assert response.json()["error"]["code"] == "not_on_the_hour"
    assert _ledger(client, member["id"]) == before

    listed = client.get("/bookings", headers=AUTH, params={"hoist_id": bay["id"]})
    assert listed.json() == []


def test_off_the_hour_quote_is_400(client: TestClient) -> None:
    response = client.post(
        "/bookings/quote",
        headers=AUTH,
        json={"start_at": "2026-11-06T16:59:00-06:00", "end_at": "2026-11-06T17:01:00-06:00"},
    )
    assert response.status_code == 400, response.text
    assert response.json()["error"]["code"] == "not_on_the_hour"


def test_two_minute_booking_no_longer_blocks_another_member(client: TestClient) -> None:
    """The review's probe A: the short booking is refused, so 16:00-18:00 stays open."""
    squatter = create_member(client, email="squat@example.com")
    other = create_member(client, email="other@example.com")
    bay = create_hoist(client, name="Bay 1")

    short = _create(client, squatter, bay, "2026-11-06T16:59:00-06:00", "2026-11-06T17:01:00-06:00")
    assert short.status_code == 400, short.text

    wanted = _create(client, other, bay, "2026-11-06T16:00:00-06:00", "2026-11-06T18:00:00-06:00")
    assert wanted.status_code == 201, wanted.text


def test_whole_hour_booking_holds_exactly_its_hours(client: TestClient) -> None:
    ada = create_member(client, email="ada-grid@example.com")
    casey = create_member(client, email="casey-grid@example.com")
    bay = create_hoist(client, name="Bay 1")

    first = _create(client, ada, bay, "2026-11-04T10:00:00-06:00", "2026-11-04T11:00:00-06:00")
    assert first.status_code == 201, first.text
    assert len(first.json()["pricing_rule"]["segments"]) == 1

    before = _create(client, casey, bay, "2026-11-04T09:00:00-06:00", "2026-11-04T10:00:00-06:00")
    after = _create(client, casey, bay, "2026-11-04T11:00:00-06:00", "2026-11-04T12:00:00-06:00")
    assert before.status_code == 201, before.text
    # Basic-tier limits do not apply: Casey is premium (2 simultaneous).
    assert after.status_code == 201, after.text


def test_member_create_and_shop_request_use_the_same_grid(client: TestClient) -> None:
    member = create_member(client, email="member-grid@example.com")
    bay = create_hoist(client, name="Bay 1")
    shop = create_hoist(client, name="Bay 6", is_shop=True)
    login_member(client, member["email"])

    window = {"start_at": "2026-11-04T10:15:00-06:00", "end_at": "2026-11-04T11:15:00-06:00"}
    own = client.post("/member/bookings", json={**window, "hoist_id": bay["id"]})
    assert own.status_code == 400, own.text
    assert own.json()["error"]["code"] == "not_on_the_hour"

    request = client.post("/member/shop-hoist-requests", json={**window, "hoist_id": shop["id"]})
    assert request.status_code == 400, request.text
    assert request.json()["error"]["code"] == "not_on_the_hour"


def test_minimum_length_constant_is_one_hour() -> None:
    assert booking_service.BOOKING_MIN_HOURS == 1
