"""R95 model adapter. On main the aiflow package is absent, so this fails."""

from __future__ import annotations

import io
import json
from urllib import error, request

import pytest

from aiflow.model import MockModel, ModelError, OpenAICompatModel

SECRET = "sk-r95-do-not-leak-9f3c"


def test_mock_returns_replies_in_order_and_records_prompts() -> None:
    replies = ["first", "second"]
    model = MockModel(replies)
    first_prompt = [{"role": "user", "content": "a"}]
    second_prompt = [{"role": "user", "content": "b"}]

    assert model.complete(first_prompt) == "first"
    assert model.complete(second_prompt) == "second"

    first_prompt[0]["content"] = "changed"
    second_prompt.append({"role": "user", "content": "extra"})
    assert model.prompts == [
        [{"role": "user", "content": "a"}],
        [{"role": "user", "content": "b"}],
    ]
    assert replies == ["first", "second"]


def test_mock_raises_index_error_when_replies_run_out() -> None:
    replies = ["only"]
    model = MockModel(replies)

    assert model.complete([{"role": "user", "content": "one"}]) == "only"
    with pytest.raises(IndexError, match="MockModel ran out of scripted replies"):
        model.complete([{"role": "user", "content": "two"}])

    assert replies == ["only"]
    assert model.prompts == [
        [{"role": "user", "content": "one"}],
        [{"role": "user", "content": "two"}],
    ]


def test_mock_records_the_prompt_when_content_is_a_list() -> None:
    model = MockModel(["ok"])
    part = {"type": "text", "text": "original"}
    content = [part]
    messages = [{"role": "user", "content": content}]

    assert model.complete(messages) == "ok"
    part["text"] = "changed"
    content.append({"type": "text", "text": "extra"})
    messages.append({"role": "user", "content": "later"})

    assert model.prompts == [
        [{"role": "user", "content": [{"type": "text", "text": "original"}]}]
    ]


def _capture(status: int, body: object):
    seen: dict = {}

    def transport(url, data, headers, timeout):
        seen["url"] = url
        seen["data"] = data
        seen["headers"] = dict(headers)
        seen["timeout"] = timeout
        return status, json.dumps(body).encode()

    return transport, seen


def test_openai_compat_posts_json_bearer_and_returns_content() -> None:
    transport, seen = _capture(
        200, {"choices": [{"message": {"content": "hello from model"}}]}
    )
    messages = [{"role": "user", "content": "hi"}]
    model = OpenAICompatModel(
        "http://127.0.0.1:11434/",
        "local-model",
        api_key=SECRET,
        transport=transport,
    )

    assert model.complete(messages) == "hello from model"
    assert messages == [{"role": "user", "content": "hi"}]
    assert seen["url"] == "http://127.0.0.1:11434/v1/chat/completions"
    assert "//" not in seen["url"].split("://", 1)[1]
    parsed = json.loads(seen["data"])
    assert parsed == {
        "model": "local-model",
        "messages": messages,
        "temperature": 0,
    }
    assert type(parsed["temperature"]) is int
    assert seen["headers"] == {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SECRET}",
    }
    assert seen["timeout"] == 30
    assert SECRET.encode() not in seen["url"].encode()
    assert SECRET.encode() not in seen["data"]


def test_openai_compat_omits_authorization_when_no_key() -> None:
    transport, seen = _capture(
        200, {"choices": [{"message": {"content": "ok"}}]}
    )
    model = OpenAICompatModel(
        "https://api.example.com",
        "cloud-model",
        transport=transport,
    )

    assert model.complete([{"role": "user", "content": "x"}]) == "ok"
    assert seen["url"] == "https://api.example.com/v1/chat/completions"
    assert seen["headers"] == {"Content-Type": "application/json"}
    assert "Authorization" not in seen["headers"]


def test_non_200_raises_model_error_without_the_key() -> None:
    transport, _seen = _capture(
        500,
        {
            "choices": [{"message": {"content": "should-not-return"}}],
            "error": SECRET,
        },
    )
    model = OpenAICompatModel(
        "http://127.0.0.1:11434",
        "local-model",
        api_key=SECRET,
        transport=transport,
    )

    with pytest.raises(ModelError) as caught:
        model.complete([{"role": "user", "content": "hi"}])

    assert caught.value.status == 500
    text = f"{caught.value} {caught.value!r}"
    assert "500" in text
    assert SECRET not in text


@pytest.mark.parametrize(
    "body",
    [
        {"id": "x", "error": SECRET},
        {"choices": [], "error": SECRET},
        {"choices": None, "error": SECRET},
    ],
)
def test_body_without_choices_raises_model_error_without_the_key(body: dict) -> None:
    transport, seen = _capture(200, body)
    model = OpenAICompatModel(
        "https://api.example.com/",
        "cloud-model",
        api_key=SECRET,
        transport=transport,
        timeout=12,
    )

    with pytest.raises(ModelError) as caught:
        model.complete([{"role": "user", "content": "hi"}])

    assert caught.value.status == 200
    assert seen["timeout"] == 12
    assert seen["url"] == "https://api.example.com/v1/chat/completions"
    text = f"{caught.value} {caught.value!r}"
    assert "200" in text
    assert SECRET not in text


def test_default_transport_posts_with_urllib(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = []

    class _Resp:
        status = 200

        def read(self) -> bytes:
            return b'{"choices":[{"message":{"content":"from-urllib"}}]}'

        def __enter__(self):
            return self

        def __exit__(self, *args: object) -> bool:
            return False

    def fake_urlopen(req, timeout=None):
        calls.append((req, timeout))
        return _Resp()

    monkeypatch.setattr("aiflow.model.request.urlopen", fake_urlopen)
    model = OpenAICompatModel(
        "http://127.0.0.1:11434/",
        "local-model",
        api_key=SECRET,
    )

    assert model.complete([{"role": "user", "content": "q"}]) == "from-urllib"
    assert len(calls) == 1
    req, timeout = calls[0]
    assert req.full_url == "http://127.0.0.1:11434/v1/chat/completions"
    assert "//" not in req.full_url.split("://", 1)[1]
    assert req.get_method() == "POST"
    assert timeout == 30
    assert req.get_header("Authorization") == f"Bearer {SECRET}"
    parsed = json.loads(req.data)
    assert parsed["model"] == "local-model"
    assert parsed["temperature"] == 0
    assert type(parsed["temperature"]) is int
    assert SECRET.encode() not in req.data


def test_default_transport_http_error_hides_the_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_urlopen(req, timeout=None):
        raise error.HTTPError(
            req.full_url,
            500,
            "nope",
            hdrs=None,
            fp=io.BytesIO(SECRET.encode()),
        )

    monkeypatch.setattr("aiflow.model.request.urlopen", fake_urlopen)
    model = OpenAICompatModel(
        "http://127.0.0.1:11434",
        "local-model",
        api_key=SECRET,
    )

    with pytest.raises(ModelError) as caught:
        model.complete([{"role": "user", "content": "q"}])

    assert caught.value.status == 500
    text = f"{caught.value} {caught.value!r}"
    assert "500" in text
    assert SECRET not in text


def test_default_transport_does_not_forward_the_bearer_on_redirect(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = []

    class _Resp:
        status = 200

        def read(self) -> bytes:
            return b'{"choices":[{"message":{"content":"from-urllib"}}]}'

        def __enter__(self):
            return self

        def __exit__(self, *args: object) -> bool:
            return False

    def fake_urlopen(req, timeout=None):
        calls.append(req)
        return _Resp()

    monkeypatch.setattr("aiflow.model.request.urlopen", fake_urlopen)
    model = OpenAICompatModel(
        "http://127.0.0.1:11434/",
        "local-model",
        api_key=SECRET,
    )

    assert model.complete([{"role": "user", "content": "q"}]) == "from-urllib"
    assert len(calls) == 1
    req = calls[0]
    assert req.full_url == "http://127.0.0.1:11434/v1/chat/completions"
    assert req.get_method() == "POST"
    assert req.get_header("Authorization") == f"Bearer {SECRET}"

    redirected = request.HTTPRedirectHandler().redirect_request(
        req, None, 302, "Found", {}, "http://evil.example/steal"
    )
    assert redirected is not None
    assert redirected.get_method() == "GET"
    assert redirected.full_url == "http://evil.example/steal"
    assert redirected.get_header("Authorization") is None
    forwarded = " ".join(value for _key, value in redirected.header_items())
    assert SECRET not in forwarded
    assert SECRET not in redirected.full_url
