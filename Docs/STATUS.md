# Status — 2026-09-06

Living one-pager: what’s live, what’s next, locks. Product detail stays in the start-here specs. Stay-up / CORS / Pages runbooks live elsewhere — this file is not a runbook.

---

## Live

- **Brochure:** https://projectcar.ca and https://www.projectcar.ca. Origin: Cloudflare Worker **`projectcar-brochure`** Direct Upload of `apps/website/html` from `main` (PR #5). Classic Pages git is skipped for now. Not the Doc `:8088` tunnel.
- **Pages:** Home, About, The Shop, Membership, Roadmap, Contact. Chat nav/page stripped (PR #5). Apex deferred.
- **Waitlist:** Membership / Contact `POST` JSON to `https://api.projectcar.ca/waitlist`. CORS allowlist includes `https://projectcar.ca`, `https://www.projectcar.ca`, and localhost. **e2e PASS.** See `cors-origins.md`.
- **Shop API:** `api.projectcar.ca` = Cloudflare tunnel → Doc `localhost:8000`. Primary stay-up: LaunchAgent `com.projectcar.shop-api` (KeepAlive) → `~/hermes-tools/mission-control/shop-api/run-shop-api.sh` → uvicorn `:8000`. Lid-close / sleep still kills the Mac. See `api-stay-up.md`.
- **Shop OS on `main` (PR #2 + #3 + later):** public waitlist path; Owner API + Next.js UI under `apps/project-car/` — tiers, members, hoists, bookings, append-only token ledger, dashboard / week schedule. Seed: **6 hoists** (one shop-priority) and **Basic 1000 / Premium 1500**. **Not** claimed live on `app.projectcar.ca`. The shop is not open.

---

## Next

1. **Owner booking live** on Doc / `app.projectcar.ca`. Duration pricing (hours × 100 × band × overlay) is **in the Owner API + schedule** — not claimed live on `app.projectcar.ca` yet.
2. **Member self-serve booking + token balance UI** (+ Member auth / OIDC as needed) — first-class next slice after Owner live. Not buried under “later.” Token balance + hoist booking is a primary customer (Member) page. **Not shipped.** May unlock OIDC / Member auth earlier than a vague v2 dump.
3. Hold **Mission Control cockpit** until Owner booking is merged **and** live on Doc. Do not start the cockpit early.
4. Brochure hygiene P0-3…P0-7 is **in git** (`apps/website/html`: robots, sitemap, `404.html`, favicon set, Home progress bar removed). Live Worker picks it up on the next Direct Upload (Zone). Classic Pages git still skipped.
5. Public Apex chat: **deferred (Ben)**. Not P0. Do not revive.
6. Payments / Stripe: later. Staff login can follow Member auth; do not dump Member into a vague v2.
7. **Token pricing** v1 is **landed for Owner booking** — `token-pricing.md`. Member self-serve still not shipped. Pricing math will apply there the same way.

---

## Later (not v1)

- Member-to-member hoist time trades/offers — bookings should not be glued to one member forever (transferable booking or trade-offer entity). Design note only; do not design the trade system now.

---

## Locks (unchanged)

- No Stripe. No “shop is open” claims. No live pricing until Ben says so.
- Token pricing v1 is locked: bands + overlay in `America/Regina` — `token-pricing.md`. Defaults are Owner-editable placeholders, not public prices. Allotments: **Basic 1000 / Premium 1500** per period. Two tiers only (no Pro, no Weekly).
- **6 hoists** in calendar/seed. Exactly one is the shop hoist (`is_shop`). Shop/business work (`kind=shop`, Owner-only) has priority on that bay — customer bookings that overlap open shop work are rejected. No silent displacement. See `token-pricing.md`.
- Hold the Mission Control cockpit until Owner booking is merged **and** live on Doc.
- Shop members never get Nextcloud accounts.
- No n8n.

Specs: `project-car-application-specification.md` §13, `token-pricing.md`, `website-webapp-specification.md`, `platform-architecture.md`.
