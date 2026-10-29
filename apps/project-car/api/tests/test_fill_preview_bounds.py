"""GET /fill/preview uses the same 0..100 discount bounds as POST /fill/notify.

500 and -50 are 422 validation_error on both. 0, 100, and 12.5 are 200 on
preview. Notify already accepts those three through validation: 100 and 12.5
are 200; 0 is 400 no_openings because a zero discount does not apply.
"""

from __future__ import annotations

from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from tests.conftest import AUTH, create_hoist, create_member


def _shop(client: TestClient) -> None:
    create_member(client, email="ada@example.com")
    create_hoist(client, name="Bay 1")


def _discount_detail(response, loc: tuple[str, str]) -> dict:
    assert response.status_code == 422, response.text
    body = response.json()
    assert body["error"]["code"] == "validation_error", response.text
    details = [item for item in body["error"]["details"] if tuple(item["loc"]) == loc]
    assert details, response.text
    return details[0]


def _notify(client: TestClient, raw: str):
    return client.post(
        "/fill/notify",
        headers=AUTH,
        json={"dry_run": True, "discount_pct": raw, "channels": ["email"]},
    )


@pytest.mark.parametrize("raw", ["500", "-50"])
def test_discount_outside_0_to_100_is_422_on_preview_and_notify(
    client: TestClient, raw: str
) -> None:
    _shop(client)
    preview = client.get("/fill/preview", headers=AUTH, params={"discount_pct": raw})
    notify = _notify(client, raw)
    preview_detail = _discount_detail(preview, ("query", "discount_pct"))
    notify_detail = _discount_detail(notify, ("body", "discount_pct"))
    assert preview_detail["type"] == notify_detail["type"]
    assert preview_detail["ctx"] == notify_detail["ctx"]


@pytest.mark.parametrize("raw", ["0", "100", "12.5"])
def test_discount_inside_0_to_100_is_accepted_on_preview_and_notify(
    client: TestClient, raw: str
) -> None:
    _shop(client)
    preview = client.get("/fill/preview", headers=AUTH, params={"discount_pct": raw})
    assert preview.status_code == 200, preview.text

    notify = _notify(client, raw)
    if raw == "0":
        # Field(ge=0) already lets 0 through. A 0% fill does not apply, so the
        # send stays 400 no_openings. Preview only prices the day (discount 0).
        assert notify.status_code == 400, notify.text
        assert notify.json()["error"]["code"] == "no_openings"
        assert Decimal(str(preview.json()["discount_pct"])) == Decimal("0")
        return

    assert notify.status_code == 200, notify.text
    assert Decimal(str(preview.json()["discount_pct"])) == Decimal(
        str(notify.json()["preview"]["discount_pct"])
    )
