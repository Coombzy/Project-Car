"""Flow result and step-expect helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from aiflow.client import ApiClient
from aiflow.model import Model


@dataclass
class FlowResult:
    """A single step result inside a flow.

    ``name`` is a human-readable label for the step.
    ``passed`` is ``False`` by default and may be set later.
    ``steps`` is an empty list by default and may be appended to.
    """

    name: str
    passed: bool = False
    steps: list = field(default_factory=list)


def expect_step(
    status: int,
    body: dict,
    want_status: int,
    want_code: str | None = None,
) -> bool:
    """Return ``True`` when the response matches the expected status and code.

    ``status`` must equal ``want_status``.  When ``want_code`` is provided,
    ``body['error']['code']`` must equal it.  Returns ``False`` on any
    missing key rather than raising.
    """
    if status != want_status:
        return False
    if want_code is not None:
        try:
            actual_code = body["error"]["code"]
        except (KeyError, TypeError):
            return False
        if actual_code != want_code:
            return False
    return True


def fill_draft_flow(
    model: Model,
    api: ApiClient,
) -> FlowResult:
    """Create a fill draft via the AI model, then attempt acceptance.

    Steps:

    1. Ask the model for a short fill notice text.
    2. POST ``/fill/drafts`` with ``{"body": text}``.  Must return **201**.
    3. POST ``/fill/drafts/{id}/accept`` as the same AI.  Must return **403**
       with ``error.code == "cannot_approve_own_request"``.

    Stops at the first miss and returns ``passed=False``.
    """
    result = FlowResult(name="fill_draft")
    text = model.complete([{"role": "user", "content": "Write a short fill notice"}])
    status, body = api.call("POST", "/fill/drafts", json={"body": text})
    if not expect_step(status, body, 201):
        return result
    draft_id = body["id"]
    status, body = api.call("POST", f"/fill/drafts/{draft_id}/accept")
    if not expect_step(status, body, 403, "cannot_approve_own_request"):
        return result
    result.passed = True
    result.steps = list(api.steps)
    return result
