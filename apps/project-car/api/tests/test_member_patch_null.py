"""PATCH /members/{id} must not write an explicit null into a NOT NULL column.

name and status null are 422 validation_error and the row is unchanged.
phone, emergency_contact_name, and waiver_signed_at null still clear and answer 200.
tier_name null stays 400 unknown_tier.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from tests.conftest import AUTH, create_member


def _stored_member(client: TestClient) -> dict:
    created = create_member(
        client,
        email="ada-null@example.com",
        phone="403-555-0100",
        emergency_contact_name="Sam Reyes",
        waiver_signed_at="2026-01-15T18:00:00Z",
    )
    current = client.get(f"/members/{created['id']}", headers=AUTH)
    assert current.status_code == 200, current.text
    body = current.json()
    assert body["name"] == "Ada Reyes"
    assert body["status"] == "active"
    assert body["phone"] == "403-555-0100"
    assert body["emergency_contact_name"] == "Sam Reyes"
    assert body["waiver_signed_at"] is not None
    assert body["tier_name"] == "premium"
    return body


def test_member_patch_null_name_is_422_and_unchanged(client: TestClient) -> None:
    before = _stored_member(client)
    response = client.patch(
        f"/members/{before['id']}",
        headers=AUTH,
        json={"name": None},
    )
    assert response.status_code == 422, response.text
    assert response.json()["error"]["code"] == "validation_error"
    after = client.get(f"/members/{before['id']}", headers=AUTH)
    assert after.status_code == 200, after.text
    assert after.json() == before


def test_member_patch_null_status_is_422_and_unchanged(client: TestClient) -> None:
    before = _stored_member(client)
    response = client.patch(
        f"/members/{before['id']}",
        headers=AUTH,
        json={"status": None},
    )
    assert response.status_code == 422, response.text
    assert response.json()["error"]["code"] == "validation_error"
    after = client.get(f"/members/{before['id']}", headers=AUTH)
    assert after.status_code == 200, after.text
    assert after.json() == before


def test_member_patch_clears_nullable_fields(client: TestClient) -> None:
    before = _stored_member(client)
    cleared = client.patch(
        f"/members/{before['id']}",
        headers=AUTH,
        json={
            "phone": None,
            "emergency_contact_name": None,
            "waiver_signed_at": None,
        },
    )
    assert cleared.status_code == 200, cleared.text
    body = cleared.json()
    assert body["phone"] is None
    assert body["emergency_contact_name"] is None
    assert body["waiver_signed_at"] is None
    assert body["name"] == before["name"]
    assert body["status"] == before["status"]
    assert body["tier_name"] == before["tier_name"]
    stored = client.get(f"/members/{before['id']}", headers=AUTH)
    assert stored.status_code == 200, stored.text
    stored_body = stored.json()
    assert stored_body["phone"] is None
    assert stored_body["emergency_contact_name"] is None
    assert stored_body["waiver_signed_at"] is None
    assert stored_body["name"] == before["name"]
    assert stored_body["status"] == before["status"]


def test_member_patch_null_tier_name_stays_unknown_tier(client: TestClient) -> None:
    before = _stored_member(client)
    response = client.patch(
        f"/members/{before['id']}",
        headers=AUTH,
        json={"tier_name": None},
    )
    assert response.status_code == 400, response.text
    assert response.json()["error"]["code"] == "unknown_tier"
    after = client.get(f"/members/{before['id']}", headers=AUTH)
    assert after.status_code == 200, after.text
    assert after.json() == before
