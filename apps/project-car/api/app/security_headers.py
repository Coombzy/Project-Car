"""Headers on every API response. Dev docs skip CSP so Swagger can load."""

from __future__ import annotations

from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.auth import shop_dev_mode

_CSP = "default-src 'none'; frame-ancestors 'none'"
_DOCS_PATHS = {"/docs", "/redoc"}


class SecurityHeadersMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        path = scope.get("path") or ""
        skip_csp = shop_dev_mode() and path in _DOCS_PATHS

        async def send_with_headers(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers["X-Content-Type-Options"] = "nosniff"
                headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
                headers["Referrer-Policy"] = "no-referrer"
                headers["X-Frame-Options"] = "DENY"
                if not skip_csp:
                    headers["Content-Security-Policy"] = _CSP
            await send(message)

        await self.app(scope, receive, send_with_headers)
