"""A failed request must still leave a step behind, and the error must surface."""

import pytest

from aiflow.client import ApiClient


def test_failed_request_records_step_then_reraises() -> None:
    err = ConnectionError("x")

    def boom(*args, **kwargs):
        raise err

    client = ApiClient(request=boom, ai_bearer="dev-ai-secret")

    with pytest.raises(ConnectionError) as excinfo:
        client.call("GET", "/p")

    assert excinfo.value is err
    assert client.steps == [
        {"method": "GET", "path": "/p", "status": None, "error": "ConnectionError"}
    ]


def test_successful_request_records_exactly_one_step() -> None:
    def fake_request(method, path, json=None, headers=None):
        return 200, {}

    client = ApiClient(request=fake_request, ai_bearer="dev-ai-secret")
    client.call("GET", "/p")

    assert len(client.steps) == 1
    assert client.steps[0] == {"method": "GET", "path": "/p", "status": 200}
