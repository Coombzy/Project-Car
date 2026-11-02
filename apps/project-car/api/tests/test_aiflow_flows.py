"""Tests for the aiflow flows module."""

from aiflow.client import ApiClient
from aiflow.flows import fill_draft_flow
from aiflow.model import MockModel


def test_fill_draft_flow_passes_on_main(client) -> None:
    def req(method: str, path: str, json: dict | None = None, headers: dict | None = None) -> tuple[int, dict]:
        resp = client.request(method, str(client.base_url) + path, json=json, headers=headers)
        return resp.status_code, resp.json()

    api = ApiClient(req, "dev-ai-secret")
    model = MockModel(["Bay 2 is free"])
    result = fill_draft_flow(model, api)
    assert result.passed is True
    assert [s["status"] for s in result.steps] == [201, 403]
