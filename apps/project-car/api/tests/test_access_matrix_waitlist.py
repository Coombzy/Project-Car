"""Route x caller access matrix for the public and Owner waitlist routes.

Backlog R143 / PC-AUD-030 part 1. On this tip:

- POST /waitlist is public. No Owner cookie or bearer token is required.
- GET /waitlist and POST /waitlist/{entry_id}/convert take `_owner: Owner`.

A covered route fails this file when it lets the wrong caller through:
anonymous must not list the waitlist or convert a row, and Owner must be
able to do both. Other route groups are later PRs.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from tests.conftest import AUTH

CONVERT = "/waitlist/{entry_id}/convert"
LIST = "/waitlist"

# caller -> headers. "anonymous" sends no credential at all.
CALLERS = {"anonymous": {}, "owner": AUTH}

# (caller, path, method, ok). ok is whether that caller may reach the handler.
MATRIX = [
    ("anonymous", LIST, "post", True),
    ("owner", LIST, "post", True),
    ("anonymous", LIST, "get", False),
    ("owner", LIST, "get", True),
    ("anonymous", CONVERT, "post", False),
    ("owner", CONVERT, "post", True),
]

# Status that proves the caller got past the auth dependency.
SUCCESS_STATUS = {("post", LIST): 201, ("get", LIST): 200, ("post", CONVERT): 200}

DENIED_STATUSES = (401, 403)


def _case_email(caller: str, method: str, path: str) -> str:
    """One unique waitlist email per case, so creates never collide."""
    slug = "list" if path == LIST else "convert"
    return f"{caller}-{method}-{slug}@example.com"


def _body_for(method: str, path: str, email: str) -> dict | None:
    if path == CONVERT:
        return {"tier_name": "basic"}
    if method == "post":
        return {"name": "Matrix", "email": email}
    return None


def _seed_row(client: TestClient, email: str) -> str:
    """Put one row on the list through the public create route."""
    response = client.post("/waitlist", json={"name": "Matrix", "email": email})
    assert response.status_code == 201, response.text
    return response.json()["id"]


@pytest.mark.parametrize("caller,path,method,ok", MATRIX)
def test_waitlist_access_matrix(
    client: TestClient, caller: str, path: str, method: str, ok: bool
) -> None:
    email = _case_email(caller, method, path)
    target = path
    if "{entry_id}" in path:
        # Convert needs a real row. Seed it through the public route so the
        # case only measures the convert route's own access check.
        target = path.format(entry_id=_seed_row(client, f"seed-{email}"))

    kwargs: dict = {"headers": CALLERS[caller]}
    body = _body_for(method, path, email)
    if body is not None:
        kwargs["json"] = body
    response = getattr(client, method)(target, **kwargs)

    if ok:
        assert response.status_code == SUCCESS_STATUS[(method, path)], response.text
        return

    assert response.status_code in DENIED_STATUSES, response.text
    assert response.json()["error"]["code"] == "unauthorized", response.text
