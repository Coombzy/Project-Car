"""Staff parts, tool-crib exceptions, and shop jobs trim text.

Required sku, tool_code, and title are 422 when empty after trimming.
Optional note, reason, and notes that are only spaces are stored as null.
"""

from __future__ import annotations

from uuid import uuid4

from fastapi.testclient import TestClient

from app.schemas import ShopJobCreate, StaffPartsRequestCreate, ToolCribExceptionCreate
from tests.conftest import AUTH, create_member, login_member


def _assert_blank_rejected(response, field: str) -> None:
    assert response.status_code == 422, response.text
    body = response.json()
    assert body["error"]["code"] == "validation_error"
    matched = [item for item in body["error"]["details"] if tuple(item["loc"]) == ("body", field)]
    assert matched, body
    assert matched[0]["type"] == "string_too_short", matched


def test_owner_parts_request_rejects_blank_sku(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com")
    response = client.post(
        "/parts-requests",
        headers=AUTH,
        json={"member_id": member["id"], "sku": "  "},
    )
    _assert_blank_rejected(response, "sku")


def test_owner_parts_request_stores_trimmed_sku(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com")
    response = client.post(
        "/parts-requests",
        headers=AUTH,
        json={"member_id": member["id"], "sku": " PT-100 "},
    )
    assert response.status_code == 201, response.text
    assert response.json()["sku"] == "PT-100"


def test_staff_create_schemas_strip_padded_required_fields() -> None:
    member_id = str(uuid4())
    parsed = {
        "sku": StaffPartsRequestCreate.model_validate(
            {"member_id": member_id, "sku": " PT-100 "}
        ).sku,
        "tool_code": ToolCribExceptionCreate.model_validate(
            {"member_id": member_id, "tool_code": " TC-FL-001 "}
        ).tool_code,
        "title": ShopJobCreate.model_validate({"title": " Sweep the floor "}).title,
    }
    assert parsed == {
        "sku": "PT-100",
        "tool_code": "TC-FL-001",
        "title": "Sweep the floor",
    }


def test_owner_tool_exception_rejects_blank_tool_code(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com")
    response = client.post(
        "/tool-crib-exceptions",
        headers=AUTH,
        json={"member_id": member["id"], "tool_code": " "},
    )
    _assert_blank_rejected(response, "tool_code")


def test_member_tool_exception_rejects_blank_tool_code(client: TestClient) -> None:
    create_member(client, email="ada@example.com")
    login_member(client, "ada@example.com")
    response = client.post("/member/tool-crib-exceptions", json={"tool_code": " "})
    _assert_blank_rejected(response, "tool_code")


def test_shop_job_rejects_blank_title(client: TestClient) -> None:
    response = client.post("/jobs", headers=AUTH, json={"title": "  "})
    _assert_blank_rejected(response, "title")


def test_blank_optional_text_is_stored_as_null(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com")
    parts = client.post(
        "/parts-requests",
        headers=AUTH,
        json={"member_id": member["id"], "sku": "PT-100", "note": "  "},
    )
    assert parts.status_code == 201, parts.text
    assert parts.json()["note"] is None

    tool = client.post(
        "/tool-crib-exceptions",
        headers=AUTH,
        json={"member_id": member["id"], "tool_code": "TC-FL-001", "reason": "  "},
    )
    assert tool.status_code == 201, tool.text
    assert tool.json()["reason"] is None

    login_member(client, "ada@example.com")
    member_tool = client.post(
        "/member/tool-crib-exceptions",
        json={"tool_code": "TC-FL-001", "reason": "  "},
    )
    assert member_tool.status_code == 201, member_tool.text
    assert member_tool.json()["reason"] is None

    job = client.post(
        "/jobs",
        headers=AUTH,
        json={"title": "Sweep the floor", "notes": "  "},
    )
    assert job.status_code == 201, job.text
    assert job.json()["notes"] is None


def test_non_string_optional_text_is_rejected(client: TestClient) -> None:
    member = create_member(client, email="grace@example.com")
    parts = client.post(
        "/parts-requests",
        headers=AUTH,
        json={"member_id": member["id"], "sku": "PT-100", "note": True},
    )
    assert parts.status_code == 422, parts.text

    tool = client.post(
        "/tool-crib-exceptions",
        headers=AUTH,
        json={"member_id": member["id"], "tool_code": "TC-FL-001", "reason": 12},
    )
    assert tool.status_code == 422, tool.text

    job = client.post(
        "/jobs",
        headers=AUTH,
        json={"title": "Sweep the floor", "notes": {"a": 1}},
    )
    assert job.status_code == 422, job.text
