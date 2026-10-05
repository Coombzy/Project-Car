# Build rules

Same instruction file as pBay. The proof tool is the shop test suite.

Do not add a queue row that Ben has not asked for or that is not already in the docs. If fewer than three rows are open, copy the next planned local item from the shop docs. If none is left, ask Ben. Do not generate one.

Lead merges only when the shop checks are green. A red pull request stays open. The writer does not merge.

Write the failing proof, run it red, then write the code. The proof and the code land in the same commit. A reload must show the stored row. A sample row is marked sample and is not counted.

No open pull request is not idle. Read `Docs/queue.md`. This repo is second while pBay has an open row. A status check does not ping. A missing token is a skip.

One writer on shared files. One migration at a time. Do not add a review note for a pass.

Do not deploy Doc. Do not add Stripe. Do not say the shop is open.
