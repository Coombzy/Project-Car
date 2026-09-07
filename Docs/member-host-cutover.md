# Member UI → projectcar.ca cutover

**Status:** Checklist / plan only — **not shipped**  
**Updated:** 2026-09-07  
**Related:** `STATUS.md` Next #1, `cors-origins.md`, `api-stay-up.md`, `website-webapp-specification.md` §3

Plan the move of Member self-serve from the shop UI `/member` (today on **`ops.`** + temporary **`app.`** alias) onto the customer host **projectcar.ca / www**. This file is a runbook. It does **not** implement the migration, change DNS, or cut the `app.projectcar.ca` alias.

Do **not** invent Stripe, a shop opening, a shipped Member host migration, a removed `app.` alias, Matrix, or Apex revival. Demo session cookies stay demo cookies — **not OIDC**.

**Ben GO required** before Garage (site) or Zone (Cloudflare DNS / tunnel / CORS edge) start this cutover. Cutover planning outranks new breadth placeholders.

---

## Reality today (do not claim this is done)

| Surface | Live origin |
|---------|-------------|
| **Brochure** | Cloudflare Worker **`projectcar-brochure`** Direct Upload of `apps/website/html` from `main`. **Not** the Doc `:8088` tunnel. **Not** `~/hermes-tools/project-car-website`. |
| **Member demo** | Shop-UI `/member` on Doc `:3000` (`next start` via LaunchAgent `com.projectcar.shop-web`). Reachable on **`https://ops.projectcar.ca/member`** and **`https://app.projectcar.ca/member`**. |
| **Ops / staff** | Same Doc `:3000` shop UI on **`ops.`** (LIVE). Temporary **`app.`** alias still live. **Not removed.** |
| **Shop API** | `api.projectcar.ca` → Doc `:8000`. Lead owns uvicorn. |

---

## 1. Which `/member` routes move vs what stays on the brochure

Two products share the customer host after cutover. They are **not** the same app.

### Moves to projectcar.ca / www (Member app — separate surface)

Shop-web App Router paths under `/member` (today parked on ops/app):

| Path | What |
|------|------|
| `/member/login` | Demo Member login (`ada.reyes@example.com` + `MEMBER_DEMO_PASSWORD`). Cookie `pc_member_session`. |
| `/member` | Balance + ledger + personal todos + next-24h hours on bays that member booked. |
| `/member/schedule` | Book / quote / confirm / cancel on **Bays 1–5 only**. Shop hoist stays `400 shop_hoist_owner_only`. |
| `/member/schedule/quote` | Same-origin quote POST (browser → Next, not browser → API). |
| `/member/chat`, `/member/chat/{id}` | Chat v1 — own rooms, reply, poll. Logged-out **auth-gate 307**. |
| `/member/parts` | Parts **request desk** (PT / TC SKUs). Not commerce. |
| `/member/jobs` | Job board placeholder (token amounts). Not claim/complete. |
| `/member/cameras` | Primary shop cam placeholder only. |
| `/member/todos/{id}/ics` | ICS download for that member's todo. |

Middleware today treats `path === "/member"` or `path.startsWith("/member/")` as the Member area (`apps/project-car/web/middleware.ts`). Those paths are the cutover unit.

### Stays on the brochure (Worker `projectcar-brochure`)

Static `apps/website/html` — **do not** serve these from shop-web:

| Page | File |
|------|------|
| Home | `index.html` |
| About | `about.html` |
| The Shop | `the-shop.html` |
| Membership | `membership.html` |
| Roadmap | `roadmap.html` |
| Contact | `contact.html` |

Plus `waitlist.js`, `shop-config.js`, `robots.txt`, `sitemap.xml`, `404.html`, favicons. Chat nav/page stays **stripped**. Apex sidecar stays **deferred**.

### Stays on ops. (and temporary app. alias)

Owner / staff shop-web — **do not** put these on projectcar.ca:

`/`, `/login`, `/schedule`, `/members`, `/hoists`, `/waitlist` (ops list, not the brochure form), `/tiers`, `/fill`, `/chat`, `/parts`, `/tools`, `/jobs`, `/cameras`, `/payments`, Owner todos / ICS.

Staff stay on **`ops.`**. Some clients still miss `ops.` in local DNS cache — they use **`app.`**. Do not strand them.

### Coexistence (same customer host, two origins behind it)

| Rule | Why |
|------|-----|
| Brochure stays Worker `projectcar-brochure` Direct Upload of `apps/website/html`. | Live customer marketing + waitlist. Not shop-web. |
| Member is a **separate surface** that will **share the customer host**. | Host split lock: customer = projectcar.ca / www. |
| Edge path split: `/member` and `/member/*` → Member app. Everything else on that host → Worker. | Shop-web catch-all must not steal Home / About / Membership / Contact. |
| Do not deploy shop-web as the apex origin. | That would replace the brochure. |
| Do not fold Member into `apps/website`. | Different stack (Next.js + API cookies vs static HTML). |

Exact Cloudflare route / Worker / tunnel wiring is **Zone**, after Ben GO — not this PR.

---

## 2. Cookie domain + Secure + CORS allowlist

### Today (ops / app)

Browser talks to shop-web only. Next.js server calls FastAPI with the session cookie. Member UI does **not** call `api.projectcar.ca` from the browser (except the **brochure** waitlist, which is a different stack).

| Cookie | Set by | Attributes today |
|--------|--------|------------------|
| `pc_member_session` | shop-web `writeMemberSessionCookie` (`lib/session.ts`); API also `set_member_session_cookie` | `HttpOnly`; `SameSite=Lax`; `Path=/`; **no `Domain`** (host-only); `Secure` when `SHOP_COOKIE_SECURE=true` **or** `NODE_ENV=production` (`cookie-secure.ts`). API side: `COOKIE_SECURE`. |
| `pc_owner_session` | same pattern | Same flags. Stays on **ops. / app.** — do not issue Owner cookies on the customer host. |

Public HTTPS on ops/app already needs Secure. Shop-web KeepAlive is **`next start`** (`NODE_ENV=production`), so Secure is on even without the env override. Keep `COOKIE_SECURE=true` / `SHOP_COOKIE_SECURE=true` on Doc anyway. Local `http://127.0.0.1:3000` leaves both unset or false.

### What must change for Member on projectcar.ca

- **Domain:** keep **host-only** (omit `Domain`). Do **not** set `Domain=.projectcar.ca` — that would send `pc_member_session` to `ops.`, `app.`, and `api.`. Owner and Member cookies stay on different hosts.
- **www vs apex:** pick one canonical customer host for Member cookies (or set the cookie on the host the browser actually hit). Host-only cookies do **not** follow a www ↔ apex hop. Zone should keep the existing brochure www/apex pair working; do not assume one cookie covers both.
- **Path:** today `Path=/` because the whole shop-web origin is the app. After share-host, prefer **`Path=/member`** so brochure pages do not receive the Member session. Login / logout / `delete_cookie` must use the same Path. If Path stays `/`, brochure requests will send the cookie — avoid leaking it to static HTML unless you have a reason.
- **Secure:** **must stay true** on HTTPS projectcar.ca / www. Same `COOKIE_SECURE` / `SHOP_COOKIE_SECURE` (and `next start` production).
- **SameSite:** keep **`Lax`**. Member login is a same-site form POST; Lax is enough. Do not switch to `None` (needs Secure + cross-site; not this architecture). Do not switch to `Strict` without checking login redirects from brochure links.
- **HttpOnly:** keep. Demo stub — still not OIDC.

### API CORS (`CORS_ORIGINS`)

Live allowlist (`cors-origins.md`) already includes brochure + ops + app:

```
http://localhost:3000,http://127.0.0.1:3000,https://projectcar.ca,https://www.projectcar.ca,https://ops.projectcar.ca,https://app.projectcar.ca
```

| Must stay | Why |
|-----------|-----|
| `https://projectcar.ca`, `https://www.projectcar.ca` | Brochure waitlist `POST` JSON from Membership / Contact. After cutover, same origins still submit waitlist. Member quote stays same-origin to shop-web (`/member/schedule/quote`) — CORS is for **browser → API**, mainly waitlist. |
| `https://ops.projectcar.ca` | Ops UI still calls the API (server-side today; keep the origin if any browser call exists). |
| `https://app.projectcar.ca` | Temporary alias still live until **Ben** cuts DNS. Do not drop it in this cutover. |
| localhost / 127.0.0.1:3000 | Doc / local demo. |

Never `*`. After any `.env` change, **Lead** restarts uvicorn (`cors-origins.md`). Adding a new Member-only origin is only needed if the browser starts calling the API from a host that is **not** already listed. Sharing projectcar.ca / www does **not** require a new origin — those two are already on the list.

### Next.js middleware host allowlist

Today there is **no** explicit host allowlist. `middleware.ts` redirects with `publicUrl` → `publicOrigin` (`lib/request-origin.ts`), which trusts a well-formed `X-Forwarded-Host` / `Host` plus `X-Forwarded-Proto`. Tests cover `app.projectcar.ca` and localhost, not projectcar.ca / www.

Before Member is reachable on the customer host:

- [ ] Tunnel / edge must forward `Host` or `X-Forwarded-Host` as `projectcar.ca` or `www.projectcar.ca` (and `https`). Otherwise redirects hop to `localhost:3000` — the same class of bug already fixed on ops.
- [ ] Add an **explicit allowlist** (recommended): `localhost` / `127.0.0.1`, `ops.projectcar.ca`, `app.projectcar.ca`, `projectcar.ca`, `www.projectcar.ca`. Reject anything else so a junk `X-Forwarded-Host` cannot mint a login redirect.
- [ ] Extend `request-origin` tests for customer-host redirects (`/member/login`, `/member`).
- [ ] Do **not** allowlist `api.projectcar.ca` as a shop-web redirect host.

---

## 3. Waitlist form coexistence

Brochure Membership + Contact keep `POST` JSON to `https://api.projectcar.ca/waitlist` (`apps/website/html/waitlist.js` + `shop-config.js`). **e2e must keep PASS** while Member lands on the same customer host.

| Check | Detail |
|-------|--------|
| Brochure pages still Worker | `/`, `/membership.html`, `/contact.html` (and the other brochure files) must **not** be captured by a shop-web `/:path*` on projectcar.ca. |
| `Origin` still brochure | Browser `Origin` is `https://projectcar.ca` or `https://www.projectcar.ca`. Those stay on `CORS_ORIGINS`. |
| No Member cookie required | `POST /waitlist` is public. Do not gate it on `pc_member_session`. |
| API host unchanged | Still `api.projectcar.ca` → Doc `:8000`. Lead owns uvicorn. Zone owns tunnel/DNS. Garage owns waitlist e2e only. |
| OPTIONS smoke | `cors-origins.md` — `Origin: https://projectcar.ca` → `Access-Control-Allow-Origin: https://projectcar.ca`. Public `/health` 200 does **not** prove CORS. |

If edge routing is wrong, the waitlist form 404s or HTML-from-Next replaces `waitlist.js`. Treat that as a **rollback** trigger, not “Garage restart uvicorn.”

---

## 4. Rollback if ops / app breaks

Goal: undo the customer-host Member slice **without stranding staff** on ops.

| Step | Who | Do |
|------|-----|----|
| Keep `app.` alias | Zone / Ben | **Do not cut** `app.projectcar.ca` in this cutover. Staff with stale `ops.` DNS keep working. Ben cuts the alias later (`STATUS.md` Next #2). |
| Keep ops tunnel | Zone | `ops` → `http://127.0.0.1:3000` stays. Do not retarget ops to the Worker or to Member-only paths. |
| Keep `/member` on shop-web | Garage / Lead | Until Ben says otherwise, ops/app `/member` remains the **safe** Member demo. First cutover is **add** customer-host routing, not **delete** the park. |
| Revert customer-host path rules | Zone | Point `projectcar.ca` / `www` `/member*` back off the Member origin (Worker-only again). Brochure returns to the pre-cutover map. |
| Revert cookie / CORS only if you changed them | Lead | If `COOKIE_SECURE` / `CORS_ORIGINS` / cookie Path were edited for the cutover, restore the last known-good Doc `.env` and **Lead** restarts uvicorn + shop-web. Do not hand restarts to Garage. |
| Do not flip DNS for ops | Zone | Local DNS cache ≠ rollback. Tell staff to use `app.` or flush cache. |

Rollback is **edge + env**, not “remove the Worker” and not “cut `app.`.” This PR does not change DNS.

---

## 5. Success criteria (measurable)

All of these must be true before calling the cutover done. **None of them are true yet.**

| # | Check | Expect |
|---|--------|--------|
| 1 | Member login on customer host | `https://projectcar.ca/member/login` (and www if that host is in play) serves the demo form. Seed `ada.reyes@example.com` + demo password sets `pc_member_session` (Secure, Lax, host-only, Path as decided). Redirect stays on projectcar.ca / www — **no localhost hop**. |
| 2 | Balance | Logged-in `GET /member` shows tokens + ledger (same demo as ops `/member`). |
| 3 | Booking routes | `/member/schedule` renders Bays 1–5; quote / book / cancel still work; shop hoist still `400 shop_hoist_owner_only`. `/member/schedule/quote` same-origin. |
| 4 | Member extras still gated | `/member/chat` auth-gate 307 when logged out; logged-in own rooms. Placeholders (`/member/parts`, `/jobs`, `/cameras`) load as demo UI — not Stripe / Frigate / checkout. |
| 5 | Brochure still brochure | Home / About / The Shop / Membership / Roadmap / Contact **200** from Worker HTML. Chat page stays gone. |
| 6 | Waitlist e2e | Membership / Contact `POST` → `api.projectcar.ca/waitlist` still **PASS**. OPTIONS smoke still returns `Access-Control-Allow-Origin` for brochure origins. |
| 7 | Ops still healthy | `https://ops.projectcar.ca/` → `Location: https://ops.projectcar.ca/login` (no localhost). `/login` **200**. Staff dashboard / schedule / chat still on ops. Temporary `https://app.projectcar.ca` still serves the same Doc `:3000` origin. |
| 8 | Public API health | `GET https://api.projectcar.ca/health` → **200** `{"status":"ok","service":"project-car-api"}`. |
| 9 | Alias not cut | `app.projectcar.ca` DNS / tunnel still live. Docs still call it a temporary alias. |

Lid-close / sleep on Doc can still take the API (Cloudflare **502** or **530 / error 1033**). That is not a cutover failure — see `api-stay-up.md`.

---

## 6. Sequencing

Lead sequences this vs more breadth placeholders: **cutover planning outranks new placeholders.** Calendar (#18), fill (#20), placeholders (#21), cookies (#22), schedule harden (#24), inventory (#26), Chat (#27), and Dashboard (#28) are already on `main` (`afb37f9`). Do not start another IA placeholder slice to dodge this plan.

| Order | Gate | Who | Notes |
|-------|------|-----|-------|
| 0 | **This doc exists** | Docs PR | You are here. No DNS. No `app.` cut. No code migration. |
| 1 | **Ben GO** | Ben | Required. Do not start Garage site work or Zone edge work from this file alone. |
| 2 | Cookie / CORS / middleware allowlist on Doc | Lead (process) + Garage (shop-web change) | Code + `.env` only after GO. Lead restarts uvicorn if `CORS_ORIGINS` changes. |
| 3 | Edge path split on projectcar.ca / www | **Zone** | Cloudflare DNS / tunnel / route so `/member*` hits Member and brochure paths stay Worker. CORS **edge** if Zone owns a WAF/origin check — API allowlist stays Lead `.env`. |
| 4 | Member UI on customer host | **Garage** (site) | Wire the Member surface; do not replace the Worker brochure. |
| 5 | Prove success criteria | Garage e2e waitlist; anyone can curl health / ops probes | If ops/app or waitlist breaks → §4 rollback. |
| 6 | Ben cuts `app.` alias | Ben / Zone | **Later.** `STATUS.md` Next #2. Not this cutover. |

**Ownership (unchanged):** Lead owns Doc `:8000` uvicorn. Zone owns tunnel / DNS / CORS edge. Garage waitlist e2e only (plus site work after GO). Do not hand uvicorn restarts to Chief or Garage.

**Out of scope for the cutover itself:** Stripe, shop-open claims, Staff/Member OIDC, Matrix, Apex sidecar, Mission Control cockpit, cutting `app.`, Pages git cutover, new breadth placeholders.

---

## Locks (copy from STATUS — do not weaken)

- Host split: customer = projectcar.ca / www. Management = **ops.projectcar.ca** (LIVE; not Owner-only). `app.` = temporary alias until Ben cuts DNS.
- This checklist is **not** a ship claim.
- No Stripe. The shop is not open.
- Do not revive Apex or Matrix.
- Shop-web KeepAlive is **`next start`**, not `next dev`.
- Lead owns Doc `:8000`.
