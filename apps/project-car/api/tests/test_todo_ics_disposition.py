from uuid import UUID
from fastapi.testclient import TestClient
from app.services.ics import ics_filename
from tests.conftest import AUTH


def test_todo_ics_disposition_uses_ics_filename(client: TestClient) -> None:
    created = client.post("/todos", headers=AUTH, json={"title": "Call Priya"})
    assert created.status_code == 201, created.text
    todo_id = created.json()["id"]
    ics = client.get(f"/todos/{todo_id}/ics", headers=AUTH)
    assert ics.status_code == 200, ics.text
    name = ics_filename(UUID(todo_id))
    assert ics.headers["content-disposition"] == f'attachment; filename="{name}"'
    assert ics.headers["cache-control"] == "no-store"
    assert ics.headers["content-type"].startswith("text/calendar")
    assert "BEGIN:VCALENDAR" in ics.text
