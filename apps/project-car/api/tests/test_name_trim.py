"""Member, hoist, tier, and waitlist names that are only spaces are rejected.

Each required name is 422 when empty after trimming, and a padded value is stored trimmed.
Whitespace-only waitlist creates are not stored, so they do not take an R28 per-IP slot.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from tests.conftest import AUTH, create_hoist, create_member

# Not the default TestClient host, and not the R28 cap test's 203.0.113.28.
_WAITLIST_IP = ("203.0.113.38", 50000)


def _assert_blank_rejected(response, field: str) -> None:
    assert response.status_code == 422, response.text
    body = response.json()
    assert body["error"]["code"] == "validation_error"
    matched = [item for item in body["error"]["details"] if tuple(item["loc"]) == ("body", field)]
    assert matched, body
    assert matched[0]["type"] == "string_too_short", matched


def test_member_create_name_blank_is_422_and_padded_is_trimmed(client: TestClient) -> None:
    blank = client.post(
        "/members",
        headers=AUTH,
        json={"name": "   ", "email": "blank-member@example.com", "tier_name": "basic"},
    )
    _assert_blank_rejected(blank, "name")
    assert client.get("/members", headers=AUTH).json() == []

    created = client.post(
        "/members",
        headers=AUTH,
        json={"name": "  Bay 2  ", "email": "bay-member@example.com", "tier_name": "basic"},
    )
    assert created.status_code == 201, created.text
    assert created.json()["name"] == "Bay 2"

    over = client.post(
        "/members",
        headers=AUTH,
        json={"name": " " + ("x" * 200), "email": "over-member@example.com", "tier_name": "basic"},
    )
    assert over.status_code == 422, over.text
    assert [row["email"] for row in client.get("/members", headers=AUTH).json()] == [
        "bay-member@example.com"
    ]


def test_member_patch_name_blank_is_422_and_padded_is_trimmed(client: TestClient) -> None:
    member = create_member(client, email="ada-patch@example.com")
    blank = client.patch(
        f"/members/{member['id']}",
        headers=AUTH,
        json={"name": "   "},
    )
    _assert_blank_rejected(blank, "name")
    current = client.get(f"/members/{member['id']}", headers=AUTH)
    assert current.status_code == 200, current.text
    assert current.json()["name"] == "Ada Reyes"

    patched = client.patch(
        f"/members/{member['id']}",
        headers=AUTH,
        json={"name": "  Bay 2  "},
    )
    assert patched.status_code == 200, patched.text
    assert patched.json()["name"] == "Bay 2"

    over = client.patch(
        f"/members/{member['id']}",
        headers=AUTH,
        json={"name": " " + ("x" * 200)},
    )
    assert over.status_code == 422, over.text
    assert client.get(f"/members/{member['id']}", headers=AUTH).json()["name"] == "Bay 2"


def test_hoist_create_name_blank_is_422_and_padded_is_trimmed(client: TestClient) -> None:
    blank = client.post(
        "/hoists",
        headers=AUTH,
        json={"name": "   ", "location_label": "South wall"},
    )
    _assert_blank_rejected(blank, "name")
    assert client.get("/hoists", headers=AUTH).json() == []

    created = client.post(
        "/hoists",
        headers=AUTH,
        json={"name": "  Bay 2  ", "location_label": "South wall"},
    )
    assert created.status_code == 201, created.text
    assert created.json()["name"] == "Bay 2"
    assert created.json()["location_label"] == "South wall"

    over = client.post(
        "/hoists",
        headers=AUTH,
        json={"name": " " + ("x" * 120), "location_label": "South wall"},
    )
    assert over.status_code == 422, over.text
    names = [row["name"] for row in client.get("/hoists", headers=AUTH).json()]
    assert names == ["Bay 2"]


def test_hoist_patch_name_blank_is_422_and_padded_is_trimmed(client: TestClient) -> None:
    hoist = create_hoist(client, name="Bay 1")
    blank = client.patch(
        f"/hoists/{hoist['id']}",
        headers=AUTH,
        json={"name": "   "},
    )
    _assert_blank_rejected(blank, "name")
    listed = client.get("/hoists", headers=AUTH)
    row = next(item for item in listed.json() if item["id"] == hoist["id"])
    assert row["name"] == "Bay 1"

    patched = client.patch(
        f"/hoists/{hoist['id']}",
        headers=AUTH,
        json={"name": "  Bay 2  "},
    )
    assert patched.status_code == 200, patched.text
    assert patched.json()["name"] == "Bay 2"

    over = client.patch(
        f"/hoists/{hoist['id']}",
        headers=AUTH,
        json={"name": " " + ("x" * 120)},
    )
    assert over.status_code == 422, over.text
    assert client.get("/hoists", headers=AUTH).json()[0]["name"] == "Bay 2"


def test_tier_create_display_name_blank_is_422_and_padded_is_trimmed(client: TestClient) -> None:
    payload = {
        "name": "weekend",
        "price": "40.00",
        "included_tokens": 100,
        "booking_window_days": 7,
        "max_simultaneous_bookings": 1,
    }
    blank = client.post("/tiers", headers=AUTH, json={**payload, "display_name": "   "})
    _assert_blank_rejected(blank, "display_name")
    names = {row["name"] for row in client.get("/tiers", headers=AUTH).json()}
    assert names == {"basic", "premium"}

    created = client.post("/tiers", headers=AUTH, json={**payload, "display_name": "  Bay 2  "})
    assert created.status_code == 201, created.text
    assert created.json()["name"] == "weekend"
    assert created.json()["display_name"] == "Bay 2"

    over = client.post(
        "/tiers",
        headers=AUTH,
        json={**payload, "name": "overflow", "display_name": " " + ("x" * 120)},
    )
    assert over.status_code == 422, over.text
    names = {row["name"] for row in client.get("/tiers", headers=AUTH).json()}
    assert names == {"basic", "premium", "weekend"}


def test_tier_patch_display_name_blank_is_422_and_padded_is_trimmed(client: TestClient) -> None:
    blank = client.patch("/tiers/basic", headers=AUTH, json={"display_name": "   "})
    _assert_blank_rejected(blank, "display_name")
    basic = next(row for row in client.get("/tiers", headers=AUTH).json() if row["name"] == "basic")
    assert basic["display_name"] == "Basic"
    assert basic["included_tokens"] == 1000

    patched = client.patch("/tiers/basic", headers=AUTH, json={"display_name": "  Bay 2  "})
    assert patched.status_code == 200, patched.text
    assert patched.json()["display_name"] == "Bay 2"
    assert patched.json()["included_tokens"] == 1000

    over = client.patch(
        "/tiers/basic",
        headers=AUTH,
        json={"display_name": " " + ("x" * 120)},
    )
    assert over.status_code == 422, over.text
    basic = next(row for row in client.get("/tiers", headers=AUTH).json() if row["name"] == "basic")
    assert basic["display_name"] == "Bay 2"


def test_waitlist_name_blank_is_422_and_padded_is_trimmed(client: TestClient) -> None:
    """Eight blank names must not fill the per-IP cap. The next real name is stored trimmed."""
    previous = client._transport.client
    client._transport.client = _WAITLIST_IP
    try:
        for index in range(8):
            blank = client.post(
                "/waitlist",
                json={"name": "   ", "email": f"blank-wait-{index}@example.com"},
            )
            _assert_blank_rejected(blank, "name")
        assert client.get("/waitlist", headers=AUTH).json() == []

        created = client.post(
            "/waitlist",
            json={"name": "  Bay 2  ", "email": "bay-wait@example.com"},
        )
        assert created.status_code == 201, created.text
        assert created.json()["name"] == "Bay 2"

        over = client.post(
            "/waitlist",
            json={"name": " " + ("x" * 200), "email": "over-wait@example.com"},
        )
        assert over.status_code == 422, over.text
        stored = client.get("/waitlist", headers=AUTH).json()
        assert [row["email"] for row in stored] == ["bay-wait@example.com"]
        assert stored[0]["name"] == "Bay 2"
    finally:
        client._transport.client = previous
