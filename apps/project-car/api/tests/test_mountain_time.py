"""One shop clock, labelled Mountain Time.

Typed times, bands, weeks, and months share one UTC−6 zone. Member-facing
copy says Mountain Time. It does not say America/Regina, America/Edmonton,
MDT, or CST.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from app.shop_time import PRICING_TZ, SHOP_TZ, format_shop_time

REPO = Path(__file__).resolve().parents[4]
MEMBER_FACING = (
    "apps/project-car/web/app/member",
    "apps/project-car/web/app/page.tsx",
    "apps/project-car/web/app/fill/page.tsx",
    "apps/project-car/web/app/tiers/page.tsx",
    "apps/project-car/web/components/member-booking-form.tsx",
    "apps/project-car/web/components/member-booking-card.tsx",
    "apps/project-car/web/components/create-booking-form.tsx",
    "apps/project-car/web/components/calendar-connect.tsx",
    "apps/project-car/web/components/todo-panel.tsx",
    "apps/project-car/api/app/services/notify.py",
    "apps/project-car/api/app/routers/member.py",
)
BANNED = ("America/Regina", "America/Edmonton", "MDT", "CST")


def test_january_afternoon_is_4pm_mountain_time() -> None:
    slot = datetime(2027, 1, 15, 16, 0, tzinfo=SHOP_TZ)
    label = format_shop_time(slot)
    assert label == "4:00 p.m. Mountain Time"
    assert SHOP_TZ is PRICING_TZ
    for banned in BANNED:
        assert banned not in label


def test_member_facing_copy_does_not_name_a_zone_database() -> None:
    hits: list[str] = []
    for relative in MEMBER_FACING:
        path = REPO / relative
        files = [path] if path.is_file() else sorted(path.rglob("*.tsx"))
        for file in files:
            text = file.read_text()
            for banned in BANNED:
                if banned in text:
                    hits.append(f"{file.relative_to(REPO)}: {banned}")
    assert hits == []
