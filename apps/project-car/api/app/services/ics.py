"""ICS export for a personal to-do due date (America/Regina)."""

from __future__ import annotations

from datetime import datetime, timedelta
from uuid import UUID

from app.models import Todo
from app.shop_time import PRICING_TZ, as_utc


def _fold(line: str) -> str:
    escaped = (
        line.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )
    if len(escaped) <= 73:
        return escaped
    chunks = [escaped[:73]]
    rest = escaped[73:]
    while rest:
        chunks.append(rest[:72])
        rest = rest[72:]
    return "\r\n ".join(chunks)


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
        f"SUMMARY:{_fold(todo.title)}",
        f"DESCRIPTION:{_fold(description)}",
        "END:VEVENT",
        "END:VCALENDAR",
    ]
    return "\r\n".join(lines) + "\r\n"


def ics_filename(todo_id: UUID) -> str:
    return f"project-car-todo-{todo_id}.ics"
