"""Client address for the login and waitlist caps.

The header name comes from settings (`CLIENT_IP_HEADER`). Nothing here
names a proxy header. A value is one IP address, or it is not used.
"""

from __future__ import annotations

import hmac
import ipaddress

from fastapi import Request

from app.config import get_settings


def client_ip(request: Request, header_name: str) -> str:
    """Address the in-process caps key on.

    When `header_name` is set and that header carries one IP, return that
    address. An empty name, a missing header, or a value that is not one IP
    returns the TCP peer, including the historical ``unknown`` fallback.
    """
    peer = _peer_host(request)
    settings = get_settings()
    shop = _shop_client_ip(request, settings.shop_proxy_secret)
    if shop is not None:
        return shop
    name = header_name.strip()
    if not name or name.lower() == "x-forwarded-for" or not _peer_trusted(peer, settings.trusted_proxies):
        return peer
    raw = request.headers.get(name)
    if raw is None:
        return peer
    parsed = _one_ip(raw)
    return peer if parsed is None else parsed


def _shop_client_ip(request: Request, secret: str) -> str | None:
    if not secret:
        return None
    presented = request.headers.get("X-Shop-Proxy-Secret")
    if presented is None:
        return None
    if not hmac.compare_digest(presented.encode("utf-8"), secret.encode("utf-8")):
        return None
    return _one_ip(request.headers.get("X-Shop-Client-IP") or "")


def _peer_trusted(peer: str, trusted: str) -> bool:
    return peer in {item.strip() for item in trusted.split(",") if item.strip()}


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
