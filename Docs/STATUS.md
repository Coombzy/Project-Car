# Status — 2026-09-06 ~12:55 America/Edmonton

Living one-pager: what’s live, what’s next, locks. Product detail stays in the start-here specs. Stay-up / CORS / Pages runbooks live elsewhere — this file is not a runbook.

Write-up of today’s product discussion (Ben GO ~12:22; management hostname corrected via Master Chief) plus the **ops DNS cut** (~12:55). Distinguishes **Live** vs **Next** vs **Later**, and **build-breadth (now)** vs **ship-MVP cut (later)**. Do not invent Stripe, a shop opening, a shipped Member host migration, or a removed `app.` alias.

---

## Host split (LOCKED — Ben GO ~12:22; ops LIVE ~12:55)

| Host | Role |
|------|------|
| **projectcar.ca / www** | **Customer app.** Brochure + waitlist are live today. Member self-serve booking / balance **migrates here** as a follow-up slice. |
| **ops.projectcar.ca** | **LIVE management hostname** (2026-09-06 ~12:55 America/Edmonton). Staff-on-shift / ops management UI. Owner uses it too. Staff login via OIDC later. **Not Owner-only.** |
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
| **Build breadth (now)** | Breadth-first **placeholders** / rough IA so layout can be ironed out. Put planned features in the app (Parts, Tools, job board, cams, calendar / fill, member surfaces, Payments). Do **not** leave a planned surface out of the **build** for polish. A placeholder is not shipped product. |
| **Ship-MVP cut (later gate)** | At **public MVP release**, cut unfinished and unnecessary features. Do **not** ship every placeholder as the public product. What ships then is a later Ben cut — not “everything we sketched now.” |

Do not invent extra product from this table. Calendar heat-map / weekly per-hoist is on `main` (PR #18). Next-day fill is on `main` (PR #20). Member parts **purchasing** is a placeholder now; **full** purchasing is **Later**.

---

## Live

- **Brochure:** https://projectcar.ca and https://www.projectcar.ca. Origin: Cloudflare Worker **`projectcar-brochure`** Direct Upload of `apps/website/html` from `main`. Classic Pages git is skipped for now. Not the Doc `:8088` tunnel. Apex deferred.
- **Pages:** Home, About, The Shop, Membership, Roadmap, Contact. Chat nav/page stripped (PR #5). Apex deferred.
- **Brochure hygiene:** P0-3…P0-7 is in git (`apps/website/html`: robots, sitemap, `404.html`, favicon set, Home progress bar removed) **and already live** on the Worker (re-uploaded 2026-09-06). Classic Pages git still skipped.
- **Waitlist:** Membership / Contact `POST` JSON to `https://api.projectcar.ca/waitlist`. CORS allowlist includes brochure origins (`https://projectcar.ca`, `https://www.projectcar.ca`), localhost, **`https://ops.projectcar.ca`**, and the temporary alias **`https://app.projectcar.ca`**. **e2e PASS** (brochure). See `cors-origins.md`.
- **Shop API:** `api.projectcar.ca` = Cloudflare tunnel → Doc `:8000` KeepAlive. Primary stay-up: LaunchAgent `com.projectcar.shop-api` → `~/hermes-tools/mission-control/shop-api/run-shop-api.sh` → uvicorn `:8000`. **Lead owns Doc `:8000`.** Public `GET /health` **200**. Lid-close / sleep still kills the Mac. See `api-stay-up.md`.
- **Ops management UI (LIVE):** **`https://ops.projectcar.ca` is LIVE** (2026-09-06 ~12:55 America/Edmonton). Zone Cloudflare tunnel v8 hostname `ops` → `http://127.0.0.1:3000` (same Doc shop UI as `app.`). KeepAlive `com.projectcar.shop-web`. Tunnel origin preferred `http://127.0.0.1:3000` (not bare localhost) after IPv6 `[::1]` 502. Doc checkout includes `main` `58827f0` (PR #16 — honor public host on shop UI middleware redirects). Public probes: `/` → `Location: https://ops.projectcar.ca/login` (no localhost hop); `/login` **200**. CORS includes `https://ops.projectcar.ca`. Still the Doc demo — not a shop opening.
- **Temporary `app.` alias (still live, not removed):** **`https://app.projectcar.ca`** remains a **temporary alias** on the same Doc `:3000` origin until Ben cuts that DNS. Do not treat the alias as gone.
- **Ops booking (live on Doc + `ops.` + temporary `app.` alias):** duration × band × overlay is on `main` (PR #12) and **live on Doc** — shop UI `:3000` — **and reachable via `https://ops.projectcar.ca` and `https://app.projectcar.ca`**. Shop OS seed: **6 hoists** (one shop-priority, Owner-only bay) and **Basic 1000 / Premium 1500**. Demo session cookies — **not OIDC**. HTTPS ops/app demo requires **Secure** cookies (`COOKIE_SECURE` / `SHOP_COOKIE_SECURE`). No Stripe. The shop is not open.
- **Member self-serve (demo, still `/member` on the shop UI):** PR #14 merged → `main` `9baf3c4` and walked on Doc; reachable via `https://ops.projectcar.ca/member` and `https://app.projectcar.ca/member`. Member login (seed `ada.reyes@example.com`); `/member/me` balance + ledger; `/member/hoists` + schedule on **Bays 1–5 only**; shop hoist Owner-only (`400 shop_hoist_owner_only`). Demo session cookie (`pc_member_session`) — **not OIDC**. Secure cookies required on HTTPS ops/app. **Not** migrated to projectcar.ca. No Stripe. The shop is not open.
- **Token pricing engine (live for Owner + Member booking):** `hours × 100 × band × overlay` in `America/Regina`. Same `token-pricing.md` lock. Defaults are Owner-editable placeholders, **not** public brochure prices.
- **Breadth-first placeholders (demo UI only):** Ops on **`ops.`** and the temporary `app.` alias: `/parts` (ops-side shop/parts POs — **not** the member catalog), `/tools` (inventory / orders / member requests / planned purchases), `/jobs` (sample tasks **with token bounties**), `/cameras` (every cam + door logs + AI stubs), `/payments` (membership + parts billing stubs; AI tracks by default, humans on exceptions). Member (customer-facing `/member`): Parts placeholder, job board with token amounts, **primary camera only**. **Not** live purchasing, inventory, Frigate, Stripe, or claim/complete. The shop is not open.

---

## Next (in flight — Ben GO ~12:22)

Two gates — do **not** collapse them into “v1 includes everything forever.”

| Gate | Meaning |
|------|---------|
| **Build breadth (now)** | Put planned features into the app as placeholders / rough IA (Parts, Tools, job board, cams, calendar / fill, member surfaces, …) so layout can be ironed out. Placeholders are OK. Do **not** leave a planned surface out of the **build** for polish. |
| **Ship-MVP cut (later gate)** | Before the **public MVP** ship, cut unfinished and unnecessary features. Do **not** ship every placeholder as the public product. |

The numbered items below include calendar / fill (already on `main`) plus remaining Next (host migration). They are not a promise that every placeholder ships in MVP.

Calendar redesign is on `main` (#18). Fill landed on `main` as #20. This PR is placeholders only — do not rewrite calendar or drop fill. **`ops.projectcar.ca` is LIVE.** `app.` remains the temporary alias — do not cut it here.

1. **Calendar redesign (on `main`, PR #18).** Monthly = heat-map by hoist booking density vs 08:00–21:00. Weekly = **separate per-hoist hour grids** (not the old combined week table). Owner includes the shop hoist (Owner-only); Member is Bays 1–5. Create / quote / cancel unchanged. Fill chips and quote math from #20 stay. Do not rewrite this UI from a placeholders PR.
2. **Next-day open-slot fill (on `main`, PR #20).** Notify members (email stub / later push / SMS) of leftover hours with a **10–25%** fill factor on available hours. Urgency drives the discount (emptier / closer to start → bigger cut inside that range). Explicit extra multiplier — not a change to the locked v1 band / overlay tables. See `token-pricing.md`. Management `/fill` on Doc demo (`ops.` + temporary `app.` alias); notify targets members. Not a public price. No Stripe.
3. **Host migration — Member UI on projectcar.ca.** Customer surface (self-serve booking + balance) moves to **projectcar.ca**. Management stays on **`ops.`** (temporary `app.` alias still live). Today Member demo still lives on shop-UI `/member`. Do **not** claim this is shipped.
4. **Ben cuts the `app.` alias.** `ops.` is already LIVE. `app.` stays until Ben cuts that DNS. Do not remove the alias from docs or edge config in this PR.
5. **Mission Control cockpit** still needs **Ben GO** before start. Owner + Member booking are already live on Doc **and** the public ops / app hosts — that earlier hold is satisfied. Do not start the cockpit in this PR.
6. Staff **OIDC** later (on **`ops.`**). Payments / Stripe later. Public Apex chat **deferred (Ben)** — not P0; do not revive. Do not dump the rest of v2 here.

Placeholder pages (Parts, Tools, Job board, Cameras, Payments) are **demo UI** (Live above). Item 6 still means **live Stripe / OIDC** — not the Payments placeholder. They do not rewrite calendar (#18) or drop fill (#20). Do not cut the `app.` alias here.

---

## Later (parked)

- Member-to-member hoist time trades/offers — bookings should not be glued to one member forever (transferable booking or trade-offer entity). Design note only; do not design the trade system now.
- Member booking assistant (Ben later-want) — a bot that helps members book hoist dates. Same Later bucket as trades. After Member UI is solid; likely Grok / Apex-replacement public chat lane, **not** Owner admin. Do **not** build in current Shop OS slices.
- **Member parts purchasing (full).** Placeholder on the Parts surface is **build-breadth (now)**. Ops Parts is a PO tracker, not the member catalog. Full member purchasing is **Later**. Do not claim a shop is selling parts. Flag `pc.marketplace` stays **off**.
- **Job board claim / complete / assign** — workflow is Later. Placeholder board with sample token-paid chores is what shipped.
- **Live Frigate (or equivalent NVR)** — flag `pc.cameras` stays **off** until wired. Occupancy is a **hint, not source of truth**. Door logs ops-only.
- **Live tool inventory / QR / checkout** — ops Tools placeholders are IA only.
- **Stripe / live billing** — ops Payments placeholder (membership + parts; AI default, human on exceptions) is IA only. `pc.payments` stays **off**.

---

## Locks

- **Host split** is locked (table above). Customer = `projectcar.ca` / www. Management = **`ops.projectcar.ca`** (LIVE; staff-on-shift, not Owner-only). `app.` is a **temporary alias** until Ben cuts that DNS — **not removed**.
- **Build breadth (now)** and **Ship-MVP cut (later gate)** are **two locks** (tables above). Build = placeholders in the app for IA. Public MVP = later cut of unfinished / unnecessary. Do **not** read this as “v1 includes everything forever.”
- **Ops sections (locked IA, placeholders now):** **Parts** and **Tools**. Tools = tool inventory, tool orders, customer/member tool requests, planned tool purchases. Not a claim that inventory or purchasing is shipped.
- **Job board (locked IA, placeholder now):** shop chores (cleaning, tool maintenance, random upkeep). Ops posts a **token bounty**; member claim/complete credits the **append-only token ledger** (same tokens as hoist booking, **not Stripe**). Placeholder must show sample amounts. Full workflow Later.
- **Cameras (locked IA, placeholder now):** members = **one primary shop cam**. Ops = **all cams** + door entry logs + Frigate / AI collection. Not a claim that Frigate is wired on `main`.
- **Member parts purchasing** = placeholder now; **full Later**.
- No Stripe. No “shop is open” claims. No live public pricing until Ben says so.
- Token pricing v1 is locked: bands + overlay in `America/Regina` — `token-pricing.md`. `hours × 100 × band × overlay × fill`. Defaults are Owner-editable placeholders, not public prices. Allotments: **Basic 1000 / Premium 1500** per period. Two tiers only (no Pro, no Weekly). Fill is an explicit extra factor (10–25%), not a rewrite of the overlay table.
- **6 hoists** in calendar/seed. Exactly one is the shop hoist (`is_shop`). **v1 = (A) Owner-only** — customers cannot book that **bay** (`400 shop_hoist_owner_only`). **(B) bumpable** is a later tweak only. See `token-pricing.md`.
- HTTPS ops/app Doc demo requires **Secure** session cookies (`COOKIE_SECURE` / `SHOP_COOKIE_SECURE`). Demo cookies — **not OIDC**.
- Mission Control cockpit needs **Ben GO** before start. Do not start the cockpit from a docs PR.
- Do not revive Apex.
- Shop members never get Nextcloud accounts.
- No n8n.
- **Lead owns Doc `:8000`.**
- **Ops Parts** is a shop/parts PO tracker — distinct from `/member/parts`.
- **Payments (ops):** membership + parts. AI tracks by default; humans on exceptions. Placeholder only. Stripe Later.

Specs: `project-car-application-specification.md` §2 / §13 / §15 / §16, `token-pricing.md`, `website-webapp-specification.md`, `platform-architecture.md` §5.
