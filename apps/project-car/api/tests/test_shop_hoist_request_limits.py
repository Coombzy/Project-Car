"""Shop hoist request lists stop loading every row (PC-new-3).

GET /shop-hoist-requests and GET /member/shop-hoist-requests default to 200
rows, newest `created_at` first, with `id` descending as the tie-break.
`limit` is an integer from 1 to 500 (422 outside that, including a non-integer).
The owner status filter and the member's own-row filter still apply before the cap.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from uuid import UUID

from fastapi.testclient import TestClient

from app.models import ActorKind, ShopHoistRequest, ShopHoistRequestStatus
from app.shop_time import as_utc
from tests.conftest import AUTH, create_hoist, create_member, login_member

HEAVY = 205
DEFAULT_LIMIT = 200
_BASE = datetime(2026, 1, 1, tzinfo=timezone.utc)
OWNER_PATH = "/shop-hoist-requests"
MEMBER_PATH = "/member/shop-hoist-requests"


def _notes_newest(count: int, limit: int | None = None, prefix: str = "req") -> list[str]:
    """Newest first. `limit` None means every inserted row of this prefix."""
    take = count if limit is None else min(limit, count)
    newest = count - 1
    oldest_kept = newest - take + 1
    return [f"{prefix}-{index:03d}" for index in range(newest, oldest_kept - 1, -1)]


def _add_row(
    session,
    *,
    member_id: str,
    hoist_id: str,
    index: int,
    prefix: str,
    status: ShopHoistRequestStatus,
    created_offset: int = 0,
    row_id: UUID | None = None,
    created_at: datetime | None = None,
) -> None:
    created = created_at if created_at is not None else _BASE + timedelta(minutes=created_offset + index)
    # Appointment time follows creation, so start_at order is the opposite of newest-first.
    start = as_utc(_BASE + timedelta(hours=created_offset + index))
    row = ShopHoistRequest(
        member_id=UUID(member_id),
        hoist_id=UUID(hoist_id),
        start_at=start,
        end_at=as_utc(start + timedelta(hours=1)),
        status=status,
        token_quote=Decimal("0"),
        notes=f"{prefix}-{index:03d}",
        created_by_kind=ActorKind.HUMAN,
        created_by_id="owner@projectcar.ca",
        created_at=created,
    )
    if row_id is not None:
        row.id = row_id
    session.add(row)


def _seed(
    client: TestClient,
    member_id: str,
    hoist_id: str,
    count: int,
    *,
    prefix: str = "req",
    status: ShopHoistRequestStatus = ShopHoistRequestStatus.PENDING,
    created_offset: int = 0,
) -> None:
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        for index in range(count):
            _add_row(
                session,
                member_id=member_id,
                hoist_id=hoist_id,
                index=index,
                prefix=prefix,
                status=status,
                created_offset=created_offset,
            )
        session.commit()
    finally:
        session.close()


def _notes(response) -> list[str]:
    assert response.status_code == 200, response.text
    return [row["notes"] for row in response.json()]


def test_pc_new_3_default_list_is_newest_200_of_205(client: TestClient) -> None:
    """205 stored rows: both list routes return the 200 newest, newest first."""
    member = create_member(client, name="Ada Reyes", email="hoist-cap@example.com", allocate_tokens=False)
    shop = create_hoist(client, name="Shop", is_shop=True)
    _seed(client, member["id"], shop["id"], HEAVY)
    login_member(client, "hoist-cap@example.com")
    expected = _notes_newest(HEAVY, DEFAULT_LIMIT)

    assert _notes(client.get(OWNER_PATH, headers=AUTH)) == expected
    assert _notes(client.get(MEMBER_PATH)) == expected


def test_pc_new_3_limit_1_and_500_keep_newest_first(client: TestClient) -> None:
    member = create_member(client, name="Ada Reyes", email="hoist-bounds@example.com", allocate_tokens=False)
    shop = create_hoist(client, name="Shop", is_shop=True)
    _seed(client, member["id"], shop["id"], HEAVY)
    login_member(client, "hoist-bounds@example.com")

    for path, headers in ((OWNER_PATH, AUTH), (MEMBER_PATH, None)):
        one = client.get(path, headers=headers, params={"limit": 1})
        wide = client.get(path, headers=headers, params={"limit": 500})
        assert _notes(one) == _notes_newest(HEAVY, 1)
        assert _notes(wide) == _notes_newest(HEAVY)


def test_pc_new_3_five_rows_returns_all_five_newest_first(client: TestClient) -> None:
    member = create_member(client, name="Ada Reyes", email="hoist-light@example.com", allocate_tokens=False)
    shop = create_hoist(client, name="Shop", is_shop=True)
    _seed(client, member["id"], shop["id"], 5)
    login_member(client, "hoist-light@example.com")
    expected = _notes_newest(5)

    assert _notes(client.get(OWNER_PATH, headers=AUTH)) == expected
    assert _notes(client.get(MEMBER_PATH)) == expected


def test_pc_new_3_limit_0_abc_and_501_are_422(client: TestClient) -> None:
    create_member(client, name="Ada Reyes", email="hoist-reject@example.com", allocate_tokens=False)
    login_member(client, "hoist-reject@example.com")
    for limit in (0, "abc", 501):
        for path, headers in ((OWNER_PATH, AUTH), (MEMBER_PATH, None)):
            response = client.get(path, headers=headers, params={"limit": limit})
            assert response.status_code == 422, (path, limit, response.text)
            body = response.json()
            assert body["error"]["code"] == "validation_error"
            locs = [tuple(item["loc"]) for item in body["error"]["details"]]
            assert ("query", "limit") in locs, body


def test_pc_new_3_status_filter_applies_before_the_cap(client: TestClient) -> None:
    """Newer denied rows do not consume the pending page."""
    member = create_member(client, name="Ada Reyes", email="hoist-status@example.com", allocate_tokens=False)
    shop = create_hoist(client, name="Shop", is_shop=True)
    _seed(client, member["id"], shop["id"], HEAVY, prefix="pend")
    _seed(
        client,
        member["id"],
        shop["id"],
        10,
        prefix="deny",
        status=ShopHoistRequestStatus.DENIED,
        created_offset=10_000,
    )

    pending = client.get(OWNER_PATH, headers=AUTH, params={"status": "pending"})
    assert _notes(pending) == _notes_newest(HEAVY, DEFAULT_LIMIT, prefix="pend")

    mixed = _notes(client.get(OWNER_PATH, headers=AUTH))
    assert mixed[:10] == _notes_newest(10, prefix="deny")
    assert mixed[10:] == _notes_newest(HEAVY, DEFAULT_LIMIT - 10, prefix="pend")
    assert len(mixed) == DEFAULT_LIMIT


def test_pc_new_3_member_list_ignores_other_members(client: TestClient) -> None:
    ada = create_member(client, name="Ada Reyes", email="hoist-ada@example.com", allocate_tokens=False)
    sam = create_member(client, name="Sam Okonkwo", email="hoist-sam@example.com", allocate_tokens=False)
    shop = create_hoist(client, name="Shop", is_shop=True)
    _seed(client, ada["id"], shop["id"], HEAVY, prefix="ada")
    _seed(client, sam["id"], shop["id"], 5, prefix="sam", created_offset=10_000)

    login_member(client, "hoist-ada@example.com")
    ada_notes = _notes(client.get(MEMBER_PATH))
    assert ada_notes == _notes_newest(HEAVY, DEFAULT_LIMIT, prefix="ada")
    assert all(not note.startswith("sam-") for note in ada_notes)

    client.post("/auth/member/logout")
    login_member(client, "hoist-sam@example.com")
    assert _notes(client.get(MEMBER_PATH)) == _notes_newest(5, prefix="sam")


def test_pc_new_3_same_created_at_orders_by_id_desc(client: TestClient) -> None:
    """Equal created_at breaks ties by id descending, not by appointment start."""
    member = create_member(client, name="Ada Reyes", email="hoist-tie@example.com", allocate_tokens=False)
    shop = create_hoist(client, name="Shop", is_shop=True)
    tied = datetime(2026, 3, 1, tzinfo=timezone.utc)
    low_id = UUID("00000000-0000-4000-8000-000000000001")
    high_id = UUID("00000000-0000-4000-8000-000000000002")
    newest_id = UUID("00000000-0000-4000-8000-000000000000")
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        _add_row(
            session,
            member_id=member["id"],
            hoist_id=shop["id"],
            index=0,
            prefix="low",
            status=ShopHoistRequestStatus.PENDING,
            row_id=low_id,
            created_at=tied,
        )
        _add_row(
            session,
            member_id=member["id"],
            hoist_id=shop["id"],
            index=1,
            prefix="high",
            status=ShopHoistRequestStatus.PENDING,
            row_id=high_id,
            created_at=tied,
        )
        _add_row(
            session,
            member_id=member["id"],
            hoist_id=shop["id"],
            index=2,
            prefix="new",
            status=ShopHoistRequestStatus.PENDING,
            row_id=newest_id,
            created_at=tied + timedelta(minutes=1),
        )
        session.commit()
    finally:
        session.close()

    listed = client.get(OWNER_PATH, headers=AUTH)
    assert listed.status_code == 200, listed.text
    assert [row["id"] for row in listed.json()] == [str(newest_id), str(high_id), str(low_id)]
