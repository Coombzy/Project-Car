# Status — 2026-09-06

Living one-pager: what’s live, what’s next, locks. Product detail stays in the start-here specs. Stay-up / CORS / Pages runbooks live elsewhere — this file is not a runbook.

---

## Live

- **Brochure:** https://projectcar.ca and https://www.projectcar.ca. Origin: Cloudflare Worker **`projectcar-brochure`** Direct Upload of `apps/website/html` from `main` (PR #5). Classic Pages git is skipped for now. Not the Doc `:8088` tunnel.
- **Pages:** Home, About, The Shop, Membership, Roadmap, Contact. Chat nav/page stripped (PR #5). Apex deferred.
- **Waitlist:** Membership / Contact `POST` JSON to `https://api.projectcar.ca/waitlist`. CORS allowlist includes `https://projectcar.ca`, `https://www.projectcar.ca`, and localhost. **e2e PASS.** See `cors-origins.md`.
- **Shop API:** `api.projectcar.ca` = Cloudflare tunnel → Doc `localhost:8000`. Primary stay-up: LaunchAgent `com.projectcar.shop-api` (KeepAlive) → `~/hermes-tools/mission-control/shop-api/run-shop-api.sh` → uvicorn `:8000`. Lid-close / sleep still kills the Mac. See `api-stay-up.md`.
- **Shop OS on `main` (PR #2 + #3 + later):** public waitlist path; Owner API + Next.js UI under `apps/project-car/` — tiers, members, hoists, bookings, append-only token ledger, dashboard / week schedule. Seed: **6 hoists** (one shop-priority) and **Basic 1000 / Premium 1500**. **Not** claimed live on `app.projectcar.ca`. The shop is not open.
- **Member self-serve (demo, this slice):** Member session cookie (`pc_member_session`) parallel to Owner. Seeded Member (`ada.reyes@example.com` / `changeme`) can see their token balance + ledger, quote duration × band × overlay, and book / confirm / cancel on **Bays 1–5 only**. Shop hoist stays Owner-only (`400 shop_hoist_owner_only`). Not OIDC — Staff OIDC can follow. **Not** claimed live on `app.projectcar.ca`.

---

## Next

1. **Owner booking live** on Doc / `app.projectcar.ca`. Duration pricing (hours × 100 × band × overlay) is **in the Owner API + schedule** — not claimed live on `app.projectcar.ca` yet.
2. **Member self-serve** is **in git** (balance + book/cancel + schedule quote; Member session cookie). Harden + walk it on Doc after merge. Not claimed live on `app.projectcar.ca`. Staff OIDC can follow; do not dump the rest of v2 here.
3. Hold **Mission Control cockpit** until Owner booking is merged **and** live on Doc. Do not start the cockpit early.
4. Brochure hygiene P0-3…P0-7 is **in git** (`apps/website/html`: robots, sitemap, `404.html`, favicon set, Home progress bar removed). Live Worker picks it up on the next Direct Upload (Zone). Classic Pages git still skipped.
5. Public Apex chat: **deferred (Ben)**. Not P0. Do not revive.
6. Payments / Stripe: later. Staff login (OIDC) can follow the Member session stub; do not dump the rest of v2 here.
7. **Token pricing** v1 is landed for Owner **and** Member booking — same `token-pricing.md` engine. Defaults are Owner-editable placeholders, not public prices.

---

## Later (not v1)

- Member-to-member hoist time trades/offers — bookings should not be glued to one member forever (transferable booking or trade-offer entity). Design note only; do not design the trade system now.

---

## Locks (unchanged)

- No Stripe. No “shop is open” claims. No live pricing until Ben says so.
- Token pricing v1 is locked: bands + overlay in `America/Regina` — `token-pricing.md`. Defaults are Owner-editable placeholders, not public prices. Allotments: **Basic 1000 / Premium 1500** per period. Two tiers only (no Pro, no Weekly).
- **6 hoists** in calendar/seed. Exactly one is the shop hoist (`is_shop`). **v1 = (A) Owner-only** — customers cannot book it (`400 shop_hoist_owner_only`). **(B) bumpable** (customers book it, shop work displaces them) is a later tweak only. See `token-pricing.md`. No Stripe. The shop is not open.
- Hold the Mission Control cockpit until Owner booking is merged **and** live on Doc.
- Shop members never get Nextcloud accounts.
- No n8n.

Specs: `project-car-application-specification.md` §13, `token-pricing.md`, `website-webapp-specification.md`, `platform-architecture.md`.
