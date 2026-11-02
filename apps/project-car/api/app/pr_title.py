"""Detect a backlog row id in a pull request title or body.

pBay writes the word "row" and a number. Project Car writes an R or a C
and digits. The title is checked before the body. Inside one field, the
earlier match wins.
"""

from __future__ import annotations

import re

_PBAY_ROW = re.compile(r"\brow\s+\d+\b", re.IGNORECASE)
_PROJECT_CAR_ROW = re.compile(r"\b[RC]\d+\b")


def backlog_row_named(title: str, body: str) -> str | None:
    for text in (title, body):
        named = _named_in(text)
        if named is not None:
            return named
    return None


def _named_in(text: str) -> str | None:
    matches = [match for match in (_PBAY_ROW.search(text), _PROJECT_CAR_ROW.search(text)) if match is not None]
    if not matches:
        return None
    return min(matches, key=lambda match: match.start()).group(0)
