# Status — 2026-09-06 ~11:52 America/Edmonton

Living one-pager: what’s live, what’s next, locks. Product detail stays in the start-here specs. Stay-up / CORS / Pages runbooks live elsewhere — this file is not a runbook.

---

## Live

- **Brochure:** https://projectcar.ca and https://www.projectcar.ca. Origin: Cloudflare Worker **`projectcar-brochure`** Direct Upload of `apps/website/html` from `main`. Classic Pages git is skipped for now. Not the Doc `:8088` tunnel. Apex deferred.
- **Pages:** Home, About, The Shop, Membership, Roadmap, Contact. Chat nav/page stripped (PR #5). Apex deferred.
- **Brochure hygiene:** P0-3…P0-7 is in git (`apps/website/html`: robots, sitemap, `404.html`, favicon set, Home progress bar removed) **and already live** on the Worker (re-uploaded 2026-09-06). Classic Pages git still skipped.
- **Waitlist:** Membership / Contact `POST` JSON to `https://api.projectcar.ca/waitlist`. CORS allowlist includes `https://projectcar.ca`, `https://www.projectcar.ca`, localhost, and **`https://app.projectcar.ca`**. **e2e PASS.** See `cors-origins.md`.
- **Shop API:** `api.projectcar.ca` = Cloudflare tunnel → Doc `localhost:8000`. Primary stay-up: LaunchAgent `com.projectcar.shop-api` (KeepAlive) → `~/hermes-tools/mission-control/shop-api/run-shop-api.sh` → uvicorn `:8000`. Public `GET /health` **200**. Lid-close / sleep still kills the Mac. See `api-stay-up.md`.
- **Public shop UI:** **`https://app.projectcar.ca` is LIVE** (Ben GO ~11:41). Zone Cloudflare tunnel + DNS/SSL → Doc shop UI `:3000`. KeepAlive `com.projectcar.shop-web` running. Tunnel origin preferred `http://127.0.0.1:3000` (not bare localhost) after IPv6 `[::1]` 502; KeepAlive bind hostname `::` (dual-stack). Doc checkout is `main` `58827f0` (PR #16 — honor public host on shop UI middleware redirects). Public probes: `/` → login **200** on the app host; `/login` **200**. Still the Doc demo — not a shop opening.
- **Owner booking (live on Doc + public app host):** duration × band × overlay is on `main` (PR #12) and **live on Doc** — Owner UI `:3000` — **and reachable via `https://app.projectcar.ca`**. Shop OS seed: **6 hoists** (one shop-priority) and **Basic 1000 / Premium 1500**. Demo session cookies — **not OIDC**. No Stripe. The shop is not open.
- **Member self-serve (live on Doc demo + public app host):** PR #14 merged → `main` `9baf3c4` and walked on Doc; now also reachable via `https://app.projectcar.ca`. Member login (seed `ada.reyes@example.com`); `/member/me` balance + ledger; `/member/hoists` + schedule on **Bays 1–5 only**; shop hoist Owner-only (`400 shop_hoist_owner_only`). Demo session cookie (`pc_member_session`) — **not OIDC**. No Stripe. The shop is not open.

---

## Next

1. **Mission Control cockpit** still needs **Ben GO** before start. Owner + Member booking are live on Doc **and** on the public app host — that earlier hold is satisfied. Do not start the cockpit in this PR.
2. Staff **OIDC** can follow the Member session stub. Do not dump the rest of v2 here.
3. Payments / Stripe: later. No “shop is open.”
4. Public Apex chat: **deferred (Ben)**. Not P0. Do not revive.
5. **Token pricing** v1 is landed for Owner **and** Member booking — same `token-pricing.md` engine. Defaults are Owner-editable placeholders, not public prices.

---

## Later (not v1)

- Member-to-member hoist time trades/offers — bookings should not be glued to one member forever (transferable booking or trade-offer entity). Design note only; do not design the trade system now.
- Member booking assistant (Ben later-want) — a bot that helps members book hoist dates. Same Later bucket as trades. After Member UI is solid; likely Grok / Apex-replacement public chat lane, **not** Owner admin. Do **not** build in current Shop OS slices.

---

## Locks (unchanged)

- No Stripe. No “shop is open” claims. No live pricing until Ben says so.
- Token pricing v1 is locked: bands + overlay in `America/Regina` — `token-pricing.md`. Defaults are Owner-editable placeholders, not public prices. Allotments: **Basic 1000 / Premium 1500** per period. Two tiers only (no Pro, no Weekly).
- **6 hoists** in calendar/seed. Exactly one is the shop hoist (`is_shop`). **v1 = (A) Owner-only** — customers cannot book it (`400 shop_hoist_owner_only`). **(B) bumpable** (customers book it, shop work displaces them) is a later tweak only. See `token-pricing.md`. No Stripe. The shop is not open.
- Mission Control cockpit needs **Ben GO** before start. Do not start the cockpit from a docs PR.
- Shop members never get Nextcloud accounts.
- No n8n.

Specs: `project-car-application-specification.md` §13, `token-pricing.md`, `website-webapp-specification.md`, `platform-architecture.md`.
