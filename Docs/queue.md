# Queue

Same name as pBay `Docs/queue.md`. This repo is second. Do not start a row here until the pBay queue says its rows are on `main`.

A row is done when it is on `main`. An open pull request is not done. A green check merges, then the next row starts in the same pass. One writer. Do not open a second agent on the same files.

Skipped facts are in `Docs/later.md`. They are not a stop.

## Now

No open row.

## Already on main

The shop hoist request is on main at cea06d2. Migration `20261004_0011` revises `20261004_0010`. A member request stays pending until an Owner or an approved bot confirms it. A member cannot confirm their own. Bays 1 to 5 stay a direct booking. The proof reads the stored request. Staff actions in `Docs/ai-control.md` write an audit row. The proof is `apps/project-car/api/tests/test_staff_actions.py`. Public pages do not say the shop is open. Earlier merges on this chain: bay-hour eec9f01, token debit 66937b3, parts ef9263e, crib 0c58833, job claim 4488dab.

Do not deploy Doc. Do not add Stripe. Do not cut DNS.
