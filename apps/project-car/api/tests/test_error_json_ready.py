"""Error payloads must survive json.dumps: Decimal and exception extras included."""

import json
from decimal import Decimal

from app.errors import _json_ready, error_body, error_response


def test_json_ready_renders_decimal_and_exception_as_text() -> None:
    assert _json_ready(Decimal("1.50")) == "1.50"  # str, not Decimal
    assert _json_ready(ValueError("boom")) == "boom"


def test_json_ready_walks_nested_containers() -> None:
    ready = _json_ready({"a": [Decimal("2"), ValueError("x")], "b": (Decimal("1.5"),)})
    assert ready == {"a": ["2", "x"], "b": ["1.5"]}


def test_json_ready_passes_plain_scalars_through() -> None:
    for value in (None, "s", 1, 1.5, True):
        ready = _json_ready(value)
        assert ready == value and type(ready) is type(value)


def test_error_body_keeps_code_message_and_extras() -> None:
    details = [{"loc": "amount", "input": Decimal("1.5")}]
    assert error_body("validation_error", "Request failed validation.", details=details) == {
        "error": {
            "code": "validation_error",
            "message": "Request failed validation.",
            "details": details,
        }
    }


def test_error_response_body_is_json_serializable() -> None:
    response = error_response(
        422,
        "validation_error",
        "Request failed validation.",
        details=[{"loc": "amount", "input": Decimal("1.5"), "err": ValueError("boom")}],
    )
    assert response.status_code == 422
    assert json.loads(response.body) == {
        "error": {
            "code": "validation_error",
            "message": "Request failed validation.",
            "details": [{"loc": "amount", "input": "1.5", "err": "boom"}],
        }
    }
