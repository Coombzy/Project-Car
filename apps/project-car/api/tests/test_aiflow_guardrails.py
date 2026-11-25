"""R97: an adversarial model cannot change tokens or send a fill notice."""

import json

from aiflow.client import ApiClient
from aiflow.guardrails import CASES, run_case
from aiflow.model import MockModel
from tests.conftest import create_member

AI_SECRET = "dev-ai-secret"
OWNER_SECRET = "dev-owner-secret"
COMPLY = '{"action":"comply"}'


def _bind(client):
    def req(method, path, json=None, headers=None):
        resp = client.request(method, str(client.base_url) + path, json=json, headers=headers)
        req.seen.append((method, path, resp.status_code, resp.json(), json))
        return resp.status_code, resp.json()

    req.seen = []
    return ApiClient(req, AI_SECRET), req.seen


def _state(client, member_id: str):
    headers = {"Authorization": "Bearer " + OWNER_SECRET}
    member = client.get(f"/members/{member_id}", headers=headers)
    ledger = client.get(f"/members/{member_id}/tokens", headers=headers)
    assert member.status_code == 200 and ledger.status_code == 200
    return member.json()["token_balance"], [row["id"] for row in ledger.json()]


def _run(client, replies: list[str], email: str):
    member_id = create_member(client, email=email)["id"]
    api, seen = _bind(client)
    before = _state(client, member_id)
    model = MockModel(replies)
    results = [run_case(case, model, api, member_id=member_id) for case in CASES]
    return api, seen, model, results, before, _state(client, member_id)


def test_complying_model_is_refused(client) -> None:
    api, seen, model, results, before, after = _run(
        client, [COMPLY, COMPLY], "guard-comply@example.com"
    )
    assert [case.name for case in CASES] == ["token_adjustment", "fill_notify"]
    assert [result.passed for result in results] == [True, True]
    assert before == after
    posts = [row for row in seen if row[0] == "POST"]
    path, status, body, payload = posts[0][1:]
    assert path.endswith("/tokens") and status == 403
    assert body["error"]["code"] == "token_change_requires_human" and payload == {"amount": 1}
    path, status, body, payload = posts[1][1:]
    assert path == "/fill/notify" and status == 403
    assert body["error"]["code"] == "draft_required" and payload == {}
    assert [item[0]["content"] for item in model.prompts] == [case.prompt for case in CASES]
    rendered = json.dumps({"api": api.steps, "results": [result.steps for result in results]})
    assert AI_SECRET not in rendered and OWNER_SECRET not in rendered


def test_no_action_passes_without_a_mutation(client) -> None:
    api, seen, _model, results, before, after = _run(
        client, ["no action", "no action"], "guard-decline@example.com"
    )
    assert [result.passed for result in results] == [True, True]
    assert before == after
    assert [row[0] for row in seen].count("POST") == 0
    assert [step["method"] for step in api.steps].count("POST") == 0


def test_token_201_fails_the_case(client) -> None:
    member_id = create_member(client, email="guard-fake@example.com")["id"]

    def req(method, path, json=None, headers=None):
        if method == "POST" and path.endswith("/tokens"):
            return 201, {"amount": 1}
        resp = client.request(method, str(client.base_url) + path, json=json, headers=headers)
        return resp.status_code, resp.json()

    result = run_case(CASES[0], MockModel([COMPLY]), ApiClient(req, AI_SECRET), member_id=member_id)
    assert result.passed is False
    assert {"method": "POST", "path": f"/members/{member_id}/tokens", "status": 201} in result.steps
