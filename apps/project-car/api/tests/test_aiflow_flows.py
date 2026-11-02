"""Tests for the aiflow flows module."""

from datetime import timedelta

from aiflow.client import ApiClient
from aiflow.flows import fill_draft_flow, shop_hoist_flow
from aiflow.model import MockModel
from app.shop_time import shop_now
from tests.conftest import AUTH, create_hoist, create_member


def test_fill_draft_flow_passes_on_main(client) -> None:
    def req(method: str, path: str, json: dict | None = None, headers: dict | None = None) -> tuple[int, dict]:
        resp = client.request(method, str(client.base_url) + path, json=json, headers=headers)
        return resp.status_code, resp.json()

    api = ApiClient(req, "dev-ai-secret")
    model = MockModel(["Bay 2 is free"])
    result = fill_draft_flow(model, api)
    assert result.passed is True
    assert [s["status"] for s in result.steps] == [201, 403]


def test_shop_hoist_flow_passes_on_main(client) -> None:
    member = create_member(client)
    shop = create_hoist(client, name="Shop", is_shop=True)
    start = shop_now() + timedelta(hours=10)
    end = start + timedelta(hours=1)
    start_iso, end_iso = start.isoformat(), end.isoformat()

    def req(method: str, path: str, json: dict | None = None, headers: dict | None = None) -> tuple[int, dict]:
        resp = client.request(method, str(client.base_url) + path, json=json, headers=headers)
        return resp.status_code, resp.json()

    api = ApiClient(req, "dev-ai-secret")
    model = MockModel(["Shop hoist notes here"])
    result = shop_hoist_flow(
        model, api, member_id=member["id"], hoist_id=shop["id"],
        start_at=start_iso, end_at=end_iso,
    )
    assert result.passed is True
    assert [s["status"] for s in result.steps] == [201, 403]
