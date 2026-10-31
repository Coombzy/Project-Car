"""Weekly peak-hour cap (Ben, D13).

A member may hold at most ``PEAK_HOURS_PER_WEEK`` (4) peak-band hours per
America/Regina week (Monday to Sunday). Peak is the ``weekend_fri_eve`` band.
Each held hour counts on its own, so a mixed booking only counts its peak
hours. Cancelled bookings free their hours. Over the cap is 409 ``peak_cap``.

What happens over the cap is ``PEAK_OVER_CAP_POLICY``. Only ``refuse`` exists;
a later premium on extra peak hours is a new policy value, not built here.
"""

from __future__ import annotations

from datetime import datetime

import pytest
from app.services.peak_cap import PeakOverCapPolicy
from fastapi.testclient import TestClient

from app.services import peak_cap
from app.shop_time import PRICING_TZ
from tests.conftest import AUTH, create_hoist, create_member, freeze_shop_clock

MONDAY = datetime(2026, 11, 2, 9, 0, tzinfo=PRICING_TZ)


def _at(day: int, hour: int) -> datetime:
    return datetime(2026, 11, day, hour, 0, tzinfo=PRICING_TZ)


@pytest.fixture
def setup(client: TestClient) -> tuple[TestClient, dict, dict]:
    freeze_shop_clock(MONDAY)
    member = create_member(client)
    hoist = create_hoist(client)
    return client, member, hoist


def _book(client: TestClient, member: dict, hoist: dict, start: datetime, end: datetime):
    return client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
        },
    )


def test_defaults_match_d13() -> None:
    assert peak_cap.PEAK_HOURS_PER_WEEK == 4
    assert peak_cap.PEAK_BAND_IDS == frozenset({"weekend_fri_eve"})
    assert peak_cap.PEAK_OVER_CAP_POLICY is PeakOverCapPolicy.REFUSE
    assert list(PeakOverCapPolicy) == [PeakOverCapPolicy.REFUSE]


def test_fifth_peak_hour_in_a_week_is_refused(setup) -> None:
    client, member, hoist = setup
    first = _book(client, member, hoist, _at(7, 10), _at(7, 14))
    assert first.status_code == 201, first.text

    refused = _book(client, member, hoist, _at(7, 15), _at(7, 16))

    assert refused.status_code == 409, refused.text
    error = refused.json()["error"]
    assert error["code"] == "peak_cap"
    assert (error["cap"], error["used"], error["requested"]) == (4, 4, 1)
    assert error["week_start"] == "2026-11-02"
    listed = client.get("/bookings", headers=AUTH, params={"member_id": member["id"]}).json()
    assert [row["id"] for row in listed] == [first.json()["id"]]


def test_one_booking_over_the_cap_is_refused_outright(setup) -> None:
    client, member, hoist = setup
    refused = _book(client, member, hoist, _at(7, 10), _at(7, 15))
    assert refused.status_code == 409, refused.text
    assert (refused.json()["error"]["used"], refused.json()["error"]["requested"]) == (0, 5)


def test_only_peak_hours_of_a_mixed_booking_count(setup) -> None:
    client, member, hoist = setup
    # Friday 13-18: 13-16 weekday day, 16-18 peak (2).
    friday = _book(client, member, hoist, _at(6, 13), _at(6, 18))
    assert friday.status_code == 201, friday.text

    # Sunday 18-22: 18-21 peak (3), 21-22 late night.
    refused = _book(client, member, hoist, _at(8, 18), _at(8, 22))
    assert refused.status_code == 409, refused.text
    assert (refused.json()["error"]["used"], refused.json()["error"]["requested"]) == (2, 3)

    # Sunday 19-22: 19-21 peak (2) brings Ada to exactly 4.
    fits = _book(client, member, hoist, _at(8, 19), _at(8, 22))
    assert fits.status_code == 201, fits.text


def test_cancelled_hours_free_the_cap(setup) -> None:
    client, member, hoist = setup
    first = _book(client, member, hoist, _at(7, 10), _at(7, 14))
    assert first.status_code == 201, first.text
    assert client.post(f"/bookings/{first.json()['id']}/cancel", headers=AUTH).status_code == 200

    again = _book(client, member, hoist, _at(7, 15), _at(7, 19))

    assert again.status_code == 201, again.text


def test_the_cap_resets_each_monday(setup) -> None:
    client, member, hoist = setup
    assert _book(client, member, hoist, _at(8, 10), _at(8, 14)).status_code == 201

    next_week = _book(client, member, hoist, _at(14, 10), _at(14, 14))

    assert next_week.status_code == 201, next_week.text


def test_off_peak_hours_are_not_capped(setup) -> None:
    client, member, hoist = setup
    assert _book(client, member, hoist, _at(7, 10), _at(7, 14)).status_code == 201

    weekday = _book(client, member, hoist, _at(3, 8), _at(3, 16))

    assert weekday.status_code == 201, weekday.text


def test_cap_is_per_member(setup) -> None:
    client, member, hoist = setup
    other = create_member(client, name="Other", email="other@example.com")
    assert _book(client, member, hoist, _at(7, 10), _at(7, 14)).status_code == 201

    theirs = _book(client, other, hoist, _at(7, 15), _at(7, 19))

    assert theirs.status_code == 201, theirs.text


def test_cap_constant_is_the_only_knob(setup, monkeypatch: pytest.MonkeyPatch) -> None:
    client, member, hoist = setup
    monkeypatch.setattr(peak_cap, "PEAK_HOURS_PER_WEEK", 2)

    refused = _book(client, member, hoist, _at(7, 10), _at(7, 13))

    assert refused.status_code == 409, refused.text
    assert refused.json()["error"]["cap"] == 2
