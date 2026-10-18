from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
NEXT = ROOT / "scripts" / "next-row.sh"
CHECK = ROOT / "scripts" / "check-result.sh"


def write_queue(directory: Path, now_body: str) -> None:
    docs = directory / "Docs"
    docs.mkdir(parents=True)
    (docs / "queue.md").write_text(f"# Queue\n\n## Now\n\n{now_body}## Already on main\n\nDone.\n")


def run_script(script: Path, cwd: Path, args: list[str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["sh", str(script), *(args or [])],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )


def test_queue_scripts_read_the_fixture_queue(tmp_path: Path) -> None:
    assert NEXT.is_file(), "scripts/next-row.sh is missing"
    assert CHECK.is_file(), "scripts/check-result.sh is missing"
    for script in (NEXT, CHECK):
        text = script.read_text()
        assert "grok-bot" not in text
        assert "gbot-to-lead" not in text
        assert "gh pr merge" not in text
        assert "curl " not in text

    empty = tmp_path / "empty"
    none = tmp_path / "none"
    one = tmp_path / "one"
    write_queue(empty, "")
    write_queue(none, "No open row.\n\n")
    write_queue(one, "1. Alpha row stays open.\n\n2. Beta row waits.\n\n")

    empty_run = run_script(NEXT, empty)
    assert empty_run.returncode == 0
    assert empty_run.stdout.strip() == "", empty_run.stdout

    none_run = run_script(NEXT, none)
    assert none_run.returncode == 0
    assert none_run.stdout.strip() == "", none_run.stdout

    one_run = run_script(NEXT, one)
    assert one_run.returncode == 0
    assert one_run.stdout.strip() == "1. Alpha row stays open.", one_run.stdout

    green = run_script(CHECK, one, ["success", "41", "grok-build/fixture"])
    assert green.returncode == 0
    assert green.stdout == (
        "merge pull request 41 grok-build/fixture\n"
        "move to Already on main: 1. Alpha row stays open.\n"
    ), green.stdout

    red = run_script(CHECK, one, ["failure", "41", "grok-build/fixture"])
    assert red.returncode == 0
    assert red.stdout == (
        "| Queue check failed on PR 41 grok-build/fixture; leave the pull request open | proof | |\n"
    ), red.stdout
    assert "merge" not in red.stdout


def test_next_row_reads_the_shop_queue(tmp_path: Path) -> None:
    real = (ROOT / "Docs" / "queue.md").read_text()
    live = run_script(NEXT, ROOT)
    assert live.returncode == 0
    row = live.stdout.strip()
    assert row.startswith("Harden job claim and job done.")
    assert "Baseline:" in row
    assert "Target:" in row
    assert "Must not get worse:" in row

    copy = tmp_path / "shop"
    (copy / "Docs").mkdir(parents=True)
    (copy / "Docs" / "queue.md").write_text(real.replace(row, "1. Alpha row stays open.", 1))
    one = run_script(NEXT, copy)
    assert one.returncode == 0 and one.stdout.strip() == "1. Alpha row stays open.", (
        f"next-row did not print the shop row {one.stdout!r}"
    )
