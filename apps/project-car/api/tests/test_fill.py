from __future__ import annotations

from datetime import datetime, time, timedelta
from decimal import Decimal
from uuid import uuid4

from fastapi.testclient import TestClient

from app.models import Booking, BookingStatus, Hoist, HoistStatus
from app.services.fill import detect_openings, select_discount_pct
from app.services.pricing import quote_reserve
from app.shop_time import PRICING_TZ, pricing_clock_window, pricing_next_day, pricing_now
from tests.conftest import AUTH, create_hoist, create_member, login_member


def _regina(year: int, month: int, day: int, hour: int, minute: int = 0) -> datetime:
    return datetime(year, month, day, hour, minute, tzinfo=PRICING_TZ)


def _bay(name: str = "Bay 1") -> Hoist:
    return Hoist(id=uuid4(), name=name, location_label="", status=HoistStatus.AVAILABLE, is_shop=False)


def _booking(hoist: Hoist, start: datetime, end: datetime) -> Booking:
    return Booking(
        id=uuid4(),
        hoist_id=hoist.id,
        start_at=start,
        end_at=end,
        status=BookingStatus.CONFIRMED,
    )


def test_discount_selection_scales_with_open_hours() -> None:
    assert select_discount_pct(Decimal("0"), Decimal("13")) == Decimal("0")
    assert select_discount_pct(Decimal("13"), Decimal("0")) == Decimal("0")
    empty = select_discount_pct(Decimal("13"), Decimal("13"))
    assert empty == Decimal("25.00")
    half = select_discount_pct(Decimal("6.5"), Decimal("13"))
    assert half == Decimal("17.50")
    sliver = select_discount_pct(Decimal("0.0001"), Decimal("13"))
    assert sliver == Decimal("10.00")
    assert Decimal("10") <= sliver <= Decimal("25")
    assert Decimal("10") <= half <= Decimal("25")


def test_opening_detection_excludes_shop_hoist_and_finds_gaps() -> None:
    day = datetime(2026, 9, 8, tzinfo=PRICING_TZ).date()
    window_start, window_end = pricing_clock_window(day, time(8, 0), time(21, 0))
    bay = _bay("Bay 1")
    shop = Hoist(id=uuid4(), name="Shop", location_label="", status=HoistStatus.AVAILABLE, is_shop=True)
    busy_start = _regina(2026, 9, 8, 10)
    busy_end = _regina(2026, 9, 8, 12)
    snapshot = detect_openings(
        bays=[bay],
        bookings=[
            _booking(bay, busy_start, busy_end),
            _booking(shop, _regina(2026, 9, 8, 8), _regina(2026, 9, 8, 21)),
        ],
        target_date=day,
        window_start=window_start,
        window_end=window_end,
    )
    assert snapshot.bay_count == 1
    assert snapshot.capacity_hours == Decimal("13.0000")
    assert snapshot.booked_hours == Decimal("2.0000")
    assert snapshot.open_hours == Decimal("11.0000")
    assert snapshot.applies is True
    assert snapshot.discount_pct == select_discount_pct(Decimal("11"), Decimal("13"))
    names = {gap.hoist_name for gap in snapshot.gaps}
    assert names == {"Bay 1"}
    hours = [gap.hours for gap in snapshot.gaps]
    assert sum(hours, Decimal("0")) == Decimal("11.0000")


def test_full_day_open_uses_max_discount() -> None:
    day = datetime(2026, 9, 8, tzinfo=PRICING_TZ).date()
    window_start, window_end = pricing_clock_window(day, time(8, 0), time(21, 0))
    bay_a = _bay("Bay 1")
    bay_b = _bay("Bay 2")
    snapshot = detect_openings(
        bays=[bay_a, bay_b],
        bookings=[],
        target_date=day,
        window_start=window_start,
        window_end=window_end,
    )
    assert snapshot.open_hours == Decimal("26.0000")
    assert snapshot.discount_pct == Decimal("25.00")
    assert snapshot.fill_multiplier == Decimal("0.75")
    assert snapshot.urgency == "high"
    factor = snapshot.as_factor()
    start = _regina(2026, 9, 8, 10)
    quote = quote_reserve(start, start + timedelta(hours=1), reserved_at=start - timedelta(hours=72), fill=factor)
    assert quote.final_reserve_cost == Decimal("75.00")
    assert quote.as_rule()["fill_id"] == "next_day_open"


def test_preview_and_notify_outbox(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com", phone="403-555-0100")
    create_hoist(client, name="Bay 1")
    create_hoist(client, name="Shop", is_shop=True)
    preview = client.get("/fill/preview", headers=AUTH)
    assert preview.status_code == 200, preview.text
    body = preview.json()
    assert body["tz"] == "America/Regina"
    assert body["target_date"] == pricing_next_day().isoformat()
    assert body["bay_count"] == 1
    assert Decimal(str(body["capacity_hours"])) == Decimal("13.0000")
    assert Decimal(str(body["open_hours"])) == Decimal("13.0000")
    assert Decimal(str(body["discount_pct"])) == Decimal("25.00")
    assert body["applies"] is True
    assert all(gap["hoist_name"] != "Shop" for gap in body["gaps"])

    dry = client.post(
        "/fill/notify",
        headers=AUTH,
        json={"dry_run": True, "channels": ["email", "sms", "push"]},
    )
    assert dry.status_code == 200, dry.text
    dry_body = dry.json()
    assert dry_body["dry_run"] is True
    assert dry_body["published"] is False
    assert dry_body["queued"] == 3
    statuses = {row["channel"]: row["status"] for row in dry_body["notifications"]}
    assert statuses["email"] == "dry_run"
    assert statuses["sms"] == "dry_run"
    assert statuses["push"] == "dry_run"

    sent = client.post(
        "/fill/notify",
        headers=AUTH,
        json={"dry_run": False, "discount_pct": "15", "channels": ["email", "sms", "push"]},
    )
    assert sent.status_code == 200, sent.text
    sent_body = sent.json()
    assert sent_body["published"] is True
    assert Decimal(str(sent_body["preview"]["discount_pct"])) == Decimal("15.00")
    by_channel = {row["channel"]: row for row in sent_body["notifications"]}
    assert by_channel["email"]["status"] == "sent"
    assert by_channel["email"]["to_address"] == member["email"]
    assert by_channel["email"]["payload"]["adapter"] == "email_stub"
    assert by_channel["sms"]["status"] == "skipped"
    assert by_channel["sms"]["last_error"] == "sms_not_configured"
    assert by_channel["push"]["status"] == "skipped"
    assert "25%" not in (by_channel["email"]["subject"] or "")
    assert "15%" in (by_channel["email"]["subject"] or "")

    outbox = client.get("/fill/outbox", headers=AUTH)
    assert outbox.status_code == 200
    assert len(outbox.json()) >= 6


def test_booked_hours_lower_discount_and_quote_uses_fill(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com", tier_name="premium")
    hoist = create_hoist(client, name="Bay 1")
    target = pricing_next_day()
    busy_start = datetime.combine(target, time(9, 0), tzinfo=PRICING_TZ)
    busy_end = datetime.combine(target, time(12, 0), tzinfo=PRICING_TZ)
    booked = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": busy_start.isoformat(),
            "end_at": busy_end.isoformat(),
        },
    )
    assert booked.status_code == 201, booked.text
    preview = client.get("/fill/preview", headers=AUTH)
    assert preview.status_code == 200, preview.text
    body = preview.json()
    assert Decimal(str(body["booked_hours"])) == Decimal("3.0000")
    assert Decimal(str(body["open_hours"])) == Decimal("10.0000")
    expected_discount = select_discount_pct(Decimal("10"), Decimal("13"))
    assert Decimal(str(body["discount_pct"])) == expected_discount

    slot_start, _ = pricing_clock_window(target, time(16, 0), time(18, 0))
    slot_end = slot_start + timedelta(hours=1)
    quoted = client.post(
        "/bookings/quote",
        headers=AUTH,
        json={
            "start_at": slot_start.isoformat(),
            "end_at": slot_end.isoformat(),
            "member_id": member["id"],
        },
    )
    assert quoted.status_code == 200, quoted.text
    rule = quoted.json()["pricing_rule"]
    assert rule["fill_id"] == "next_day_open"
    fill = Decimal(str(rule["fill_multiplier"]))
    bare = quote_reserve(slot_start, slot_end)
    assert Decimal(str(quoted.json()["reserved_tokens"])) == (
        bare.final_reserve_cost * fill
    ).quantize(Decimal("0.01"))


def test_member_fill_and_next_day_quote(client: TestClient) -> None:
    create_member(client, email="ada@example.com")
    create_hoist(client, name="Bay 1")
    login_member(client, "ada@example.com")
    denied = client.get("/fill/preview")
    assert denied.status_code == 401
    preview = client.get("/member/fill")
    assert preview.status_code == 200, preview.text
    assert preview.json()["applies"] is True
    assert preview.json()["tz"] == "America/Regina"

    target = pricing_next_day()
    start, _ = pricing_clock_window(target, time(10, 0), time(12, 0))
    end = start + timedelta(hours=1)
    quoted = client.post(
        "/member/bookings/quote",
        json={"start_at": start.isoformat(), "end_at": end.isoformat()},
    )
    assert quoted.status_code == 200, quoted.text
    assert quoted.json()["pricing_rule"]["fill_id"] == "next_day_open"
    assert quoted.json()["pricing_rule"]["fill_discount_pct"] == "25"


def test_same_day_slot_does_not_take_fill(client: TestClient) -> None:
    create_member(client, email="ada@example.com")
    create_hoist(client, name="Bay 1")
    now = pricing_now()
    start = now + timedelta(hours=2)
    if start.astimezone(PRICING_TZ).date() != now.astimezone(PRICING_TZ).date():
        start = now.replace(hour=10, minute=0, second=0, microsecond=0)
        if start <= now:
            start = now + timedelta(minutes=30)
    end = start + timedelta(hours=1)
    if start.astimezone(PRICING_TZ).date() != now.astimezone(PRICING_TZ).date():
        return
    quoted = client.post(
        "/bookings/quote",
        headers=AUTH,
        json={"start_at": start.isoformat(), "end_at": end.isoformat()},
    )
    assert quoted.status_code == 200, quoted.text
    assert quoted.json()["pricing_rule"]["fill_id"] == "none"
    assert quoted.json()["pricing_rule"]["fill_multiplier"] == "1"
