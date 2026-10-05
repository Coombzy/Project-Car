# Queue

Same name as pBay `Docs/queue.md`. This repo is second. Do not start a row here until the pBay queue says its rows are on `main`.

A row is done when it is on `main`. An open pull request is not done. A green check merges, then the next row starts in the same pass. One writer. Do not open a second agent on the same files.

Skipped facts are in `Docs/later.md`. They are not a stop.

Next rows, in order:

1. Merge green drafts in this order, one migration parent: bay-hour proof, token debit and cancel, parts request, crib checkout, job claim, shop-hoist request.
2. A member shop-hoist request stays pending until an Owner or an approved bot confirms it. A member cannot confirm their own. Bays 1 to 5 stay direct.
3. An approved bot can run the staff actions in `Docs/ai-control.md` and writes an audit row.
4. Public pages do not say the shop is open.

Do not deploy Doc. Do not add Stripe. Do not cut DNS.
