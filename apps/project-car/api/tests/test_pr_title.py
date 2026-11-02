"""A pull request title and body must not name a backlog row.

pBay names a row as the word "row" plus a number. Project Car names a row as
an R or a C followed by digits. Either form in the title or the body fails.
"""

from __future__ import annotations

from app.pr_title import backlog_row_named


def test_pbay_row_number_in_the_title_is_named() -> None:
    assert backlog_row_named("row 4: ship the queue", "No id in the body.") == "row 4"


def test_project_car_row_ids_in_title_or_body_are_named() -> None:
    assert backlog_row_named("R12: Owner queue shows pending requests", "") == "R12"
    assert backlog_row_named("Cameras stay on the member shell", "See C3.") == "C3"


def test_title_match_wins_when_the_body_also_names_a_row() -> None:
    assert backlog_row_named("R12: queue", "row 4 stays parked") == "R12"


def test_clean_title_and_body_name_no_backlog_row() -> None:
    title = "Refresh schedule screenshots for the week booking calendar"
    body = (
        "The member schedule opens on the week. "
        "A job claim and a done each store a row. "
        "Ledger rows name each extra hour."
    )
    assert backlog_row_named(title, body) is None


def test_row_word_without_a_number_is_not_a_backlog_row() -> None:
    assert backlog_row_named("store a row", "token credit stays later") is None
    assert backlog_row_named("arrow 12", "row12") is None
    assert backlog_row_named("r12 stays lowercase", "c3 stays lowercase") is None
