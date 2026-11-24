from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.config import get_settings

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Referrer-Policy": "no-referrer",
    "X-Frame-Options": "DENY",
    "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
}

DEV_DOCS_PATHS = {"/docs", "/redoc"}


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add the five shop security headers to every response.

    CSP is skipped on the dev docs so Swagger UI can load its own assets.
    The flag is Settings.shop_dev_mode, which reads the environment and .env.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        dev_docs = get_settings().shop_dev_mode and request.url.path in DEV_DOCS_PATHS
        for name, value in SECURITY_HEADERS.items():
            if dev_docs and name == "Content-Security-Policy":
                continue
            response.headers.setdefault(name, value)
        return response
