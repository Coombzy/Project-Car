"""Model adapter for the AI flow test bot.

Stdlib ``urllib`` only. ``OpenAICompatModel`` POSTs
``{model, messages, temperature: 0}`` to ``<base_url>/v1/chat/completions``.
``base_url`` is an origin, for example ``http://127.0.0.1:11434`` (Ollama) or
a cloud host. A trailing slash is stripped so the path is not ``//v1``.

``transport(url, body, headers, timeout) -> (status, body)`` is injectable.
Tests pass a fake and never open a socket. The default calls
``urllib.request.urlopen``.

A non-200, or a 200 body with no ``choices``, raises ``ModelError``. The
message includes the status and never the API key or the response body.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Protocol
from urllib import error, request

Transport = Callable[[str, bytes, dict[str, str], float], tuple[int, bytes]]


class ModelError(Exception):
    """The model HTTP call failed. ``status`` is the response status."""

    def __init__(self, status: int, detail: str) -> None:
        self.status = status
        super().__init__(f"status {status}: {detail}")


class Model(Protocol):
    def complete(self, messages: list[dict]) -> str: ...


class MockModel:
    """Scripted replies, in order.

    ``prompts`` is every ``messages`` list passed to ``complete``, including
    a call that finds no reply left. The caller's lists are not stored.
    """

    def __init__(self, replies: list[str]) -> None:
        self._replies = list(replies)
        self.prompts: list[list[dict]] = []

    def complete(self, messages: list[dict]) -> str:
        self.prompts.append([dict(message) for message in messages])
        if not self._replies:
            raise IndexError("MockModel ran out of scripted replies")
        return self._replies.pop(0)


def _urllib_transport(
    url: str,
    body: bytes,
    headers: dict[str, str],
    timeout: float,
) -> tuple[int, bytes]:
    req = request.Request(url, data=body, headers=headers, method="POST")
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            return int(resp.status), resp.read()
    except error.HTTPError as exc:
        return int(exc.code), exc.read()


def _message_content(status: int, raw: bytes) -> str:
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        raise ModelError(status, "response is not JSON") from None
    choices = parsed.get("choices") if isinstance(parsed, dict) else None
    if not isinstance(choices, list) or not choices:
        raise ModelError(status, "response has no choices")
    first = choices[0]
    message = first.get("message") if isinstance(first, dict) else None
    content = message.get("content") if isinstance(message, dict) else None
    if not isinstance(content, str):
        raise ModelError(status, "response has no message content")
    return content


class OpenAICompatModel:
    """POST chat completions to an OpenAI-compatible endpoint.

    ``api_key`` is optional. When it is set it is sent only as
    ``Authorization: Bearer``. ``timeout`` defaults to 30 seconds.
    """

    def __init__(
        self,
        base_url: str,
        model: str,
        api_key: str | None = None,
        transport: Transport | None = None,
        timeout: float = 30,
    ) -> None:
        self.base_url = base_url
        self.model = model
        self._api_key = api_key
        self._transport: Transport = (
            _urllib_transport if transport is None else transport
        )
        self.timeout = timeout

    def complete(self, messages: list[dict]) -> str:
        url = self.base_url.rstrip("/") + "/v1/chat/completions"
        body = json.dumps(
            {"model": self.model, "messages": messages, "temperature": 0}
        ).encode()
        headers = {"Content-Type": "application/json"}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"
        status, raw = self._transport(url, body, headers, self.timeout)
        if status != 200:
            raise ModelError(status, "model response was not OK")
        return _message_content(status, raw)
