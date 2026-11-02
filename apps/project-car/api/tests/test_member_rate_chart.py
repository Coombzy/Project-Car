"""The member rate chart reads the saved bands, not a fixed table."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from fastapi.testclient import TestClient

from app.shop_time import PRICING_TZ
from tests.conftest import AUTH, create_hoist, create_member, freeze_shop_clock, login_member

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


def test_edited_band_agrees_on_chart_quote_cap_cell_and_peak_line(client: TestClient) -> None:
    """One saved multiplier is what the chart, quote, cap, open cell, and peak line use."""
    freeze_shop_clock(datetime(2026, 11, 2, 8, tzinfo=PRICING_TZ))
    patched = client.patch(
        "/tiers/bands/weekend_fri_eve",
        headers=AUTH,
        json={"multiplier": "1.60"},
    )
    assert patched.status_code == 200, patched.text
    member = create_member(client, email="agree@example.com")
    hoist = create_hoist(client, name="Bay 1")
    login_member(client, member["email"])

    chart = client.get("/member/rates")
    assert chart.status_code == 200, chart.text
    owner = client.get("/tiers/rate-chart", headers=AUTH)
    assert owner.status_code == 200, owner.text
    hours = {(row["weekday"], row["hour"]): row for row in chart.json()["hours"]}
    owner_hours = {(row["weekday"], row["hour"]): row for row in owner.json()["hours"]}
    assert hours[(5, 10)]["tokens_per_hour"] == "160"
    assert hours[(5, 10)]["counts_toward_peak_cap"] is True
    assert owner_hours[(5, 10)] == hours[(5, 10)]
    assert chart.json()["peak_cap_hours"] == 4

    start = datetime(2026, 11, 7, 10, tzinfo=PRICING_TZ)
    end = datetime(2026, 11, 7, 11, tzinfo=PRICING_TZ)
    quoted = client.post(
        "/bookings/quote",
        headers=AUTH,
        json={"member_id": member["id"], "start_at": start.isoformat(), "end_at": end.isoformat()},
    )
    assert quoted.status_code == 200, quoted.text
    assert Decimal(str(quoted.json()["reserved_tokens"])) == Decimal("160.00")

    held = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
        },
    )
    assert held.status_code == 201, held.text
    refused = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": datetime(2026, 11, 7, 11, tzinfo=PRICING_TZ).isoformat(),
            "end_at": datetime(2026, 11, 7, 15, tzinfo=PRICING_TZ).isoformat(),
        },
    )
    assert refused.status_code == 409, refused.text
    error = refused.json()["error"]
    assert error["code"] == "peak_cap"
    assert (error["cap"], error["used"]) == (4, 1)

    web = Path(__file__).resolve().parents[2] / "web"
    shown = subprocess.run(
        [
            "node",
            "--import",
            "./lib/test-resolver.mjs",
            "--experimental-strip-types",
            "--input-type=module",
            "-e",
            """
            import { bandAt, peakWeek } from "./lib/booking-calendar.ts";
            const chunks = [];
            for await (const chunk of process.stdin) chunks.push(chunk);
            const input = JSON.parse(Buffer.concat(chunks).toString("utf8"));
            const cell = bandAt(input.day, input.hour, input.hours);
            const tokens = Number.isInteger(cell.tokens) ? String(cell.tokens) : cell.tokens.toString();
            const usage = peakWeek(input.bookings, input.weekStart, {
              hours: input.hours,
              peakCapHours: input.cap,
            });
            console.log(JSON.stringify({ tokens, gutter: cell.gutter, counts: cell.countsTowardPeakCap, used: usage.used, cap: usage.cap, line: usage.line }));
            """,
        ],
        cwd=web,
        input=json.dumps(
            {
                "day": "2026-11-07",
                "hour": 10,
                "hours": chart.json()["hours"],
                "cap": chart.json()["peak_cap_hours"],
                "weekStart": "2026-11-02",
                "bookings": [
                    {
                        "status": "confirmed",
                        "startAt": "2026-11-07T10:00:00",
                        "endAt": "2026-11-07T11:00:00",
                    }
                ],
            }
        ),
        capture_output=True,
        text=True,
        check=False,
    )
    assert shown.returncode == 0, shown.stderr
    line = next(row for row in shown.stdout.splitlines() if row.startswith("{"))
    display = json.loads(line)
    assert display["tokens"] == hours[(5, 10)]["tokens_per_hour"]
    assert display["gutter"] == "Peak 160"
    assert display["counts"] is True
    assert (display["used"], display["cap"]) == (error["used"], error["cap"])
    assert display["line"] == "Peak hours this week: 1 used · 3 left"
