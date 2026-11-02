"""Flow result and step-expect helpers."""

from __future__ import annotations

from dataclasses import dataclass, field


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
