"""Detect a backlog row id in a pull request title or body.

pBay writes the word "row" and a number. Project Car writes an R or a C,
digits, and an optional letter. A difficulty tag is not a row id. The title
is checked before the body. Inside one field, the earlier match wins.
"""

from __future__ import annotations

import re

_PBAY_ROW = re.compile(r"\brow\s+\d+\b", re.IGNORECASE)
_PROJECT_CAR_ROW = re.compile(r"\b[RC]\d+[a-z]?\b")
# [D# · S# C# R# T#]. Context and Risk scores are not row ids.
_DIFFICULTY_TAG = re.compile(r"\[D\d+ · S\d+ C\d+ R\d+ T\d+\]")


def backlog_row_named(title: str, body: str) -> str | None:
    for text in (title, body):
        named = _named_in(text)
        if named is not None:
            return named
    return None


def _named_in(text: str) -> str | None:
    # Same width, so a later id keeps its place. '#' cannot form a row id.
    visible = _DIFFICULTY_TAG.sub(lambda match: "#" * len(match.group(0)), text)
    matches = [
        match
        for match in (_PBAY_ROW.search(visible), _PROJECT_CAR_ROW.search(visible))
        if match is not None
    ]
    if not matches:
        return None
    return min(matches, key=lambda match: match.start()).group(0)
