# Later

One ledger of skipped work and placeholders. A small roadblock does not stop the rest of Project Car.

**Updated:** 2026-10-04  
**Related:** [STATUS.md](STATUS.md)

There is no second list. Do not add `gaps.md`, `placeholders.md`, or another file of the same kind. If one appears, fold its rows here and delete it.

Open rows do not block other work.

## How a row closes

A row closes only when both are true:

1. The fix in that row has landed.
2. A proof names that row (the merge, commit, or smoke that did the fix).

Update this file in the same commit that changes a row. Point [STATUS.md](STATUS.md) at this file in the same commit that adds the pointer. Do not close a row from a plan, a queue, or from this file alone.

This ledger does not deploy to Doc, cut DNS, add Stripe, open the shop, or change live cookies or Zone. Doc stays at `795f301` until the Doc row’s fix lands.

## Rows

| Item | Fix that closes it | Proof |
|------|--------------------|-------|
| [PR #89](https://github.com/Coombzy/Project-Car/pull/89) still open | Ben merges it | |
| Zone member path-split not done ([member-zone-edge.md](member-zone-edge.md)) | Ben plus Zone | |
| Doc held at `795f301` | Ben says to pull. Do not deploy, cut DNS, add Stripe, or open the shop in this pass. | |
| Public demo owner password `owner@projectcar.ca` / `changeme` still present off loopback | Remove it and refuse those credentials off loopback | |
| Shop client that pipes member listings into pBay not started | A later pass, not this one | |
