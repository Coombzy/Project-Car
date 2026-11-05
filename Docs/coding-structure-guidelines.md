# Coding Structure Best Practices

Applies to all apps (Project Car, pBay, Liquid Estate, and any future apps).

These rules exist because large single files and stacked mega-PRs have already caused review difficulty, merge conflicts, and incomplete proofs. The goal is small, focused modules and small, proof-driven changes. The guidelines below combine project-specific lessons with well-known, tested practices.

## 1. File size and focus

- No source file should grow past ~15–20 KB without a clear reason.
- One primary responsibility per file (Single Responsibility Principle).
- If a file contains more than one domain (e.g. members + bookings + tokens), split it.
- Prefer many small files over one large file.

**Examples of what to avoid**
- A single `models.py` that holds the entire domain.
- A single `schemas.py` that holds every request/response model.
- A single service file that mixes create, confirm, cancel, settle, and ledger logic.

## 2. Package layout

Group by domain, not by technical type alone.

```
app/
  models/
    __init__.py          # re-exports so existing imports keep working
    base.py
    members.py
    bookings.py
    tokens.py
    ...
  schemas/
    __init__.py
    members.py
    bookings.py
    ...
  services/
    bookings/
      create.py
      confirm_cancel.py
      hours.py
      settle.py
    tokens.py
    ...
  routers/
    members.py
    bookings.py
    ...
```

- Keep a thin `__init__.py` that re-exports the public names so callers do not break.
- Do not put business logic in routers or models. Routers call services; services call models.
- Dependencies should point inward: routers → services → models. Services should not import from routers.

## 3. Models

- One domain concept (or a tightly related group) per module.
- Relationships and constraints stay with the models they belong to.
- Shared helpers (Base, enum helpers, JSON types) live in `base.py`.
- When adding a new column that is a derived sum or cache (e.g. `token_balance == allowance + purchased`), the service that writes it must have a proof that the invariant holds after every write.

## 4. Schemas (API models)

- Mirror the models split. Do not let schemas become a second god file.
- Extract repeated validators (strip, normalize email, blank-to-none) into small helpers (DRY).
- Keep presentation logic (e.g. `from_booking`) thin; prefer it on the schema or a small mapper, not buried in a giant file.

## 5. Services

- One main action or closely related set of actions per module.
- Booking create, confirm, cancel, hour claiming, and settlement should not all live in one file once the file grows.
- Ledger writes and balance updates belong in a dedicated token/ledger service with explicit invariant tests.
- Prefer pure functions or small classes that are easy to test in isolation.

## 6. Frontend API clients

- Group endpoint wrappers by domain (`shop-api/members.ts`, `shop-api/bookings.ts`, etc.).
- Re-export from an index so existing imports continue to work.
- Avoid a single 700+ line flat list of functions.

## 7. Changes and PRs

- Prefer small, proof-driven PRs (RED commit, then GREEN commit).
- One logical change per PR.
- Do not stack large feature branches on other large feature branches.
- If a change touches a file that is already over the size guideline, consider splitting it in the same PR or immediately after.
- Do not edit `.github/workflows` unless the change is specifically about CI and has been approved.
- YAGNI: do not add features, abstractions, or configuration that are not needed for the current slice.

## 8. Proofs and invariants

- Any new constraint or derived field needs a test that proves the invariant.
- Examples:
  - `token_balance == allowance_balance + purchased_balance` after every reserve/refund/purchase.
  - A second refund for the same booking fails as expected.
  - A refused book leaves no pending row.
- Prefer diffs and short prompts when using local models or agents.
- Tests should be deterministic and not depend on external services or the current time unless the time is injected.

## 9. Language and sharing

- Apps that share data shapes (ads, catalog, metrics) should share the same file and schema layout even if the codebases are still separate.
- When two apps need the same logic, extract it to a shared package rather than copying (DRY).
- Align on TypeScript for new shared code and front-ends where practical.

## 10. Naming and consistency

- Use clear, consistent names. Prefer full words over abbreviations except for well-known terms (id, url, utc).
- Boolean names should read as questions or states (`is_shop`, `has_bookings`, `can_cancel`).
- Functions that return data should be named for what they return (`get_member`, `list_bookings`). Functions that change state should be named for the action (`confirm_booking`, `adjust_tokens`).
- Keep the same terms across the stack (e.g. "booking" not mixed with "reservation" or "visit" unless there is a deliberate distinction).

## 11. Error handling

- Fail early with clear, specific errors.
- Do not swallow exceptions silently.
- User-facing messages should be helpful but not leak internal details.
- Prefer typed errors or consistent error codes so the front end can handle them predictably.

## 12. Review checklist (for agents and humans)

Before merging a PR, confirm:
- [ ] No new god file was created or significantly enlarged.
- [ ] The change is small enough to review.
- [ ] Required invariants have a proof.
- [ ] Existing tests still pass.
- [ ] The PR is not stacked on another large unmerged feature branch unless necessary.
- [ ] Names are clear and consistent with the rest of the codebase.
- [ ] No unnecessary abstraction or feature was added (YAGNI).

## Applying this to existing code

- `models.py`, `schemas.py`, `services/bookings.py`, and large API client files are the first candidates for splitting.
- Split incrementally with re-exports so behavior does not change.
- Use the existing split plans (`Docs/models-split-plan.md` and related) as the starting point for Project Car.
- Apply the same patterns to pBay and Liquid Estate as those codebases grow.

These guidelines are the default for all new work and for any refactoring of large files.
