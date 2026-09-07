# Temporary `app.` alias cut

**Status:** Checklist / plan only — **not executed**  
**Updated:** 2026-09-07  
**Related:** `STATUS.md` Next #2, `member-host-cutover.md` (Next #1; does **not** require this cut first), `member-zone-edge.md`, `cors-origins.md`, `shop-web-stay-up.md`, `api-stay-up.md`, `doc-lid-restore.md`, `website-webapp-specification.md` §3

Plan Ben cutting the temporary **`app.projectcar.ca`** alias once ready. This file is a runbook. It does **not** change DNS, tunnel hostnames, CORS, or shop-web allowlists.

Do **not** invent Stripe, a shop opening, a shipped Member host migration, a **removed** `app.` alias, Matrix, or Apex revival. Demo session cookies stay demo cookies — **not OIDC**.

---

## Locks (read first — do not weaken)

| Lock | Meaning |
|------|---------|
| **Do not execute from a docs PR** | Merging this file is **not** a cut. Do not edit Cloudflare, Doc `.env`, or shop-web allowlists from docs work. No Garage / Zone / Hatch fan-out from this PR. |
| **Member cutover does not require cutting `app.` first** | STATUS Next #1 (`member-host-cutover.md` / `member-zone-edge.md`) can ship with the alias **still live**. This cut is Next #2 — **later**, when Ben is ready. |
| **`ops.` stays the management host** | Staff-on-shift + Owner stay on **`ops.projectcar.ca`**. Do not retarget management to `app.`, apex, or www. Do not describe `ops.` as Owner-only. |

Ben decides when to execute. This file does **not** ping Ben.

---

## Reality today (do not claim this is done)

| Surface | Live origin |
|---------|-------------|
| **Ops / staff** | Doc `:3000` shop UI on **`https://ops.projectcar.ca`** (LIVE at the edge when Doc origin is up). **Stays** the management host after this cut. |
| **Temporary `app.` alias** | **Still live.** Same Doc `:3000` origin (`https://app.projectcar.ca`). Tunnel hostname `app` + proxied DNS. **Not removed.** |
| **Member demo** | Shop-UI `/member` on **`ops.`** and the temporary **`app.`** alias. Customer-host migration is Next #1 — **independent** of this cut. |
| **CORS** | Live allowlist still includes `https://app.projectcar.ca` (`cors-origins.md`). |
| **Shop-web host allowlist** | `lib/request-origin.ts` still allowlists `app.projectcar.ca` (PR **#36**, `f952cd3` — **on git**; Doc pull/rebuild **pending**). |
| **Shop API** | `api.projectcar.ca` → Doc `:8000`. Lead owns uvicorn. |

Some clients still miss `ops.` in **local DNS cache** and use `app.` as a crutch. That is why the alias exists. It is **not** proof that `ops.` is down.

---

## Ordered checklist (execute later — not this PR)

Do these **in order** when Ben is ready. Do **not** drop CORS or the shop-web allowlist while the alias still serves browsers.

### 1. Zone — remove tunnel hostname + proxied DNS for `app.`

| Who | Do | Do not |
|-----|----|--------|
| **Zone** | Remove the Cloudflare tunnel public hostname **`app`** (origin today `http://127.0.0.1:3000`). Remove the **proxied** DNS record for `app.projectcar.ca`. | Touch **`ops.`**, **`api.`**, apex, or `www`. Retarget `app.` at the Worker or at Member-only paths. Cut `app.` as part of Next #1. |

`ops` → `http://127.0.0.1:3000` **stays**. Lead does not edit Cloudflare.

### 2. Ops-only smoke (gate before allowlist drops)

Prove staff can work **without** the alias. Lid-close **530 / 1033** is not a cut failure (`doc-lid-restore.md`).

| Check | Expect |
|-------|--------|
| `GET https://ops.projectcar.ca/` | `Location: https://ops.projectcar.ca/login` — **no localhost** hop |
| `GET https://ops.projectcar.ca/login` | **200** |
| Staff surfaces on `ops.` | Dashboard / schedule / chat still on **`ops.`** |
| `GET https://api.projectcar.ca/health` | **200** `{"status":"ok","service":"project-car-api"}` when Doc origin is up |
| Brochure waitlist | Membership / Contact still POST to `api.projectcar.ca/waitlist` (Garage e2e when health is 200) |

If `ops.` fails, **rollback** (§ Rollback) — do **not** proceed to CORS or shop-web drops.

### 3. CORS allowlist — drop `app.` **only after** ops-only smoke passes

| Who | Do | Do not |
|-----|----|--------|
| **Lead** | After §2 is green: remove **`https://app.projectcar.ca` only** from Doc `CORS_ORIGINS`. **Lead** restarts uvicorn (`cors-origins.md`). Smoke OPTIONS for `Origin: https://projectcar.ca` and `https://ops.projectcar.ca`. | Drop `https://ops.projectcar.ca`. Drop brochure `https://projectcar.ca` / `https://www.projectcar.ca`. Set `*`. Drop `app.` **before** Zone cut or **before** ops-only smoke. Hand the restart to Garage / Zone. |

Live list today (`cors-origins.md`) — **do not edit it in a docs PR:**

```
http://localhost:3000,http://127.0.0.1:3000,https://projectcar.ca,https://www.projectcar.ca,https://ops.projectcar.ca,https://app.projectcar.ca
```

After a real cut, `https://app.projectcar.ca` is the **only** origin that leaves. `ops.` stays.

### 4. Shop-web host allowlist — drop `app.`

| Who | Do | Do not |
|-----|----|--------|
| **Garage** (shop-web) + **Lead** (Doc rebuild) | After §3: drop `app.projectcar.ca` from `apps/project-car/web/lib/request-origin.ts` (and matching tests). Keep `localhost` / `127.0.0.1`, `ops.projectcar.ca`, `projectcar.ca`, `www.projectcar.ca`. Still **never** allowlist `api.projectcar.ca`. Lead `git pull` + `npm run build` + KeepAlive **`next start`** (`shop-web-stay-up.md`). | Drop `ops.`. Drop customer-host names Next #1 still needs. Claim #36 is live on Doc until that rebuild. Cut allowlist while `app.` DNS / tunnel still serve browsers (leftover `Host` / `X-Forwarded-Host: app.projectcar.ca` would then fail closed / hop to the listen origin). |

`#36` (`f952cd3`) **added** the allowlist (including `app.`). This step **removes** `app.` after the hostname is gone. Last recorded Doc **BUILD** is still Dashboard **#28** (`afb37f9`) until Lead rebuilds — do not collapse those facts.

### 5. Lookout / STATUS language flip

After the hostname is actually gone — **not** from this docs PR:

| Surface | Flip to |
|---------|---------|
| **Lookout** | Stop treating `https://app.projectcar.ca` as a required live host. Keep **`ops.`** + **`api.`** probes (`projectcar-api-health-watch` class). An `app.` fail after the cut is **expected**, not a new outage. |
| **STATUS.md** | Host-split row + Live bullet: alias **cut**; management = **`ops.`** only. Locks stop saying “use `app.` if `ops.` DNS is flaky.” Next #2 is done. |
| **Stay-up / restore** | `shop-web-stay-up.md`, `doc-lid-restore.md`, `cors-origins.md`: drop “use the `app.` alias” as the staff path. Staff path is **`ops.`** + flush cache. |

Do **not** flip this language while the tunnel / DNS still serve `app.`.

### 6. Client DNS-cache note (why `app.` can still resolve)

After Zone removes the proxied record, some clients **still resolve** `app.projectcar.ca` for a while.

| Why | What it is not |
|-----|----------------|
| OS / browser / recursive resolver **TTL** still holds the old Cloudflare answer. Some stub caches ignore TTL longer than the record did. | Proof the cut “didn’t take.” Proof `ops.` is down. A reason to keep `app.` on CORS / shop-web allowlists forever. |

Cached clients may see Cloudflare **1033 / 530**, an old error page, or a dead tunnel — **not** a healthy shop UI. Tell them: use **`https://ops.projectcar.ca`**, flush local DNS (and the browser DNS cache). Do **not** re-add the alias just because one laptop still resolves `app.`.

This is the same class of cache already documented the other way (clients that miss `ops.` and used `app.` as a crutch). Cache lag after a cut is expected.

---

## Rollback = re-add the `app.` hostname

Undo the alias cut **without** moving management off `ops.`.

| Step | Who | Do |
|------|-----|----|
| Re-add tunnel + DNS | **Zone** | Restore tunnel hostname **`app`** → `http://127.0.0.1:3000` (not bare `localhost`) and the **proxied** DNS record for `app.projectcar.ca`. Same origin as `ops.`. |
| Restore CORS if already dropped | **Lead** | Put `https://app.projectcar.ca` back on `CORS_ORIGINS`. Restart uvicorn. OPTIONS-smoke brochure + ops + app. |
| Restore shop-web allowlist if already dropped | **Garage** + **Lead** | Put `app.projectcar.ca` back on the host allowlist + tests. Lead rebuilds shop-web. |
| Revert language | Docs / Lookout | STATUS + stay-up call it a **temporary alias** again. Lookout may probe `app.` as a cache crutch, not as the intended name. |

Rollback is **re-add `app.`**. It is **not** “make `app.` the management host.” **`ops.` stays.**

---

## Sequencing vs Next #1

| Order | Gate | Notes |
|-------|------|-------|
| — | **This doc exists** | Done. No DNS. No CORS edit. No allowlist edit. |
| Next #1 | Member UI on apex `projectcar.ca` | `member-host-cutover.md` / `member-zone-edge.md`. **Ben GO.** Alias **stays live** through that cutover (success criterion #9 there). |
| Next #2 | This cut | **Later.** Ben ready. `ops.` already LIVE. Does **not** wait on Member host — and Member host does **not** wait on this cut. |
| After Zone §1 | Ops-only smoke | Gate. Fail → rollback. |
| Then | CORS drop `app.` only | Lead. After smoke. |
| Then | Shop-web allowlist drop `app.` | Garage + Lead rebuild. |
| Then | Lookout / STATUS flip | After the hostname is gone. |

**Ownership (unchanged):** Zone owns tunnel / DNS. Lead owns Doc `:8000` uvicorn and shop-web rebuild. Garage owns the shop-web allowlist PR + waitlist e2e — not process restarts, not Cloudflare.

**Out of scope:** Stripe, shop-open claims, Staff/Member OIDC, Matrix, Apex sidecar, Mission Control cockpit, executing Next #1, Classic Pages git, new breadth placeholders, pinging Ben from a docs PR.

---

## Locks (copy from STATUS — do not weaken)

- Host split: customer = `projectcar.ca` / www. Management = **`ops.projectcar.ca`** (LIVE; not Owner-only). `app.` = temporary alias until Ben cuts DNS — **not removed** until this checklist is actually run.
- This checklist is **not** a ship claim and **not** a live cut.
- Member cutover does **not** require cutting `app.` first.
- No Stripe. The shop is not open.
- Do not revive Apex or Matrix.
- Shop-web KeepAlive is **`next start`**, not `next dev`.
- Lead owns Doc `:8000`.
