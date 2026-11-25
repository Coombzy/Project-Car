from uuid import UUID

from pydantic import BaseModel

from app.models import ActorKind
from app.schemas import ShopHoistRequestOut, StaffPartsRequestOut, ToolCribExceptionOut


def _from_row(cls, row):
    name = row.member.name if row.member is not None else "Member"
    return cls.model_validate(row).model_copy(update={"member_name": name})


class NamedStaffPartsRequestOut(StaffPartsRequestOut):
    member_name: str = "Member"

    @classmethod
    def from_row(cls, row):
        return _from_row(cls, row)


class NamedToolCribExceptionOut(ToolCribExceptionOut):
    member_name: str = "Member"

    @classmethod
    def from_row(cls, row):
        return _from_row(cls, row)


class OpenNamedRequestsOut(BaseModel):
    shop_hoist: list[ShopHoistRequestOut]
    parts: list[NamedStaffPartsRequestOut]
    tool_crib: list[NamedToolCribExceptionOut]
    actor_kind: ActorKind
    action_id: UUID
