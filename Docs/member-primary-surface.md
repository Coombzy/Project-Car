# Member primary surface — IA lock

**Status:** Living one-pager — product lock (IA only)  
**Locked:** 2026-09-06 (Ben GO)  
**Recorded:** 2026-09-18 (Lead standing GO — plan-improve bounce)  
**Related:** `STATUS.md` Next #1, `Docs/README.md` (start-here + living ops), `member-host-cutover.md`, `member-zone-edge.md`, `token-pricing.md`, `project-car-application-specification.md` §2 / §3

Locks Ben’s 2026-09-06 product decision: **Member token balance + self-serve hoist schedule** is the **primary customer-facing surface**. It is **not** Owner-only.

This file is an **IA lock**. It nests under existing STATUS **Next #1** (Member UI host migration to **projectcar.ca**). It does **not** replace `member-host-cutover.md` or `member-zone-edge.md`, and it is **not** that cutover.

Merging this file is **not** Member host cutover, **not** Doc unfreeze, **not** Stripe / shop-open, **not** Garage login / `changeme`, **not** Apex revive, and **not** vault retarget.

Do **not** invent Stripe, a shop opening, a shipped Member host migration, a removed `app.` alias, Matrix, or Apex revival. Demo session cookies stay demo cookies — **not OIDC**.

---

## Lock (do not weaken)

| Lock | Meaning |
|------|---------|
| **Primary customer page / functions** | A logged-in Member’s first job is **token balance** (own ledger cache) and **self-serve hoist booking / schedule** on **Bays 1–5**. That is the customer product. |
| **Not Owner-only** | Balance and customer-bay schedule are **Member self-serve**. Do **not** hide them behind Owner login or treat them as ops-only tools. Owner still has the management host (`ops.`; temporary `app.` alias). |
| **Shop hoist stays Owner-only** | Bay 6 / `is_shop` remains `400 shop_hoist_owner_only`. That is a **bay** lock (`token-pricing.md`), not a gate on the Member surface. |
| **IA freeze, not a reshuffle** | Do **not** start a major IA rewrite from this file. Record priority so reviewers do not need chat history. |
| **This file is not the cutover** | Host move to apex `projectcar.ca` stays STATUS Next #1 runbooks. **Ben GO** still required before Garage / Zone execute those files. |

---

## IA order (`/member` or the customer-host equivalent)

Same path unit after Next #1 (`/member` and `/member/*` on **projectcar.ca**). Today the demo still lives on shop-UI `/member` (`ops.` + temporary `app.`). Do **not** claim the customer-host migration is shipped.

| Priority | Surface | Role |
|----------|---------|------|
| **First** | **Balance** (`/member`) | Own token balance + ledger. Primary home. |
| **First** | **Schedule** (`/member/schedule`) | Book / quote / confirm / cancel on **Bays 1–5**. Shop hoist stays Owner-only. |
| **Secondary** | Parts (`/member/parts`) | Request desk (PT / TC). Not commerce. |
| **Secondary** | Jobs (`/member/jobs`) | Placeholder board with sample token amounts. Not claim/complete. |
| **Secondary** | Cams (`/member/cameras`) | Primary shop cam placeholder only. |

Chat v1 (`/member/chat`) is already a live dual surface (human / polling). It does **not** outrank Balance + Schedule and does **not** become the primary customer page.

Nav already leads with Balance then Schedule (`member-shell`). Keep that order. Parts / Jobs / Cams stay secondary placeholders (build-breadth now; ship-MVP cut later).

---

## Pointers (this file does not replace them)

| Need | Doc |
|------|-----|
| Member UI → apex `projectcar.ca` (plan only; **Ben GO**) | `member-host-cutover.md` |
| Zone path-split `/member*` on the customer host (plan only; **Ben GO**) | `member-zone-edge.md` |
| STATUS Next #1 + host split | `STATUS.md` |
| Docs catalog (start-here + living ops) | `Docs/README.md` |
| Token math / shop-hoist (A) | `token-pricing.md` |

Cutover planning still outranks new breadth polish. This lock tells Garage / reviewers **what** the customer surface is. Those runbooks tell **where** it moves and **how** the edge splits.

---

## Non-goals

Do **not** start these from this file. Merge is not permission.

| Out | Why |
|-----|-----|
| **Stripe / live billing** | Tokens are the shop ledger. `pc.payments` stays **off**. Full Stripe is Later. |
| **Shop-is-open claims** | Demo / waitlist only. The shop is not open. |
| **Owner-only gates on balance / schedule** | Members see their own balance and book customer bays themselves. Do not fold those functions into Owner-only ops. |
| **Apex revive** | Brochure stays Worker / Pages. Apex sidecar **deferred**. Do not revive Apex or Matrix. |
| **Soft-530 accounting** | Morning **530 / 1033** after lid-close is expected infrastructure (`doc-lid-restore.md`). Not a product defect and not a reason to rewrite Member IA. |
| **Host cutover / edge flip** | `member-host-cutover.md` / `member-zone-edge.md` after **Ben GO**. Not this PR. |
| **Doc unfreeze** | `doc-unfreeze.md` after **Ben GO**. Green Shop OS CI is **not** that GO. |
| **`app.` alias cut** | STATUS Next #2 — `app-alias-cut.md`. Member IA does **not** require cutting `app.` first. |
| **Garage login / `changeme`** | Not this lock. Do not execute shop credentials from a docs PR. |
| **Vault retarget** | Not this lock. |

---

## Done-when (this doc)

This file is done when **all** of these are true. **None** of them mean the Member host cutover shipped.

| # | Check |
|---|--------|
| 1 | Living-ops indexes link it: `STATUS.md` (living-ops), `deployment-guide.md` (stay-up / deploy table), `Docs/README.md` (start-here product lock + living ops). |
| 2 | Reviewers can see IA priority (**Balance + Schedule first**; Parts / Jobs / Cams secondary) without reading chat history. |
| 3 | Next #1 still points at `member-host-cutover.md` + `member-zone-edge.md` for the actual move. This file stays the IA lock only. |

**Out of scope for “done”:** DNS, Zone path rules, Doc pull/rebuild, Stripe, shop-open, Apex, vault, Garage login, amending held **#70** / **#75–#79** / **#81–#83**, folding STATUS Reality tip onto this PR.
