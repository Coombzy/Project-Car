# Ops demo hardening — Soft-530-CLEAR Next Ben GO (#79)

**Status:** Plan only — Soft-530-CLEAR **Next Ben GO**, **parallel to #82**. **Not** a GO from this tip-fold. Do **not** change login HTML or enable Cloudflare Access here. Garage **#79.1** strip-changeme is **git-only until Doc unfreeze+pull**.  
**Updated:** 2026-09-11 (#79.1 freeze honesty on held **#70**)  
**Related:** `STATUS.md` living-ops / Next (this card), `deployment-guide.md`, `security-playbook.md`, `shop-web-stay-up.md`, `api-stay-up.md`, `cors-origins.md`, `doc-lid-restore.md`, `doc-unfreeze.md`, `app-alias-cut.md` (later — do **not** cut `app.` here), `apps/project-car/web/app/login/page.tsx`, `apps/project-car/web/app/login/login-form.tsx`, `apps/project-car/web/app/member/login/page.tsx`, `apps/project-car/web/app/member/login/login-form.tsx`

Standing plan for two interim gates while the shop is **not** open and staff **OIDC** (STATUS Next #5) is still later. Original plan PR is **#79**. This tip-fold **elevates** the card into STATUS living-ops / Next because Soft-530 **CLEAR** re-exposed public demo credentials. Merging this file / folding it on held **#70** is **not** a login-code change, **not** an Access enable, **not** a Doc pull, and **not** OIDC.

Garage **#79.1** strip-changeme (Owner/Member banner + password prefill) is **git-only until Doc unfreeze+pull**. Merge alone will **not** clear public `ops.` / `app.` `/login` while the freeze holds (`4cf8924` / BUILD_ID **`5swmVz`**). Soft-530 is **CLEAR**; live `/login` still prints `changeme` on that frozen build.

Do **not** execute Garage or Zone from this tip-fold. **Ben GO** is required before either flip. Soft-530-CLEAR **#79** Next Ben GO stays **parallel to #82** — **not** blocked on Worker SEO / Option A upload / Bulk Phase1. Soft-530 CLEAR makes this **more urgent** than when Doc was 530 (login HTML was then often unreachable behind lid-close **530 / 1033**). Do **not** invent Stripe, a shop opening, a shipped Member host migration, a removed `app.` alias, Mission Control cockpit work, or an OIDC implementation. This file does **not** ping Ben. Do **not** rewrite **#82** → Zone upload+purge; **#83** after **#82**; Bulk for Member. **Never #81.**

---

## Locks (read first — do not weaken)

| Lock | Meaning |
|------|---------|
| **Plan only — this tip-fold is not GO** | Held **#70** paper. It is **not** a Ben GO to strip the login password or to turn on Access. Do **not** edit shop-web login, Cloudflare Access, DNS, or tunnels from this docs PR. |
| **#79.1 merge ≠ public login cleared** | Garage **#79.1** strip-changeme is **git-only until Doc unfreeze+pull**. Merge alone will **not** clear public `/login` while freeze holds (`4cf8924` / **`5swmVz`**). |
| **#79 parallel to #82** | Soft-530-CLEAR Next Ben GO is **not** blocked on Worker SEO / Option A upload / Bulk Phase1. **#82** sequence stays **#82 → Zone upload+purge; #83 after #82; Bulk for Member**. **Never #81.** |
| **Soft-530 CLEAR = more urgent** | Origin is **LIVE**. Public `/login` is reachable again. The plaintext password print + prefill is a live leak, not a 530-era paper note. Urgency is **higher** than when Doc was 530. Still **not** license to execute without Ben GO. |
| **Brochure stays public** | `projectcar.ca` / `www` (Worker `projectcar-brochure`) stay **public**. Do not put Access on the brochure hosts. |
| **`app.` stays** | Temporary alias **`app.projectcar.ca`** stays live until STATUS Next #2 (`app-alias-cut.md`). Optional Access may cover the alias. Do **not** cut DNS / tunnel / CORS / allowlist here. |
| **API waitlist stays public** | `https://api.projectcar.ca/waitlist` (and `GET /health`) stay reachable from the brochure. Access must **exclude** `api.` waitlist paths. |
| **OIDC is later** | Staff OIDC on **`ops.`** is STATUS Next #5. This file does **not** design, invent, or start OIDC. Access is an **optional** gate **until** that later slice. |
| **Ben GO before either flip** | Garage password-print stop **and** Zone Access enable each need their **own** Ben GO. This tip-fold is neither. |
| **Doc freeze unchanged** | Doc checkout stays **`4cf8924`** / BUILD_ID **`5swmVz`** until the **separate** unfreeze GO (`doc-unfreeze.md`). Garage **#79.1** strip-changeme is **git-only** until that pull + rebuild — same class as **#36** / **#69**. Hardening GO ≠ unfreeze GO. |
| **No #82 / Option A / Bulk fan-out** | Do **not** execute or rewrite **#82** Worker-live, Option A **FULL 10/10**, or Bulk Phase1 from this card. **#79** stays **parallel** — do **not** wait for **#82**. |
| **No shop CF cutover** | McKing shop-host cutover stays **paper**. Soft-530 five-row gate = **Doc shop hosts only** (`cloud.` / `api.` / `app.` / `ops.`) — **vault EXCLUDED**. |

Ben decides when to execute. This file does **not** ping Ben.

---

## Reality today (do not claim this is done)

Soft-530 is **CLEAR** / **LIVE** (Lead verified 2026-09-11 ~06:50 America/Edmonton): public `GET /health` **200**; `ops.` + `app.` **307** → `/login`; waitlist **OPTIONS 200**. Future lid-close can still **530 / 1033**.

**Soft-530 CLEAR re-exposed the public demo password.** Lead/Chief verified live: `https://ops.projectcar.ca/login` (and the `app.` alias) still shows banner Password `` `changeme` `` and **prefills** the password input **on frozen Doc BUILD_ID `5swmVz`**. Same-class leak on `/member/login`. Email prefill is **ok**. That is why **#79** is now Soft-530-CLEAR **Next Ben GO** — more urgent than when Doc was 530 — and **parallel to #82**. Garage **#79.1** merge will **not** change that public HTML until unfreeze+pull.

Public management hosts still serve the Doc shop-web demo **when Doc origin is up**. The shop is not open. Demo session cookies — **not OIDC**.

| Surface | Live behavior |
|---------|----------------|
| **`https://ops.projectcar.ca/login`** | **200** when Doc origin is up (Lead/Chief live). HTML prints demo Owner email **and** plaintext password **`changeme`** (`apps/project-car/web/app/login/page.tsx` banner + `login-form.tsx` `defaultValue`). Frozen Doc tip **`4cf8924`** / BUILD_ID **`5swmVz`**. Garage **#79.1** strip-changeme on git does **not** change this public body until unfreeze+pull. |
| **`https://app.projectcar.ca/login`** | Same Doc `:3000` origin (temporary alias). Same HTML leak. **Not removed.** |
| **Member `/member/login`** | Same hosts; same plaintext **`changeme`** in the Member banner + form. Seed email `ada.reyes@example.com` is fine to keep visible. Customer-host migration is STATUS Next #1 — **not** this file. |
| **Brochure** | `projectcar.ca` / `www` stay public Worker HTML + waitlist. No demo Owner password on those pages. |
| **Shop API** | `api.projectcar.ca` → Doc `:8000`. Public `GET /health` + brochure `POST /waitlist`. Lead owns uvicorn. Soft-530 **CLEAR**. |
| **Doc checkout** | Frozen at `4cf8924` / `BUILD_ID` `5swmVz` until **Ben GO** (`doc-unfreeze.md`). Garage **#79.1** strip-changeme is **git-only** until that pull + rebuild. Merge alone will **not** clear public login. |
| **Access** | **Off.** Anonymous `GET /login` is Shop OS HTML when Doc is up (lid-close **530 / 1033** is not Access). A Cloudflare **403** `cf-mitigated: challenge` from some egress IPs is existing WAF — **not** Access on. |
| **Probes** | Lookout `projectcar-api-health-watch` is **resumed** (`enabled:true`) 2026-09-11 ~06:52 America/Edmonton (Lookout confirmed; live `/health` **200**). Lead interim probe **ended**. **#78 lookout-resume** is **LIVE-SUPERSEDED** — api-health already `enabled:true`. Soft-530 companion watches stay **HOLD / not armed** (Ben skipped ~14:35 America/Edmonton — do **not** re-ask). Do **not** re-pause or re-arm from this file. |

Anyone can view-source `/login` on `ops.` / `app.` and read `changeme` while the shop is not open **and Soft-530 is CLEAR**. That is the leak this plan names. It is **not** a shop opening and **not** “OIDC is live.”

---

## 1. Garage — stop printing the plaintext password (after Ben GO)

**Who:** Garage (shop-web). **Lead** rebuilds on Doc only after the **separate** unfreeze GO (`doc-unfreeze.md`). **Not this tip-fold.**

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

### Garage implement notes (**#79.1** — **not this tip-fold**)

1. **Ben GO** to strip the print (this file is the elevated plan, not that GO). Garage **#79.1** is the strip-changeme slice.
2. Edit `apps/project-car/web/app/login/page.tsx` + `login-form.tsx` (and the Member login pair). Email may stay. Password field empty. Banner must not include `changeme`.
3. Tests / lint via Shop OS CI (`shop-os-ci.md`). Green CI is **not** Doc unfreeze. **#79.1** merge is **git-only**.
4. **Lead** `git pull` + `npm run build` + `next start` only after **Ben GO** unfreeze (`doc-unfreeze.md`). Until that rebuild, public `/login` HTML on Doc is still the frozen **`5swmVz`** banner. **Merge of #79.1 will not clear public login while freeze holds.**
5. Smoke (post-rebuild, Doc origin up): `GET https://ops.projectcar.ca/login` **200**; response body has Owner email **without** `changeme`. Temporary `app.` same. Lid-close **530 / 1033** aborts the public check.

Do **not** flip Access from the Garage PR. Do **not** cut `app.`. Do **not** start or execute **#79.1** from this **#70** fold.

---

## 2. Optional Zone — Cloudflare Access on `ops` (+ optional `app`) until OIDC

**Who:** Zone (Cloudflare Zero Trust / Access). **Ben GO before enable.** **Not this tip-fold.** **Not OIDC.**

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
| `GET /health` | Lookout `projectcar-api-health-watch` (**already** `enabled:true`). |
| `OPTIONS` / `POST /waitlist` | Brochure Membership / Contact. CORS allowlist unchanged. |
| Waitlist-adjacent public reads Zone already treats as public | Do not invent new public API surface. |

Do **not** put Access in front of the brochure Worker so that waitlist “needs a login.” Do **not** attach an Access application to `api.` as a shortcut for ops hardening.

### Identity (until OIDC — do not invent OIDC here)

Access IdP is **Cloudflare Access** (email OTP / an IdP Zone already has). That is **not** staff OIDC on Shop OS (`STATUS.md` Next #5). Do not design Auth0 / Google Workspace shop-web login, do not add callback routes, and do not replace `pc_owner_session` from this plan.

Staff still sign in to Shop OS with the **demo Owner** session after they pass Access. Password stays in seed / ops note once Garage has stripped the HTML print.

---

## 3. Service Auth / bypass — Lookout (resumed) + stay-up probes

Access on `ops.` / `app.` must **not** break stay-up probes. Access on `api.` waitlist / health must **not** happen (see §2).

| Probe | Today | After Access on `ops` / `app` |
|-------|--------|-------------------------------|
| **Lookout Soft-530** | **`enabled:true`** on `api.` `/health` (resumed 2026-09-11). Lead interim probe ended. | `api.` `/health` stays public. Do **not** put Access on `api.`. |
| **Ops/app HTML** | Public `/login` **200** when Doc is up (the leak). | If Access is enabled, HTML probes need a **Service Auth** token (or an Access bypass policy) so origin **200** is still visible — not an Access login 302. |

### Zone setup (after Ben GO to enable — **not now**)

1. Create a Cloudflare Access **Service Auth** token (or service token) for probes. **No values in git.**
2. Access policy: allow humans Ben names **and** the service token. Fail closed for anonymous internet.
3. Lead stores the token on Doc / probe env (not shop-web, not the brochure Worker, not this repo).
4. If Lookout also probes `ops.` / `app.` `/login`, hand Lookout the **same** Service Auth (or a sibling token). Do **not** change Lookout `enabled` from this file.

A Cloudflare **403** HTML challenge (`cf-mitigated: challenge`) on some egress is existing WAF — not this Access application. Do not treat brochure/API challenge as “Access is on.”

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
| — | **This doc exists on held #70** | Elevated 2026-09-11. No login edit. No Access. No DNS. |
| Held **#70** | This Reality tip fold | Paper / STATUS / MC arch only. **Not** Garage/Zone execute. |
| **#79** | Soft-530-CLEAR **Next Ben GO** | This card. **Parallel to #82** — not blocked on Worker SEO / Option A upload / Bulk Phase1. |
| **#79.1** | Garage strip-changeme | **Git-only until Doc unfreeze+pull.** Merge alone will **not** clear public login while freeze holds (`4cf8924` / **`5swmVz`**). |
| **#78** | Lookout re-arm | **LIVE-SUPERSEDED** — api-health already `enabled:true`. Soft-530 companions stay **HOLD** (Ben skipped). Do **not** flip `enabled` from here. |
| **#82** / Option A / Bulk Phase1 | Worker-live + capacity | **Do not touch.** Sequence **unchanged**: **#82** → Zone upload+purge; **#83** after **#82**; Bulk for Member. **Never #81.** Option A stays **FULL 10/10**. **#82** not yet Worker-live. |
| Garage §1 / **#79.1** | Stop printing password | **Ben GO.** Git PR, then Doc rebuild only after **separate** unfreeze GO. |
| Zone §2 | Optional Access enable | **Ben GO.** Independent of Garage §1. Either order is fine; both need GO. |
| Later | Staff OIDC on `ops.` | STATUS Next #5. **Not this file.** Access comes **off** (or in front of OIDC) only when that later slice says so. |
| Later | `app.` alias cut | STATUS Next #2. **Not this file.** |
| Later | McKing shop CF cutover | Paper only. Soft-530 five-row = Doc shop hosts only. **Not this file.** |

**Ownership (unchanged):** Garage owns shop-web login HTML after GO. Zone owns Access / Service Auth. Lead owns Doc `:8000` and shop-web rebuild after unfreeze GO. Lookout owns the live `api.` `/health` watch (already resumed). This **#70** tip-fold owns **none** of those flips.

---

## Smoke (run after a later GO — **not** this tip-fold)

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

- Executing Garage §1 or Zone §2 from this **#70** tip-fold (Ben GO required).
- Inventing or implementing staff **OIDC** (Next #5).
- Cutting the `app.` alias (Next #2).
- Flipping Access, Service Auth, or login code from this PR.
- Amending **#82** / rewriting Option A **10/10** / executing Bulk Phase1.
- Doc pull / rebuild / unfreeze ask (separate GO).
- Member host GO / Zone path-split execute.
- Lookout `enabled` flip (**#78** is **LIVE-SUPERSEDED** — api-health already resumed; companions **HOLD**).
- Mission Control cockpit start (MC arch tip-fold on #70 is paper honesty only).
- McKing shop CF cutover (stays paper).
- Brochure About **P3-2 / P3-3**.
- Stripe / shop-open / live public pricing.
- Tip-only finance stamps.
- Pinging Ben from a docs PR.

---

## Locks (copy from STATUS — do not weaken)

- Host split: customer = `projectcar.ca` / www. Management = **`ops.projectcar.ca`** (LIVE; not Owner-only). `app.` = temporary alias until Ben cuts DNS — **not removed**.
- This checklist is **not** a ship claim, **not** an Access enable, and **not** OIDC.
- Soft-530 **CLEAR** re-exposed the leak on frozen **`5swmVz`**; that is **Next Ben GO**, **parallel to #82**, not “GO now.”
- Garage **#79.1** strip-changeme is **git-only until Doc unfreeze+pull**. Merge alone will **not** clear public login.
- Demo cookies stay demo cookies until the later OIDC slice.
- No Stripe. The shop is not open.
- Do not revive Apex or Matrix.
- Shop-web KeepAlive is **`next start`**, not `next dev`.
- Lead owns Doc `:8000`.
- Soft-530 five-row shop gate = `cloud.` / `api.` / `app.` / `ops.` only — vault EXCLUDED.

---

## Index

- `STATUS.md` living-ops / Next (Soft-530-CLEAR **Next Ben GO**, **parallel to #82**; **#79.1** git-only until unfreeze+pull)
- `deployment-guide.md` stay-up / deploy index (plan only)
- `security-playbook.md` Related
