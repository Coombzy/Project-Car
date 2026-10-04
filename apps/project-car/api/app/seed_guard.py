"""Refuse the demo Owner login unless the database host is loopback."""

from __future__ import annotations

import ipaddress

from sqlalchemy.engine import make_url
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import Session

from app.config import DEMO_OWNER_EMAIL, DEMO_OWNER_PASSWORD


class DemoOwnerSeedRefused(RuntimeError):
    """The demo Owner pair was aimed at a database host that is not loopback."""


def database_host(url: str) -> str | None:
    return _host_from_url(make_url(url))


def session_database_host(session: Session) -> str | None:
    bind = session.get_bind()
    url = getattr(bind, "url", None)
    if url is None:
        return None
    if isinstance(url, str):
        return database_host(url)
    return _host_from_url(url)


def is_loopback_host(host: str | None) -> bool:
    """True when there is no TCP host (SQLite or a local socket) or the host is loopback."""
    if host is None:
        return True
    name = host.strip().lower()
    if name.startswith("[") and name.endswith("]") and len(name) > 2:
        name = name[1:-1]
    if name == "localhost":
        return True
    try:
        address = ipaddress.ip_address(name)
    except ValueError:
        return False
    return bool(address.is_loopback)


def refuse_demo_owner_off_loopback(host: str | None, email: str, password: str) -> None:
    if is_loopback_host(host) or not _is_demo_owner_pair(email, password):
        return
    shown = host if host else "(none)"
    raise DemoOwnerSeedRefused(
        f"Refusing to seed: demo owner credentials are loopback-only (database host {shown})."
    )


def _is_demo_owner_pair(email: str, password: str) -> bool:
    return email.strip().lower() == DEMO_OWNER_EMAIL and password == DEMO_OWNER_PASSWORD


def _host_from_url(url: URL) -> str | None:
    if url.host:
        return url.host
    query_host = url.query.get("host")
    if isinstance(query_host, (list, tuple)):
        query_host = query_host[0] if query_host else None
    if not isinstance(query_host, str):
        return None
    name = query_host.strip()
    if not name or name.startswith("/"):
        return None
    return name
