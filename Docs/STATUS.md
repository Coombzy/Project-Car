# Status — 2026-09-06

Living one-pager: what’s live, what’s next, locks. Product detail stays in the start-here specs. Stay-up / CORS / Pages runbooks live elsewhere — this file is not a runbook.

---

## Live

- **Brochure:** https://projectcar.ca and https://www.projectcar.ca. Origin: Cloudflare Worker **`projectcar-brochure`** Direct Upload of `apps/website/html` from `main` (PR #5). Classic Pages git is skipped for now. Not the Doc `:8088` tunnel.
- **Pages:** Home, About, The Shop, Membership, Roadmap, Contact. Chat nav/page stripped (PR #5). Apex deferred.
- **Waitlist:** Membership / Contact `POST` JSON to `https://api.projectcar.ca/waitlist`. CORS allowlist includes `https://projectcar.ca`, `https://www.projectcar.ca`, and localhost. **e2e PASS.** See `cors-origins.md`.
- **Shop API:** `api.projectcar.ca` = Cloudflare tunnel → Doc `localhost:8000`. Primary stay-up: LaunchAgent `com.projectcar.shop-api` (KeepAlive) → `~/hermes-tools/mission-control/shop-api/run-shop-api.sh` → uvicorn `:8000`. Lid-close / sleep still kills the Mac. See `api-stay-up.md`.
- **Shop OS on `main` (PR #2 + #3):** public waitlist path; Owner API + Next.js UI under `apps/project-car/` — tiers, members, hoists, bookings, append-only token ledger, dashboard / week schedule. **Not** claimed live on `app.projectcar.ca`.

---

## Next

1. **Owner booking hardened + live** on Doc / `app.projectcar.ca`.
2. Hold **Mission Control cockpit** until that booking path is live.
3. Brochure hygiene P0-3…P0-7 is **in git** (`apps/website/html`: robots, sitemap, `404.html`, favicon set, Home progress bar removed). Live Worker picks it up on the next Direct Upload (Zone). Classic Pages git still skipped.
4. Public Apex chat: **deferred (Ben)**. Not P0. Do not revive.
5. Staff / Member login and payments: later.
6. **Token pricing** (bands + overlay) is **spec-locked** — `token-pricing.md`. Implement later. Not this docs drop.

---

## Locks (unchanged)

- No Stripe. No “shop is open” claims. No live pricing until Ben says so.
- Token pricing v1 is locked: bands + overlay in `America/Regina` — `token-pricing.md`. Defaults are Owner-editable placeholders, not public prices.
- Hold the Mission Control cockpit until Owner booking is merged **and** live on Doc.
- Shop members never get Nextcloud accounts.
- No n8n.

Specs: `project-car-application-specification.md` §13, `token-pricing.md`, `website-webapp-specification.md`, `platform-architecture.md`.
