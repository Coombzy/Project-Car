"""Personal todos scoped to the current Owner or Member."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import Principal
from app.models import Todo, TodoStatus
from app.shop_time import as_utc

TODO_LIST_DEFAULT_LIMIT = 200
TODO_LIST_MAX_LIMIT = 500


def _error(status: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status, detail={"code": code, "message": message})


def _scope(stmt, principal: Principal):
    if principal.role == "owner":
        return stmt.where(Todo.owner_email == principal.email, Todo.member_id.is_(None))
    if principal.member_id is None:
        raise _error(401, "unauthorized", "Authentication required.")
    return stmt.where(Todo.member_id == principal.member_id)


def list_todos(
    session: Session,
    principal: Principal,
    *,
    status: TodoStatus = TodoStatus.OPEN,
    limit: int = TODO_LIST_DEFAULT_LIMIT,
) -> list[Todo]:
    """Open rows by default, capped at 200 (1–500). Pass status=done for finished rows."""
    if limit < 1 or limit > TODO_LIST_MAX_LIMIT:
        raise _error(422, "validation_error", "Limit must be from 1 to 500.")
    if status == TodoStatus.OPEN:
        chosen = TodoStatus.OPEN
    elif status == TodoStatus.DONE:
        chosen = TodoStatus.DONE
    else:
        raise _error(422, "validation_error", "Status must be open or done.")
    stmt = _scope(select(Todo), principal).where(Todo.status == chosen)
    if chosen == TodoStatus.DONE:
        # Newest completion first so a cap still leaves Reopen targets.
        stmt = stmt.order_by(Todo.updated_at.desc(), Todo.created_at.desc(), Todo.id.desc())
    else:
        stmt = stmt.order_by(
            Todo.status,
            Todo.due_at.is_(None),
            Todo.due_at,
            Todo.created_at,
            Todo.id,
        )
    return list(session.scalars(stmt.limit(limit)).all())


def get_todo(session: Session, principal: Principal, todo_id: UUID) -> Todo:
    todo = session.scalars(_scope(select(Todo).where(Todo.id == todo_id), principal)).first()
    if todo is None:
        raise _error(404, "todo_not_found", "That to-do is not on your list.")
    return todo


def create_todo(
    session: Session,
    principal: Principal,
    *,
    title: str,
    notes: str | None,
    due_at: datetime | None,
) -> Todo:
    # An AI principal has no owner email and no member id, so the row would match nobody.
    if principal.role == "ai":
        raise _error(
            403,
            "todo_requires_person",
            "An AI cannot keep its own to-do list.",
        )
    cleaned = title.strip()
    if not cleaned:
        raise _error(422, "validation_error", "Title is required.")
    due = as_utc(due_at) if due_at is not None else None
    row = Todo(
        owner_email=principal.email if principal.role == "owner" else None,
        member_id=principal.member_id if principal.role == "member" else None,
        title=cleaned,
        notes=(notes or "").strip() or None,
        due_at=due,
        status=TodoStatus.OPEN,
    )
    session.add(row)
    session.flush()
    return row


def patch_todo(
    session: Session,
    principal: Principal,
    todo_id: UUID,
    *,
    title: str | None = None,
    notes: str | None = None,
    due_at: datetime | None = None,
    clear_due: bool = False,
    status: TodoStatus | None = None,
) -> Todo:
    row = get_todo(session, principal, todo_id)
    if title is not None:
        cleaned = title.strip()
        if not cleaned:
            raise _error(422, "validation_error", "Title is required.")
        row.title = cleaned
    if notes is not None:
        row.notes = notes.strip() or None
    if clear_due:
        row.due_at = None
    elif due_at is not None:
        row.due_at = as_utc(due_at)
    if status is not None:
        row.status = status
    session.add(row)
    session.flush()
    return row


def delete_todo(session: Session, principal: Principal, todo_id: UUID) -> None:
    row = get_todo(session, principal, todo_id)
    session.delete(row)
    session.flush()
