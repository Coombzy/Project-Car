# Member zone edge — path split on projectcar.ca / www

**Status:** Checklist / plan only — **not shipped**. Capacity-blocked by Option A **FULL 10/10**. Do **not** execute until **#82** Worker-live + Bulk Phase1 **and** **Ben GO**.  
**Updated:** 2026-09-11 (Option A capacity lock on held **#70**)  
**Related:** `STATUS.md` Next #1, `member-host-cutover.md`, `app-alias-cut.md` (STATUS Next #2; later — do **not** cut `app.` here), `brochure-worker-deploy.md` (Option A matrix / Member-precondition receipt; `brochure-worker-ci.md` **not drafted** — queued), `shop-web-stay-up.md`, `brochure-pages-cutover.md`, `cors-origins.md`, `website-webapp-specification.md` §3, `mcking-shop-host-cutover.md` (later shop origin — **not** this cut)

This file is the **edge / path-split** slice Zone needs for STATUS **Next #1** (Member UI on **projectcar.ca**). Cookie Domain / Path / Secure / SameSite, CORS allowlist, and Next middleware host allowlist live in `member-host-cutover.md` §2 — **summarize + point**, do not rewrite that essay here.

This file does **not** implement the migration, change DNS, cut the `app.projectcar.ca` alias, upload shop-web as the apex origin, or start Garage / Zone / Hatch work. A docs merge is not GO. This tip-fold is **not** Member GO, **not** Bulk Phase1 execute, **not** **#82** Worker upload.

Do **not** invent Stripe, a shop opening, a shipped Member host migration, a removed `app.` alias, Matrix, or Apex revival. Demo session cookies stay demo cookies — **not OIDC**.

---

## Reality today (do not claim this is done)

| Surface | Live origin |
|---------|-------------|
| **Brochure** | Cloudflare Worker **`projectcar-brochure`** Direct Upload of `apps/website/html` from `main` (`brochure-worker-deploy.md`). Serves **all** public paths on `projectcar.ca` / `www` today. |
| **Member demo** | Shop-UI `/member` on Doc `:3000` (`next start` via LaunchAgent `com.projectcar.shop-web`). Reachable on **`https://ops.projectcar.ca/member`** and **`https://app.projectcar.ca/member`**. **Not** on the customer host. |
| **Ops / staff** | Same Doc `:3000` shop UI on **`ops.`** (LIVE when Doc origin is up). Temporary **`app.`** alias still live. **Not removed.** |
| **Shop API** | `api.projectcar.ca` → Doc `:8000`. Lead owns uvicorn. |

Exact Cloudflare product (tunnel public hostname vs Worker route vs Transform) is **Zone’s** after GO. This file locks the **traffic map**, not a dashboard click-path.

---

## 0. Option A capacity lock — Member edge is blocked

STATUS Next #1 Member edge is **capacity-blocked** by Option A. The CF Dynamic Redirect pack is **FULL 10/10**. Member cutover needs Dynamic (or equivalent) for `/member*` path/tunnel ranking **BEFORE** brochure Redirect Rules, plus www→apex `/member*` **301** that does **not** fight brochure dual-host.

Soft-530 is **CLEAR** / **LIVE**. That does **not** unlock Member edge. **#82** Home canonical/og/sitemap `/index.html` is **not yet Worker-live**. Do **not** execute Garage/Zone from this tip-fold.

| Hard gate | Meaning |
|-----------|---------|
| **Member edge Ben GO only after #82 Worker-live + Bulk Phase1** | Bulk Phase1 frees pretty-URL Dynamic slots. Redirect SSOT pick A is **already parked** (`brochure-worker-deploy.md` Option A matrix — Member-precondition receipt). `brochure-worker-ci.md` is **not drafted**; that matrix is the queue/index receipt until it exists. |
| **Keep `root` / `shop` Dynamic** | `root` / `index` / `shop` / `chat` stay Dynamic until Member **needs** those remaining slots. Do **not** migrate them in Bulk Phase1 just to “make room.” |
| **Rank `/member*` BEFORE the brochure Redirect pack** | Path/tunnel + www→apex `/member*` 301 evaluate **first**. Brochure pretty-URLs (including `membership` → `membership.html`) must not win. |
| **Anti-collision** | Apex + www `/member/login` must **NOT** 301 into `membership.html`. Today `/member*` is Worker **404** — preserve that distinction. `/membership*` is brochure; `/member*` is Member (later) / 404 (today). |

`/member` is a prefix of `/membership`. A `starts_with /member` brochure rule, or a `/member*` rule ranked **after** `membership` → `membership.html`, collides. Ranking + exact `/member` / `/member/*` (not `/membership`) is the lock.

www→apex **301** applies to **`/member*` only**. Brochure static stays **dual-host**. Do **not** 301 all of www to free a slot or “simplify” cookies.

---

## 1. Path split

Two products will share `projectcar.ca` / `www`. They are **not** the same app. Do **not** deploy shop-web as the apex catch-all — that would replace the brochure.

| Path on `projectcar.ca` / `www` | Origin | Notes |
|----------------------------------|--------|-------|
| `/member` and `/member/*` | Doc shop-web tunnel → **`http://127.0.0.1:3000`** | **Same** KeepAlive origin as `ops.` / `app.` (`shop-web-stay-up.md`). Not a second Next process. Not Doc `:8088`. |
| Everything else on those hosts | Worker **`projectcar-brochure`** Direct Upload | Home / About / The Shop / Membership / Roadmap / Contact, waitlist JS, robots, sitemap, 404, favicons. Standing upload: `brochure-worker-deploy.md`. |

Route unit matches shop-web middleware: `path === "/member"` or `path.startsWith("/member/")` (`member-host-cutover.md` §1). That includes `/member/login`, `/member/schedule`, `/member/chat`, `/member/parts`, `/member/jobs`, `/member/cameras`, `/member/todos/{id}/ics`.

| Do | Do not |
|----|--------|
| Add a **path** rule so only `/member*` leaves the Worker. | Point apex / www **catch-all** at Doc `:3000`. |
| Keep Worker **`projectcar-brochure`** on all other customer-host paths. | Upload `apps/project-car/web` as the brochure. Fold Member into `apps/website`. |
| Origin bind **`http://127.0.0.1:3000`** (not bare `localhost` — IPv6 `[::1]` historically **502**’d ops). | Retarget `ops.`, `app.`, or `api.` tunnels. |
| Leave ops/app `/member` parked until Ben says otherwise. First cutover **adds** customer-host routing. | Delete the ops/app Member park as part of the edge add. |
| Leave Chat stripped on the brochure. Apex sidecar **deferred**. | Revive brochure Chat or Apex to “make the split easier.” |

Which `/member` routes move vs what stays on the brochure vs what stays on `ops.`: `member-host-cutover.md` §1. Do not copy that table here.

---

## 2. www vs apex Member cookies

Full flags, CORS allowlist, and middleware host allowlist: **`member-host-cutover.md` §2**. Zone does not rewrite cookies from the edge. Garage / Lead own Path / Secure / `.env` **after GO**.

**Canonical Member cookie host is apex `projectcar.ca`.** Locked for this plan. Not www. This is **plan only** — do **not** claim the hop is live and do **not** apply a Zone rule from this file.

What Zone must not break:

| Rule | Why |
|------|-----|
| Cookies stay **host-only** (no `Domain=.projectcar.ca`). | A parent Domain would send `pc_member_session` to `ops.`, `app.`, and `api.`. Owner and Member cookies stay on different hosts. |
| Prefer **`Path=/member`** after share-host. | Brochure pages must not receive the Member session. Login / logout / `delete_cookie` must use the same Path (`member-host-cutover.md` §2). Shop-web already supports this behind **`SHOP_MEMBER_COOKIE_PATH_SCOPED=true`** (default **OFF** → `Path=/`). Do **not** flip the Doc env until Ben GO / cutover. |
| **Canonical host = apex `projectcar.ca`.** Zone plan: **301** `www.projectcar.ca/member*` → `https://projectcar.ca/member*`. | Host-only `pc_member_session` does **not** follow a www ↔ apex hop. A login on www and a bounce to apex would drop the session. The 301 puts Member only on apex so that cannot happen. |
| Brochure static stays **dual-host** on Worker (`projectcar.ca` + `www`). | Marketing + waitlist already use both. Do **not** 301 all of www — only `/member*`. |
| **Secure** stays true on HTTPS. **SameSite=Lax**. **HttpOnly**. | Same as ops/app today. Do not switch to `None` or `Strict` at the edge. **Not OIDC.** |

After Ben GO, say the 301 is in the GO notes and put Member only on apex. Silent hops without that 301 are a cookie bug, not a “refresh.” Do **not** invent a live edge flip from this PR.

CORS: `https://projectcar.ca` and `https://www.projectcar.ca` are **already** on `CORS_ORIGINS` (`cors-origins.md`). Sharing the customer host does **not** require a new origin. Lead restarts uvicorn only if `.env` changes.

---

## 3. Host / X-Forwarded-Host

Tunnel / edge must forward the **real public host** and **https** into shop-web. Next `publicUrl` / `publicOrigin` (`lib/request-origin.ts`) trusts a well-formed `Host` or `X-Forwarded-Host` plus `X-Forwarded-Proto`.

| Forward | Value |
|---------|--------|
| `Host` or `X-Forwarded-Host` | **`projectcar.ca`** for `/member*` (canonical cookie host after the planned www→apex 301). Brochure paths may still be `www.projectcar.ca`. |
| `X-Forwarded-Proto` | `https` |

If these are missing or set to `localhost` / `127.0.0.1:3000`, login and auth-gate redirects hop to **`http://localhost:3000/...`**. That class of bug is **already fixed on ops** (`shop-web-stay-up.md` public smoke). Do not reintroduce it on the customer host.

Do **not** allowlist `api.projectcar.ca` as a shop-web redirect host (`member-host-cutover.md` §2). Recommended explicit allowlist (Garage, after GO): localhost / `127.0.0.1`, `ops.projectcar.ca`, `app.projectcar.ca`, `projectcar.ca`, `www.projectcar.ca`.

---

## 4. Smoke curls

**None of these are true yet.** Run only after Ben GO + Zone path rules + Garage Member surface. HTML from some networks hits a Cloudflare challenge (**403**) — that is WAF, not a failed split (`website-improvements.md`).

Lid-close / sleep on Doc can still take shop-web and the API (Cloudflare **502** or **530 / error 1033**). That is **not** a path-split failure — see `shop-web-stay-up.md` and `api-stay-up.md`. Skip Member / waitlist / ops probes until Doc origin is up. Brochure Worker HTML should still **200** while Doc sleeps.

| # | Check | Expect |
|---|--------|--------|
| 0 | **Anti-collision (today — preserve)** | Apex + www `https://projectcar.ca/member/login` and `https://www.projectcar.ca/member/login` must **NOT** **301** into `/membership.html`. Today `/member*` is Worker **404** (branded `404.html` ok). Distinct from live Option A `/membership` / `/membership/` → **301** `/membership.html`. A 301 `/member/login` → `/membership.html` is a **failed** rank / prefix collision — rollback, not “pretty URL working.” |
| 1 | Member login on customer host | **After GO only.** **Apex only:** `https://projectcar.ca/member/login` serves the demo form. Seed `ada.reyes@example.com` + demo password sets `pc_member_session` (Secure, Lax, host-only, Path as decided — prefer `/member` when `SHOP_MEMBER_COOKIE_PATH_SCOPED` is on). Redirect stays on **`projectcar.ca`** — **no localhost hop**, **no www hop**. Do **not** smoke `https://www.projectcar.ca/member…` as a success path. After GO, Zone **301** `www…/member*` → `https://projectcar.ca/member*` (plan only — not live). `/member*` rules ranked **BEFORE** the brochure Redirect pack. |
| 2 | Brochure still Worker | Home / About / The Shop / Membership / Roadmap / Contact **200** Worker HTML. Chat page stays gone. Not Next HTML. |
| 3 | Waitlist still works | Membership / Contact `POST` → `api.projectcar.ca/waitlist` still **PASS** when API health is 200. OPTIONS still returns `Access-Control-Allow-Origin` for brochure origins (`cors-origins.md`). |
| 4 | Ops / app still healthy | `https://ops.projectcar.ca/` → `Location: https://ops.projectcar.ca/login` (no localhost). `/login` **200 when Doc origin is up**. Temporary `https://app.projectcar.ca` still the same Doc `:3000` origin. |
| 5 | No localhost `Location` | Member, ops, and app redirects stay on their public hosts. |

```bash
# Anti-collision (today + after GO): /member/login must NOT 301 → /membership.html
curl -sS -D - -o /dev/null https://projectcar.ca/member/login | grep -iE 'HTTP/|location:'
curl -sS -D - -o /dev/null https://www.projectcar.ca/member/login | grep -iE 'HTTP/|location:'
# Today expect Worker 404 (or WAF 403) — not Location: /membership.html
# Live brochure pretty-URL (distinct):
curl -sS -D - -o /dev/null https://projectcar.ca/membership | grep -iE 'HTTP/|location:'
# Member path — apex only after GO (canonical cookie host). Do not treat www as a Member host.
curl -sS -D - -o /dev/null https://projectcar.ca/member/login | grep -iE 'HTTP/|location:'
# Brochure paths must stay Worker (dual-host; www brochure is fine)
curl -sS -o /dev/null -w '%{http_code}\n' https://projectcar.ca/
curl -sS -o /dev/null -w '%{http_code}\n' https://www.projectcar.ca/
curl -sS -o /dev/null -w '%{http_code}\n' https://projectcar.ca/membership.html
curl -sS -o /dev/null -w '%{http_code}\n' https://projectcar.ca/contact.html
# Waitlist / API — 200 only when Doc origin is up; 502 / 530 / 1033 = lid-close
curl -sS -o /dev/null -w '%{http_code}\n' https://api.projectcar.ca/health
# Ops / app must still be the shop UI (no localhost Location)
curl -sS -D - -o /dev/null https://ops.projectcar.ca/ | grep -iE 'HTTP/|location:'
curl -sS -o /dev/null -w '%{http_code}\n' https://ops.projectcar.ca/login
curl -sS -D - -o /dev/null https://app.projectcar.ca/ | grep -iE 'HTTP/|location:'
curl -sS -o /dev/null -w '%{http_code}\n' https://app.projectcar.ca/login
```

Full Member success criteria (balance, booking, chat gate): `member-host-cutover.md` §5. If brochure pages come back as Next, or waitlist JS 404s, treat it as **rollback** — not “Garage restart uvicorn.”

---

## 5. Rollback

Undo the customer-host Member **path rules** only. Brochure returns to Worker-only on `projectcar.ca` / `www` (`brochure-worker-deploy.md`).

| Step | Who | Do |
|------|-----|----|
| Remove path rules | **Zone** | Point `projectcar.ca` / `www` `/member*` back off the shop-web origin. Apex / www are Worker-only again. |
| Confirm Worker attach | **Zone** | `projectcar.ca` and `www.projectcar.ca` still attach to Worker **`projectcar-brochure`**. Re-upload only if a bad split corrupted the Worker — otherwise leave the last good version. |
| Keep `app.` alias | Zone / Ben | **Do not cut** `app.projectcar.ca`. Staff with stale `ops.` DNS keep working. Ben cuts the alias later (`STATUS.md` Next #2 — plan: **`app-alias-cut.md`**). |
| Keep ops tunnel | **Zone** | `ops` → `http://127.0.0.1:3000` stays. Do not retarget ops to the Worker or to Member-only paths. |
| Keep `/member` on ops/app | Garage / Lead | Safe Member demo until Ben says otherwise. |
| Do not flip DNS for ops | **Zone** | Local DNS cache ≠ rollback. Tell staff to use `app.` or flush cache. |

Rollback is **edge path rules**, not “remove the Worker,” not “cut `app.`,” and not “restart uvicorn.” Cookie / CORS revert only if Lead changed `.env` for the cutover (`member-host-cutover.md` §4).

---

## 6. Locks (do not weaken)

- **Keep the `app.` alias.** Temporary until Ben cuts DNS. This plan does not touch `ops.` / `app.` tunnels except to leave them alone.
- **Classic Pages git stays outranked.** `brochure-pages-cutover.md` is still blocked on CF ↔ GitHub auth and is **outranked** by this Member edge work **and** by STATUS Next #1. Direct Upload remains the locked live brochure method. Do not start Pages git from this file.
- **No Apex.** Brochure stays Worker / Pages — no Apex sidecar, no brochure Chat page.
- **No Stripe.** The shop is not open. Interest waitlist only.
- **Capacity-blocked (Option A FULL 10/10).** Member edge Ben GO only after **#82** Worker-live + Bulk Phase1 frees pretty-URL Dynamic slots. Keep `root` / `shop` Dynamic until Member needs those slots. Do **not** add `/member*` Dynamic rules while the pack is full.
- **`/member*` ranks BEFORE the brochure Redirect pack.** www→apex `/member*` 301 must not fight brochure dual-host. `/member/login` must never 301 into `membership.html`.
- **No Garage / Zone / Hatch fan-out from this PR.** Plan only. **#82** / Bulk Phase1 / Member GO are **not** this tip-fold.
- **No shop-web apex catch-all.** Path split or nothing.
- Host split: customer = `projectcar.ca` / www. Management = **`ops.projectcar.ca`**. `app.` = temporary alias.
- Shop-web KeepAlive is **`next start`**, not `next dev`.
- Lead owns Doc processes (`:8000` / `:3000`). Zone owns Cloudflare path rules / tunnel hostname for the Member path.
- **Next #1 origin stays Doc.** STATUS Next #1 still says `/member*` → Doc `:3000`. If McKing later becomes the shop origin, that path-split retargets with the Soft-530 flip — **not now**.

---

## 7. Who

| Role | Owns | Does not own |
|------|------|----------------|
| **Zone** | Cloudflare **path rules** and **tunnel hostname** so `/member*` on `projectcar.ca` / `www` hits Doc `:3000` (`http://127.0.0.1:3000`) and all other paths stay Worker **`projectcar-brochure`**. Forward real host + https. Rollback = remove those path rules. | HTML content, shop-web code, uvicorn, `app.` cut, Pages git, cookie Path edits |
| **Garage** | shop-web Member surface **after GO** (`member-host-cutover.md`). Waitlist e2e after public API health is **200**. | Cloudflare path rules, tunnel hostnames, DNS, Direct Upload, process restarts |
| **Lead** | Doc processes — LaunchAgent `com.projectcar.shop-web` (`next start` `:3000`) and `com.projectcar.shop-api` (uvicorn `:8000`). Restarts if `.env` / cookie Path change. | Brochure edge. Do not hand path rules or Worker uploads to Lead. |
| **Ben** | **GO** before anyone executes this file or `member-host-cutover.md`. Later `app.` cut (Next #2 — `app-alias-cut.md`). | — |

Alerts can come from anyone who sees Next HTML on Home, a localhost `Location`, or waitlist 404. **Recovery of a bad path split is Zone** (rollback above). **Recovery of a down shop-web / API is Lead** (process) / **Zone** (tunnel only).

---

## Sequencing vs `member-host-cutover.md`

| Order | Gate | Who | Notes |
|-------|------|-----|-------|
| 0 | **Both plan docs exist** | Docs PR | You are here. No DNS. No `app.` cut. No path rules. |
| 0a | **#82 Worker-live + Bulk Phase1** | Garage / Zone after those GOs | **Hard gate.** Frees pretty-URL Dynamic slots (Redirect A parked). Keep `root` / `shop` Dynamic until Member needs those slots. **Not this tip-fold.** |
| 1 | **Ben GO** (Member edge) | Ben | Required **after** 0a. Do not start Zone path rules or Garage site work from this file alone. Capacity-blocked until 0a. |
| 2 | Cookie / CORS / middleware allowlist on Doc | Lead + Garage | `member-host-cutover.md` §2. Code + `.env` only after GO. |
| 3 | **This file** — edge path split | **Zone** | `/member*` rules ranked **BEFORE** brochure Redirect pack. `/member*` → `http://127.0.0.1:3000`. www→apex `/member*` 301 only. Everything else → Worker. Host + proto forwarding. Anti-collision: `/member/login` ≠ `membership.html`. |
| 4 | Member UI on customer host | **Garage** | Wire the surface; do not replace the Worker brochure. |
| 5 | Prove smoke (§4) + `member-host-cutover.md` §5 | Garage e2e; anyone can curl | If brochure / waitlist / ops/app break → §5 rollback. |
| 6 | Ben cuts `app.` alias | Ben / Zone | **Later.** STATUS Next #2. Checklist: **`app-alias-cut.md`**. Not this edge add — Member path-split does **not** require cutting `app.` first. |
| — | Classic Pages git | Zone | **Outranked.** `brochure-pages-cutover.md` after CF ↔ GitHub auth. Not a substitute for Next #1. |

**Out of scope for this file:** app code, DNS edits, Garage / Zone / Hatch fan-out, Stripe, shop-open, Apex, Mission Control cockpit, cutting `app.`, executing Pages git.

**Ownership (unchanged):** Zone owns Cloudflare path rules / Member-path tunnel hostname. Garage owns shop-web after GO. Lead owns Doc processes. Ben GO gates execution.
