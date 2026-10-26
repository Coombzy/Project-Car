"""Client address for the login and waitlist caps.

The header name comes from settings (`CLIENT_IP_HEADER`). Nothing here
names a proxy header. A value is one IP address, or it is not used.
"""

from __future__ import annotations

import ipaddress

from fastapi import Request


def client_ip(request: Request, header_name: str) -> str:
    """Address the in-process caps key on.

    When `header_name` is set and that header carries one IP, return that
    address. An empty name, a missing header, or a value that is not one IP
    returns the TCP peer, including the historical ``unknown`` fallback.
    """
    peer = _peer_host(request)
    name = header_name.strip()
    if not name:
        return peer
    raw = request.headers.get(name)
    if raw is None:
        return peer
    parsed = _one_ip(raw)
    if parsed is None:
        return peer
    return parsed


def _peer_host(request: Request) -> str:
    client = request.client
    if client is None or not client.host:
        return "unknown"
    return client.host


def _one_ip(value: str) -> str | None:
    candidate = value.strip()
    if not candidate:
        return None
    try:
        return str(ipaddress.ip_address(candidate))
    except ValueError:
        return None
