from __future__ import annotations

from starlette.types import ASGIApp, Message, Receive, Scope, Send

# Origin kind -> (allow-methods, allow-headers, allow-credentials).
_CRED = ("GET, POST, PATCH, DELETE, OPTIONS, HEAD", "Accept, Content-Type, Authorization", b"true")
_PUBLIC = ("POST, OPTIONS", "Content-Type", None)


class ShopCorsMiddleware:
    """Brochure origins may preflight and POST /waitlist only, never credentialed."""

    def __init__(self, app: ASGIApp, *, public_origins: set[str], credentialed_origins: set[str]) -> None:
        self.app = app
        self.public, self.credentialed = set(public_origins), set(credentialed_origins)

    def _kind(self, scope: Scope, origin: str) -> str | None:
        if origin in self.credentialed:
            return "credentialed"
        waitlist = scope["path"].rstrip("/") == "/waitlist" and scope["method"] in ("OPTIONS", "POST")
        return "public" if waitlist and origin in self.public else None

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        origin = next((value.decode() for key, value in scope.get("headers", []) if key == b"origin"), None)
        kind = self._kind(scope, origin) if scope["type"] == "http" and origin else None
        if kind is None:
            await self.app(scope, receive, send)
            return
        methods, headers, credentials = _CRED if kind == "credentialed" else _PUBLIC
        pairs = [(b"access-control-allow-origin", origin.encode()), (b"vary", b"Origin")]
        if credentials:
            pairs.append((b"access-control-allow-credentials", credentials))
        if scope["method"] == "OPTIONS":
            pairs += [(b"access-control-allow-methods", methods.encode()),
                      (b"access-control-allow-headers", headers.encode())]
        async def send_wrapped(message: Message) -> None:
            if message["type"] == "http.response.start":
                message["headers"] = list(message.get("headers", [])) + pairs
            await send(message)
        if scope["method"] == "OPTIONS":
            await send_wrapped({"type": "http.response.start", "status": 200, "headers": []})
            await send_wrapped({"type": "http.response.body", "body": b""})
            return
        await self.app(scope, receive, send_wrapped)
