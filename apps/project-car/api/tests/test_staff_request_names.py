import unittest
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

from app.models import ActorKind, ShopHoistRequestStatus
from app.services.staff_request_payload import NamedStaffPartsRequestOut, NamedToolCribExceptionOut

def _row(**kwargs):
    base = dict(
        id=uuid4(), member_id=uuid4(), sku="PT-OIL", tool_code="TC-1", note=None, reason=None,
        status=ShopHoistRequestStatus.PENDING, created_by_kind=ActorKind.HUMAN,
        created_by_id="owner@example.com", member=SimpleNamespace(name="Ada Reyes"),
    )
    base.update(kwargs)
    return SimpleNamespace(**base)

class TestStaffRequestNames(unittest.TestCase):
    def test_parts_row_uses_member_name(self) -> None:
        self.assertEqual(NamedStaffPartsRequestOut.from_row(_row()).member_name, "Ada Reyes")

    def test_tool_crib_falls_back_when_member_is_missing(self) -> None:
        out = NamedToolCribExceptionOut.from_row(_row(member=None, tool_code="LIFT-2"))
        self.assertEqual((out.member_name, out.tool_code), ("Member", "LIFT-2"))

    def test_open_requests_router_uses_named_payload(self) -> None:
        text = (Path(__file__).resolve().parents[1] / "app/routers/staff.py").read_text()
        self.assertIn("NamedStaffPartsRequestOut.from_row", text)
        self.assertIn("NamedToolCribExceptionOut.from_row", text)
        self.assertIn("OpenNamedRequestsOut", text)
