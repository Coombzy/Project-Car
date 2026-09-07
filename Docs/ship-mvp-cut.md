# Ship-MVP cut — proposed keep vs cut (draft)

**Status:** Draft planning doc — **not** a Ben decision lock  
**Updated:** 2026-09-07  
**Related:** `STATUS.md` (Ship-MVP cut later gate; Next #1), `member-host-cutover.md`, `project-car-application-specification.md` §11 / §15 / §16, `platform-architecture.md` §5, `token-pricing.md`

Propose a **cut-vs-keep** table for the **public MVP gate** (`STATUS.md` “Ship-MVP cut (later gate)”). Purpose: **stop polishing cut-candidates** before STATUS Next #1 — Member UI on **projectcar.ca** (`member-host-cutover.md`; **Ben GO** for execution).

This file does **not** ship product, change DNS, cut `app.`, or start Garage / Zone fan-out. It does **not** invent Stripe live, a shop opening, a shipped Member host migration, or a Ben-approved cut. What actually ships at public MVP is a **later Ben cut**. Rows below are **proposed** candidates aligned with STATUS Later + build-breadth locks.

**Two gates stay two gates.** Build-breadth placeholders stay in the app so IA can freeze. Public MVP is a later cut of unfinished / unnecessary — not “everything we sketched now.”

---

## How to read the proposal column

| Label | Meaning in this draft |
|-------|------------------------|
| **KEEP** | Must stay, or land before / at public MVP. Do not drop for polish. |
| **KEEP-thin** | Leave the existing demo / placeholder. Do **not** deepen it before Member host migration. |
| **CUT** | Do not ship as public product. Hide or drop the unfinished surface at the later Ben cut — do not polish it now. |
| **DEFER** | STATUS Later / parked. No implementation work before Next #1. Not a public-MVP build target. |

A row can be **KEEP-thin** (the IA shell stays) and **DEFER** (the real workflow). The proposal cell is the action for **right now** and for **public MVP intent**.

---

## Keep-path (must stay / land before or at MVP)

Do **not** trade these away to “finish” a Later placeholder.

| Feature | Status today | MVP proposal | Why | Notes |
|---------|--------------|--------------|-----|-------|
| **Member host → projectcar.ca** | Still `/member` on ops/app shop-ui. Plan only. | **KEEP** | STATUS Next #1. Cutover planning outranks new breadth polish. | Checklist: `member-host-cutover.md`. **Ben GO** before Garage (site) / Zone (CF). This draft is not that GO. |
| **Token booking / hoist schedule** | Live on Doc + `ops.` / temp `app.`. Owner + Member self-serve on **Bays 1–5**; shop hoist **Owner-only** (`400 shop_hoist_owner_only`). Calendar #18 + fill #20 + harden #24. | **KEEP** | Core Shop OS. Public MVP without booking is not the product. | Token math locked: `token-pricing.md`. No Stripe. Shop not open. `(B) bumpable` stays Later. |
| **Brochure + waitlist** | Worker `projectcar-brochure` live. Waitlist e2e PASS → `api.projectcar.ca/waitlist`. | **KEEP** | Customer host already does this. Do not replace the Worker with shop-web. | Re-deploy: `brochure-worker-deploy.md`. Apex sidecar **deferred**. Classic Pages git is not an MVP blocker. |
| **Ops management on `ops.`** | `ops.projectcar.ca` LIVE at edge. Temp `app.` alias until Ben cuts DNS. | **KEEP** | Staff-on-shift host (not Owner-only). Member migrates off this host; ops stays. | Do **not** cut `app.` in this doc. Stay-up: `shop-web-stay-up.md`. |
| **Chat v1 human / polling** | LIVE on Doc (#27). Owner starts rooms; Member reply; poll. Dual `/chat` + `/member/chat`. | **KEEP** | Already the demo chat. Do **not** elevate to Matrix / AI / Grok. | Auth-gate 307 when logged out. Demo cookies. Follow-ons are DEFER below. |
| **Dashboard basics** | LIVE on Doc (#28). 24h bay strips (Bays 1–6), personal todos + ICS, parts PO strip. | **KEEP** | Demo IA already live. Do not rewrite. | No “Today’s bookings” list. Google / Apple Connect are stubs — two-way is not keep-path. |

---

## Cut / defer candidates (polish traps before Member host)

Explicit table for STATUS Later + build-breadth placeholders that are easy to over-build. **Do not polish these instead of Next #1.**

| Feature | Status today | MVP proposal | Why | Notes |
|---------|--------------|--------------|-----|-------|
| **Full member Parts commerce** | Member `/member/parts` = **request desk** (PT / TC). Ops `/parts` = PT qty / reorder + POs. Not a cart. | **DEFER** | STATUS Later. `pc.marketplace` **off**. Request desk is enough for IA. | Placeholder **KEEP-thin**. Do not invent member checkout or eBay. Marketplace / eBay specs are Later — do not implement from those files. |
| **Job board claim / complete / assign** | Placeholder boards with **sample token bounties** (`/jobs`, `/member/jobs`). No workflow. | **DEFER** | STATUS Later. Tokens are the hoist ledger, **not Stripe**. | Board **KEEP-thin** (amounts must stay visible). Do not build claim/complete/assign before cutover. |
| **Live Frigate / NVR / door logs wired** | Cameras **placeholder**. Members = one primary cam. Ops = all cams + door-log + AI stubs. | **DEFER** | STATUS Later. `pc.cameras` **off**. Occupancy is a hint, not source of truth. | Pages **KEEP-thin**. Do not wire Frigate / NVR / live door hardware. Calendar still owns the bay. |
| **Staff OIDC** | Demo session cookies (`pc_member_session` / Owner cookie). Secure cookies on HTTPS ops/app. | **DEFER** | STATUS Next/Later. Identity v1 is cookies. | Do not swap demo auth for Pocket ID / Authelia before Member host. `pc.member_login` stays **off**. |
| **Stripe / live billing** | Ops `/payments` placeholder (membership + parts; AI default, human on exceptions). | **DEFER** | STATUS Later. `pc.payments` **off**. No live processor. | Placeholder **KEEP-thin**. Do not claim Stripe is live. Token job bounties are not this table. Shop is not open. |
| **Chat AI / Grok / Matrix bridge** | Chat v1 human/polling LIVE. Brochure Chat page stripped. | **DEFER** | Do not elevate Chat v1. Matrix retired. Apex **deferred**. Not a public-MVP build. | Grok on projectcar.ca, assign / staff notes / escalate, websockets = Later. Member booking assistant = Later. Do not revive Matrix or Apex. |
| **CM consumables full desk** | Prefix **CM** reserved. Trivial stub note only. | **DEFER** | Inventory lock: do not build a full CM UI now. | Leave the prefix. No consumables desk before cutover (or at public MVP unless Ben later says so). |
| **QR tool hardware / live checkout readers** | Ops `/tools` = B1–B6 + TC crib **demo lists**. Prefixes locked (#26). | **DEFER** | STATUS Later. `pc.access_readers` **off**. | Lists **KEEP-thin**. No QR, NFC/FOB, return-mail, overdue workflow, or readers. No member Tools nav. |
| **Member booking assistant** | Not built. Ben later-want. | **DEFER** | STATUS Later. Same bucket as trades. After Member UI is solid. | Likely Grok / Apex-replacement public chat lane — **not** Owner admin. Do not build in current Shop OS slices. |
| **Hoist time trades / offers** | Design note only. | **DEFER** | STATUS Later. Do not design the trade system now. | Bookings stay glued to one member until a later Ben lock. |
| **Marketplace / eBay / estate-sale** | Specs exist; flagged Later / not v1. | **DEFER** | `pc.marketplace` **off**. Separate products. | Do not implement from `eBay-Automation-Module-Spec.md`, marketplace, or estate-sale specs. |
| **NFC / FOB check-in** | Door **entry log** stub on ops cameras page only. | **DEFER** | `pc.access_readers` **off**. v3 in the app spec. | Not a public-MVP gate. Do not polish door logs into a live reader. |
| **Google / Apple two-way calendar** | ICS + copy-event + Connect **stub** (`GET /calendar/google/start` → 501). | **DEFER** | STATUS Next #6 — outranked by Member host. | ICS **KEEP-thin**. Do not start OAuth / two-way sync to dodge cutover. Apple stays ICS import. |
| **Fill notify (push / SMS)** | Fill factor **shipped** (#20). Notification outbox = email stub. | **DEFER** (channels) | Fill math is keep-path. Extra channels are polish. | Do not build Twilio / push before Next #1. Not a public price. |
| **Waiver capture / v2 billing records** | Not built. | **DEFER** | App spec v2. Not the public-MVP keep-path. | Do not start a waiver desk as a substitute for Member host. |
| **Mission Control cockpit** | Parked. | **DEFER** | Needs **Ben GO**. Private hub, not Shop OS public MVP. | Do not start from a docs PR. Shop members never get Nextcloud accounts. |
| **Apex sidecar / brochure Chat page** | Brochure Chat stripped. Apex deferred (Ben). | **DEFER** | Already locked deferred. | Brochure stays Worker / Pages. Do not revive. |
| **Classic Pages git cutover** | Worker Direct Upload is live. Pages git skipped (CF ↔ GitHub auth). | **DEFER** | Not required for public MVP while Worker serves the brochure. | Zone owns CF. Not a Garage e2e rewrite. |
| **`app.` alias removal** | Temporary alias still live. | **DEFER** | STATUS Next #2. **Ben** cuts that DNS. | This doc does **not** cut `app.`. Ops stay-up still documents the alias. |

---

## Sequencing

1. **Now:** treat the DEFER / CUT rows as **do-not-polish**. IA freeze still allows the KEEP-thin shells to exist.
2. **Next #1:** Member → projectcar.ca per `member-host-cutover.md` after **Ben GO**. Garage = site; Zone = tunnel / DNS / CORS edge; Lead = Doc `:8000`.
3. **Later Ben cut:** public MVP feature set. Ben decides what disappears vs stays thin. This table is input, not the lock.
4. **Later still:** Next #2 (`app.` cut), OIDC, Stripe, NVR, hardware, Chat follow-ons — only when STATUS / Ben say so.

Cutover planning **outranks** new breadth placeholders. Calendar (#18), fill (#20), placeholders (#21), cookies (#22), schedule harden (#24), inventory (#26), Chat (#27), and Dashboard (#28) are already on `main`. Do not start another IA-deepening slice to dodge Member host.

---

## Locks (copy — do not weaken)

- **IA freeze.** Do not start major IA reshuffles.
- **Build-breadth ≠ ship-MVP.** Placeholders in the app are not the public product.
- **No Stripe.** `pc.payments` off. Do not claim live billing.
- **Shop is not open.** No live public pricing until Ben says so.
- **`app.` not cut in this doc.** Temporary alias stays until Ben cuts DNS.
- **Apex deferred.** Do not revive. Brochure stays Worker / Pages.
- **Lead owns Doc `:8000`.** Do not hand uvicorn restarts to Chief.
- **Zone owns Cloudflare** (tunnel / DNS / CORS edge).
- **Garage** owns site work after GO + waitlist e2e — not process restarts.
- Chat v1 stays human / polling. No Matrix. No Grok elevation.
- Inventory prefixes stay **B1–B6 / TC / PT**. **B6 = shop hoist bay**, not `SH`. **CM** later.
- 6 hoists; shop hoist Owner-only. Token bands + overlay + fill in `America/Regina`.

**Out of scope for this file:** app code, DNS, Garage/Zone fan-out, Ben GO, a locked public-MVP ship list.
