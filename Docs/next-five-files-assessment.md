# Assessment of the next 5 largest source files

After `models.py` (~50 KB), these are the next largest non-test source files.

## 1. `apps/project-car/api/app/seed.py` (~38 KB)

**What it is**  
Demo data seeder for the shop OS. Creates tiers, members, hoists, bookings, token ledger rows, chat threads, todos, etc. for walkthroughs.

**Strengths**  
- Clear docstring explaining usage and what `--reset` does.  
- Uses stable UUIDs (`uuid5`) so demo data is reproducible.  
- Calls the real pricing and ledger services instead of hard-coding token amounts.

**Issues**  
- Large and procedural. Reset logic, booking creation, chat seeding, and todo seeding are all in one file.  
- Tightly coupled to many models and services. Any model change requires updates here.  
- Hard to test in isolation.

**Recommendation**  
Split by domain (tiers/members, bookings, chat, todos) into smaller seed modules. Keep a thin `seed.py` that orchestrates them. Low priority compared to models and services.

---

## 2. `apps/project-car/api/app/schemas.py` (~35 KB)

**What it is**  
Pydantic request/response models for the entire API (members, bookings, tokens, hoists, parts, todos, etc.).

**Strengths**  
- Consistent use of validators (strip, normalize email, blank-to-none).  
- Good caps on numeric fields.  
- `from_attributes` used where appropriate.

**Issues**  
- Another god file. Every new endpoint adds more models here.  
- Some duplication (similar strip/blank validators repeated across many classes).  
- BookingOut and related classes contain presentation logic (`from_booking`).

**Recommendation**  
Split by domain alongside the models split (`schemas/members.py`, `schemas/bookings.py`, etc.). Extract common validators into helpers. Medium priority.

---

## 3. `apps/project-car/api/app/services/bookings.py` (~25 KB, 694 lines, ~25 functions)

**What it is**  
Core booking business logic: create, confirm, cancel, settle no-shows, claim hours, peak/overlap checks, etc.

**Strengths**  
- Central place for booking rules.  
- Uses the hour-claiming and pricing services.

**Issues**  
- Growing into a second god file for booking behavior.  
- Mixes validation, state transitions, ledger writes, and hour claiming.  
- Hard for agents to modify safely without loading the whole file.

**Recommendation**  
Split by concern once the models are split:  
- `bookings/create.py`  
- `bookings/confirm_cancel.py`  
- `bookings/hours.py`  
- `bookings/settle.py`  
High value after the models split.

---

## 4. `apps/project-car/web/lib/shop-api.ts` (~24 KB, 728 lines, 81 exports)

**What it is**  
Frontend API client. One function per endpoint for both owner and member flows.

**Strengths**  
- Consistent `shopJson` / `memberJson` wrappers.  
- Clear separation of owner vs member session cookies.

**Issues**  
- Very long flat list of functions.  
- Easy for agents to miss an existing helper and duplicate a call.  
- No grouping by domain.

**Recommendation**  
Group into domain modules (`shop-api/members.ts`, `shop-api/bookings.ts`, etc.) and re-export from an index. Low-to-medium priority; mostly organizational.

---

## 5. `apps/project-car/api/app/services/staff.py` (~18 KB, 591 lines, ~31 functions)

**What it is**  
Staff desk actions: shop-hoist requests, parts requests, tool-crib exceptions, refunds, etc.

**Strengths**  
- Covers the owner-side operational workflows.

**Issues**  
- Another large service file that mixes many unrelated staff actions.  
- Similar growth pattern to bookings.py.

**Recommendation**  
Split by subject (shop hoist, parts, tool crib, refunds) when next touched. Medium priority.

---

## Summary

| File | Size | Main issue | Priority to split |
|------|------|------------|-------------------|
| seed.py | 38 KB | Procedural demo seeder | Low |
| schemas.py | 35 KB | God file of Pydantic models | Medium |
| services/bookings.py | 25 KB | Core logic becoming a second god file | High (after models) |
| web/lib/shop-api.ts | 24 KB | Flat list of 81 functions | Low-medium |
| services/staff.py | 18 KB | Mixed staff actions | Medium |

The highest-leverage next split after `models.py` is `services/bookings.py`, followed by `schemas.py`. The others can be done opportunistically when those areas are next modified.
