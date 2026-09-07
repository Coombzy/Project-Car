# Status — 2026-09-07

Living one-pager: what’s live, what’s next, locks. Product detail stays in the start-here specs. Stay-up / CORS / brochure-deploy runbooks live elsewhere — this file is not a runbook. Living ops: [doc-lid-restore.md](doc-lid-restore.md) · [shop-web-stay-up.md](shop-web-stay-up.md) · [api-stay-up.md](api-stay-up.md) · [brochure-worker-deploy.md](brochure-worker-deploy.md). Member host cutover (plan only): [member-host-cutover.md](member-host-cutover.md). Member edge / path-split (plan only; **Ben GO**): [member-zone-edge.md](member-zone-edge.md). Brochure → Classic Pages git (plan only; skipped until CF ↔ GitHub auth; outranked by Next #1 + Member edge): [brochure-pages-cutover.md](brochure-pages-cutover.md). Proposed public-MVP cut-vs-keep (draft, not a Ben lock): [ship-mvp-cut.md](ship-mvp-cut.md).

Reality tip: `main` **`0a614f3`** (after Docs tip-bump **#42**). Shop-web host allowlist **#36** (`f952cd3`) is on git. Docs **#30–#42** already on `main`. Last full product walk remains 2026-09-06 ~16:16 (Dashboard **#28** / `afb37f9` **LIVE on Doc**). **Doc pull/rebuild pending** — do **not** claim #36 is live on Doc until Lead `git pull` + shop-web rebuild. Public tunneled hosts can still be morning **530 / 1033** (lid-close). Ordered restore: [doc-lid-restore.md](doc-lid-restore.md). Distinguishes **Live** vs **Next** vs **Later**, and **build-breadth (now)** vs **ship-MVP cut (later)**. Do not invent Stripe, a shop opening, a shipped Member host migration, a removed `app.` alias, or Matrix / Apex / Grok chat. **Chat v1** (human / polling / Owner-starts-rooms) and **Dashboard** (24h bay strips + todos + parts POs) are **LIVE on Doc**.

---

## Host split (LOCKED — Ben GO ~12:22; ops LIVE at edge ~12:55)

| Host | Role |
|------|------|
| **projectcar.ca / www** | **Customer app.** Brochure + waitlist are live today. Member self-serve booking / balance **migrates here** as a follow-up slice. |
| **ops.projectcar.ca** | **LIVE management hostname** at the edge (2026-09-06 ~12:55 America/Edmonton). Staff-on-shift / ops management UI. Owner uses it too. Staff login via OIDC later. **Not Owner-only.** Some clients still have **local DNS cache** that misses `ops.` — use `app.` or flush cache; do not treat that as “ops is not live.” |
| **app.projectcar.ca** | **Temporary alias** until Ben cuts this DNS. Still live on the same Doc shop UI (`:3000`). Do not treat `app.` as the intended name. **Not removed.** |
| **api.projectcar.ca** | Shop API. Public waitlist + authenticated Owner / Member. Tunnel → Doc `:8000`. Lead owns Doc `:8000`. |

Do **not** describe the management host as Owner-only. Staff will use `ops.` (OIDC later); Owner uses the same host.

**Today** the Member demo still lives on the shop UI at `/member` (reachable on **`ops.`** and the temporary **`app.`** alias). Do **not** claim the customer-host migration is shipped. “Member UI on projectcar.ca” is **Next**.

Private Mission Control stays off these hosts.

---

## Build breadth (now) vs Ship-MVP cut (later gate)

Ben / Chief lock. Two horizons — do **not** collapse them into one “v1 includes everything forever.”

| Horizon | Meaning |
|---------|---------|
| **Build breadth (now)** | Breadth-first **placeholders** / rough IA so layout can be ironed out. Put planned features in the app (Parts, Tools, job board, cams, calendar / fill, member surfaces, Payments, Chat v1 demo). Do **not** leave a planned surface out of the **build** for polish. A placeholder is not shipped product. |
| **Ship-MVP cut (later gate)** | At **public MVP release**, cut unfinished and unnecessary features. Do **not** ship every placeholder as the public product. What ships then is a later Ben cut — not “everything we sketched now.” Draft cut-vs-keep (proposed candidates, not a Ben lock): [ship-mvp-cut.md](ship-mvp-cut.md). |

Do not invent extra product from this table. Calendar heat-map / weekly per-hoist is on `main` (PR #18). Next-day fill is on `main` (PR #20). Breadth placeholders are on `main` (PR #21). Inventory prefixes are locked on `main` (PR #26: B1–B6 / TC / PT; CM later) — demo lists, not live checkout. Member parts is a **request desk** now; **full** purchasing is **Later**. **Chat v1** (human / polling / Owner-starts-rooms) is **LIVE on Doc** (PR #27) — not Matrix, not Apex, not Grok. **Dashboard** 24h strips + todos + parts POs are **LIVE on Doc** (PR #28).

---

## Live

- **Brochure:** https://projectcar.ca and https://www.projectcar.ca. Origin: Cloudflare Worker **`projectcar-brochure`** Direct Upload of `apps/website/html` from `main`. Classic Pages git is **skipped** pending Cloudflare ↔ GitHub auth — plan only: [brochure-pages-cutover.md](brochure-pages-cutover.md). Do not start Pages git from a docs PR. Not the Doc `:8088` tunnel. **Apex sidecar deferred** (brochure stays Pages/Worker). Standing re-deploy: `brochure-worker-deploy.md`.
- **Pages:** Home, About, The Shop, Membership, Roadmap, Contact. Chat nav/page stripped (PR #5). Apex deferred.
- **Brochure hygiene:** P0-3…P0-7 is in git (`apps/website/html`: robots, sitemap, `404.html`, favicon set, Home progress bar removed) **and already live** on the Worker (re-uploaded 2026-09-06). Classic Pages git still skipped (plan: `brochure-pages-cutover.md`).
- **Waitlist:** Membership / Contact `POST` JSON to `https://api.projectcar.ca/waitlist`. CORS allowlist includes brochure origins (`https://projectcar.ca`, `https://www.projectcar.ca`), localhost, **`https://ops.projectcar.ca`**, and the temporary alias **`https://app.projectcar.ca`**. **e2e PASS** (brochure → api). See `cors-origins.md`.
- **Lid-close / morning 530:** Soft **530 / 1033** on `api.` / `ops.` / `app.` after lid-close is expected. Amphetamine / plugged-in no-sleep is mitigation, not a guarantee (`doc-software-baseline.md`). Stay quiet and restore when Doc is reachable; ping Ben only if Doc will not wake / Grok Bot desktop is offline / the outage is prolonged. Ordered Lead sequence: [doc-lid-restore.md](doc-lid-restore.md). Zone only if local origin is healthy but public is still 1033. No edge flip, no CF↔GitHub re-ask, no Member GO.
- **Shop API:** `api.projectcar.ca` = Cloudflare tunnel → Doc `:8000` KeepAlive. Primary stay-up: LaunchAgent `com.projectcar.shop-api` → `~/hermes-tools/mission-control/shop-api/run-shop-api.sh` → uvicorn `:8000`. **Lead owns Doc `:8000`.** Do **not** hand uvicorn restarts to Chief. Public `GET /health` is **200 when Doc origin is up** — not a permanent guarantee. Lid-close / sleep (mornings included) still kills the Mac; the public edge then returns Cloudflare **502** or **530 / error 1033**. Lookout owns the live probe (`projectcar-api-health-watch`). See [api-stay-up.md](api-stay-up.md). Ordered restore: [doc-lid-restore.md](doc-lid-restore.md).
- **Ops management UI (LIVE at edge):** **`https://ops.projectcar.ca` is LIVE** (2026-09-06 ~12:55 America/Edmonton) **when Doc origin is up**. Zone Cloudflare tunnel v8 hostname `ops` → `http://127.0.0.1:3000` (same Doc shop UI as `app.`). KeepAlive `com.projectcar.shop-web` runs **`next start`** (not `next dev`) on Doc. Shop-web **BUILD** last recorded on Doc after Dashboard **#28** (`afb37f9`, `BUILD_ID` `5swmVz-T2CqKEQzTk1ifU`). **`main` tip `f952cd3` (#36 host allowlist) is on git, not yet on Doc** — pull/rebuild **pending**; do not call #36 live on Doc. Tunnel origin preferred `http://127.0.0.1:3000` (not bare localhost) after IPv6 `[::1]` 502. Public probes **when Doc origin is up**: `/` → `Location: https://ops.projectcar.ca/login` (no localhost hop); `/login` **200**. Lid-close / sleep (mornings included) still kills the Mac; the public edge then returns Cloudflare **502** or **530 / error 1033** — tunnel / lid-close, not a new product break. Lookout owns the live probe (same class as `projectcar-api-health-watch`). CORS includes `https://ops.projectcar.ca`. Some clients still have **flaky local DNS cache** for `ops.` — **use the `app.` alias**. Still the Doc demo — not a shop opening. Stay-up / rebuild / 1033-vs-flap: [shop-web-stay-up.md](shop-web-stay-up.md). Ordered restore: [doc-lid-restore.md](doc-lid-restore.md).
- **Temporary `app.` alias (still live, not removed):** **`https://app.projectcar.ca`** remains a **temporary alias** on the same Doc `:3000` origin until Ben cuts that DNS. Reachable **when Doc origin is up** (same morning **530 / 1033** class as ops — not a new product break). Do not treat the alias as gone.
- **Owner + Member booking + tokens (live):** duration × 100 × band × advance overlay in `America/Regina` is on `main` (PR #12 / #14) and **live on Doc** — shop UI `:3000` — **and reachable via `https://ops.projectcar.ca` and `https://app.projectcar.ca`**. Shop OS seed: **6 hoists** (one shop-priority, Owner-only bay) and **Basic 1000 / Premium 1500**. Demo session cookies — **not OIDC**. HTTPS ops/app demo requires **Secure** cookies (`COOKIE_SECURE` / `SHOP_COOKIE_SECURE`, PR #22). No Stripe. The shop is not open.
- **Member self-serve (demo, still `/member` on the shop UI):** PR #14 merged → `main` `9baf3c4` and walked on Doc; reachable via `https://ops.projectcar.ca/member` and `https://app.projectcar.ca/member`. Member login (seed `ada.reyes@example.com`); `/member/me` balance + ledger; `/member/hoists` + schedule on **Bays 1–5 only**; shop hoist Owner-only (`400 shop_hoist_owner_only`). Demo session cookie (`pc_member_session`) — **not OIDC**. **Not** migrated to projectcar.ca.
- **Calendar redesign (on `main`, PR #18):** Monthly = hoist-density heat-map vs 08:00–21:00. Weekly = **separate per-hoist hour grids**. Owner includes the shop hoist (Owner-only); Member is Bays 1–5. Create / quote / cancel unchanged.
- **Next-day fill (on `main`, PR #20):** leftover customer-bay hours tomorrow get a **10–25%** fill factor; urgency drives the cut. Notification outbox (email stub / later push / SMS). Management `/fill` on Doc demo (`ops.` + temporary `app.` alias). Explicit extra multiplier — not a change to the locked v1 band / overlay tables. See `token-pricing.md`. Not a public price. No Stripe.
- **Breadth-first placeholders (on `main`, PR #21 — demo UI only; Tools / Parts deepened in #26):** Ops on **`ops.`** and the temporary `app.` alias: `/parts` (PT stock + qty / reorder + POs — **not** the member catalog), `/tools` (B1–B6 bay kits + TC crib checkout stub + orders / requests / planned), `/jobs` (sample tasks **with token bounties**), `/cameras` (every cam + door logs + AI stubs), `/payments` (membership + parts billing stubs; **AI tracks by default**, humans on exceptions). Member (customer-facing `/member`): Parts **request desk** (PT / TC SKUs, not commerce), job board with token amounts, **primary camera only**. **Not** live purchasing, QR checkout, Frigate, Stripe, or claim/complete. Demo SKUs are labeled placeholder.
- **Schedule harden (on `main`, PR #24):** Owner `/schedule` and Member `/member/schedule` **fail-soft** if bookings list 500s — month heat-map + weekly grids still render. Windows are sent as **America/Regina instants (UTC ISO)** so FastAPI cannot 422 on naive wall-clock strings.
- **Inventory prefixes (on `main`, PR #26):** **B1–B6** / **TC** / **PT** locked (CM later). **B6 = shop hoist bay**, not `SH`. Demo lists only.
- **Shop OS Chat v1 (LIVE on Doc, PR #27):** Owner-start rooms; Member↔Ops; human polling. Owner/Ops `/chat` — see-all threads, **Owner-only create room**, mute. Member `/member/chat` — own rooms, reply, poll every few seconds while a thread is open. Logged-out `/chat` and `/member/chat` **auth-gate 307**. Seeded demo threads. **Not** live Matrix, **not** Apex, **not** Grok. Demo cookies. The shop is not open.
- **Dashboard 24h + todos (LIVE on Doc, PR #28):** Owner `/` shows **Bays 1–6** (Bay 6 = shop hoist) with every booked hour in the next **24 hours** (`America/Regina`) plus member + vehicle/notes. **No “Today’s bookings” list.** Personal to-dos (CRUD) + ICS / copy-event. Parts orders strip (PT SKU / ordered–shipped–in transit–received stubs). Member `/member` gets the same todos + only bays that member booked. Google / Apple **Connect** stubs only. Not a shop opening.

---

## Next (not shipped)

Two gates — do **not** collapse them into “v1 includes everything forever.” Calendar (#18), fill (#20), placeholders (#21), cookies (#22), Docs (#23 / #25 / **#30–#42**), schedule harden (#24), inventory (#26), Chat (#27), Dashboard (#28), and shop-web host allowlist (**#36**, `f952cd3`) are **on `main`** — they are not Next. **#36 is on `main` only** until Doc pull + rebuild. **`ops.projectcar.ca` is LIVE** at the edge. `app.` remains the temporary alias — do not cut it here.

| Gate | Meaning |
|------|---------|
| **Build breadth (now)** | Put planned features into the app as placeholders / rough IA (Parts, Tools, job board, cams, calendar / fill, member surfaces, Chat v1 demo, …) so layout can be ironed out. Placeholders are OK. Do **not** leave a planned surface out of the **build** for polish. |
| **Ship-MVP cut (later gate)** | Before the **public MVP** ship, cut unfinished and unnecessary features. Do **not** ship every placeholder as the public product. Draft table: [ship-mvp-cut.md](ship-mvp-cut.md). |

1. **Host migration — Member UI on projectcar.ca.** Customer surface (self-serve booking + balance) moves to **projectcar.ca**. Management stays on **`ops.`** (temporary `app.` alias still live). Today Member demo still lives on shop-UI `/member`. Cutover checklist (plan only — not shipped, no DNS, no `app.` cut): **`member-host-cutover.md`**. Zone path-split checklist (plan only — `/member*` → Doc `:3000`, everything else stays Worker): **`member-zone-edge.md`**. Garage (site) / Zone (path rules / tunnel hostname / CORS edge) wait for these docs **and Ben GO**. Do **not** execute the edge plan from a docs PR. Cutover planning outranks new breadth placeholders **and** Classic Pages git (`brochure-pages-cutover.md`). Do **not** claim this is shipped.
2. **Ben cuts the `app.` alias.** `ops.` is already LIVE at the edge. `app.` stays until Ben cuts that DNS. Do not remove the alias from docs or edge config in a docs PR.
3. **Chat follow-ons (not Chat v1).** Chat v1 human/polling/Owner-starts-rooms is **LIVE on Doc** (Live above). Later: Grok on **projectcar.ca**, assign / staff notes / escalate, websockets. **Apex sidecar stays deferred.** Do not revive Matrix.
4. **Mission Control cockpit** still needs **Ben GO** before start. Owner + Member booking are already live on Doc **and** the public ops / app hosts — that earlier hold is satisfied. Do not start the cockpit from a docs PR.
5. Staff **OIDC** later (on **`ops.`**). **Full Stripe later.** Public Apex chat **deferred (Ben)** — not P0; do not revive. Do not dump the rest of v2 here.
6. **Google Calendar two-way sync.** PR #28 shipped ICS download + “copy event” + a Connect Google / Apple stub (`GET /calendar/google/start` is `501` until `GOOGLE_OAUTH_*` is set). Token exchange and two-way event sync stay **Next**. Apple stays ICS import (no public OAuth in this slice).

Placeholder pages (Parts, Tools, Job board, Cameras, Payments) are **demo UI** (Live above). Item 5 still means **live Stripe / OIDC** — not the Payments placeholder. They do not rewrite calendar (#18) or drop fill (#20). Do not cut the `app.` alias here.

---

## Later (parked)

- Member-to-member hoist time trades/offers — bookings should not be glued to one member forever (transferable booking or trade-offer entity). Design note only; do not design the trade system now.
- Member booking assistant (Ben later-want) — a bot that helps members book hoist dates. Same Later bucket as trades. After Member UI is solid; likely Grok / Apex-replacement public chat lane, **not** Owner admin. Do **not** build in current Shop OS slices. Related to the planned chat dual surface (Next) — still not an implementation.
- **Member parts purchasing (full).** Member `/member/parts` is a **request desk** (build-breadth now) — PT stock or TC crib tool, not a cart. Ops Parts is PT qty / reorder + POs, not the member catalog. Full member purchasing is **Later**. Do not claim a shop is selling parts. Flag `pc.marketplace` stays **off**.
- **Job board claim / complete / assign** — workflow is Later. Placeholder board with sample token-paid chores is what shipped.
- **Live Frigate (or equivalent NVR)** — flag `pc.cameras` stays **off** until wired. Occupancy is a **hint, not source of truth**. Door logs ops-only.
- **Live tool inventory / QR / checkout / hardware** — prefix model is locked (below); ops `/tools` lists are demo SKUs. Return mail, overdue workflow, and readers stay Later.
- **Consumables (`CM`)** — prefix reserved. Full CM desk Later. Trivial stub note only.
- **Stripe / live billing** — ops Payments placeholder (membership + parts; AI default, human on exceptions) is IA only. `pc.payments` stays **off**. Full Stripe is Later. AI tracks payments by default; humans get alerts on exceptions.

---

## Locks

- **Host split** is locked (table above). Customer = `projectcar.ca` / www. Management = **`ops.projectcar.ca`** (LIVE at edge; staff-on-shift, not Owner-only). `app.` is a **temporary alias** until Ben cuts that DNS — **not removed**. Local DNS cache on some clients is not a product rollback — use `app.`.
- **IA freeze.** Ben is happy with the current app direction. Do **not** start major IA reshuffles.
- **Build breadth (now)** and **Ship-MVP cut (later gate)** are **two locks** (tables above). Build = placeholders in the app for IA. Public MVP = later cut of unfinished / unnecessary. Do **not** read this as “v1 includes everything forever.” Proposed keep vs cut (draft): [ship-mvp-cut.md](ship-mvp-cut.md).
- **Inventory prefixes (LOCKED — Ben + Chief):** **B1–B6** = resident bay hand-tool kits (one kit per hoist/bay). **B6 = shop hoist bay** — same B-scheme as other bays, **not `SH`**. **TC** = tool-crib specialty tools (checkout / return / overdue). **PT** = parts inventory (stock, PO, member requests). **CM** = consumables **later** (do not build a full CM UI now). SKU shape `PREFIX-CATEGORY-NNN` (category may include extra hyphen segments): `B2-WR-014`, `TC-TQ-003`, `PT-OIL-5W30-012`. Bay-resident tools stay on the cart (no crib checkout). Crib tools check out. Parts are qty / reorder + requests — not tool checkout and not member commerce. Demo UI / seed SKUs only until a thin API lands. Existing `tools` table (`name` / `part_number`) stays schema-only in this slice.
- **Ops sections (locked IA, placeholders now):** **Parts** (PT list + POs) and **Tools** (B1–B6 lists + TC checkout stub, plus orders / requests / planned). Not a claim that inventory or purchasing is shipped.
- **Job board (locked IA, placeholder now):** shop chores (cleaning, tool maintenance, random upkeep). Ops posts a **token bounty**; member claim/complete credits the **append-only token ledger** (same tokens as hoist booking, **not Stripe**). Placeholder must show sample amounts. Full workflow Later.
- **Cameras (locked IA, placeholder now):** members = **one primary shop cam**. Ops = **all cams** + door entry logs + Frigate / AI collection. Not a claim that Frigate is wired on `main`.
- **Member parts / tool requests** = request desk now; **full purchasing Later**. No member Tools nav.
- **Chat v1** = human messaging + polling. **Owners start rooms.** Members reply in rooms they are in. Ops/Owner see-all + mute. Dual surfaces `/chat` and `/member/chat`. No AI/Grok/Matrix bridge. Not the brochure Chat page (still stripped). Apex sidecar **deferred**.
- No Stripe. No “shop is open” claims. No live public pricing until Ben says so.
- Token pricing v1 is locked: bands + overlay in `America/Regina` — `token-pricing.md`. `hours × 100 × band × overlay × fill`. Defaults are Owner-editable placeholders, not public prices. Allotments: **Basic 1000 / Premium 1500** per period. Two tiers only (no Pro, no Weekly). Fill is an explicit extra factor (10–25%), not a rewrite of the overlay table.
- **6 hoists** in calendar/seed. Exactly one is the shop hoist (`is_shop`) — **Bay 6**. **v1 = (A) Owner-only** — customers cannot book that **bay** (`400 shop_hoist_owner_only`). **(B) bumpable** is a later tweak only. See `token-pricing.md`. Owner Dashboard is Bays 1–6 next-24h strips; no “Today’s bookings” list.
- HTTPS ops/app Doc demo requires **Secure** session cookies (`COOKIE_SECURE` / `SHOP_COOKIE_SECURE`). Demo cookies — **not OIDC**.
- Shop-web KeepAlive on Doc uses **`next start`**, not `next dev`. See [shop-web-stay-up.md](shop-web-stay-up.md).
- Mission Control cockpit needs **Ben GO** before start. Do not start the cockpit from a docs PR.
- Do not revive Apex. Brochure stays Worker / Pages — no Apex sidecar.
- Shop members never get Nextcloud accounts.
- No n8n.
- **Lead owns Doc `:8000`.** Do not hand uvicorn restarts to Chief.
- **Ops Parts** is PT stock + PO tracker — distinct from `/member/parts` (requests only).
- **Payments (ops):** membership + parts. AI tracks by default; humans on exceptions. Placeholder only. Stripe Later.

Specs: `project-car-application-specification.md` §2 / §13 / §15 / §16 / §17, `token-pricing.md`, `website-webapp-specification.md`, `platform-architecture.md` §5.
