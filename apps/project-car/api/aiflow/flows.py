"""Flow result and step-expect helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from aiflow.client import ApiClient
from aiflow.model import Model


@dataclass
class FlowResult:
    """Outcome of one flow.

    ``name`` is the flow label. ``passed`` stays False until every expected
    status matches. ``steps`` holds only the calls this flow made.
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


def _created_id(body: Any) -> str | None:
    """Return a 201 body's id, or None when it cannot name the next path."""
    if not isinstance(body, dict):
        return None
    created = body.get("id")
    if isinstance(created, str) and created:
        return created
    return None


def fill_draft_flow(
    model: Model,
    api: ApiClient,
) -> FlowResult:
    """Create a fill draft via the AI model, then attempt acceptance.

    Steps:

    1. Ask the model for a short fill notice text.
    2. POST ``/fill/drafts`` with ``{"body": text}``.  Must return **201**
       and a body ``id``.
    3. POST ``/fill/drafts/{id}/accept`` as the same AI.  Must return **403**
       with ``error.code == "cannot_approve_own_request"``.

    Stops at the first miss with ``passed=False``. The result's ``steps``
    are the calls this flow made, including the miss.
    """
    result = FlowResult(name="fill_draft")
    start = len(api.steps)
    try:
        text = model.complete([{"role": "user", "content": "Write a short fill notice"}])
        status, body = api.call("POST", "/fill/drafts", json={"body": text})
        if not expect_step(status, body, 201):
            return result
        draft_id = _created_id(body)
        if draft_id is None:
            return result
        status, body = api.call("POST", f"/fill/drafts/{draft_id}/accept")
        if not expect_step(status, body, 403, "cannot_approve_own_request"):
            return result
        result.passed = True
        return result
    finally:
        result.steps = list(api.steps[start:])


def shop_hoist_flow(
    model: Model,
    api: ApiClient,
    member_id: str,
    hoist_id: str,
    start_at: str,
    end_at: str,
) -> FlowResult:
    """Create a shop hoist request via the AI model, then attempt approval.

    Steps:

    1. Ask the model for shop hoist request notes.
    2. POST ``/shop-hoist-requests`` with ``member_id``, ``hoist_id``,
       ``start_at``, ``end_at``, and ``notes``.  Must return **201** and a
       body ``id``.
    3. POST ``/shop-hoist-requests/{id}/approve`` as the same AI.
       Must return **403** with ``error.code == "cannot_approve_own_request"``.

    Stops at the first miss with ``passed=False``. The result's ``steps``
    are the calls this flow made, including the miss.
    """
    result = FlowResult(name="shop_hoist")
    start = len(api.steps)
    try:
        notes = model.complete([{"role": "user", "content": "Write shop hoist request notes"}])
        status, body = api.call(
            "POST",
            "/shop-hoist-requests",
            json={
                "member_id": member_id,
                "hoist_id": hoist_id,
                "start_at": start_at,
                "end_at": end_at,
                "notes": notes,
            },
        )
        if not expect_step(status, body, 201):
            return result
        request_id = _created_id(body)
        if request_id is None:
            return result
        status, body = api.call("POST", f"/shop-hoist-requests/{request_id}/approve")
        if not expect_step(status, body, 403, "cannot_approve_own_request"):
            return result
        result.passed = True
        return result
    finally:
        result.steps = list(api.steps[start:])
