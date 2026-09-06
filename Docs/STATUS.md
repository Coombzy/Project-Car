# Status — 2026-09-06

Living one-pager: what’s live, what’s next, locks. Product detail stays in the start-here specs. Stay-up / CORS / Pages runbooks live elsewhere — this file is not a runbook.

---

## Live

- **Brochure:** https://projectcar.ca (Home, About, The Shop, Membership, Roadmap, Chat, Contact). Origin today: Doc Cloudflare Tunnel → `:8088` (`~/hermes-tools/project-car-website`). Git SSOT: `apps/website/` (Apex sidecar stripped).
- **Waitlist:** Membership / Contact `POST` JSON to `https://api.projectcar.ca/waitlist`. CORS allowlist includes `https://projectcar.ca`, `https://www.projectcar.ca`, and localhost. Live form is also on Doc hermes-tools until Pages cutover. See `cors-origins.md`.
- **Shop API:** `api.projectcar.ca` = Cloudflare tunnel → Doc `localhost:8000`. Primary stay-up: LaunchAgent `com.projectcar.shop-api` (KeepAlive) → `~/hermes-tools/mission-control/shop-api/run-shop-api.sh` → uvicorn `:8000`. Lid-close / sleep still kills the Mac. See `api-stay-up.md`.
- **Shop OS on `main` (PR #2 + #3):** public waitlist path; Owner API + Next.js UI under `apps/project-car/` — tiers, members, hoists, bookings, append-only token ledger, dashboard / week schedule. **Not** claimed live on `app.projectcar.ca`.

---

## Next

1. **Cloudflare Pages cutover** for the brochure (GO’d; blocked on CF ↔ GitHub auth). Shop API stays the lab tunnel.
2. **Owner booking hardened + live** on Doc / `app.projectcar.ca`.
3. Leftover brochure hygiene if still open: `robots.txt`, favicon, `sitemap.xml` (and related P0s in `website-improvements.md`).
4. Public Apex chat: **deferred (Ben)**. Not P0.
5. Staff / Member login and payments: later.
6. Mission Control cockpit: **held** until Owner booking is merged **and** live on Doc.

---

## Locks (unchanged)

- No Stripe. No “shop is open” claims. No live pricing until Ben says so.
- Hold the Mission Control cockpit until Owner booking is merged **and** live on Doc.
- Shop members never get Nextcloud accounts.
- No n8n.

Specs: `project-car-application-specification.md` §13, `website-webapp-specification.md`, `platform-architecture.md`.
