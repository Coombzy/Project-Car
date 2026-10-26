"""PATCH /hoists/{id} rejects an explicit null on a NOT NULL column.

name, status, is_shop, and location_label are not nullable. Sending null must
answer 422 validation_error and leave the row unchanged. A real rename is 200.
A real duplicate name is 409 duplicate_hoist.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from tests.conftest import AUTH, create_hoist

_HOIST_FIELDS = ("id", "name", "location_label", "status", "is_shop", "created_at", "updated_at")


def _stored(client: TestClient, hoist_id: str) -> dict:
    listed = client.get("/hoists", headers=AUTH)
    assert listed.status_code == 200, listed.text
    return next(row for row in listed.json() if row["id"] == hoist_id)


@pytest.mark.parametrize("field", ["name", "status", "is_shop", "location_label"])
def test_explicit_null_is_422_and_leaves_the_hoist_unchanged(
    client: TestClient, field: str
) -> None:
    hoist = create_hoist(client, name="Bay 1", location_label="North wall")
    before = _stored(client, hoist["id"])

    response = client.patch(
        f"/hoists/{hoist['id']}",
        headers=AUTH,
        json={field: None},
    )

    assert response.status_code == 422, response.text
    assert response.json()["error"]["code"] == "validation_error"
    assert _stored(client, hoist["id"]) == before


def test_rename_answers_200_and_keeps_the_patch_shape(client: TestClient) -> None:
    hoist = create_hoist(client, name="Bay 1", location_label="North wall")

    patched = client.patch(
        f"/hoists/{hoist['id']}",
        headers=AUTH,
        json={"name": "Bay 9"},
    )

    assert patched.status_code == 200, patched.text
    body = patched.json()
    assert set(body) == set(_HOIST_FIELDS)
    assert body["id"] == hoist["id"]
    assert body["name"] == "Bay 9"
    assert body["location_label"] == "North wall"
    assert body["status"] == "available"
    assert body["is_shop"] is False
    stored = _stored(client, hoist["id"])
    assert stored["name"] == "Bay 9"
    assert stored["location_label"] == "North wall"
    assert stored["status"] == "available"
    assert stored["is_shop"] is False


def test_duplicate_name_answers_409_and_leaves_the_hoist_unchanged(client: TestClient) -> None:
    create_hoist(client, name="Bay 1", location_label="North wall")
    second = create_hoist(client, name="Bay 2", location_label="South wall")
    before = _stored(client, second["id"])

    response = client.patch(
        f"/hoists/{second['id']}",
        headers=AUTH,
        json={"name": "Bay 1"},
    )

    assert response.status_code == 409, response.text
    assert response.json()["error"]["code"] == "duplicate_hoist"
    assert _stored(client, second["id"]) == before
    names = {row["name"] for row in client.get("/hoists", headers=AUTH).json()}
    assert names == {"Bay 1", "Bay 2"}
