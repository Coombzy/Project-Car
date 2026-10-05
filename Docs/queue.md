# Queue

Ben locked this on 2026-10-04. Project Car comes after pBay. Both keep moving.

A row is done when it is on `main`. An open pull request is not done. A green check merges, then the next row starts in the same pass. One writer. Do not open a second agent on the same files.

Do not deploy Doc. Do not upload the Worker. Do not cut DNS. Do not add Stripe. Do not say the shop is open.

Next rows, in order:

1. Merge green drafts: 98 parts request, 99 crib checkout, 101 job claim, 102 shop-hoist request. Add the one migration revision they need before `alembic upgrade head`.
2. A member can request the shop hoist. A human or an AI approves. No self-approve. No token debit until approval. Bays 1-5 stay a direct booking.
3. Two bookings cannot take the same bay hour.
4. A booking debits tokens and a cancel returns them.
5. Public pages do not say the shop is open.

Skipped facts stay in `Docs/later.md`. This file is the only queue. `Docs/work.md` points here.
