"""RFC 5545 §3.1: todo_ics physical lines stay within 75 UTF-8 octets.

ASCII exports keep the historical 73-then-72 character fold, including the
81-octet first SUMMARY line of a 200-character title. That byte string is
locked by test_dashboard_todos.py and must match main before and after.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

import pytest

from app.models import Todo, TodoStatus
from app.services.ics import todo_ics
from app.shop_time import PRICING_TZ

# Clock and id are fixed so the ASCII guard compares fold bytes, not DTSTAMP.
_FIXED_STAMP = datetime(2026, 6, 15, 15, 30, 0, tzinfo=PRICING_TZ)
_TODO_ID = UUID("00000000-0000-4000-8000-000000000036")

# Captured from main f4062c99 (character fold) at _FIXED_STAMP / _TODO_ID.
# 200 A's -> 73 + 72 + 55. First physical line is SUMMARY: + 73 = 81 octets.
_ASCII_200 = "A" * 200
_ASCII_200_ON_MAIN = (
    "BEGIN:VCALENDAR\r\n"
    "VERSION:2.0\r\n"
    "PRODID:-//Project Car//Shop OS//EN\r\n"
    "CALSCALE:GREGORIAN\r\n"
    "METHOD:PUBLISH\r\n"
    "BEGIN:VTIMEZONE\r\n"
    "TZID:America/Regina\r\n"
    "BEGIN:STANDARD\r\n"
    "DTSTART:19701101T020000\r\n"
    "TZOFFSETFROM:-0600\r\n"
    "TZOFFSETTO:-0600\r\n"
    "TZNAME:CST\r\n"
    "END:STANDARD\r\n"
    "END:VTIMEZONE\r\n"
    "BEGIN:VEVENT\r\n"
    "UID:todo-00000000-0000-4000-8000-000000000036@projectcar.ca\r\n"
    "DTSTAMP:20260615T153000\r\n"
    "DTSTART;TZID=America/Regina:20260615T153000\r\n"
    "DTEND;TZID=America/Regina:20260615T163000\r\n"
    "SUMMARY:"
    + ("A" * 73)
    + "\r\n "
    + ("A" * 72)
    + "\r\n "
    + ("A" * 55)
    + "\r\n"
    "DESCRIPTION:Shop OS to-do\r\n"
    "END:VEVENT\r\n"
    "END:VCALENDAR\r\n"
)


def _calendar(title: str, notes: str | None = None) -> str:
    return todo_ics(
        Todo(
            id=_TODO_ID,
            title=title,
            notes=notes,
            status=TodoStatus.OPEN,
        )
    )


def _freeze_stamp(monkeypatch: pytest.MonkeyPatch) -> None:
    class FrozenDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            if tz is None:
                return _FIXED_STAMP.replace(tzinfo=None)
            return _FIXED_STAMP.astimezone(tz)

    monkeypatch.setattr("app.services.ics.datetime", FrozenDateTime)


def _physical_lines(body: str) -> list[bytes]:
    raw = body.encode("utf-8")
    assert raw.decode("utf-8") == body
    assert raw.endswith(b"\r\n")
    lines = raw.split(b"\r\n")[:-1]
    assert lines
    assert all(b"\r" not in line for line in lines)
    return lines


def _line_starting(body: str, prefix: bytes) -> bytes:
    matches = [line for line in _physical_lines(body) if line.startswith(prefix)]
    assert matches, prefix
    return matches[0]


def _unfolded_value(body: str, name: str) -> str:
    """RFC 5545 unfold: drop CRLF + one WSP. Value is the text after NAME:."""
    start = body.index(f"{name}:")
    i = start
    while i < len(body):
        if body.startswith("\r\n", i):
            nxt = i + 2
            if nxt < len(body) and body[nxt] in " \t":
                i = nxt + 1
                continue
            chunk = body[start:i]
            break
        i += 1
    else:
        raise AssertionError(f"{name} property did not end with CRLF")
    unfolded = chunk.replace("\r\n ", "").replace("\r\n\t", "")
    marker = f"{name}:"
    assert unfolded.startswith(marker)
    return unfolded[len(marker):]


def _escaped(text: str) -> str:
    """Same escapes as ics._escape, written out so the test does not call it."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return (
        normalized.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def _assert_folded(
    body: str, name: str, raw_value: str, *, description: str = "Shop OS to-do"
) -> None:
    lines = _physical_lines(body)
    for line in lines:
        assert len(line) <= 75, len(line)
        assert line.decode("utf-8").encode("utf-8") == line
    assert "\ufffd" not in body
    assert _unfolded_value(body, name) == _escaped(raw_value)
    assert _unfolded_value(body, "DESCRIPTION") == _escaped(description)


def test_sixty_eacute_title_is_at_most_75_octets() -> None:
    title = "\u00e9" * 60
    assert len(title.encode("utf-8")) == 120
    body = _calendar(title, notes=title)
    summary = _line_starting(body, b"SUMMARY:")
    value_octets = len(summary) - len(b"SUMMARY:")
    assert len(summary) <= 75, (
        f"{value_octets}-octet line: SUMMARY is {len(summary)} octets"
    )
    _assert_folded(body, "SUMMARY", title, description=title)


def test_mixed_emoji_title_is_at_most_75_octets() -> None:
    title = "Cam " + ("\U0001f527" * 20) + " seal"
    body = _calendar(title)
    summary = _line_starting(body, b"SUMMARY:")
    assert len(summary) <= 75, f"SUMMARY is {len(summary)} octets"
    _assert_folded(body, "SUMMARY", title)
    assert _unfolded_value(body, "SUMMARY").count("\U0001f527") == 20


def test_folded_multibyte_keeps_escapes() -> None:
    """A non-ASCII value that must fold still round-trips \\ ; , and newlines."""
    title = "\u00e9;,\n\\" * 20
    body = _calendar(title)
    summary = _line_starting(body, b"SUMMARY:")
    assert len(summary) <= 75, f"SUMMARY is {len(summary)} octets"
    _assert_folded(body, "SUMMARY", title)


def test_ascii_200_title_matches_main_bytes(monkeypatch: pytest.MonkeyPatch) -> None:
    _freeze_stamp(monkeypatch)
    body = _calendar(_ASCII_200)
    assert body == _ASCII_200_ON_MAIN
    assert body.encode("utf-8") == _ASCII_200_ON_MAIN.encode("utf-8")
    lines = _physical_lines(body)
    for line in lines:
        assert line.decode("utf-8").encode("utf-8") == line
    assert _unfolded_value(body, "SUMMARY") == _ASCII_200
    assert _unfolded_value(body, "DESCRIPTION") == "Shop OS to-do"
