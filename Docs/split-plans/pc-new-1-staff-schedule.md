```json
{
  "job": "pc-new-1-staff-schedule",
  "repo": "Coombzy/Project-Car",
  "base": "f1a86109629033c83c07fc6e48cf80dfdd3373de",
  "goal": "GET /staff/schedule returns Booking rows from America/Regina today-1 day through today+14 days, capped by limit (default 200, 422 outside 1..500).",
  "rows": [
    {
      "id": "r1",
      "goal": "Write test_staff_schedule_is_windowed_and_capped(client) in apps/project-car/api/tests/test_staff_schedule_window.py. create_member(..., email=\"sched-window@example.com\", allocate_tokens=False) and create_hoist(..., name=\"Schedule bay\") come from tests.conftest. Insert Booking rows with client.session_factory: start_at 10:00 America/Regina on pricing_today()-60 days, start_at 10:00 America/Regina on pricing_today()+1 day, and 205 hourly rows whose first start_at is 10:00 America/Regina on pricing_today()+2 days. Each Booking sets member_id, hoist_id, start_at, end_at one hour later, kind BookingKind.CUSTOMER, status BookingStatus.CONFIRMED, reserved_tokens Decimal(\"0\"). GET /staff/schedule with AUTH returns 200, len(json) == 200, the 60-day id is absent, and the tomorrow id is present. GET /staff/schedule with AUTH and params={\"limit\": 0} returns 422. On main the default GET returns all 207 rows.",
      "files": [
        "apps/project-car/api/tests/test_staff_schedule_window.py"
      ],
      "check": "grep -q 'def test_staff_schedule_is_windowed_and_capped' apps/project-car/api/tests/test_staff_schedule_window.py && grep -q '{\"limit\": 0}' apps/project-car/api/tests/test_staff_schedule_window.py && grep -q '422' apps/project-car/api/tests/test_staff_schedule_window.py",
      "depends_on": [],
      "est_lines": 52,
      "tests": 1,
      "api": [
        {
          "method": "GET",
          "path": "/staff/schedule"
        }
      ],
      "builds_requests": false,
      "integration": false
    },
    {
      "id": "r2",
      "goal": "Add resolve_schedule_window(window_start: date | None, window_end: date | None, *, today: date) -> tuple[datetime, datetime] in apps/project-car/api/app/services/schedule_window.py. SCHEDULE_PAST_DAYS is 1 and SCHEDULE_FUTURE_DAYS is 14. Use PRICING_TZ and as_utc from app.shop_time. A missing window_start is today minus 1 day and a missing window_end is today plus 14 days. Return the half-open UTC pair from 00:00 America/Regina on the start day through 00:00 America/Regina on the day after the end day. today=date(2026, 6, 15) with both arguments None returns 2026-06-14T06:00:00Z and 2026-06-30T06:00:00Z. resolve_schedule_window(date(2026, 7, 1), date(2026, 7, 3), today=date(2026, 6, 15)) returns 2026-07-01T06:00:00Z and 2026-07-04T06:00:00Z.",
      "files": [
        "apps/project-car/api/app/services/schedule_window.py"
      ],
      "check": "cd apps/project-car/api && python -c 'from datetime import date, datetime, timezone; from app.services.schedule_window import resolve_schedule_window; s,e=resolve_schedule_window(None, None, today=date(2026,6,15)); assert (s,e)==(datetime(2026,6,14,6,0,tzinfo=timezone.utc), datetime(2026,6,30,6,0,tzinfo=timezone.utc)); s2,e2=resolve_schedule_window(date(2026,7,1), date(2026,7,3), today=date(2026,6,15)); assert (s2,e2)==(datetime(2026,7,1,6,0,tzinfo=timezone.utc), datetime(2026,7,4,6,0,tzinfo=timezone.utc))'",
      "depends_on": [
        "r1"
      ],
      "est_lines": 28,
      "tests": 0,
      "api": [],
      "builds_requests": false,
      "integration": false
    },
    {
      "id": "r3",
      "goal": "Add read_schedule_window(session: Session, principal: Principal, *, window_start: datetime, window_end: datetime, limit: int) -> list[Booking] in apps/project-car/api/app/services/staff_schedule.py. Select Booking with selectinload(Booking.member) and selectinload(Booking.hoist), where start_at >= window_start and start_at < window_end, order_by Booking.start_at, limit(limit). Then record_action(session, principal=principal, action=\"read\", request_id=None, subject=StaffSubject.SCHEDULE) and return those rows. A row whose start_at equals window_end is excluded. limit=1 returns the earliest in-window row.",
      "files": [
        "apps/project-car/api/app/services/staff_schedule.py"
      ],
      "check": "cd apps/project-car/api && python -c 'from datetime import datetime, timedelta, timezone; from sqlalchemy import create_engine, select; from sqlalchemy.orm import sessionmaker; from app.auth import Principal; from app.models import Base, Booking, BookingKind, BookingStatus, Hoist, Member, MembershipTier, StaffAction, StaffSubject; from app.services.staff_schedule import read_schedule_window; engine=create_engine(\"sqlite://\"); Base.metadata.create_all(engine); s=sessionmaker(bind=engine)(); s.add(MembershipTier(name=\"basic\", display_name=\"Basic\")); s.flush(); m=Member(name=\"A\", email=\"a@example.com\", tier_name=\"basic\"); h=Hoist(name=\"Bay\"); s.add_all([m, h]); s.flush(); base=datetime(2026, 6, 1, tzinfo=timezone.utc); specs=[(timedelta(days=-10), \"past\"), (timedelta(days=1), \"in\"), (timedelta(days=2), \"later\"), (timedelta(days=5), \"edge\")]; [s.add(Booking(member_id=m.id, hoist_id=h.id, start_at=base+delta, end_at=base+delta+timedelta(hours=1), kind=BookingKind.CUSTOMER, status=BookingStatus.CONFIRMED, notes=note)) for delta, note in specs]; s.commit(); p=Principal(role=\"owner\", email=\"owner@example.com\"); kw=dict(window_start=base, window_end=base+timedelta(days=5)); one=read_schedule_window(s, p, limit=1, **kw); many=read_schedule_window(s, p, limit=10, **kw); assert [row.notes for row in one]==[\"in\"]; assert [row.notes for row in many]==[\"in\", \"later\"]; actions=list(s.scalars(select(StaffAction)).all()); assert len(actions)==2 and all(a.action==\"read\" and a.request_id is None and a.subject_kind==StaffSubject.SCHEDULE for a in actions)'",
      "depends_on": [
        "r1"
      ],
      "est_lines": 32,
      "tests": 0,
      "api": [],
      "builds_requests": false,
      "integration": false
    },
    {
      "id": "r4",
      "goal": "Change staff_schedule in apps/project-car/api/app/routers/staff.py to staff_schedule(session: DbSession, principal: Owner, window_start: date | None = Query(default=None), window_end: date | None = Query(default=None), limit: int = Query(default=200, ge=1, le=500)) -> list[BookingOut]. Call resolve_schedule_window(window_start, window_end, today=pricing_today()) and read_schedule_window(session, principal, window_start=start, window_end=end, limit=limit), then return BookingOut.from_booking for each row. GET /staff/schedule?limit=0 and GET /staff/schedule?limit=501 return 422 from the Query bounds before the body runs. The route no longer calls app.services.staff.read_schedule.",
      "files": [
        "apps/project-car/api/app/routers/staff.py"
      ],
      "check": "cd apps/project-car/api && python -m pytest tests/test_staff_schedule_window.py::test_staff_schedule_is_windowed_and_capped -q && grep -q 422 tests/test_staff_schedule_window.py",
      "depends_on": [
        "r1",
        "r2",
        "r3"
      ],
      "est_lines": 22,
      "tests": 0,
      "api": [
        {
          "method": "GET",
          "path": "/staff/schedule"
        }
      ],
      "builds_requests": false,
      "integration": true
    }
  ]
}
```

| id | file | depends_on | est_lines | tests | calibrated | check |
| --- | --- | --- | --- | --- | --- | --- |
| r1 | `apps/project-car/api/tests/test_staff_schedule_window.py` | — | 52 | 1 | 54.6 | Test file defines `test_staff_schedule_is_windowed_and_capped`, `{"limit": 0}`, and `422`. |
| r2 | `apps/project-car/api/app/services/schedule_window.py` | r1 | 28 | 0 | 47.6 | `resolve_schedule_window` defaults for 2026-06-15 and an explicit 1–3 Jul window. |
| r3 | `apps/project-car/api/app/services/staff_schedule.py` | r1 | 32 | 0 | 54.4 | `read_schedule_window` drops `past` and `edge`, `limit=1` returns `in`, and writes two `SCHEDULE` reads. |
| r4 | `apps/project-car/api/app/routers/staff.py` | r1, r2, r3 | 22 | 0 | 37.4 | `pytest` `test_staff_schedule_is_windowed_and_capped` (200 rows, no 60-day booking, `limit=0` is 422). |

`app/services/staff.py` is open in pull request 283 and `tests/test_staff_actions.py` is open in pull requests 282 and 283, so those paths are not rows. `read_schedule` stays `select(Booking).order_by(start_at)` with no window and no limit. `staff_schedule` stops calling it. `test_ai_reads_schedule_balance_and_open_requests` books via `_window(5)` (5 hours ahead), which stays inside today−1 … today+14.
