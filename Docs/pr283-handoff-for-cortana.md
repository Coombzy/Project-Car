# Handoff for Cortana: PR #283 slices

## What was done
PR #283 (member and owner booking screens) is too large to review or merge (153 files, stacked on the booking-rules branch, labeled queue:hold).

Instead of trying to land it, the useful pieces were extracted into small, proof-driven slices that can be implemented against `main`.

## Document location
- `Docs/pr283-slices.md` (this branch: `docs/pr283-slices`)
- Contains 7 slices with target, RED-first proof, acceptance criteria, files, dependencies, and a suggested order.

## Slices summary
1. Book creates and confirms in one submit
2. Member schedule shows active and overdue visits
3. Manual token adjustment sends typed reason as ledger note
4. Closing a bay requires a reason and refunds future bookings
5. "This week" returns to the current week
6. Signup mode (self-serve vs waitlist) and stand-in token purchase
7. Restore pure shop-error helpers and session redirects

## What to do next
- Review the slices in `Docs/pr283-slices.md`.
- Turn each slice into a normal backlog row or a small PR (RED then GREEN).
- Implement them one at a time, preferably with the local models or Grok Build for the code.
- Use the screenshots and UI checklist from #283 as reference.
- Leave #283 open on hold; do not merge it.
- Once the slices land, the older PRs that #283 superseded can be closed.

## Constraints
- Do not edit `.github/workflows`.
- Keep PRs small.
- Prefer diffs and short prompts when using local models.
- #283 stays as reference only.

This note and the slices doc are on branch `docs/pr283-slices`. A PR for the branch has been prepared so the docs can be reviewed and merged.
