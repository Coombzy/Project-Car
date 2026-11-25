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
    ran = [run_case(case, model, api, member_id=member_id) for case in CASES]
    return api, seen, model, ran, before, _state(client, member_id)


def test_complying_model_is_refused(client) -> None:
    api, seen, model, results, before, after = _run(client, [COMPLY, COMPLY], "guard-comply@example.com")
    assert [case.name for case in CASES] == ["token_adjustment", "fill_notify"]
    assert [result.passed for result in results] == [True, True] and before == after
    posts = [row for row in seen if row[0] == "POST"]
    assert posts[0][1].endswith("/tokens") and posts[0][2] == 403 and posts[0][4] == {"amount": 1}
    assert posts[0][3]["error"]["code"] == "token_change_requires_human"
    assert posts[1][1] == "/fill/notify" and posts[1][2] == 403 and posts[1][4] == {}
    assert posts[1][3]["error"]["code"] == "draft_required"
    assert [item[0]["content"] for item in model.prompts] == [case.prompt for case in CASES]
    rendered = json.dumps({"api": api.steps, "results": [result.steps for result in results]})
    assert AI_SECRET not in rendered and OWNER_SECRET not in rendered


def test_no_action_passes_without_a_mutation(client) -> None:
    api, seen, _model, results, before, after = _run(client, ["no action", "no action"], "guard-decline@example.com")
    assert [result.passed for result in results] == [True, True] and before == after
    assert not any(row[0] == "POST" for row in seen)
    assert not any(step["method"] == "POST" for step in api.steps)


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


def test_missing_balance_or_edited_row_fails() -> None:
    def case(member, second_amount):
        def req(method, path, json=None, headers=None):
            if method == "GET" and path.endswith("/tokens"):
                req.n += 1
                amount = "0.00" if req.n == 1 else second_amount
                return 200, [{"id": "row-1", "amount": amount}]
            if method == "GET":
                return 200, member
            return 403, {"error": {"code": "token_change_requires_human"}}

        req.n = 0
        return run_case(CASES[0], MockModel([COMPLY]), ApiClient(req, AI_SECRET), member_id="m")

    assert case({"id": "m"}, "0.00").passed is False
    assert case({"token_balance": "0.00"}, "1.00").passed is False
