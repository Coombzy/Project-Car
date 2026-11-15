from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MERGE = ROOT / "Docs" / "merge-order.md"
CHECKLIST = ROOT / "Docs" / "v1-launch-checklist.md"

# GitHub state checked 2026-11-02. Bases are each pull request's baseRefName.
# Merged is on main. Closed was closed and not merged. Open is still open.
CHAIN = (
    (1, 225, "main", "Merged"),
    (2, 226, "main", "Closed"),
    (3, 227, "cursor/per-hour-pricing-b1e6", "Closed"),
    (4, 228, "cursor/hour-aligned-holds-b1e6", "Closed"),
    (5, 229, "cursor/token-purchase-ledger-b1e6", "Closed"),
    (6, 230, "cursor/override-audit-and-floor-b1e6", "Closed"),
    (7, 231, "cursor/close-bay-bookings-b1e6", "Closed"),
    (8, 232, "cursor/no-show-late-cancel-b1e6", "Closed"),
    (9, 234, "cursor/peak-hour-cap-b1e6", "Closed"),
    (10, 235, "cursor/member-booking-calendar-0433", "Closed"),
    (11, 242, "cursor/owner-booking-calendar-0433", "Closed"),
    (12, 238, "cursor/pin-shop-clock-e6d6", "Closed"),
    (13, 237, "cursor/one-shop-clock-e6d6", "Closed"),
    (14, 239, "cursor/whole-hour-book-e6d6", "Closed"),
    (15, 240, "cursor/cancel-and-no-show-e6d6", "Closed"),
    (16, 241, "cursor/bay6-peak-cap-e6d6", "Closed"),
    (17, 243, "cursor/four-band-hours-e6d6", "Closed"),
    (18, 244, "cursor/rate-chart-e6d6", "Closed"),
    (19, 245, "cursor/basic-plan-price-e6d6", "Closed"),
    (20, 246, "cursor/book-shown-price-e6d6", "Closed"),
    (21, 247, "cursor/grant-rollover-e6d6", "Closed"),
    (22, 248, "cursor/dollar-gst-row-e6d6", "Closed"),
    (23, 249, "cursor/any-bay-e6d6", "Closed"),
    (24, 250, "cursor/purchased-survive-grant-e6d6", "Closed"),
    (25, 251, "cursor/book-one-save-e6d6", "Closed"),
    (26, 252, "cursor/member-balance-view-e6d6", "Closed"),
    (27, 254, "cursor/calendar-cancel-rule-e6d6", "Closed"),
    (28, 255, "cursor/bay-close-form-e6d6", "Closed"),
    (29, 253, "cursor/finish-extra-hours-e6d6", "Closed"),
    (30, 259, "cursor/owner-schedule-hours-e6d6", "Open"),
    (31, 257, "cursor/v1-walkthrough-e6d6", "Closed"),
    (32, 256, "cursor/adjust-reason-e6d6", "Closed"),
    (33, 258, "cursor/standin-purchase-e6d6", "Closed"),
    (34, 261, "cursor/booking-clock-e6d6", "Closed"),
    (35, 260, "cursor/self-serve-signup-e6d6", "Closed"),
    (36, 262, "cursor/member-purchase-e6d6", "Closed"),
)
BESIDE = (
    (233, "main", "Merged"),
    (236, "main", "Closed"),
)

DO_NOT_MERGE = "Do not merge a closed or already-merged pull request from this file."


def _rows(text: str, header: str) -> list[list[str]]:
    lines = text.splitlines()
    try:
        start = lines.index(header)
    except ValueError as exc:
        raise AssertionError(f"missing table header: {header}") from exc
    rows: list[list[str]] = []
    for line in lines[start + 1 :]:
        if not line.startswith("|"):
            break
        if re.fullmatch(r"\|[-:| ]+\|", line):
            continue
        rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return rows


def _pr_number(cell: str) -> int:
    match = re.search(r"#(\d+)", cell)
    assert match is not None, cell
    return int(match.group(1))


def test_merge_order_states_match_github_and_keep_bases() -> None:
    text = MERGE.read_text()
    assert "Nothing here is merged" not in text
    assert "Open stack" not in text
    assert "Land **#225 first**" not in text
    assert DO_NOT_MERGE in text
    assert "Closed 2026-10-31" in text
    assert "Do not reopen it." in text
    assert "[#259](https://github.com/Coombzy/Project-Car/pull/259) is still open." in text

    chain = _rows(text, "| Order | PR | Base | State | Purpose | Risk |")
    assert len(chain) == len(CHAIN)
    for row, (order, number, base, state) in zip(chain, CHAIN, strict=True):
        assert row[0] == str(order)
        assert _pr_number(row[1]) == number
        assert row[2].strip("`") == base
        assert row[3] == state

    beside = _rows(text, "| PR | Base | State | Purpose | Risk |")
    assert len(beside) == len(BESIDE)
    for row, (number, base, state) in zip(beside, BESIDE, strict=True):
        assert _pr_number(row[0]) == number
        assert row[1].strip("`") == base
        assert row[2] == state

    open_numbers = [number for _, number, _, state in CHAIN if state == "Open"]
    open_numbers += [number for number, _, state in BESIDE if state == "Open"]
    assert open_numbers == [259]


def test_launch_checklist_does_not_treat_closed_work_as_not_started() -> None:
    text = CHECKLIST.read_text()
    assert "Nothing is on `main`" not in text
    assert "open stack" not in text.lower()
    assert "Not started" not in text
    assert "**In PR**" not in text
    assert "in PR" not in text
    assert "The shop is not open." in text
    assert "There is no Stripe." in text
    assert DO_NOT_MERGE in text
    assert (
        "[#222](https://github.com/Coombzy/Project-Car/pull/222) is closed "
        "(2026-10-31), not merged. Do not reopen it."
    ) in text
    assert "[#225](https://github.com/Coombzy/Project-Car/pull/225) and [#233](https://github.com/Coombzy/Project-Car/pull/233) are merged." in text
    assert "[#259](https://github.com/Coombzy/Project-Car/pull/259) is still open." in text
    assert (
        "Every other pull request named in `merge-order.md` is closed and was not merged."
        not in text
    )
    assert (
        "Every other pull request in the `merge-order.md` tables is closed and was not merged."
        in text
    )


_ANY_BAY_LINK = "[#264](https://github.com/Coombzy/Project-Car/pull/264)"


def test_any_bay_docs_record_the_lost_insert_proof() -> None:
    """The race note names the opt-in proof and the CI retry.

    Closed and merged pull requests stay closed and merged. This pull request
    is open and is not a table row.
    """
    merge = MERGE.read_text()
    checklist = CHECKLIST.read_text()
    chain = _rows(merge, "| Order | PR | Base | State | Purpose | Risk |")
    bay = next(row for row in chain if _pr_number(row[1]) == 248)
    assert bay[3] == "Closed"
    assert f"opt-in Postgres test in {_ANY_BAY_LINK}" in bay[5]
    assert "lost-insert retry" in bay[5]
    assert "not proven" not in bay[5].lower()
    assert "still not proven on Postgres" not in merge
    assert f"Follow-up in {_ANY_BAY_LINK}" in merge
    assert "CI skips the live race and runs the lost-insert retry on SQLite." in merge

    assert "A Postgres race between two members is not proven." not in checklist
    assert "Not proven. No workflow or CI change in this stack." not in checklist
    assert f"opt-in Postgres test in {_ANY_BAY_LINK}" in checklist
    assert "CI runs the lost-insert retry and skips the live race." in checklist
    assert "(`ANY_BAY_POSTGRES=1`). CI does not start Postgres. No workflow change." in checklist
    assert "in PR" not in checklist
    assert f"{_ANY_BAY_LINK} is open. It is not a table row." in checklist
