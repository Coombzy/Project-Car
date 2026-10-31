"""The member rate chart reads the saved bands, not a fixed table."""

from __future__ import annotations

from fastapi.testclient import TestClient

from tests.conftest import AUTH, create_member, login_member

NOTE = "Only Peak counts toward the 4-hour weekly cap."


def test_member_week_follows_the_saved_peak_rate(client: TestClient) -> None:
    member = create_member(client)
    login_member(client, member["email"])

    chart = client.get("/member/rates")
    assert chart.status_code == 200, chart.text
    body = chart.json()
    assert body["tz_label"] == "Mountain Time"
    assert body["note"] == NOTE
    assert body["peak_cap_hours"] == 4
    assert len(body["hours"]) == 7 * 24

    hours = {(row["weekday"], row["hour"]): row for row in body["hours"]}
    assert hours[(0, 10)]["label"] == "Normal"
    assert hours[(0, 10)]["tokens_per_hour"] == "100"
    assert hours[(0, 10)]["counts_toward_peak_cap"] is False
    assert hours[(4, 16)]["label"] == "Evening"
    assert hours[(4, 16)]["tokens_per_hour"] == "125"
    assert hours[(5, 10)]["label"] == "Peak"
    assert hours[(5, 10)]["tokens_per_hour"] == "150"
    assert hours[(5, 10)]["counts_toward_peak_cap"] is True
    assert hours[(5, 18)]["label"] == "Evening"
    assert hours[(5, 18)]["counts_toward_peak_cap"] is False
    assert hours[(5, 22)]["label"] == "Off-peak"
    assert hours[(5, 22)]["tokens_per_hour"] == "75"
    assert hours[(6, 9)]["counts_toward_peak_cap"] is True

    patched = client.patch(
        "/tiers/bands/weekend_fri_eve",
        headers=AUTH,
        json={"multiplier": "1.60"},
    )
    assert patched.status_code == 200, patched.text
    again = client.get("/member/rates").json()
    peak = {(row["weekday"], row["hour"]): row for row in again["hours"]}
    assert peak[(5, 10)]["tokens_per_hour"] == "160"
    assert peak[(0, 10)]["tokens_per_hour"] == "100"
    bands = {row["id"]: row for row in again["bands"]}
    assert bands["weekend_fri_eve"]["label"] == "Peak"
    assert bands["weekend_fri_eve"]["tokens_per_hour"] == "160"
