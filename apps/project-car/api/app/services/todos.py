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


def _error(status: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status, detail={"code": code, "message": message})


def _scope(stmt, principal: Principal):
    if principal.role == "owner":
        return stmt.where(Todo.owner_email == principal.email, Todo.member_id.is_(None))
    if principal.member_id is None:
        raise _error(401, "unauthorized", "Authentication required.")
    return stmt.where(Todo.member_id == principal.member_id)


def list_todos(session: Session, principal: Principal) -> list[Todo]:
    stmt = _scope(select(Todo), principal).order_by(
        Todo.status,
        Todo.due_at.is_(None),
        Todo.due_at,
        Todo.created_at,
    )
    return list(session.scalars(stmt).all())


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
