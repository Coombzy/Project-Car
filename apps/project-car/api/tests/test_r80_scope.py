"""R80 does not lengthen the owner /schedule shot or free visual ports."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
WEB = ROOT / "apps" / "project-car" / "web"


def test_schedule_clock_and_visual_build_stay_outside_r80() -> None:
    spec = (WEB / "visual" / "pages.spec.ts").read_text(encoding="utf-8")
    assert "const MAX_LAYOUT_SHIFT = 0.1;" in spec
    assert "const SETTLE_MS = 800;" in spec
    assert "test.setTimeout(120_000)" not in spec
    assert 'if (shot.path === "/schedule")' not in spec

    build = (WEB / "visual" / "build-web.sh").read_text(encoding="utf-8")
    assert "npx playwright install" not in build
    assert "free_visual_ports" not in build
    assert "\nnpm run build\n" in build

    assert not (WEB / "visual" / "free_visual_ports.py").exists()

    calendar = (WEB / "components" / "week-hoist-calendars.tsx").read_text(encoding="utf-8")
    slot = calendar.index("className={`hour-slot")
    assert slot >= 0
    assert "prefetch={false}" not in calendar[slot : slot + 500]
