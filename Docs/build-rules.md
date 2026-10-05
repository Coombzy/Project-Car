# Build rules

Same instruction file as pBay `Docs/build-rules.md`. The proof tool is the shop test suite, not `npm run v0-proof`.

The suite is the sign-off. The writer does not sign off. A failing check cannot merge. A branch pass is not enough. The checks are `shop-api pytest` and `shop-web lint / typecheck / build`.

The failing proof runs before the feature code. The red output is in the pass. Then the code makes it green, in the same pull request. A reload must show the stored row.

Do not add a review note. Do not auto-apply review-bot comments. Do not add a review bot that merges its own suggestions.

No open pull request is not idle. Read `Docs/queue.md` and start the next row. A status check does not ping. A missing token is a skip. An unwritten local case is built the safe way and named in `Docs/later.md`.

Build leaves `passes` false until Ben has seen the screen. That does not stop the next row.

One writer on shared files. A second agent only gets a worktree that does not touch the same migration. One migration at a time. Do not add a review note for a pass.

Do not deploy Doc. Do not add Stripe. Do not say the shop is open. This repo is second only while pBay `Docs/queue.md` has an open row.
