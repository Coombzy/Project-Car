# Handoff for Cortana: models.py split

## What was done
Assessed the largest source file in the repo (`apps/project-car/api/app/models.py`, ~50 KB) and wrote a concrete split plan.

## Documents on this branch (`docs/models-split-plan`)
- `Docs/models-split-plan.md` — full plan (target structure, incremental steps, related issues, rules).
- This handoff note.

## Key points
- Split into a package under `app/models/` with re-exports so existing imports keep working.
- Do it in small steps (base + enums first, then domain modules one at a time, bookings last).
- Each step is a small PR with a proof that imports still work and the test suite stays green.
- Related issues from the #283 review (balance drift, unique constraint, migration ordering, hard-coded stand-in) are listed with the proofs needed to close them.

## What to do next
- Review `Docs/models-split-plan.md`.
- Turn Step 1 (create the package and re-export) into a small proof-driven PR when ready.
- The split can run in parallel with the #283 slices.
- Do not mix new features into an extraction step.

## Constraints
- No behavior change.
- No new features in the same PR as an extraction.
- Do not edit `.github/workflows`.
- Prefer short prompts and diffs when using local models.
