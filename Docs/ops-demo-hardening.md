# Ops demo hardening — login password print + optional Access

**Status:** Plan only — **not a GO** to change login HTML or enable Cloudflare Access  
**Updated:** 2026-09-08  
**Related:** `STATUS.md` living-ops, `deployment-guide.md`, `security-playbook.md`, `shop-web-stay-up.md`, `api-stay-up.md`, `cors-origins.md`, `doc-lid-restore.md`, `doc-unfreeze.md`, `app-alias-cut.md` (later — do **not** cut `app.` here), `apps/project-car/web/app/login/page.tsx`, `apps/project-car/web/app/login/login-form.tsx`

Standing plan for two interim gates while the shop is **not** open and staff **OIDC** (STATUS Next #5) is still later. Merging this file is **not** a login-code change, **not** an Access enable, **not** a Doc pull, and **not** OIDC.

Do **not** invent Stripe, a shop opening, a shipped Member host migration, a removed `app.` alias, Mission Control cockpit work, or an OIDC implementation. This file does **not** ping Ben.

---

## Locks (read first — do not weaken)

| Lock | Meaning |
|------|---------|
| **Plan only** | This file is the checklist. It is **not** a Ben GO to strip the login password or to turn on Access. Do not edit shop-web login, Cloudflare Access, DNS, or tunnels from a docs PR. |
| **Brochure stays public** | `projectcar.ca` / `www` (Worker `projectcar-brochure`) stay **public**. Do not put Access on the brochure hosts. |
| **`app.` stays** | Temporary alias **`app.projectcar.ca`** stays live until STATUS Next #2 (`app-alias-cut.md`). Optional Access may cover the alias. Do **not** cut DNS / tunnel / CORS / allowlist here. |
| **API waitlist stays public** | `https://api.projectcar.ca/waitlist` (and `GET /health`) stay reachable from the brochure. Access must **exclude** `api.` waitlist paths. |
| **OIDC is later** | Staff OIDC on **`ops.`** is STATUS Next #5. This file does **not** design, invent, or start OIDC. Access is an **optional** gate **until** that later slice. |
| **Ben GO before either flip** | Garage password-print stop **and** Zone Access enable each need their **own** Ben GO. This file is neither. |

Ben decides when to execute. This file does **not** ping Ben.

---

## Reality today (do not claim this is done)

Public management hosts still serve the Doc shop-web demo **when Doc origin is up**. The shop is not open. Demo session cookies — **not OIDC**.

| Surface | Live behavior |
|---------|----------------|
| **`https://ops.projectcar.ca/login`** | **200** when Doc origin is up. HTML prints demo Owner email **and** plaintext password **`changeme`** (`apps/project-car/web/app/login/page.tsx` banner + `login-form.tsx` `defaultValue`). |
| **`https://app.projectcar.ca/login`** | Same Doc `:3000` origin (temporary alias). Same HTML leak. **Not removed.** |
| **Member `/member/login`** | Same hosts; same plaintext **`changeme`** in the Member banner + form. Seed email `ada.reyes@example.com` is fine to keep visible. Customer-host migration is STATUS Next #1 — **not** this file. |
| **Brochure** | `projectcar.ca` / `www` stay public Worker HTML + waitlist. No demo Owner password on those pages. |
| **Shop API** | `api.projectcar.ca` → Doc `:8000`. Public `GET /health` + brochure `POST /waitlist`. Lead owns uvicorn. |
| **Doc checkout** | Frozen at `4cf8924` / `BUILD_ID` `5swmVz` until **Ben GO** (`doc-unfreeze.md`). A merged Garage login PR is **git-only** until that pull + rebuild. |
| **Access** | **Off.** Anonymous `GET /login` is **200** (lid-close **530 / 1033** is not Access). |
| **Probes** | Lookout `projectcar-api-health-watch` class on `api.` `/health`. While that watch is **paused**, **Lead** owns the interim morning/public probe. Re-arm is a **separate** card (held **#78**) — do **not** re-arm from this file. |

Anyone can view-source `/login` on `ops.` / `app.` and read `changeme` while the shop is not open. That is the leak this plan names. It is **not** a shop opening and **not** “OIDC is live.”

---

## 1. Garage — stop printing the plaintext password (after Ben GO)

**Who:** Garage (shop-web). **Lead** rebuilds on Doc only after **Ben GO** unfreeze (`doc-unfreeze.md`). **Not this PR.**

### Target

| Keep | Stop |
|------|------|
| Demo **email** on `/login` (`owner@projectcar.ca`) — ok to show / prefill | Plaintext **password** in the `/login` banner (`<code>changeme</code>`) |
| Seed / ops note as the password source | `defaultValue="changeme"` on the Owner password input |
| “Demo / shop is not open / not OIDC” honesty | Shipping the password in public HTML |

Same-class leak on **`/member/login`**: keep seed email `ada.reyes@example.com`; stop printing / prefilling **`changeme`**. Do **not** treat that as Member host cutover.

### Password via seed / ops note (not the public page)

After the HTML stop, the demo password still exists in seed and local docs — **not** in the public response body:

| Source | What it already says |
|--------|----------------------|
| Shop-api seed | `python -m app.seed` prints `owner@projectcar.ca / changeme` (localhost demo). `MEMBER_DEMO_PASSWORD` / `OWNER_PASSWORD` stay env defaults. |
| `apps/project-car/web/README.md` | Owner + Member tables list `changeme` for **localhost** walkthroughs. |
| `apps/project-car/api/README.md` | Same seed table. |

Do **not** paste a new production password into git. Do **not** rotate `changeme` in this slice unless a later Ben GO says so — the cut is **stop printing it on the public login page**, not inventing OIDC or a new secret store.

### Garage implement notes (later PR — not now)

1. **Ben GO** to strip the print (this file is the plan, not that GO).
2. Edit `apps/project-car/web/app/login/page.tsx` + `login-form.tsx` (and the Member login pair if in scope). Email may stay. Password field empty. Banner must not include `changeme`.
3. Tests / lint via Shop OS CI (`shop-os-ci.md`). Green CI is **not** Doc unfreeze.
4. **Lead** `git pull` + `npm run build` + `next start` only after **Ben GO** (`doc-unfreeze.md`). Until that rebuild, public `/login` HTML on Doc is still the old banner.
5. Smoke (post-rebuild, Doc origin up): `GET https://ops.projectcar.ca/login` **200**; response body has Owner email **without** `changeme`. Temporary `app.` same. Lid-close **530 / 1033** aborts the public check.

Do **not** flip Access from the Garage PR. Do **not** cut `app.`.

---

## 2. Optional Zone — Cloudflare Access on `ops` (+ optional `app`) until OIDC

**Who:** Zone (Cloudflare Zero Trust / Access). **Ben GO before enable.** **Not this PR.** **Not OIDC.**

Optional edge gate so anonymous internet cannot load the Shop OS login HTML while staff OIDC is still later. Demo cookies behind Access are still demo cookies.

### Scope

| Host | Access? |
|------|---------|
| **`ops.projectcar.ca`** | **Yes** (the intended management host). Application covers the hostname (login + authenticated shop-web). |
| **`app.projectcar.ca`** | **Optional same policy** while the alias is still live. If Access is on `ops.` only, the alias remains a public HTML hole — do not call that “hardened.” Do **not** cut the alias to “solve” Access. |
| **`projectcar.ca` / `www`** | **No.** Brochure stays **public**. Waitlist forms stay public. |
| **`api.projectcar.ca`** | **No Access on waitlist paths.** Prefer **no** Access application on `api.` at all. Public `GET /health` + `OPTIONS`/`POST /waitlist` must stay brochure-reachable (`cors-origins.md`). |

Exact dashboard click-path is Zone’s after GO. This file locks the **traffic map**, not a Zero Trust tutorial.

### Exclude `api` waitlist paths

If a later GO ever puts any Access near `api.`, these stay **unauthenticated / bypassed**:

| Path | Why |
|------|-----|
| `GET /health` | Lead interim probe + Lookout `projectcar-api-health-watch` (when re-armed). |
| `OPTIONS` / `POST /waitlist` | Brochure Membership / Contact. CORS allowlist unchanged. |
| Waitlist-adjacent public reads Zone already treats as public | Do not invent new public API surface. |

Do **not** put Access in front of the brochure Worker so that waitlist “needs a login.” Do **not** attach an Access application to `api.` as a shortcut for ops hardening.

### Identity (until OIDC — do not invent OIDC here)

Access IdP is **Cloudflare Access** (email OTP / an IdP Zone already has). That is **not** staff OIDC on Shop OS (`STATUS.md` Next #5). Do not design Auth0 / Google Workspace shop-web login, do not add callback routes, and do not replace `pc_owner_session` from this plan.

Staff still sign in to Shop OS with the **demo Owner** session after they pass Access. Password stays in seed / ops note once Garage has stripped the HTML print.

---

## 3. Service Auth / bypass — Lead interim probe + Lookout re-arm

Access on `ops.` / `app.` must **not** break stay-up probes. Access on `api.` waitlist / health must **not** happen (see §2).

| Probe | Today | After Access on `ops` / `app` |
|-------|--------|-------------------------------|
| **Lead interim** (watch paused) | Lead curls public `api.` `/health` and ops/app `/login` **200** when Doc origin is up (`doc-lid-restore.md`). | `api.` `/health` stays public. Ops/app HTML probes need a **Service Auth** token (or an Access bypass policy for that service) so Lead still sees origin **200**, not an Access login 302. |
| **Lookout re-arm** | Held **#78** is the re-arm **plan** — not enabled from here. Watch class `projectcar-api-health-watch` on `api.` `/health`. | Same: `api.` stays public. If Lookout also probes `ops.` / `app.` `/login`, hand Lookout the **same** Service Auth (or a dedicated service token). Do **not** re-arm Lookout from this file. |

### Zone setup (after Ben GO to enable — not now)

1. Create a Cloudflare Access **Service Auth** token (or service token) for probes. **No values in git.**
2. Access policy: allow humans Ben names **and** the service token. Fail closed for anonymous internet.
3. Lead stores the token on Doc / probe env (not shop-web, not the brochure Worker, not this repo).
4. When Lookout is re-armed (separate GO / held **#78**), Lookout gets the token or a sibling token. Do not wait on re-arm to write this plan.

A Cloudflare **403** HTML challenge (`cf-mitigated: challenge`) on brochure is existing WAF — not this Access application. Do not treat brochure challenge as “Access is on.”

Lid-close **530 / 1033** is still lid-close. Access **302** to `*.cloudflareaccess.com` is a different failure — do not send Lead to restart uvicorn for it.

---

## 4. Rollback

Undo Access **without** cutting `app.`, **without** touching brochure, and **without** inventing OIDC.

| Step | Who | Do |
|------|-----|----|
| 1. Disable the application | **Zone** | Turn **off** (or delete) the Access application on `ops.projectcar.ca` and, if enabled, `app.projectcar.ca`. |
| 2. Confirm anonymous login HTML | Garage or Lead | `GET https://ops.projectcar.ca/login` → **200** with **no** Access redirect (when Doc origin is up). Same for `app.` if it was covered. |
| 3. Brochure + waitlist | Garage | Apex + www **200**. `GET https://api.projectcar.ca/health` **200**. OPTIONS / POST `/waitlist` still CORS-ok (`cors-origins.md`). |
| 4. Probes | Lead / Lookout | Drop Service Auth headers from curls only after Access is off. Do not leave a required token on a now-public host. |

Rollback is **disable Access**. It is **not** “cut `app.`,” **not** “put Access on the brochure,” and **not** “start OIDC to replace Access.”

If Garage already stripped the password print and Doc has been rebuilt, rollback of Access does **not** require putting `changeme` back on the page.

---

## 5. Sequencing vs other cards

| Order | Gate | Notes |
|-------|------|-------|
| — | **This doc exists** | Done. No login edit. No Access. No DNS. |
| Held **#70** | Reality tip fold | Stays on **#70**. This PR does **not** tip-fold. |
| Held **#75** / **#77** | Lead interim probe language | Do **not** amend. Service Auth in §3 assumes that interim still exists until re-arm. |
| Held **#76** | Member edge blocked on Doc unfreeze | Out of scope. Do not execute Member GO. |
| Held **#78** | Lookout re-arm plan | Do **not** amend. Do **not** flip `enabled`. §3 is the Access bypass for when re-arm happens. |
| Garage §1 | Stop printing password | **Ben GO.** Git PR, then Doc rebuild only after unfreeze GO. |
| Zone §2 | Optional Access enable | **Ben GO.** Independent of Garage §1. Either order is fine; both need GO. |
| Later | Staff OIDC on `ops.` | STATUS Next #5. **Not this file.** Access comes **off** (or in front of OIDC) only when that later slice says so. |
| Later | `app.` alias cut | STATUS Next #2. **Not this file.** |

**Ownership (unchanged):** Garage owns shop-web login HTML after GO. Zone owns Access / Service Auth. Lead owns Doc `:8000`, shop-web rebuild after unfreeze GO, and the interim probe while Lookout is paused. Lookout owns the live probe when re-armed. This docs PR owns **none** of those flips.

---

## Smoke (run after a later GO — **not** this PR)

Lid-close **530 / 1033** aborts the public checks; restore first (`doc-lid-restore.md`).

### After Garage §1 + Doc rebuild

```bash
curl -sS https://ops.projectcar.ca/login | grep -E 'changeme|owner@projectcar.ca' || true
curl -sS -o /dev/null -w '%{http_code}\n' https://ops.projectcar.ca/login
```

Expect **200**, email present, **`changeme` absent**. Temporary `app.` same until Next #2.

### After Zone §2 Access enable

| Check | Expect |
|-------|--------|
| Anonymous `GET https://ops.projectcar.ca/login` | Access login / **302** — **not** raw Shop OS HTML |
| Anonymous `GET https://projectcar.ca/` | **200** brochure (no Access) |
| `GET https://api.projectcar.ca/health` | **200** without a service token |
| OPTIONS `https://api.projectcar.ca/waitlist` | CORS for `https://projectcar.ca` (`cors-origins.md`) |
| Lead / Lookout with Service Auth | ops/app `/login` origin **200** (or the documented probe code), not an Access bounce |
| Rollback §4 | Anonymous ops `/login` **200** again (Doc up) |

Do **not** run the Access-on row until Ben GO + Zone enable.

---

## Out of scope

- Inventing or implementing staff **OIDC** (Next #5).
- Cutting the `app.` alias (Next #2).
- Flipping Access, Service Auth, or login code from this PR.
- Amending held **#70**, **#75**, **#76**, **#77**, or **#78**.
- Tip-folding the STATUS Reality tip (stays on held **#70**).
- Doc pull / rebuild / unfreeze ask.
- Member host GO / Zone path-split execute.
- Lookout re-arm / `enabled:true`.
- Mission Control cockpit.
- Brochure About **P3-2 / P3-3**.
- Stripe / shop-open / live public pricing.
- Tip-only finance stamps.
- Pinging Ben from a docs PR.

---

## Locks (copy from STATUS — do not weaken)

- Host split: customer = `projectcar.ca` / www. Management = **`ops.projectcar.ca`** (LIVE; not Owner-only). `app.` = temporary alias until Ben cuts DNS — **not removed**.
- This checklist is **not** a ship claim, **not** an Access enable, and **not** OIDC.
- Demo cookies stay demo cookies until the later OIDC slice.
- No Stripe. The shop is not open.
- Do not revive Apex or Matrix.
- Shop-web KeepAlive is **`next start`**, not `next dev`.
- Lead owns Doc `:8000`.

---

## Index

- `STATUS.md` living-ops
- `deployment-guide.md` stay-up / deploy index (plan only)
- `security-playbook.md` Related
