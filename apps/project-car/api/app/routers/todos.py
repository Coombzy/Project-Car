from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import Response

from app.deps import AnyPrincipal, DbSession
from app.schemas import TodoCreate, TodoOut, TodoPatch
from app.services import todos as todo_service
from app.services.ics import ics_filename, todo_ics

router = APIRouter(tags=["todos"])


@router.get("/todos", response_model=list[TodoOut])
def list_my_todos(session: DbSession, principal: AnyPrincipal) -> list[TodoOut]:
    return [TodoOut.model_validate(row) for row in todo_service.list_todos(session, principal)]


@router.get("/todos/{todo_id}", response_model=TodoOut)
def get_todo(todo_id: UUID, session: DbSession, principal: AnyPrincipal) -> TodoOut:
    return TodoOut.model_validate(todo_service.get_todo(session, principal, todo_id))


@router.post("/todos", response_model=TodoOut, status_code=201)
def create_todo(body: TodoCreate, session: DbSession, principal: AnyPrincipal) -> TodoOut:
    row = todo_service.create_todo(
        session,
        principal,
        title=body.title,
        notes=body.notes,
        due_at=body.due_at,
    )
    return TodoOut.model_validate(row)


@router.patch("/todos/{todo_id}", response_model=TodoOut)
def patch_todo(
    todo_id: UUID,
    body: TodoPatch,
    session: DbSession,
    principal: AnyPrincipal,
) -> TodoOut:
    row = todo_service.patch_todo(
        session,
        principal,
        todo_id,
        title=body.title,
        notes=body.notes,
        due_at=body.due_at,
        clear_due=body.clear_due,
        status=body.status,
    )
    return TodoOut.model_validate(row)


@router.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: UUID, session: DbSession, principal: AnyPrincipal) -> Response:
    todo_service.delete_todo(session, principal, todo_id)
    return Response(status_code=204)


@router.get("/todos/{todo_id}/ics")
def download_todo_ics(todo_id: UUID, session: DbSession, principal: AnyPrincipal) -> Response:
    row = todo_service.get_todo(session, principal, todo_id)
    payload = todo_ics(row)
    filename = ics_filename(row.id)
    return Response(
        content=payload,
        media_type="text/calendar; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Cache-Control": "no-store",
        },
    )
