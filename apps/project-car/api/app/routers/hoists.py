from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.deps import DbSession, Owner
from app.models import Hoist
from app.schemas import HoistCreate, HoistOut, HoistPatch

router = APIRouter(tags=["hoists"])


@router.get("/hoists", response_model=list[HoistOut])
def list_hoists(session: DbSession, _owner: Owner) -> list[HoistOut]:
    rows = session.scalars(select(Hoist).order_by(Hoist.name)).all()
    return [HoistOut.model_validate(row) for row in rows]


@router.post("/hoists", response_model=HoistOut, status_code=201)
def create_hoist(body: HoistCreate, session: DbSession, _owner: Owner) -> HoistOut:
    row = Hoist(name=body.name, location_label=body.location_label, status=body.status)
    session.add(row)
    try:
        session.flush()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail={"code": "duplicate_hoist", "message": "A hoist with that name already exists."},
        ) from None
    session.refresh(row)
    return HoistOut.model_validate(row)


@router.patch("/hoists/{hoist_id}", response_model=HoistOut)
def patch_hoist(hoist_id: UUID, body: HoistPatch, session: DbSession, _owner: Owner) -> HoistOut:
    row = session.get(Hoist, hoist_id)
    if row is None:
        raise HTTPException(status_code=404, detail={"code": "not_found", "message": "Hoist not found."})
    updates = body.model_dump(exclude_unset=True)
    if "name" in updates and updates["name"]:
        updates["name"] = updates["name"].strip()
    if "location_label" in updates and updates["location_label"] is not None:
        updates["location_label"] = updates["location_label"].strip()
    for key, value in updates.items():
        setattr(row, key, value)
    session.add(row)
    try:
        session.flush()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail={"code": "duplicate_hoist", "message": "A hoist with that name already exists."},
        ) from None
    session.refresh(row)
    return HoistOut.model_validate(row)
