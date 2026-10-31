"""Client address for the login and waitlist caps.

`CLIENT_IP_HEADER` is used only when the TCP peer is listed in
`TRUSTED_PROXIES`. The supported production header is `CF-Connecting-IP`.
`X-Forwarded-For` is refused at startup. `X-Shop-Client-IP` is a separate
hop: it counts only when `X-Shop-Proxy-Secret` matches `SHOP_PROXY_SECRET`.
A value is one IP address, or it is not used.
"""

from __future__ import annotations

import ipaddress

from fastapi import Request

from app.auth import secrets_equal
from app.config import get_settings

_SHOP_CLIENT_IP = "x-shop-client-ip"
_SHOP_PROXY_SECRET = "x-shop-proxy-secret"


def client_ip(request: Request, header_name: str) -> str:
    """Address the in-process caps key on.

    A matching proxy secret wins, from any peer. Otherwise the configured
    header is used only for a trusted peer. An empty name, a missing header,
    an untrusted peer, or a value that is not one IP returns the TCP peer,
    including the historical ``unknown`` fallback.
    """
    settings = get_settings()
    proxied = _proxy_secret_ip(request, settings.shop_proxy_secret)
    if proxied is not None:
        return proxied
    peer = _peer_host(request)
    if not _peer_is_trusted(peer, settings.trusted_proxies):
        return peer
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


def _proxy_secret_ip(request: Request, secret: str) -> str | None:
    if not secret:
        return None
    presented = request.headers.get(_SHOP_PROXY_SECRET)
    if presented is None or not secrets_equal(presented, secret):
        return None
    return _one_ip(request.headers.get(_SHOP_CLIENT_IP) or "")


def _peer_is_trusted(peer: str, trusted_proxies: str) -> bool:
    allowed = [item.strip().strip("[]") for item in trusted_proxies.split(",") if item.strip()]
    if peer in allowed:
        return True
    try:
        peer_ip = ipaddress.ip_address(peer)
    except ValueError:
        return False
    for item in allowed:
        try:
            if ipaddress.ip_address(item) == peer_ip:
                return True
        except ValueError:
            continue
    return False


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
