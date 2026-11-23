"""Client address for the login and waitlist caps.

`CLIENT_IP_HEADER` counts only when the TCP peer is in `TRUSTED_PROXIES`.
`X-Forwarded-For` never counts. `X-Shop-Client-IP` counts only when
`X-Shop-Proxy-Secret` matches `SHOP_PROXY_SECRET`.
"""

from __future__ import annotations

import hmac
import ipaddress

from fastapi import Request

from app.config import get_settings


def client_ip(request: Request, header_name: str) -> str:
    """Address the in-process caps key on.

    Shop client IP wins when the proxy secret matches. Otherwise the configured
    header counts only for a trusted peer. Anything else is the TCP peer,
    including the historical ``unknown`` fallback.
    """
    peer = _peer_host(request)
    settings = get_settings()
    shop = _shop_client_ip(request, settings.shop_proxy_secret)
    if shop is not None:
        return shop
    if not _peer_trusted(peer, settings.trusted_proxies):
        return peer
    name = header_name.strip()
    if not name or name.lower() == "x-forwarded-for":
        return peer
    parsed = _one_ip(request.headers.get(name) or "")
    return parsed if parsed is not None else peer


def _peer_host(request: Request) -> str:
    client = request.client
    if client is None or not client.host:
        return "unknown"
    return client.host


def _peer_trusted(peer: str, raw: str) -> bool:
    try:
        peer_ip = ipaddress.ip_address(peer)
    except ValueError:
        return False
    for item in raw.split(","):
        text = item.strip().strip("[]")
        try:
            if text and ipaddress.ip_address(text) == peer_ip:
                return True
        except ValueError:
            continue
    return False


def _shop_client_ip(request: Request, secret: str) -> str | None:
    if not secret:
        return None
    presented = request.headers.get("X-Shop-Proxy-Secret")
    if presented is None:
        return None
    left = presented.encode("utf-8")
    right = secret.encode("utf-8")
    if len(left) != len(right) or not hmac.compare_digest(left, right):
        return None
    return _one_ip(request.headers.get("X-Shop-Client-IP") or "")


def _one_ip(value: str) -> str | None:
    candidate = value.strip()
    if not candidate:
        return None
    try:
        return str(ipaddress.ip_address(candidate))
    except ValueError:
        return None
