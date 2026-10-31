"""Split CORS: brochure waitlist has no credentials; the shop UI does."""

from __future__ import annotations

from starlette.datastructures import MutableHeaders
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.config import get_settings

_CREDENTIALED_METHODS = "GET, POST, PATCH, DELETE, OPTIONS, HEAD"
_CREDENTIALED_HEADERS = "Accept, Content-Type, Authorization"
_PUBLIC_METHODS = "POST, OPTIONS"
_PUBLIC_HEADERS = "Content-Type"


class ShopCorsMiddleware:
    """Brochure origins may preflight and POST /waitlist. Nothing else.

    Credentialed origins may call the API with cookies. An origin on both
    lists is credentialed. Other origins get no CORS headers.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        request = Request(scope)
        origin = request.headers.get("origin")
        if not origin:
            await self.app(scope, receive, send)
            return
        kind = get_settings().cors_origin_kind(origin)
        path = request.url.path
        method = request.method.upper()
        if method == "OPTIONS" and kind == "public" and path == "/waitlist":
            await _preflight(scope, receive, send, origin, public=True)
            return
        if method == "OPTIONS" and kind == "credentialed":
            await _preflight(scope, receive, send, origin, public=False)
            return

        async def send_with_cors(message: Message) -> None:
            if message["type"] == "http.response.start" and _allows(kind, path, method):
                headers = MutableHeaders(scope=message)
                headers["Access-Control-Allow-Origin"] = origin
                headers.add_vary_header("Origin")
                if kind == "credentialed":
                    headers["Access-Control-Allow-Credentials"] = "true"
            await send(message)

        await self.app(scope, receive, send_with_cors)


def _allows(kind: str | None, path: str, method: str) -> bool:
    if kind == "credentialed":
        return True
    return kind == "public" and path == "/waitlist" and method == "POST"


async def _preflight(
    scope: Scope,
    receive: Receive,
    send: Send,
    origin: str,
    *,
    public: bool,
) -> None:
    response = Response(status_code=200)
    response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Vary"] = "Origin"
    if public:
        response.headers["Access-Control-Allow-Methods"] = _PUBLIC_METHODS
        response.headers["Access-Control-Allow-Headers"] = _PUBLIC_HEADERS
    else:
        response.headers["Access-Control-Allow-Methods"] = _CREDENTIALED_METHODS
        response.headers["Access-Control-Allow-Headers"] = _CREDENTIALED_HEADERS
        response.headers["Access-Control-Allow-Credentials"] = "true"
    await response(scope, receive, send)
