"""AUD-052 part 1: staff parts requests live at /staff/parts-requests.

POST, approve, and deny on /parts-requests stay aliases of the same handlers.
GET and PATCH /parts-requests stay the member desk.
"""

from collections.abc import Iterable

from fastapi.testclient import TestClient

from app.main import app
from tests.conftest import AUTH, create_member, login_member

STAFF = "/staff/parts-requests"
ALIAS = "/parts-requests"
SKU = "PT-OIL-5W30-012"


def _endpoints() -> dict[tuple[str, str], object]:
    """Mounted routes. FastAPI 0.165 nests included routers; older builds do not."""
    found: dict[tuple[str, str], object] = {}

    def walk(routes: Iterable[object]) -> None:
        for route in routes:
            methods = getattr(route, "methods", None)
            path = getattr(route, "path", None)
            endpoint = getattr(route, "endpoint", None)
            if methods and path and endpoint is not None:
                for method in methods:
                    if method != "HEAD":
                        found[(method, path)] = endpoint
            nested = getattr(route, "routes", None)
            if nested:
                walk(nested)
            original = getattr(route, "original_router", None)
            if original is not None:
                walk(original.routes)

    walk(app.routes)
    return found


def test_staff_parts_operations_are_registered_under_staff_prefix() -> None:
    routes = _endpoints()
    for suffix in ("", "/{request_id}/approve", "/{request_id}/deny"):
        staff = routes[("POST", STAFF + suffix)]
        alias = routes[("POST", ALIAS + suffix)]
        assert alias is staff
    assert routes[("GET", ALIAS)] is not routes[("POST", ALIAS)]
    assert ("PATCH", f"{ALIAS}/{{request_id}}") in routes


def test_post_approve_and_deny_on_staff_paths_and_aliases(client: TestClient) -> None:
    member_id = create_member(client, email="ada@example.com")["id"]
    body = {"member_id": member_id, "sku": SKU, "note": "Need oil"}
    created_ids: list[str] = []
    for path, action, status in (
        (STAFF, "approve", "approved"),
        (STAFF, "deny", "denied"),
        (ALIAS, "approve", "approved"),
        (ALIAS, "deny", "denied"),
    ):
        created = client.post(path, headers=AUTH, json=body)
        assert created.status_code == 201, created.text
        payload = created.json()
        assert payload["status"] == "pending"
        assert payload["sku"] == SKU
        assert payload["member_id"] == member_id
        request_id = payload["id"]
        created_ids.append(request_id)
        decided = client.post(f"{path}/{request_id}/{action}", headers=AUTH)
        assert decided.status_code == 200, decided.text
        decision = decided.json()
        assert decision["status"] == status
        assert decision["request_id"] == request_id
        assert decision["action"] == action
        assert decision["actor_kind"] == "human"
    assert len(set(created_ids)) == 4
    listed = client.get(ALIAS, headers=AUTH)
    assert listed.status_code == 200, listed.text
    assert listed.json() == []


def test_member_get_and_patch_keep_the_member_desk(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com")
    login_member(client, "ada@example.com")
    created = client.post("/member/parts-requests", json={"sku": SKU, "note": "Two jugs"})
    assert created.status_code == 201, created.text
    request_id = created.json()["id"]
    assert created.json()["status"] == "open"
    assert created.json()["member_id"] == ada["id"]

    listed = client.get(ALIAS, headers=AUTH)
    assert listed.status_code == 200, listed.text
    assert [(row["id"], row["status"]) for row in listed.json()] == [(request_id, "open")]

    patched = client.patch(
        f"{ALIAS}/{request_id}",
        headers=AUTH,
        json={"status": "fulfilled"},
    )
    assert patched.status_code == 200, patched.text
    assert patched.json()["status"] == "fulfilled"
    assert patched.json()["sku"] == SKU

    again = client.get(ALIAS, headers=AUTH)
    assert [(row["id"], row["status"], row["member_name"]) for row in again.json()] == [
        (request_id, "fulfilled", "Ada Reyes"),
    ]
