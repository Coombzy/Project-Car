"""Tests for the aiflow flows module."""

import json
from datetime import timedelta

from aiflow.client import ApiClient
from aiflow.flows import fill_draft_flow, shop_hoist_flow
from aiflow.model import MockModel
from tests.conftest import create_hoist, create_member, next_hour

AI_SECRET = "dev-ai-secret"
OWNER_SECRET = "dev-owner-secret"


def _live_api(client) -> ApiClient:
    def req(method: str, path: str, json: dict | None = None, headers: dict | None = None) -> tuple[int, dict]:
        resp = client.request(method, str(client.base_url) + path, json=json, headers=headers)
        return resp.status_code, resp.json()

    return ApiClient(req, AI_SECRET)


def _hoist_window(client) -> tuple[dict, dict, str, str]:
    member = create_member(client)
    shop = create_hoist(client, name="Shop", is_shop=True)
    # Requests become bookings, so the span sits on whole shop hours.
    start = next_hour(10)
    end = start + timedelta(hours=1)
    return member, shop, start.isoformat(), end.isoformat()


def _assert_no_secrets(steps: list[dict]) -> None:
    assert steps, "a step record must exist before the secret scan"
    for step in steps:
        rendered = json.dumps(step)
        assert AI_SECRET not in rendered
        assert OWNER_SECRET not in rendered


def test_fill_draft_flow_passes_on_main(client) -> None:
    api = _live_api(client)
    result = fill_draft_flow(MockModel(["Bay 2 is free"]), api)
    assert result.passed is True
    assert [s["status"] for s in result.steps] == [201, 403]
    assert [s["path"] for s in result.steps][0] == "/fill/drafts"
    assert result.steps[1]["path"].endswith("/accept")


def test_shop_hoist_flow_passes_on_main(client) -> None:
    member, shop, start_iso, end_iso = _hoist_window(client)
    api = _live_api(client)
    result = shop_hoist_flow(
        MockModel(["Shop hoist notes here"]),
        api,
        member_id=member["id"],
        hoist_id=shop["id"],
        start_at=start_iso,
        end_at=end_iso,
    )
    assert result.passed is True
    assert [s["status"] for s in result.steps] == [201, 403]
    assert result.steps[0]["path"] == "/shop-hoist-requests"
    assert result.steps[1]["path"].endswith("/approve")


def test_self_accept_allowed_is_reported_failed(client) -> None:
    def req(method: str, path: str, json: dict | None = None, headers: dict | None = None) -> tuple[int, dict]:
        resp = client.request(method, str(client.base_url) + path, json=json, headers=headers)
        if "/accept" in path:
            return 200, {"accepted": True}
        return resp.status_code, resp.json()

    api = ApiClient(req, AI_SECRET)
    result = fill_draft_flow(MockModel(["Bay 2 is free"]), api)
    assert result.passed is False
    named = [step for step in result.steps if "/accept" in step["path"]]
    assert len(named) == 1
    assert named[0]["method"] == "POST"
    assert named[0]["status"] == 200


def test_self_approve_allowed_is_reported_failed() -> None:
    def req(method: str, path: str, json: dict | None = None, headers: dict | None = None) -> tuple[int, dict]:
        if path.endswith("/approve"):
            return 200, {"approved": True}
        return 201, {"id": "req-1"}

    api = ApiClient(req, AI_SECRET)
    result = shop_hoist_flow(
        MockModel(["notes"]),
        api,
        member_id="member-1",
        hoist_id="hoist-1",
        start_at="2026-11-03T10:00:00",
        end_at="2026-11-03T11:00:00",
    )
    assert result.passed is False
    named = [step for step in result.steps if step["path"].endswith("/approve")]
    assert len(named) == 1
    assert named[0]["status"] == 200


def test_fill_draft_create_miss_names_the_step() -> None:
    def req(method: str, path: str, json: dict | None = None, headers: dict | None = None) -> tuple[int, dict]:
        return 500, {"error": {"code": "boom"}}

    api = ApiClient(req, AI_SECRET)
    result = fill_draft_flow(MockModel(["notice"]), api)
    assert result.passed is False
    assert result.steps == [{"method": "POST", "path": "/fill/drafts", "status": 500}]


def test_shop_hoist_create_miss_names_the_step() -> None:
    def req(method: str, path: str, json: dict | None = None, headers: dict | None = None) -> tuple[int, dict]:
        return 400, {"error": {"code": "not_shop_hoist"}}

    api = ApiClient(req, AI_SECRET)
    result = shop_hoist_flow(
        MockModel(["notes"]),
        api,
        member_id="member-1",
        hoist_id="hoist-1",
        start_at="2026-11-03T10:00:00",
        end_at="2026-11-03T11:00:00",
    )
    assert result.passed is False
    assert result.steps == [{"method": "POST", "path": "/shop-hoist-requests", "status": 400}]


def test_fill_draft_201_without_id_is_a_miss() -> None:
    def req(method: str, path: str, json: dict | None = None, headers: dict | None = None) -> tuple[int, dict]:
        return 201, {"body": "notice"}

    api = ApiClient(req, AI_SECRET)
    result = fill_draft_flow(MockModel(["Bay 2 is free"]), api)
    assert result.passed is False
    assert result.steps == [{"method": "POST", "path": "/fill/drafts", "status": 201}]


def test_shop_hoist_201_without_id_is_a_miss() -> None:
    def req(method: str, path: str, json: dict | None = None, headers: dict | None = None) -> tuple[int, dict]:
        return 201, {"notes": "x"}

    api = ApiClient(req, AI_SECRET)
    result = shop_hoist_flow(
        MockModel(["notes"]),
        api,
        member_id="member-1",
        hoist_id="hoist-1",
        start_at="2026-11-03T10:00:00",
        end_at="2026-11-03T11:00:00",
    )
    assert result.passed is False
    assert result.steps == [{"method": "POST", "path": "/shop-hoist-requests", "status": 201}]


def test_later_flow_reports_only_its_own_steps(client) -> None:
    member, shop, start_iso, end_iso = _hoist_window(client)

    def req(method: str, path: str, json: dict | None = None, headers: dict | None = None) -> tuple[int, dict]:
        resp = client.request(method, str(client.base_url) + path, json=json, headers=headers)
        if "/accept" in path:
            return 200, {"accepted": True}
        return resp.status_code, resp.json()

    api = ApiClient(req, AI_SECRET)
    fill = fill_draft_flow(MockModel(["Bay 2 is free"]), api)
    shop_result = shop_hoist_flow(
        MockModel(["Shop hoist notes here"]),
        api,
        member_id=member["id"],
        hoist_id=shop["id"],
        start_at=start_iso,
        end_at=end_iso,
    )
    assert fill.passed is False
    assert shop_result.passed is True
    assert len(shop_result.steps) == 2
    assert all("/fill/drafts" not in step["path"] for step in shop_result.steps)
    assert shop_result.steps[0]["path"] == "/shop-hoist-requests"
    assert shop_result.steps[1]["path"].endswith("/approve")


def test_steps_never_hold_secrets(client) -> None:
    member, shop, start_iso, end_iso = _hoist_window(client)
    api = _live_api(client)
    fill = fill_draft_flow(MockModel(["Bay 2 is free"]), api)
    shop_result = shop_hoist_flow(
        MockModel(["Shop hoist notes here"]),
        api,
        member_id=member["id"],
        hoist_id=shop["id"],
        start_at=start_iso,
        end_at=end_iso,
    )
    assert fill.passed is True
    assert shop_result.passed is True
    _assert_no_secrets(fill.steps)
    _assert_no_secrets(shop_result.steps)
    _assert_no_secrets(api.steps)
