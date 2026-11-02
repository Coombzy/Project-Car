"""HTTP client that records API call steps."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class ApiClient:
    """Thin wrapper around an injectable ``request`` callable.

    ``request(method, path, json=None, headers=None) -> (status, body)`` is
    called with ``headers={'Authorization': 'Bearer '+ai_bearer}`` on every
    call.  Each step is recorded as ``{'method', 'path', 'status'}`` (never a
    header or bearer token) in ``self.steps``.
    """

    def __init__(
        self,
        request: Callable[..., tuple[int, Any]],
        ai_bearer: str,
    ) -> None:
        self.request = request
        self.ai_bearer = ai_bearer
        self.steps: list[dict[str, Any]] = []

    def call(
        self,
        method: str,
        path: str,
        json: dict[str, Any] | list[Any] | None = None,
    ) -> tuple[int, Any]:
        headers = {"Authorization": "Bearer " + self.ai_bearer}
        status, body = self.request(method, path, json=json, headers=headers)
        self.steps.append({"method": method, "path": path, "status": status})
        return status, body
