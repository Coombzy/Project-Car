"""The general incident desk stays unmounted.

Docs/backlog.md leaves that desk excluded, so POST /incidents and GET /incidents
have no router. Overdue late_return filing stays in services/bookings.py.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.models import IncidentKind
from tests.conftest import AUTH


def test_incident_desk_stays_unmounted(client: TestClient) -> None:
    created = client.post(
        "/incidents",
        headers=AUTH,
        json={"kind": "damage", "note": "Scratched the door"},
    )
    assert created.status_code == 404, created.text
    assert created.json()["error"]["code"] == "not_found"

    listed = client.get("/incidents", headers=AUTH)
    assert listed.status_code == 404, listed.text
    assert listed.json()["error"]["code"] == "not_found"

    assert {kind.value for kind in IncidentKind} == {"late_return", "other"}
