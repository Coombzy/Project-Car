# Status — 2026-09-06 ~12:28 America/Edmonton

Living one-pager: what’s live, what’s next, locks. Product detail stays in the start-here specs. Stay-up / CORS / Pages runbooks live elsewhere — this file is not a runbook.

Write-up of today’s product discussion (Ben GO ~12:22; management hostname corrected via Master Chief). Distinguishes **Live** vs **Next** vs **Later**. Do not invent Stripe, a shop opening, a shipped Member host migration, or a live DNS cut to `ops.`.

---

## Host split (LOCKED — Ben GO ~12:22; hostname correction via Master Chief)

| Host | Role |
|------|------|
| **projectcar.ca / www** | **Customer app.** Brochure + waitlist are live today. Member self-serve booking / balance **migrates here** as a follow-up slice. |
| **ops.projectcar.ca** | **Intended management hostname.** Staff-on-shift / ops management UI. Owner uses it too. Staff login via OIDC later. **Naming lock only — no live DNS cut in this PR.** |
| **app.projectcar.ca** | **Temporary alias** until the DNS cut to `ops.`. Live today on the Doc tunnel (`:3000`). Do not treat `app.` as the intended name. |
| **api.projectcar.ca** | Shop API. Public waitlist + authenticated Owner / Member. Tunnel → Doc `:8000`. |

Do **not** describe the management host as Owner-only. Staff will use `ops.` (OIDC later); Owner uses the same host.

**Today** the Member demo still lives on the temporary `app.` alias (`/member`). Do **not** claim the customer-host migration is shipped. “Member UI on projectcar.ca” is **Next**.

Private Mission Control stays off these hosts.

---

## Live

- **Brochure:** https://projectcar.ca and https://www.projectcar.ca. Origin: Cloudflare Worker **`projectcar-brochure`** Direct Upload of `apps/website/html` from `main`. Classic Pages git is skipped for now. Not the Doc `:8088` tunnel. Apex deferred.
- **Pages:** Home, About, The Shop, Membership, Roadmap, Contact. Chat nav/page stripped (PR #5). Apex deferred.
- **Brochure hygiene:** P0-3…P0-7 is in git (`apps/website/html`: robots, sitemap, `404.html`, favicon set, Home progress bar removed) **and already live** on the Worker (re-uploaded 2026-09-06). Classic Pages git still skipped.
- **Waitlist:** Membership / Contact `POST` JSON to `https://api.projectcar.ca/waitlist`. CORS allowlist includes `https://projectcar.ca`, `https://www.projectcar.ca`, localhost, and **`https://app.projectcar.ca`**. **e2e PASS.** See `cors-origins.md`.
- **Shop API:** `api.projectcar.ca` = Cloudflare tunnel → Doc `:8000` KeepAlive. Primary stay-up: LaunchAgent `com.projectcar.shop-api` → `~/hermes-tools/mission-control/shop-api/run-shop-api.sh` → uvicorn `:8000`. Public `GET /health` **200**. Lid-close / sleep still kills the Mac. See `api-stay-up.md`.
- **Ops management UI (live today via temporary `app.` alias):** **`https://app.projectcar.ca` is LIVE** (Ben GO ~11:41) as the **temporary alias**. Zone Cloudflare tunnel + DNS/SSL → Doc shop UI `:3000`. KeepAlive `com.projectcar.shop-web`. Tunnel origin preferred `http://127.0.0.1:3000` (not bare localhost) after IPv6 `[::1]` 502. Doc checkout includes `main` `58827f0` (PR #16 — honor public host on shop UI middleware redirects). Public probes: `/` → login **200** on the alias; `/login` **200**. Intended hostname is **`ops.projectcar.ca`** — **not** cut over. Still the Doc demo — not a shop opening.
- **Ops booking (live on Doc + temporary `app.` alias):** duration × band × overlay is on `main` (PR #12) and **live on Doc** — shop UI `:3000` — **and reachable via `https://app.projectcar.ca`**. Shop OS seed: **6 hoists** (one shop-priority, Owner-only bay) and **Basic 1000 / Premium 1500**. Demo session cookies — **not OIDC**. No Stripe. The shop is not open.
- **Member self-serve (demo, still on temporary `app.` `/member`):** PR #14 merged → `main` `9baf3c4` and walked on Doc; currently reachable via `https://app.projectcar.ca/member`. Member login (seed `ada.reyes@example.com`); `/member/me` balance + ledger; `/member/hoists` + schedule on **Bays 1–5 only**; shop hoist Owner-only (`400 shop_hoist_owner_only`). Demo session cookie (`pc_member_session`) — **not OIDC**. **Not** migrated to projectcar.ca. No Stripe. The shop is not open.
- **Token pricing engine (live for Owner + Member booking):** `hours × 100 × band × overlay` in `America/Regina`. Same `token-pricing.md` lock. Defaults are Owner-editable placeholders, **not** public brochure prices.

---

## Next (in flight — Ben GO ~12:22)

Not shipped. Do not implement from a docs PR unless a later slice is GO’d. Calendar / fill are separate in-flight product locks — not this naming PR.

1. **Calendar redesign.** Monthly = heat-map by hoist booking density. Weekly = **separate per-hoist hour grids** (not the current combined week table with hoists as rows and days as columns). Live schedule today is still that combined week grid (`/schedule`, `/member/schedule`).
2. **Next-day open-slot fill.** Notify members (email / push / SMS) of leftover hours with a **10–25%** discount on available hours. Urgency drives the discount (emptier / closer to start → bigger cut inside that range). Not a change to the locked v1 advance overlay table — see `token-pricing.md`.
3. **Host migration — Member UI on projectcar.ca.** Customer surface (self-serve booking + balance) moves to **projectcar.ca**. Management stays on **`ops.`** (today reached via the temporary `app.` alias). Today Member demo still lives on `app.` `/member`. Do **not** claim this is shipped.
4. **DNS cut `app.` → `ops.`.** Naming is locked. **No live DNS cut in this PR.** When Zone cuts DNS, the management UI origin stays Doc `:3000`; the public hostname becomes `ops.projectcar.ca`. CORS / tunnel follow that cut — not here.
5. **Mission Control cockpit** still needs **Ben GO** before start. Owner + Member booking are already live on Doc **and** the temporary public alias — that earlier hold is satisfied. Do not start the cockpit in this PR.
6. Staff **OIDC** later (on **`ops.`**). Payments / Stripe later. Public Apex chat **deferred (Ben)** — not P0; do not revive. Do not dump the rest of v2 here.

---

## Later (parked)

- Member-to-member hoist time trades/offers — bookings should not be glued to one member forever (transferable booking or trade-offer entity). Design note only; do not design the trade system now.
- Member booking assistant (Ben later-want) — a bot that helps members book hoist dates. Same Later bucket as trades. After Member UI is solid; likely Grok / Apex-replacement public chat lane, **not** Owner admin. Do **not** build in current Shop OS slices.

---

## Locks

- **Host split** is locked (table above). Customer = `projectcar.ca` / www. Management = **`ops.projectcar.ca`**. `app.` is a **temporary alias** until DNS cut. Do not describe management as an Owner-only host. Do not ship the DNS cut or Member UI on projectcar.ca from this PR.
- No Stripe. No “shop is open” claims. No live public pricing until Ben says so.
- Token pricing v1 is locked: bands + overlay in `America/Regina` — `token-pricing.md`. `hours × 100 × band × overlay`. Defaults are Owner-editable placeholders, not public prices. Allotments: **Basic 1000 / Premium 1500** per period. Two tiers only (no Pro, no Weekly). Next-day fill **10–25%** is Next, not a v1 table change.
- **6 hoists** in calendar/seed. Exactly one is the shop hoist (`is_shop`). **v1 = (A) Owner-only** — customers cannot book that **bay** (`400 shop_hoist_owner_only`). **(B) bumpable** is a later tweak only. See `token-pricing.md`.
- Mission Control cockpit needs **Ben GO** before start. Do not start the cockpit from a docs PR.
- Do not revive Apex.
- Shop members never get Nextcloud accounts.
- No n8n.

Specs: `project-car-application-specification.md` §2 / §13 / §15, `token-pricing.md`, `website-webapp-specification.md`.
