"""ICS export for a personal to-do due date (America/Regina)."""

from __future__ import annotations

from datetime import datetime, timedelta
from uuid import UUID

from app.models import Todo
from app.shop_time import PRICING_TZ, as_utc


def _escape(line: str) -> str:
    # CRLF and a lone CR are one newline, same as LF. Normalize before
    # escaping so the inserted "\n" is not doubled and folding sees the escape.
    normalized = line.replace("\r\n", "\n").replace("\r", "\n")
    return (
        normalized.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def _fold_ascii(escaped: str) -> str:
    if len(escaped) <= 73:
        return escaped
    chunks = [escaped[:73]]
    rest = escaped[73:]
    while rest:
        chunks.append(rest[:72])
        rest = rest[72:]
    return "\r\n ".join(chunks)


def _utf8_prefix(text: str, max_octets: int) -> str:
    """Longest prefix whose UTF-8 encoding is at most max_octets."""
    encoded = text.encode("utf-8")
    if max_octets <= 0 or not encoded:
        return ""
    if len(encoded) <= max_octets:
        return text
    cut = max_octets
    # Walk off a trailing continuation byte so the cut is not mid-character.
    while cut > 0 and (encoded[cut] & 0xC0) == 0x80:
        cut -= 1
    return encoded[:cut].decode("utf-8")


def _fold_octets(content: str) -> str:
    """Fold one full content line to at most 75 octets (RFC 5545 §3.1).

    A continuation starts with one space, and that space counts toward 75.
    """
    if len(content.encode("utf-8")) <= 75:
        return content
    parts: list[str] = []
    rest = content
    limit = 75
    while rest:
        piece = _utf8_prefix(rest, limit)
        if not piece:
            piece = rest[0]
        parts.append(piece)
        rest = rest[len(piece):]
        limit = 74
    return "\r\n ".join(parts)


def _fold(line: str, *, name: str) -> str:
    # ASCII keeps the 73-then-72 character fold. Those bytes are locked,
    # including a first SUMMARY line of 81 octets. A non-ASCII value is
    # folded with its property name so every physical line is at most 75 octets
    # and the cut is never inside a multi-byte character.
    escaped = _escape(line)
    if escaped.isascii():
        return f"{name}:{_fold_ascii(escaped)}"
    return _fold_octets(f"{name}:{escaped}")


def _fmt(value: datetime) -> str:
    local = as_utc(value).astimezone(PRICING_TZ)
    return local.strftime("%Y%m%dT%H%M%S")


def todo_ics(todo: Todo, *, prodid: str = "-//Project Car//Shop OS//EN") -> str:
    stamp = datetime.now(PRICING_TZ)
    start = todo.due_at or stamp
    end = as_utc(start) + timedelta(hours=1)
    uid = f"todo-{todo.id}@projectcar.ca"
    description = todo.notes or "Shop OS to-do"
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        f"PRODID:{prodid}",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "BEGIN:VTIMEZONE",
        "TZID:America/Regina",
        "BEGIN:STANDARD",
        "DTSTART:19701101T020000",
        "TZOFFSETFROM:-0600",
        "TZOFFSETTO:-0600",
        "TZNAME:CST",
        "END:STANDARD",
        "END:VTIMEZONE",
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTAMP:{_fmt(stamp)}",
        f"DTSTART;TZID=America/Regina:{_fmt(start)}",
        f"DTEND;TZID=America/Regina:{_fmt(end)}",
        _fold(todo.title, name="SUMMARY"),
        _fold(description, name="DESCRIPTION"),
        "END:VEVENT",
        "END:VCALENDAR",
    ]
    return "\r\n".join(lines) + "\r\n"


def ics_filename(todo_id: UUID) -> str:
    return f"project-car-todo-{todo_id}.ics"
