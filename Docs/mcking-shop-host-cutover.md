# McKing shop-host cutover

**Status:** Checklist / plan only — **not executed**  
**Updated:** 2026-09-11  
**Related:** `STATUS.md` (pointer only — **not** Next #1, **not** a GO), `deployment-guide.md`, `api-stay-up.md`, `shop-web-stay-up.md`, `doc-unfreeze.md` (Ben GO pull — **not** this cut), `doc-lid-restore.md` (Doc process wake only), `cors-origins.md`, `shop-os-ci.md` (green CI ≠ unfreeze, ≠ this cut), `home-lab-specification.md`, `brochure-worker-deploy.md`, `member-host-cutover.md` (different cut — customer `/member` host)

Draft paper for a **later** move of Shop OS origins (`api.` / `ops.` / temporary `app.`) from **Doc LaunchAgents** onto **McKing Docker**, reusing the same Cloudflare tunnel public hostnames. Brochure stays on Worker `projectcar-brochure`.

This file does **not** unfreeze Doc, does **not** flip DNS or tunnel origin, and does **not** start Docker on McKing.

Do **not** invent Stripe, a shop opening, a shipped Member host migration, a removed `app.` alias, McKing IPs, a McKing compose file path, or tunnel / API token values.

---

## Locks (read first — do not weaken)

| Lock | Meaning |
|------|---------|
| **Paper only** | Merging this file is **not** a cut. No live Cloudflare / DNS / Docker / LaunchAgent changes from this PR. |
| **Not Next #1** | STATUS Next #1 is Member UI on projectcar.ca (`member-host-cutover.md`). This McKing host move is a **later** machine plan. Do **not** treat it as GO’d. |
| **Not Doc unfreeze** | Doc checkout stays frozen at **`4cf8924`** / BUILD_ID **`5swmVz-T2CqKEQzTk1ifU`** until **Ben GO**. Green **shop-os-ci** is **not** that GO. Pull checklist: `doc-unfreeze.md`. This paper must **not** be read as license to pull or rebuild on Doc. |
| **No public flip until smoke PASS** | Do **not** retarget tunnel origin or public DNS until McKing private smoke **PASS** and Lookout `/health` gates are green. |
| **Brochure stays Worker** | `projectcar.ca` / www stay Cloudflare Worker **`projectcar-brochure`**. Do **not** move the brochure to McKing. |
| **No Garage / Zone fan-out** | Garage does not upload Worker HTML from this file. Zone does not edit tunnel / DNS from this file. Hatch does not execute. |
| **CORS / public names unchanged** | Same Origins (`cors-origins.md`). Same public hostnames (`api.` / `ops.` / `app.`). Origin **host** may move later; names do not. |

Ben decides when (if) to execute. This file does **not** ping Ben and is **not** a live cut.

---

## Reality today (do not claim this is done)

Soft-530 is **CLEAR** (Doc origin **LIVE** 2026-09-11). Future lid-close can still **530 / 1033**. Lookout `projectcar-api-health-watch` is **`enabled:true`**.

| Surface | Live origin |
|---------|-------------|
| **Brochure** | Cloudflare Worker **`projectcar-brochure`** Direct Upload of `apps/website/html`. **Stays.** Not Doc. Not McKing. |
| **Shop API** | Host **cloudflared** on Doc → LaunchAgent **`com.projectcar.shop-api`** → uvicorn **`:8000`**. Public `https://api.projectcar.ca`. |
| **Ops / app shop-web** | Same Doc cloudflared → LaunchAgent **`com.projectcar.shop-web`** → **`next start`** **`:3000`**. Public `https://ops.projectcar.ca` (LIVE management) + temporary `https://app.projectcar.ca`. |
| **Doc KeepAlive** | `com.projectcar.cloudflared` + `com.projectcar.shop-api` + `com.projectcar.shop-web`. Lid-close still kills the Mac. |
| **Doc checkout** | **Frozen** at **`4cf8924`** / BUILD_ID **`5swmVz-T2CqKEQzTk1ifU`** (Dashboard **#28**) until **Ben GO** (`doc-unfreeze.md`). **#36** / **#69** stay **git-only**. |
| **Git compose today** | `infra/compose/compose.yaml` is **shop Postgres only**. It does **not** start shop-api, shop-web, or cloudflared. Do not invent those services as already in git. |
| **McKing role (Ben lock — intent)** | Later: Docker + Nextcloud **home**, then Shop API + shop-web via Docker + tunnel hostname reuse. This paper does **not** claim McKing is on the tailnet or that the migrate has started. Last recorded hub note still treated McKing as later (`home-lab-specification.md`, `nextcloud-progress.md`). |

`app.` stays the temporary alias until Ben cuts that DNS (`app-alias-cut.md`). This host move does **not** require cutting `app.`.

---

## 1. Target compose services on McKing (high-level)

Later McKing shop-host is **Docker**. Name the three shop-edge services. Do **not** invent a compose file path, image tags, host IPs, or secret values.

| Service | Role | Public name (reuse) | Notes |
|---------|------|---------------------|-------|
| **shop-api** | FastAPI shop API (today uvicorn on Doc `:8000`) | `api.projectcar.ca` | Same health body: `{"status":"ok","service":"project-car-api"}`. Lead still owns the API process — on McKing that is the container, not Doc `run-shop-api.sh`. |
| **shop-web** | Next.js shop UI (today `next start` on Doc `:3000`) | `ops.projectcar.ca` + temporary `app.projectcar.ca` | Must stay **`next start`**, not `next dev`. `BUILD_ID` parity (§4). |
| **cloudflared** | Tunnel client **on McKing** | Same three public hostnames | Replaces Doc host cloudflared **after** the origin flip — not before. Zone owns hostname / DNS rules. Do **not** invent a tunnel token or config path here. |

Shop data stays **dedicated shop Postgres** — never Nextcloud MariaDB (`infra/compose` today; Mission Control hub is a separate stack). This paper does **not** invent where McKing mounts that DB or a second compose path.

Nextcloud / Vaultwarden on McKing is the **hub** move (Docker + Nextcloud home). It is **not** the brochure origin and **not** a shop-member IdP. Shop members never get Nextcloud accounts.

Do **not** write secrets into git. Copy env **shape** from existing Doc `.env.example` / stay-up docs when someone later authors the real compose — not in this PR.

---

## 2. Cloudflare tunnel hostname reuse

Same **public** hostnames. The **origin** later moves Doc → McKing.

| Public hostname | Stays | What changes (later, after smoke PASS) |
|-----------------|-------|----------------------------------------|
| `api.projectcar.ca` | Yes | Tunnel ingress target: Doc `:8000` → McKing **shop-api** |
| `ops.projectcar.ca` | Yes | Tunnel ingress target: Doc `:3000` → McKing **shop-web** |
| `app.projectcar.ca` | Yes (until Ben cuts the alias) | Same shop-web origin as `ops.` |
| `projectcar.ca` / `www` | Yes | **No change.** Worker `projectcar-brochure`. |

Reuse — do **not** mint `api-mcking.`, a second waitlist host, or a new ops name.

Zone owns the flip **when Ben is ready**. Preferred origin style stays loopback-on-that-host (today Doc uses `http://127.0.0.1:3000`, not bare `localhost` — IPv6 `[::1]` 502 class). This paper does **not** invent McKing bind addresses.

Lead does not edit Cloudflare. Zone does not start McKing containers.

---

## 3. Dual-run vs Doc KeepAlive — safe order

**Dual-run first. Flip last. Retire Doc KeepAlive only after public smoke PASS.**

Never flip public origin to prove McKing. Never stop Doc LaunchAgents before the flip is proven.

| Order | Gate | Who | Do | Do not |
|-------|------|-----|----|--------|
| 0 | **This paper exists** | Docs | Done when this file merges. | Treat merge as GO. Flip anything. |
| 1 | **Separate GOs (later)** | Ben | Unfreeze Doc only via `doc-unfreeze.md` if the live build must move past `5swmVz`. Cutover GO is **another** explicit Ben sentence — not this file, not green CI, not lid-restore. | Infer cutover from unfreeze, or unfreeze from this plan. |
| 2 | **Dual-run** | Lead (McKing boxes) | Stand up McKing **shop-api** / **shop-web** / **cloudflared** **privately**. Doc KeepAlive **stays** the public origin (`com.projectcar.cloudflared` + shop-api + shop-web). | Point public hostnames at McKing. Disable Doc LaunchAgents. |
| 3 | **Private McKing smoke** | Lead | On-box / mesh checks only: API health body, shop-web login **200**, `next start` (not `next dev`), CORS OPTIONS shape. | Public DNS / tunnel ingress edit. Invent an IP in this doc. |
| 4 | **Parity + Lookout** | Lead + Lookout | §4 BUILD_ID / checkout parity. §6: public `GET /health` **200** and Lookout `projectcar-api-health-watch` still green **on Doc**. | Flip while freeze/BUILD_ID mismatch, or while Lookout / public health is red. |
| 5 | **Origin flip** | **Zone** (after Ben cutover GO **and** smoke PASS) | Retarget the **existing** `api` / `ops` / `app` tunnel hostnames to McKing shop-api / shop-web. | New public names. Touch apex / www Worker. Flip before PASS. |
| 6 | **Public smoke + Lookout** | Lead + Lookout (+ Garage waitlist e2e only after health 200) | Same probes as today (`api-stay-up.md`, `shop-web-stay-up.md`, `cors-origins.md`). Lookout `/health` **200** on the **same** public URL. | Call the cut done on SHA alone. |
| 7 | **Retire Doc shop KeepAlive** | Lead | Only after step 6 PASS. Then Doc shop LaunchAgents can stop. Doc lid-close 530 class **ends for shop** once origin is not Doc. | Stop Doc first “to force the cut.” |
| 8 | **Rollback if fail** | Zone + Lead | §7 — origin back to Doc LaunchAgents. | Leave public on a failing McKing origin. |

Lid-restore (`doc-lid-restore.md`) stays the **Doc** wake sequence for as long as Doc is the public origin. It is **not** a McKing compose runbook and **not** a pull.

---

## 4. Freeze / BUILD_ID parity (before any cut)

What must match **before** the origin flip. Green CI does **not** satisfy this.

| Clock | Pin today | Rule before cut |
|-------|-----------|-----------------|
| **Live Doc shop-web** | BUILD_ID **`5swmVz-T2CqKEQzTk1ifU`** at checkout **`4cf8924`** (Dashboard **#28**) | If the freeze still holds, McKing shop-web must serve **that same** BUILD_ID / checkout. Do **not** cut McKing to tip and leave Doc on `#28`. |
| **Git `main`** | Moves (OwnerShell **#69**, allowlist **#36**, docs, Shop OS CI) | **#36** / **#69** are **git-only** until `doc-unfreeze.md` finishes **after** Ben GO. |
| **Shop OS CI** | GitHub Actions on `apps/project-car/**` | Green **shop-os-ci** = pytest / typecheck / `next build` on git. **Not** Ben GO unfreeze. **Not** McKing cutover GO. Essay: `shop-os-ci.md`. |
| **After a real unfreeze** | New Doc `BUILD_ID` ≠ `5swmVz` | Then McKing must match **that** new id, not the frozen `#28` id. Ordered pull: `doc-unfreeze.md`. This paper does **not** perform that pull. |

**Parity means:** the build the public will hit after flip is the build Ben intends — frozen `#28` **or** a completed unfreeze — and Lead can show the McKing `.next/BUILD_ID` (or image label equivalent) **equals** that intent.

Do **not** use this file to unfreeze Doc. Do **not** rebuild Doc to tip to “get ready for McKing.”

---

## 5. CORS / origins unchanged

Browser Origins do **not** change when the API process moves hosts. Public API name stays `https://api.projectcar.ca`.

Live allowlist (`cors-origins.md`):

```
http://localhost:3000,http://127.0.0.1:3000,https://projectcar.ca,https://www.projectcar.ca,https://ops.projectcar.ca,https://app.projectcar.ca
```

| Must stay | Why |
|-----------|-----|
| `https://projectcar.ca`, `https://www.projectcar.ca` | Brochure waitlist `POST` / OPTIONS |
| `https://ops.projectcar.ca` | LIVE management UI |
| `https://app.projectcar.ca` | Temporary alias — still live until Ben cuts DNS |
| localhost / `127.0.0.1:3000` | Local / Doc demo |

Never `*`. Adding a McKing-only Origin is **not** required if browsers still call the same public hosts. After any later `.env` change, **Lead** restarts the API **on the host that is serving** (Doc today; McKing only after a real cut). Essay: `cors-origins.md`.

Shop-web host allowlist (`ops.` / `app.` / customer hosts / localhost — never `api.`) is a **#36** git-only change until unfreeze. This paper does not flip it.

---

## 6. Lookout `/health` gates (before DNS / origin flip)

Watch: Lookout **`projectcar-api-health-watch`** (today **`enabled:true`**, live `/health` **200** as of 2026-09-11 restore).

| When | Gate | Fail → |
|------|------|--------|
| **Before** private McKing work is used as a flip argument | Public `GET https://api.projectcar.ca/health` **200** and the watch is **enabled** / not ignored | Do not flip. Restore Doc (`doc-lid-restore.md`) if this is lid-close **530 / 1033**. |
| **Before** Zone retargets ingress | Same public health still **200** on **Doc** (dual-run: McKing is up privately; Doc still serves the name) | Do not flip a red edge “to see if McKing is better.” |
| **After** origin flip | Same URL **200** with the same JSON body. Lookout stays the public probe — do not invent a second watch name in this paper. | **Rollback** (§7). |

```bash
curl -sS https://api.projectcar.ca/health
# expect: {"status":"ok","service":"project-car-api"}
```

Public health **200** does **not** prove CORS (`cors-origins.md` OPTIONS smoke) and does **not** prove shop-web login.

Soft-530 fail-soft on the Worker (`#80`) stays useful for **future** Doc lid-close **while Doc is still origin**. It is not a reason to flip to McKing.

---

## 7. Rollback to Doc LaunchAgents

If McKing smoke fails — private or public — **public origin returns to Doc**.

| Step | Who | Do |
|------|-----|----|
| Keep Doc KeepAlive ready | Lead | Do **not** boot out `com.projectcar.cloudflared` / shop-api / shop-web until a McKing public PASS. On rollback they must already be startable. |
| Retarget tunnel hostnames to Doc | Zone | `api` → Doc `:8000`. `ops` + `app` → Doc `:3000` (`http://127.0.0.1:3000` class). Same public names. |
| Prove Doc public | Lead + Lookout | `GET /health` **200**; `ops.` / `app.` `/login` **200** (or 307 → `/login` with no localhost hop). Watch green. |
| Leave McKing compose | Lead | Stop or isolate the failing McKing shop services. Do not keep a half-flip. |
| Do not touch brochure | Zone / Garage | Worker stays. No apex/www “fix” as rollback. |

Rollback is **origin + process**, not “cut `app.`,” not “upload a Worker,” and not a Doc `git pull`.

---

## 8. No public DNS / tunnel origin flip until smoke PASS

Private McKing **PASS** (and §4 / §6) is the gate. Public names stay on Doc until then.

**McKing private smoke (minimum):**

| Check | Expect |
|-------|--------|
| shop-api health (on-box / mesh — **not** the public flip) | **200** `{"status":"ok","service":"project-car-api"}` |
| shop-web | **`next start`**; login **200**; `/` same-host hop to `/login` (no localhost) |
| BUILD_ID / checkout | Matches §4 intent |
| CORS shape | Same allowlist; OPTIONS still wants `Access-Control-Allow-Origin: https://projectcar.ca` once public still-on-Doc is re-checked |

**Public smoke after flip (same as today’s stay-up):**

| Check | Expect |
|-------|--------|
| `GET https://api.projectcar.ca/health` | **200** + known JSON |
| `GET https://ops.projectcar.ca/` | Redirect to `https://ops.projectcar.ca/login` (no localhost) |
| `GET https://ops.projectcar.ca/login` | **200** (use `app.` if client DNS cache misses `ops.`) |
| `GET https://app.projectcar.ca/login` | **200** — alias **still live** |
| Waitlist OPTIONS | `cors-origins.md` — `Origin: https://projectcar.ca` |
| Brochure | Home / Membership / Contact still Worker HTML. Waitlist e2e only after health **200**. |

None of the flip-row checks are a license to run the flip from this PR.

---

## 9. Explicit non-goals

| Do not | Why |
|--------|-----|
| Live-cut from this doc | Paper only. |
| Move the brochure to McKing / Doc / Pages from here | Worker `projectcar-brochure` stays. Pages git is a different, blocked plan. |
| Garage / Zone / Hatch fan-out | No Worker upload, no tunnel/DNS edit, no compose apply. |
| Unfreeze Doc / rebuild to tip | `doc-unfreeze.md` + Ben GO only. |
| Treat green **shop-os-ci** as GO | Git quality gate only. |
| New public hostnames | Hostname **reuse**. |
| Invent McKing IPs, compose paths, or tokens | Not known in this paper; do not guess. |
| Cut `app.`, Member host, MC cockpit, CF↔GitHub, About P3-2/P3-3 | Other plans / locks. |
| Claim Soft-530 is an active outage | Restore **LIVE** 2026-09-11. Future lid-close **530 / 1033** still expected **while Doc is origin**. |

---

## Ownership (when someone later executes)

| Role | Owns | Does not own |
|------|------|----------------|
| **Ben** | Explicit unfreeze GO and (separately) cutover GO | Writing compose from this file |
| **Lead** | Doc KeepAlive today; later McKing shop containers + private smoke + rollback processes | Cloudflare hostname / DNS edits |
| **Zone** | Tunnel hostname / DNS **after** GO + smoke PASS; rollback retarget | Starting McKing Docker; Doc `git pull` |
| **Lookout** | `projectcar-api-health-watch` on public `/health` | Origin flip; compose |
| **Garage** | Brochure waitlist e2e **after** public health 200 | Tunnel, Docker, uvicorn / Next restarts |
| **Chief / plan-improve** | Standing review of this paper | Substituting for Ben’s GOs |

---

## Success criteria (none are true yet)

| # | Check | Expect when actually done |
|---|--------|---------------------------|
| 1 | Public names unchanged | `api.` / `ops.` / `app.` still the shop names; brochure still Worker |
| 2 | Origin is McKing Docker | shop-api + shop-web + cloudflared on McKing; Doc shop KeepAlive **retired only after** PASS |
| 3 | BUILD_ID parity | McKing shop-web matches the intended pin (`5swmVz` if still frozen, else post-`doc-unfreeze.md` id) |
| 4 | Lookout | `projectcar-api-health-watch` **200** on `https://api.projectcar.ca/health` |
| 5 | CORS | Unchanged allowlist; waitlist OPTIONS still brochure Origin |
| 6 | Rollback path known | Doc LaunchAgents can take origin back without a new hostname |

**None of these are true today.** Today is Doc KeepAlive + Worker brochure + freeze + Soft-530 **LIVE**.

---

## Locks (copy — do not weaken)

- Host split stays: customer = projectcar.ca / www (Worker). Management = **ops.** (temporary `app.` alias still live). API = `api.`.
- Doc frozen at `4cf8924` / `5swmVz` until Ben GO (`doc-unfreeze.md`).
- Green shop-os-ci ≠ unfreeze ≠ McKing cut.
- No live cut, no DNS/origin flip, no Garage/Zone fan-out from this file.
- Brochure Worker stays. No McKing-as-brochure.
- No Stripe. The shop is not open.
