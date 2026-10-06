# Build rules

Same instruction file as pBay `Docs/build-rules.md`. The proof tool is the shop test suite, not `npm run v0-proof`.

The suite is the sign-off. The writer does not sign off. The writer does not merge. Lead merges only after the check is green. A failing check cannot merge. A branch pass is not enough. The checks are `shop-api pytest` and `shop-web lint / typecheck / build`.

The failing proof runs before the feature code. The red output is in the pass. Then the code makes it green, in the same pull request. A reload must show the stored row.

sample rows are marked sample and are not counted by the proof.

Do not add a review note. Do not auto-apply review-bot comments. Do not add a review bot that merges its own suggestions.

No open pull request is not idle. Read `Docs/queue.md` and start the next row. A status check does not ping. A missing token is a skip. An unwritten local case is built the safe way and named in `Docs/later.md`.

Build leaves `passes` false until Ben has seen the screen. That does not stop the next row.

One writer on shared files. A second agent only gets a worktree that does not touch the same migration. One migration at a time. Do not add a review note for a pass.

Do not deploy Doc. Do not add Stripe. Do not say the shop is open. This repo is second only while pBay `Docs/queue.md` has an open row.

Every queue row states its baseline, its target, and what must not get worse.

Every pull request that touches the UI carries before and after screenshots in its body. Ben owns taste calls. A feature's `passes` stays false until Ben sees the window.

Agents do not give hour, day, or month estimates. Work is sized in rows.

Every launch prompt names the row's baseline, its target, what must not get worse, and the proof expected. The proof is the red sha, the green sha, and before and after screenshots for UI work.

One cloud agent per pull request. Rebases, CI fixes, and re-proofs go to that same agent. A new agent is only for a new row.

Lead opens the proof screenshots itself before merging. A caption, or an image that doesn't show the change, is not proof.

Proof images go in the PR body as hosted files, not committed to the branch. Reference screenshots that a visual check compares against, such as `apps/project-car/web/visual/screenshots/`, are test files and may live in the repo.

Never weaken, skip, or delete a failing check to make it pass. That includes raising the layout-shift or pixel-diff thresholds, or regenerating references to hide a real change, unless Ben has signed off on the visual change.

When the same cause shows up twice in `Docs/later.md`, Lead opens a docs PR that adds a rule here, so it doesn't happen a third time.
