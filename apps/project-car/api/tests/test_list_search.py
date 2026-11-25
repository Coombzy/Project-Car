"""Owner GET /parts-requests filters by member name/email and status.

On origin/main these query params are ignored, so q returns every row.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from tests.conftest import AUTH, create_member, login_member


def test_q_filters_parts_requests_by_member_name_or_email(client: TestClient) -> None:
    create_member(client, name="Ada Reyes", email="ada-search@example.com")
    create_member(client, name="Casey", email="casey-search@example.com", tier_name="basic")
    login_member(client, "ada-search@example.com")
    ada = client.post("/member/parts-requests", json={"sku": "PT-OIL-5W30-012"})
    assert ada.status_code == 201, ada.text
    login_member(client, "casey-search@example.com")
    casey = client.post("/member/parts-requests", json={"sku": "PT-FLT-001"})
    assert casey.status_code == 201, casey.text

    by_name = client.get("/parts-requests", headers=AUTH, params={"q": "ada"})
    assert by_name.status_code == 200, by_name.text
    assert [row["member_name"] for row in by_name.json()] == ["Ada Reyes"]

    by_email = client.get("/parts-requests", headers=AUTH, params={"q": "CASEY-SEARCH@EXAMPLE.COM"})
    assert by_email.status_code == 200, by_email.text
    assert [row["member_name"] for row in by_email.json()] == ["Casey"]

    none = client.get("/parts-requests", headers=AUTH, params={"q": "nobody-matches"})
    assert none.status_code == 200, none.text
    assert none.json() == []

    blank = client.get("/parts-requests", headers=AUTH, params={"q": "   "})
    assert blank.status_code == 200, blank.text
    assert {row["member_name"] for row in blank.json()} == {"Ada Reyes", "Casey"}


def test_status_filters_open_and_fulfilled_and_rejects_unknown(client: TestClient) -> None:
    create_member(client, name="Ada Reyes", email="ada-status@example.com")
    create_member(client, name="Casey", email="casey-status@example.com", tier_name="basic")
    login_member(client, "ada-status@example.com")
    ada = client.post("/member/parts-requests", json={"sku": "PT-OIL-5W30-012"})
    assert ada.status_code == 201, ada.text
    login_member(client, "casey-status@example.com")
    casey = client.post("/member/parts-requests", json={"sku": "PT-FLT-001"})
    assert casey.status_code == 201, casey.text

    patched = client.patch(
        f"/parts-requests/{ada.json()['id']}",
        headers=AUTH,
        json={"status": "fulfilled"},
    )
    assert patched.status_code == 200, patched.text

    open_rows = client.get("/parts-requests", headers=AUTH, params={"status": "open"})
    assert open_rows.status_code == 200, open_rows.text
    assert [row["member_name"] for row in open_rows.json()] == ["Casey"]
    assert ada.json()["id"] not in {row["id"] for row in open_rows.json()}

    fulfilled = client.get("/parts-requests", headers=AUTH, params={"status": "fulfilled"})
    assert fulfilled.status_code == 200, fulfilled.text
    assert [row["id"] for row in fulfilled.json()] == [ada.json()["id"]]

    nope = client.get("/parts-requests", headers=AUTH, params={"status": "nope"})
    assert nope.status_code == 422, nope.text


def test_parts_request_limit_caps_stay_50_and_200(client: TestClient) -> None:
    create_member(client, name="Ada Reyes", email="ada-limit@example.com")
    login_member(client, "ada-limit@example.com")
    first = client.post("/member/parts-requests", json={"sku": "PT-OIL-5W30-012"})
    second = client.post("/member/parts-requests", json={"sku": "PT-FLT-001"})
    assert first.status_code == 201, first.text
    assert second.status_code == 201, second.text

    limited = client.get("/parts-requests", headers=AUTH, params={"limit": 2})
    assert limited.status_code == 200, limited.text
    assert len(limited.json()) == 2

    too_many = client.get("/parts-requests", headers=AUTH, params={"limit": 201})
    assert too_many.status_code == 422, too_many.text


def test_member_session_is_401_on_owner_parts_requests(client: TestClient) -> None:
    create_member(client, name="Ada Reyes", email="ada-auth@example.com")
    login_member(client, "ada-auth@example.com")
    denied = client.get("/parts-requests")
    assert denied.status_code == 401
