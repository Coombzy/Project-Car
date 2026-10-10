"""Shop hoist requests. Pending is not a booking and does not move tokens."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

from fastapi.testclient import TestClient

from app.shop_time import shop_now
from tests.conftest import AUTH, create_hoist, create_member, login_member

REPO = Path(__file__).resolve().parents[4]


def _window(hours_from_now: int, length_hours: float = 1) -> tuple[str, str]:
    start = shop_now() + timedelta(hours=hours_from_now)
    end = start + timedelta(hours=length_hours)
    return start.isoformat(), end.isoformat()


def _dec(value) -> Decimal:
    return Decimal(str(value))


def _balance(client: TestClient, member_id: str) -> Decimal:
    response = client.get(f"/members/{member_id}", headers=AUTH)
    assert response.status_code == 200, response.text
    return _dec(response.json()["token_balance"])


def _ledger(client: TestClient, member_id: str) -> list[dict]:
    response = client.get(f"/members/{member_id}/tokens", headers=AUTH)
    assert response.status_code == 200, response.text
    return response.json()


def _booking_ids(client: TestClient) -> list[str]:
    response = client.get("/bookings", headers=AUTH)
    assert response.status_code == 200, response.text
    return [row["id"] for row in response.json()]


def test_member_request_is_pending_and_does_not_debit(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com")
    shop = create_hoist(client, name="Shop", location_label="Internal", is_shop=True)
    start, end = _window(8)
    login_member(client, "ada@example.com")
    balance = _dec(client.get("/member/me").json()["token_balance"])
    ledger_before = client.get("/member/tokens").json()

    created = client.post(
        "/member/shop-hoist-requests",
        json={"hoist_id": shop["id"], "start_at": start, "end_at": end, "notes": "Need the hoist"},
    )
    assert created.status_code == 201, created.text
    body = created.json()
    assert body["record"] == "shop_hoist_request"
    assert body["status"] == "pending"
    assert body["member_id"] == member["id"]
    assert body["hoist_id"] == shop["id"]
    assert _dec(body["token_quote"]) > 0
    assert _dec(client.get("/member/me").json()["token_balance"]) == balance
    assert client.get("/member/tokens").json() == ledger_before
    assert client.get("/member/bookings").json() == []

    listed = client.get("/member/shop-hoist-requests")
    assert listed.status_code == 200
    assert [row["id"] for row in listed.json()] == [body["id"]]
    assert listed.json()[0]["status"] == "pending"

    owner_view = client.get("/bookings", headers=AUTH, params={"hoist_id": shop["id"]})
    assert owner_view.status_code == 200
    assert owner_view.json() == []


def test_two_pending_requests_do_not_hold_the_hour(client: TestClient) -> None:
    ada = create_member(client, name="Ada Reyes", email="ada@example.com")
    sam = create_member(client, name="Sam Okonkwo", email="sam@example.com")
    shop = create_hoist(client, name="Shop", is_shop=True)
    start, end = _window(6)

    login_member(client, "ada@example.com")
    first = client.post(
        "/member/shop-hoist-requests",
        json={"hoist_id": shop["id"], "start_at": start, "end_at": end},
    )
    assert first.status_code == 201, first.text

    client.post("/auth/member/logout")
    login_member(client, "sam@example.com")
    second = client.post(
        "/member/shop-hoist-requests",
        json={"hoist_id": shop["id"], "start_at": start, "end_at": end},
    )
    assert second.status_code == 201, second.text
    assert second.json()["id"] != first.json()["id"]
    assert second.json()["status"] == "pending"

    bookings = client.get("/bookings", headers=AUTH, params={"hoist_id": shop["id"]})
    assert bookings.json() == []
    requests = client.get("/shop-hoist-requests", headers=AUTH)
    assert requests.status_code == 200
    assert {row["member_id"] for row in requests.json()} == {ada["id"], sam["id"]}
    assert all(row["status"] == "pending" for row in requests.json())
    assert _balance(client, ada["id"]) == Decimal("1500")
    assert _balance(client, sam["id"]) == Decimal("1500")


def test_bays_stay_a_direct_booking(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com")
    bay = create_hoist(client, name="Bay 1")
    create_hoist(client, name="Shop", is_shop=True)
    start, end = _window(5)
    login_member(client, "ada@example.com")
    balance = _dec(client.get("/member/me").json()["token_balance"])

    booked = client.post(
        "/member/bookings",
        json={"hoist_id": bay["id"], "start_at": start, "end_at": end},
    )
    assert booked.status_code == 201, booked.text
    body = booked.json()
    assert body["kind"] == "customer"
    assert body["status"] == "pending"
    assert "record" not in body
    assert _dec(client.get("/member/me").json()["token_balance"]) == balance - _dec(body["reserved_tokens"])
    assert client.get("/member/bookings").json()[0]["id"] == body["id"]

    hoists = client.get("/member/hoists")
    assert {row["name"] for row in hoists.json()} == {"Bay 1"}
    shop = client.get("/member/shop-hoist")
    assert shop.status_code == 200
    assert shop.json()["name"] == "Shop"
    assert shop.json()["is_shop"] is True


def test_request_is_not_auto_approved(client: TestClient) -> None:
    create_member(client, email="ada@example.com")
    shop = create_hoist(client, name="Shop", is_shop=True)
    start, end = _window(9)
    login_member(client, "ada@example.com")
    created = client.post(
        "/member/shop-hoist-requests",
        json={"hoist_id": shop["id"], "start_at": start, "end_at": end},
    )
    assert created.status_code == 201, created.text
    request_id = created.json()["id"]
    assert created.json()["status"] == "pending"

    confirm = client.post(f"/member/bookings/{request_id}/confirm")
    assert confirm.status_code == 404
    still = client.get("/member/shop-hoist-requests")
    assert still.json()[0]["status"] == "pending"
    assert client.get("/bookings", headers=AUTH, params={"hoist_id": shop["id"]}).json() == []


def test_owner_customer_post_is_a_request(client: TestClient) -> None:
    member = create_member(client)
    shop = create_hoist(client, name="Shop", is_shop=True)
    start, end = _window(7)
    balance = _balance(client, member["id"])
    created = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": shop["id"],
            "start_at": start,
            "end_at": end,
        },
    )
    assert created.status_code == 201, created.text
    assert created.json()["record"] == "shop_hoist_request"
    assert created.json()["status"] == "pending"
    assert created.json()["created_by_kind"] == "human"
    assert _balance(client, member["id"]) == balance
    assert "shop_hoist_owner_only" not in created.text


def test_shop_work_on_the_shop_hoist_stays_a_booking(client: TestClient) -> None:
    shop = create_hoist(client, name="Shop", is_shop=True)
    start, end = _window(4)
    created = client.post(
        "/bookings",
        headers=AUTH,
        json={"kind": "shop", "hoist_id": shop["id"], "start_at": start, "end_at": end},
    )
    assert created.status_code == 201, created.text
    assert created.json()["kind"] == "shop"
    assert _dec(created.json()["reserved_tokens"]) == Decimal("0")


def test_shop_hoist_approval_respects_pending_hold_and_simultaneous_cap(client: TestClient) -> None:
    """Pending bookings hold the shop hour, and the tier cap applies at approval."""
    ada = create_member(client, name="Ada Reyes", email="ada@example.com", tier_name="premium")
    sam = create_member(client, name="Sam Okonkwo", email="sam@example.com", tier_name="basic")
    shop = create_hoist(client, name="Shop", is_shop=True)
    bay = create_hoist(client, name="Bay 1")
    held_start, held_end = _window(8)
    bay_start, bay_end = _window(30)
    free_start, free_end = _window(48)

    shop_work = client.post(
        "/bookings",
        headers=AUTH,
        json={"kind": "shop", "hoist_id": shop["id"], "start_at": held_start, "end_at": held_end},
    )
    assert shop_work.status_code == 201, shop_work.text
    assert shop_work.json()["status"] == "pending"
    assert shop_work.json()["kind"] == "shop"

    login_member(client, "ada@example.com")
    overlapping = client.post(
        "/member/shop-hoist-requests",
        json={"hoist_id": shop["id"], "start_at": held_start, "end_at": held_end},
    )
    assert overlapping.status_code == 201, overlapping.text

    held = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": sam["id"],
            "hoist_id": bay["id"],
            "start_at": bay_start,
            "end_at": bay_end,
        },
    )
    assert held.status_code == 201, held.text
    assert held.json()["status"] == "pending"

    client.post("/auth/member/logout")
    login_member(client, "sam@example.com")
    capped_request = client.post(
        "/member/shop-hoist-requests",
        json={"hoist_id": shop["id"], "start_at": free_start, "end_at": free_end},
    )
    assert capped_request.status_code == 201, capped_request.text

    ada_ledger = _ledger(client, ada["id"])
    ada_balance = _balance(client, ada["id"])
    bookings_before = _booking_ids(client)

    overlap = client.post(f"/shop-hoist-requests/{overlapping.json()['id']}/approve", headers=AUTH)
    cap = client.post(f"/shop-hoist-requests/{capped_request.json()['id']}/approve", headers=AUTH)

    assert overlap.status_code == 409, overlap.text
    assert overlap.json()["error"]["code"] == "hoist_overlap"
    assert _ledger(client, ada["id"]) == ada_ledger
    assert _balance(client, ada["id"]) == ada_balance
    shop_rows = client.get("/bookings", headers=AUTH, params={"hoist_id": shop["id"]}).json()
    assert [row["id"] for row in shop_rows] == [shop_work.json()["id"]]

    assert cap.status_code == 400, cap.text
    assert cap.json()["error"]["code"] == "max_simultaneous_bookings"
    assert _booking_ids(client) == bookings_before
    still = client.get(
        "/shop-hoist-requests",
        headers=AUTH,
        params={"status": "pending"},
    ).json()
    assert {row["id"] for row in still} == {overlapping.json()["id"], capped_request.json()["id"]}
    assert all(row["booking_id"] is None for row in still)


def test_past_shop_hoist_start_is_rejected(client: TestClient) -> None:
    """A shop-hoist request whose start is already past is not stored and does not move tokens."""
    member = create_member(client, email="ada@example.com")
    shop = create_hoist(client, name="Shop", is_shop=True)
    past = datetime(2020, 6, 2, 16, 0, tzinfo=timezone.utc)
    past_end = past + timedelta(hours=1)
    balance = _balance(client, member["id"])
    ledger = _ledger(client, member["id"])

    login_member(client, "ada@example.com")
    member_request = client.post(
        "/member/shop-hoist-requests",
        json={
            "hoist_id": shop["id"],
            "start_at": past.isoformat(),
            "end_at": past_end.isoformat(),
        },
    )
    assert member_request.status_code == 400, member_request.text
    assert member_request.json()["error"]["code"] == "start_in_past"
    assert client.get("/member/shop-hoist-requests").json() == []
    assert client.get("/member/bookings").json() == []

    owner_request = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": shop["id"],
            "start_at": past.isoformat(),
            "end_at": past_end.isoformat(),
        },
    )
    assert owner_request.status_code == 400, owner_request.text
    assert owner_request.json()["error"]["code"] == "start_in_past"
    listed = client.get("/shop-hoist-requests", headers=AUTH)
    assert listed.status_code == 200, listed.text
    assert listed.json() == []
    assert client.get("/bookings", headers=AUTH).json() == []
    assert _balance(client, member["id"]) == balance
    assert _ledger(client, member["id"]) == ledger


def test_public_pages_do_not_say_the_shop_is_open() -> None:
    roots = [REPO / "apps" / "website" / "html", REPO / "apps" / "project-car" / "web"]
    hits: list[str] = []
    for root in roots:
        for path in root.rglob("*"):
            if path.suffix not in {".html", ".tsx", ".md"}:
                continue
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                lowered = line.lower()
                if "shop is open" not in lowered:
                    continue
                if any(token in lowered for token in ("not", "never", "don't", "do not", "isn't")):
                    continue
                hits.append(f"{path.relative_to(REPO)}:{number}")
    assert hits == []
