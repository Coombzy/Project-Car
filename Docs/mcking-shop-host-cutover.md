# McKing shop-host cutover

**Status:** Checklist / plan only — **not executed**. McKing path **OPEN**; shop CF cutover **not** GO.  
**Updated:** 2026-09-11 (~10:32 America/Edmonton hop fold)  
**Related:** `STATUS.md` (pointer only — **not** Next #1, **not** a GO), `deployment-guide.md`, `api-stay-up.md`, `shop-web-stay-up.md`, `doc-unfreeze.md` (Ben GO pull — **not** this cut), `doc-lid-restore.md` (Doc process wake only), `cors-origins.md`, `shop-os-ci.md` (green CI ≠ unfreeze, ≠ this cut), `home-lab-specification.md`, `brochure-worker-deploy.md`, `member-host-cutover.md` (different cut — customer `/member` host), `member-zone-edge.md` (Next #1 still `/member*` → Doc `:3000`)

Draft paper for a **later** move of Shop OS origins (`api.` / `ops.` / temporary `app.`) from **Doc LaunchAgents** onto **McKing Docker**, reusing the same Cloudflare tunnel public hostnames. Brochure stays on Worker `projectcar-brochure`.

**Hard gate before any public shop CF hostname leaves Doc** (`cloud.` / `api.` / `app.` / `ops.` only — **vault EXCLUDED**): the Soft-530 dual-run acceptance table below. Dual-run is **not** “McKing on public `api.` / `ops.` / `app.` while Doc is still up.” Hub dual-run NC+VW healthy does **not** mean shop CF hostname cutover GO. Vault is already **LIVE verified** on McKing — that does **not** pass this shop gate.

This file does **not** unfreeze Doc, does **not** flip DNS or tunnel origin, does **not** compose-down, and does **not** attach McKing to public shop hostnames. Paper only.

Do **not** invent Stripe, a shop opening, a shipped Member host migration, a removed `app.` alias, McKing IPs, a McKing compose file path, or tunnel / API token values.

---

## Locks (read first — do not weaken)

| Lock | Meaning |
|------|---------|
| **Paper only** | Merging this file is **not** a cut. No live Cloudflare / DNS / tunnel flip / compose-down / LaunchAgent changes from this PR. |
| **Hop OPEN ≠ cutover GO ≠ Doc unfreeze** | Path OPEN (sshd / docker / `/opt/mission-control`) is **not** license to leave Doc as public origin, and **not** Ben GO unfreeze. Freeze stays **`4cf8924`** / **`5swmVz`** until **Ben GO**. |
| **Not Next #1** | STATUS Next #1 is Member UI on projectcar.ca (`member-host-cutover.md` / `member-zone-edge.md`). This McKing host move is a **later** machine plan. Do **not** treat it as GO’d. If McKing later becomes shop origin, Next #1 `/member*` retargets with the Soft-530 flip — **not now**. |
| **Not Doc unfreeze** | Doc checkout stays frozen at **`4cf8924`** / BUILD_ID **`5swmVz-T2CqKEQzTk1ifU`** until **Ben GO**. Green **shop-os-ci** is **not** that GO. Pull checklist: `doc-unfreeze.md`. This paper must **not** be read as license to pull or rebuild on Doc. |
| **No public shop flip until Soft-530 dual-run gate PASS** | Do **not** retarget **shop** tunnel origin or public DNS (`cloud.` / `api.` / `app.` / `ops.`) until the **Soft-530 dual-run acceptance gate** (five rows below) PASSes. This gate is **Doc shop hosts only** — **vault EXCLUDED** (already LIVE on McKing). Private smoke / hub NC+VW dual-run healthy / hop OPEN / vault LIVE alone are **not** shop cutover GO. |
| **Brochure stays Worker** | `projectcar.ca` / www stay Cloudflare Worker **`projectcar-brochure`**. Do **not** move the brochure to McKing. |
| **No Garage / Zone fan-out** | Garage does not upload Worker HTML from this file. Zone does not edit tunnel / DNS from this file. Hatch does not execute. |
| **CORS / public names unchanged** | Same Origins (`cors-origins.md`). Same public hostnames (`api.` / `ops.` / `app.`). Origin **host** may move later; names do not. |

Ben decides when (if) to execute. This file does **not** ping Ben and is **not** a live cut.

---

## Reality today (do not claim this is done)

Soft-530 is **CLEAR** (Doc origin **LIVE** 2026-09-11). Future lid-close can still **530 / 1033**. Lookout `projectcar-api-health-watch` is **`enabled:true`**. **#78 lookout-resume** is **LIVE-SUPERSEDED** — that watch is already **`enabled:true` while Doc stays frozen** at `4cf8924` / `5swmVz`. Soft-530 companions stay **HOLD**.

**Shop OS/MC hop ~10:32 America/Edmonton** (lightning / Omarchy) opened the McKing path. Do **not** keep the stale hub line “McKing is not on the tailnet / migrate not started.” [home-lab-specification.md](home-lab-specification.md) host table + anti-goals now match STATUS dual-tunnel + vault LIVE (McKing / `lightning` = `vault.` → `:8222`; Doc tunnel = `cloud.` + `api.` + `app.` + `ops.` only). 2026-08-16 rows in `nextcloud-progress.md` can still be stale for that path — this paper is the shop-host reality stamp.

| Surface | Live origin |
|---------|-------------|
| **Brochure** | Cloudflare Worker **`projectcar-brochure`** Direct Upload of `apps/website/html`. **Stays.** Not Doc. Not McKing. |
| **Shop API** | Host **cloudflared** on Doc → LaunchAgent **`com.projectcar.shop-api`** → uvicorn **`:8000`**. Public `https://api.projectcar.ca`. **Doc still owns** the public name. |
| **Ops / app shop-web** | Same Doc cloudflared → LaunchAgent **`com.projectcar.shop-web`** → **`next start`** **`:3000`**. Public `https://ops.projectcar.ca` (LIVE management) + temporary `https://app.projectcar.ca`. **Doc still owns** the public names. |
| **Doc KeepAlive** | `com.projectcar.cloudflared` + `com.projectcar.shop-api` + `com.projectcar.shop-web`. Doc stays the **public CF origin / KeepAlive backup**. Lid-close still kills the Mac. |
| **Doc checkout** | **Frozen** at **`4cf8924`** / BUILD_ID **`5swmVz-T2CqKEQzTk1ifU`** (Dashboard **#28**) until **Ben GO** (`doc-unfreeze.md`). **#36** / **#69** stay **git-only**. Hop OPEN ≠ unfreeze. |
| **Git compose today** | `infra/compose/compose.yaml` is **shop Postgres only**. It does **not** start shop-api, shop-web, or cloudflared. Do not invent those services as already in git. |
| **McKing path (OPEN)** | **OPEN** 2026-09-11 ~10:32 America/Edmonton: **sshd / docker / `/opt/mission-control`**. Hub dual-run **NC+VW healthy** on **Doc + McKing**. Path OPEN ≠ shop CF hostname cutover GO ≠ Doc unfreeze ≠ `cloud.*` leave. Vault is **LIVE verified** on McKing (separate living-ops row) — vault LIVE ≠ shop cutover GO ≠ Doc unfreeze. |
| **Vault (LIVE verified — not this shop cut)** | **`vault.projectcar.ca` LIVE** on McKing: `cloudflared` → `localhost:8222`. `/api/config` reports **2026.6.0** (Chief verified). Soft-530 five-row gate does **not** apply to vault. Doc lid-restore / KeepAlive must **not** recreate `vault.` ingress on Doc. |
| **Hub NC (McKing)** | **lab/hub loopback-only — unpublished.** `/opt/mission-control` NC is **not** on the McKing CF tunnel. Public `cloud.projectcar.ca` stays on **Doc** until explicit **Ben GO**. Paper path: Tailscale Serve HTTPS mirroring VW Serve at `lightning.tailbe8f55.ts.net` + `NEXTCLOUD_TRUSTED_DOMAINS` MagicDNS — **not** a Cloudflare cutover of `cloud.*`. |
| **McKing shop role (later)** | Later: Shop API + shop-web via Docker + tunnel hostname reuse — **only after** the Soft-530 dual-run five-row gate PASSes. Do **not** treat hub NC+VW dual-run healthy as that gate. |

`app.` stays the temporary alias until Ben cuts that DNS (`app-alias-cut.md`). This host move does **not** require cutting `app.`.

---

## Dual-tunnel ownership (separate from shop CF cutover)

**Living-ops lock. Vault is LIVE verified. Not this shop-host cutover. Not a shop Zone live apply.** STATUS keeps this as its **own** row. Hop OPEN ≠ shop cutover GO ≠ Doc unfreeze.

| Tunnel | Hostnames | Origin / role |
|--------|-----------|----------------|
| **Doc tunnel** | **`cloud.` + `api.` + `app.` + `ops.` only** | Shop Soft-530 / KeepAlive (plus `cloud.`). Public **`cloud.projectcar.ca` stays on Doc** until explicit **Ben GO**. Public shop names stay on Doc until the five-row Soft-530 gate PASSes. That gate is **shop hosts only** — **vault EXCLUDED**. |
| **McKing-only tunnel** | **`vault.projectcar.ca` — LIVE verified** (+ **unpublished** NC, not a tunnel hostname) | McKing `cloudflared` → **`localhost:8222`**. Public `/api/config` reports **2026.6.0** (Chief verified). Not the Doc mission-control token. Not shop `api.` / `ops.` / `app.`. McKing `/opt/mission-control` NC is **lab/hub loopback-only** — **not** on this tunnel. |

**Anti-goals (do not weaken):**

- Never move the **Doc mission-control token** for `vault.`.
- Soft-530 lid-restore / LaunchAgent KeepAlive must **not** recreate `vault.` ingress on Doc.
- Vault LIVE ≠ shop hostname leave ≠ Doc unfreeze ≠ McKing NC publish.
- Do **not** point the `cloud.*` tunnel or CNAME at McKing until a dual-run acceptance gate PASSes (McKing `status.php` parity vs Doc `status.php`) **and** explicit **Ben GO**.

Hop OPEN ≠ shop CF cutover GO ≠ Doc unfreeze ≠ `cloud.*` leave. Shop CF cutover stays paper. Vault being LIVE is **not** a shop hostname leave. Dual-tunnel matrix stays Doc = `cloud.` / `api.` / `app.` / `ops.`; McKing = `vault.` (+ unpublished NC).

---

## Dual-Nextcloud ownership (paper — not a `cloud.*` CF cutover)

**Living-ops lock. Separate from shop CF cutover. Separate from vault LIVE.** Public `cloud.projectcar.ca` stays on **Doc** until explicit **Ben GO**. McKing `/opt/mission-control` Nextcloud stays **lab/hub loopback-only** (unpublished). Dual-tunnel matrix does **not** change: Doc = `cloud.` / `api.` / `app.` / `ops.`; McKing = `vault.` (+ unpublished NC). #82 gate unchanged. Soft-530 companions **HOLD**. Vault LIVE unchanged.

This section is **not** a Cloudflare cutover of `cloud.*`. Merging this paper is **not** Ben GO. Hub dual-run NC+VW healthy / hop OPEN / vault LIVE do **not** move `cloud.*`.

### Paper path (later execute — not this PR)

Mirror Vaultwarden Tailscale Serve on McKing (`lightning.tailbe8f55.ts.net`) — **HTTPS Serve for McKing NC**, plus `NEXTCLOUD_TRUSTED_DOMAINS` MagicDNS hostnames.

| Step | Do | Do not |
|------|----|--------|
| 1. Serve | Tailscale Serve HTTPS on McKing NC (loopback origin), same class as VW Serve at `lightning.tailbe8f55.ts.net` | Point `cloud.*` tunnel / CNAME at McKing. Add NC to the McKing CF tunnel. |
| 2. Trusted domains | Add MagicDNS hostnames to `NEXTCLOUD_TRUSTED_DOMAINS` (and matching overwrite URL if needed) | Publish McKing NC on Cloudflare / `cloud.projectcar.ca` |
| 3. Dual-run gate (before any later `cloud.*` leave) | Parity check McKing NC `status.php` vs **Doc** `status.php` (installed, not maintenance, version) **and** explicit **Ben GO** | Treat hub “NC+VW healthy” / hop OPEN / vault LIVE / Serve stand-up as that gate |

### `cloud.*` dual-run acceptance gate (before any `cloud.*` tunnel / CNAME leave)

**Hard gate for public `cloud.projectcar.ca` only.** Separate from the Soft-530 five-row **shop** gate. Soft-530 five-row still blocks shop hostname leave (`cloud.` / `api.` / `app.` / `ops.`). This table is the **extra** lock so hub dual-run is not misread as “move `cloud.*` to McKing.”

| # | Gate | Pass | Fail |
|---|------|------|------|
| 1 | **Doc still owns public `cloud.`** | `cloud.projectcar.ca` remains the Doc tunnel hostname until **Ben GO** | Do not retarget tunnel / CNAME |
| 2 | **McKing NC unpublished** | `/opt/mission-control` NC is loopback / Tailscale Serve only — **not** a McKing CF hostname | Do not attach McKing NC to `cloud.*` “to prove it” |
| 3 | **`status.php` parity** | McKing `status.php` matches Doc `status.php` (installed, not maintenance, version) | Version / maintenance / installed mismatch — do not cut |
| 4 | **Explicit Ben GO** | A Ben sentence that public `cloud.*` may leave Doc | Infer GO from hop OPEN, vault LIVE, Serve stand-up, or this paper |

**Anti-goals (do not weaken):**

- Do **not** point the `cloud.*` tunnel or CNAME at McKing until this gate PASSes.
- Do **not** treat Tailscale Serve as a Cloudflare cutover of `cloud.*`.
- McKing NC stays **unpublished** (lab/hub loopback-only) until that GO. Not on the McKing CF tunnel (that tunnel stays **`vault.` only**).
- Public `cloud.projectcar.ca` stays on **Doc** until that GO.

---

## Soft-530 dual-run acceptance gate (before any public shop CF hostname leaves Doc)

**Hard gate for Doc shop hosts only (`cloud.` / `api.` / `app.` / `ops.`).** **Vault is EXCLUDED** — `vault.projectcar.ca` is already **LIVE verified** on McKing. Do **not** cut public `api.` / `ops.` / `app.` (or `cloud.`) off Doc until **all five** rows PASS. This paper is **not** that shop cut. Soft-530 is **CLEAR** today (Doc origin **LIVE** 2026-09-11); this table is for a **later** shop execution — not a claim the shop cut started, and not a claim Soft-530 is an active outage. Vault LIVE does **not** satisfy this gate.

| # | Gate | Pass | Fail |
|---|------|------|------|
| 1 | **Compose = freeze pin** | McKing shop compose **image digests** + shop-web **BUILD_ID** match Doc frozen checkout **`4cf8924`** / BUILD_ID **`5swmVz-T2CqKEQzTk1ifU`** until **Ben GO** unfreeze. After a real unfreeze, match the **new** Doc pin — not tip-of-`main` by accident. Green **shop-os-ci** ≠ Ben GO ≠ this gate. | Do not cut. Do not treat green CI as parity. |
| 2 | **Dual-run window** | Doc KeepAlive **still owns** public `api.` / `ops.` / temporary `app.`. McKing proves shop health on **Tailscale-only** (or a **staging** hostname) — **not** public Cloudflare yet. Acceptance artifact **when it lands:** the in-flight **Doc dual-run evidence card** (Tailscale / private only). Until that card lands, this row is **not** PASS. Hub dual-run NC+VW healthy on Doc+McKing is **not** that card and is **not** shop CF hostname cutover GO. Still **no** public McKing attach for shop. | Do not attach McKing to public CF hostnames “to prove it.” |
| 3 | **Lookout streak** | Lookout **`projectcar-api-health-watch`**: **N = 15** consecutive public `GET https://api.projectcar.ca/health` **200** (same JSON body) over **~15 minutes** (~one probe/minute), **zero** CF **1033** / **530** / **502** in that window. Ben may tune **N** in **10–20** and the window; do not cut on a single 200. | Any 1033 / 530 / 502 in the window **resets** the streak. Restore Doc (`doc-lid-restore.md`) if this is lid-close. |
| 4 | **Rollback one-liner** | Re-point **cloudflared** to **Doc LaunchAgents**. Keep `com.projectcar.cloudflared` + shop-api + shop-web **available** until McKing **public** smoke **PASS**. | Do not retire Doc agents before PASS. |
| 5 | **Brochure fail-soft stays** | Soft-530 Discord waitlist fail-soft (**#80** `waitlist.js?v=3`) **stays live** on Worker `projectcar-brochure` **during** the cut. Do **not** upload a Worker that drops Discord fail-soft. | Do not touch brochure HTML / Worker as part of this host move. **#82** Home canonical/og/sitemap stays **not** Worker-live — unchanged. |

**Rollback (one line):** re-point cloudflared to Doc LaunchAgents.

---

## 1. Target compose services on McKing (high-level)

Later McKing shop-host is **Docker**. Name the three shop-edge services. Do **not** invent a compose file path, image tags, host IPs, or secret values.

| Service | Role | Public name (reuse) | Notes |
|---------|------|---------------------|-------|
| **shop-api** | FastAPI shop API (today uvicorn on Doc `:8000`) | `api.projectcar.ca` | Same health body: `{"status":"ok","service":"project-car-api"}`. Lead still owns the API process — on McKing that is the container, not Doc `run-shop-api.sh`. |
| **shop-web** | Next.js shop UI (today `next start` on Doc `:3000`) | `ops.projectcar.ca` + temporary `app.projectcar.ca` | Must stay **`next start`**, not `next dev`. Soft-530 gate row 1 + §4: **BUILD_ID** + **image digest** parity. |
| **cloudflared** | Tunnel client **on McKing** | Same three public hostnames | Attaches to public `api.` / `ops.` / `app.` **only after** the Soft-530 dual-run gate PASSes. Dual-run health is Tailscale / staging — **not** this public client. Zone owns hostname / DNS rules. Do **not** invent a tunnel token or config path here. |

Shop data stays **dedicated shop Postgres** — never Nextcloud MariaDB (`infra/compose` today; Mission Control hub is a separate stack). This paper does **not** invent where McKing mounts that DB or a second compose path.

Nextcloud / Vaultwarden on McKing is the **hub** move (Docker + Nextcloud home). McKing NC stays **lab/hub loopback-only** (unpublished) until explicit **Ben GO** + `status.php` parity vs Doc — paper path is Tailscale Serve + MagicDNS trusted domains, **not** a `cloud.*` CF cutover. It is **not** the brochure origin and **not** a shop-member IdP. Shop members never get Nextcloud accounts.

Do **not** write secrets into git. Copy env **shape** from existing Doc `.env.example` / stay-up docs when someone later authors the real compose — not in this PR.

---

## 2. Cloudflare tunnel hostname reuse

Same **public** hostnames. The **origin** later moves Doc → McKing.

| Public hostname | Stays | What changes (later, after Soft-530 dual-run gate PASS) |
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

**Dual-run first (Tailscale / staging only). Soft-530 dual-run gate PASS. Flip last. Retire Doc KeepAlive only after McKing public smoke PASS.**

Never flip public origin to prove McKing. Never stop Doc LaunchAgents before the flip is proven. Dual-run does **not** mean two public Cloudflare origins.

| Order | Gate | Who | Do | Do not |
|-------|------|-----|----|--------|
| 0 | **This paper exists** | Docs | Done when this file merges. | Treat merge as GO. Flip anything. |
| 1 | **Separate GOs (later)** | Ben | Unfreeze Doc only via `doc-unfreeze.md` if the live build must move past `5swmVz`. Cutover GO is **another** explicit Ben sentence — not this file, not green CI, not lid-restore. | Infer cutover from unfreeze, or unfreeze from this plan. |
| 2 | **Dual-run window** | Lead (McKing boxes) | Stand up McKing **shop-api** / **shop-web** on **Tailscale-only** (or a **staging** hostname). Doc KeepAlive **stays** the public CF origin (`com.projectcar.cloudflared` + shop-api + shop-web). Gate row 2 PASSes on the in-flight **Doc dual-run evidence card** (Tailscale / private only) **when it lands** — not on hub NC+VW dual-run healthy, not on hop OPEN. | Point public `api.` / `ops.` / `app.` at McKing. Start McKing cloudflared against those public names. Disable Doc LaunchAgents. |
| 3 | **Private McKing smoke** | Lead | Tailscale / staging / on-box only: API health body, shop-web login **200**, `next start` (not `next dev`), CORS OPTIONS shape. | Public DNS / tunnel ingress edit. Invent an IP in this doc. |
| 4 | **Soft-530 dual-run gate** | Lead + Lookout | All five rows in the gate table: compose **BUILD_ID** + **image digests** = freeze pin; Doc still owns public names; Lookout **N = 15** consecutive public `/health` **200** with **zero** CF **1033**; rollback one-liner ready; **#80** `waitlist.js?v=3` still on the Worker. | Flip on a single 200, on green **shop-os-ci**, or while Doc agents are already stopped. |
| 5 | **Origin flip** | **Zone** (after Ben cutover GO **and** Soft-530 dual-run gate PASS) | Retarget the **existing** `api` / `ops` / `app` tunnel hostnames to McKing shop-api / shop-web. | New public names. Touch apex / www Worker. Flip before the five-row gate PASSes. |
| 6 | **Public smoke + Lookout** | Lead + Lookout (+ Garage waitlist e2e only after health 200) | Same probes as today (`api-stay-up.md`, `shop-web-stay-up.md`, `cors-origins.md`). Lookout `/health` **200** on the **same** public URL. | Call the cut done on SHA alone. |
| 7 | **Retire Doc shop KeepAlive** | Lead | Only after step 6 PASS. Then Doc shop LaunchAgents can stop. Doc lid-close 530 class **ends for shop** once origin is not Doc. | Stop Doc first “to force the cut.” |
| 8 | **Rollback if fail** | Zone + Lead | One-liner: re-point cloudflared to Doc LaunchAgents (§7). | Leave public on a failing McKing origin. |

Lid-restore (`doc-lid-restore.md`) stays the **Doc** wake sequence for as long as Doc is the public origin. It is **not** a McKing compose runbook and **not** a pull.

---

## 4. Freeze / BUILD_ID / image-digest parity (before any cut)

Soft-530 dual-run gate **row 1**. What must match **before** the origin flip. Green CI does **not** satisfy this.

| Clock | Pin today | Rule before cut |
|-------|-----------|-----------------|
| **Live Doc shop-web** | BUILD_ID **`5swmVz-T2CqKEQzTk1ifU`** at checkout **`4cf8924`** (Dashboard **#28**) | If the freeze still holds, McKing shop-web must serve **that same** BUILD_ID / checkout. Do **not** cut McKing to tip and leave Doc on `#28`. |
| **McKing compose images** | Digests pinned to that freeze | shop-api / shop-web (and any shop-edge image the compose starts) must match the freeze pin — **digest**, not a floating `:latest`. Until Ben GO unfreeze, that pin is Doc **`4cf8924`** / **`5swmVz`**. |
| **Git `main`** | Moves (OwnerShell **#69**, allowlist **#36**, docs, Shop OS CI) | **#36** / **#69** are **git-only** until `doc-unfreeze.md` finishes **after** Ben GO. |
| **Shop OS CI** | GitHub Actions on `apps/project-car/**` | Green **shop-os-ci** = pytest / typecheck / `next build` on git. **Not** Ben GO unfreeze. **Not** McKing cutover GO. **Not** Soft-530 dual-run gate PASS. Essay: `shop-os-ci.md`. |
| **After a real unfreeze** | New Doc `BUILD_ID` ≠ `5swmVz` | Then McKing **BUILD_ID** + **image digests** must match **that** new id, not the frozen `#28` id. Ordered pull: `doc-unfreeze.md`. This paper does **not** perform that pull. |

**Parity means:** the build the public will hit after flip is the build Ben intends — frozen `#28` **or** a completed unfreeze — and Lead can show the McKing `.next/BUILD_ID` **and** compose image **digests** **equal** that intent.

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

Soft-530 dual-run gate **row 3**. Watch: Lookout **`projectcar-api-health-watch`** (today **`enabled:true`**, live `/health` **200** as of 2026-09-11 restore). **#78 lookout-resume** is **LIVE-SUPERSEDED**. Soft-530 **CLEAR** live honesty is unchanged — this streak is a **later** cut gate, not a claim the edge is down now.

**Default streak:** **N = 15** consecutive public `GET /health` **200** over **~15 minutes** (~one probe/minute), **zero** CF **1033** / **530** / **502**. Ben may tune **N** in **10–20** and the window. A single 200 is **not** the gate.

| When | Gate | Fail → |
|------|------|--------|
| **Before** private McKing work is used as a flip argument | Public `GET https://api.projectcar.ca/health` **200** and the watch is **enabled** / not ignored | Do not flip. Restore Doc (`doc-lid-restore.md`) if this is lid-close **530 / 1033**. |
| **Before** Zone retargets ingress | Soft-530 dual-run gate: Doc still serves the public names; McKing is Tailscale / staging only; Lookout **N** consecutive **200**s with **zero** CF **1033** | Do not flip a red edge “to see if McKing is better.” Do not cut on one 200. |
| **After** origin flip | Same URL **200** with the same JSON body. Lookout stays the public probe — do not invent a second watch name in this paper. | **Rollback** (§7) — re-point cloudflared to Doc LaunchAgents. |

```bash
curl -sS https://api.projectcar.ca/health
# expect: {"status":"ok","service":"project-car-api"}
```

Public health **200** does **not** prove CORS (`cors-origins.md` OPTIONS smoke) and does **not** prove shop-web login.

Soft-530 Discord waitlist fail-soft (**#80** `waitlist.js?v=3`) **stays live** on Worker `projectcar-brochure` **during** the cut (gate row 5). It is also still useful for **future** Doc lid-close **while Doc is origin**. It is **not** a reason to flip to McKing. **#82** stays not Worker-live.

---

## 7. Rollback to Doc LaunchAgents

**One-liner:** re-point cloudflared to Doc LaunchAgents.

If McKing smoke fails — Tailscale / staging **or** public — **public origin returns to Doc**. Keep Doc agents **available** until McKing **public** smoke **PASS** (Soft-530 dual-run gate row 4).

| Step | Who | Do |
|------|-----|----|
| Keep Doc KeepAlive ready | Lead | Do **not** boot out `com.projectcar.cloudflared` / shop-api / shop-web until a McKing public PASS. On rollback they must already be startable. |
| Re-point cloudflared to Doc | Zone | Same one-liner: public `api` / `ops` / `app` back to Doc LaunchAgents — `api` → Doc `:8000`; `ops` + `app` → Doc `:3000` (`http://127.0.0.1:3000` class). Same public names. |
| Prove Doc public | Lead + Lookout | `GET /health` **200**; `ops.` / `app.` `/login` **200** (or 307 → `/login` with no localhost hop). Watch green. |
| Leave McKing compose | Lead | Stop or isolate the failing McKing shop services. Do not keep a half-flip. |
| Do not touch brochure | Zone / Garage | Worker stays, including Soft-530 Discord waitlist fail-soft (**#80** `waitlist.js?v=3`). No apex/www “fix” as rollback. |

Rollback is **origin + process**, not “cut `app.`,” not “upload a Worker,” and not a Doc `git pull`.

---

## 8. No public DNS / tunnel origin flip until Soft-530 dual-run gate PASS

The **Soft-530 dual-run acceptance gate** (five rows) is the gate. Private McKing smoke + §4 + §6 are inputs to that table — not a shortcut around it. Public names stay on Doc until then.

**McKing Tailscale / staging smoke (minimum) — not public CF:**

| Check | Expect |
|-------|--------|
| shop-api health (Tailscale / staging / on-box — **not** the public flip) | **200** `{"status":"ok","service":"project-car-api"}` |
| shop-web | **`next start`**; login **200**; `/` same-host hop to `/login` (no localhost) |
| BUILD_ID / checkout / image digests | Matches Soft-530 gate row 1 + §4 intent |
| CORS shape | Same allowlist; OPTIONS still wants `Access-Control-Allow-Origin: https://projectcar.ca` once public still-on-Doc is re-checked |

**Public smoke after flip (same as today’s stay-up):**

| Check | Expect |
|-------|--------|
| `GET https://api.projectcar.ca/health` | **200** + known JSON |
| `GET https://ops.projectcar.ca/` | Redirect to `https://ops.projectcar.ca/login` (no localhost) |
| `GET https://ops.projectcar.ca/login` | **200** (use `app.` if client DNS cache misses `ops.`) |
| `GET https://app.projectcar.ca/login` | **200** — alias **still live** |
| Waitlist OPTIONS | `cors-origins.md` — `Origin: https://projectcar.ca` |
| Brochure | Home / Membership / Contact still Worker HTML. Soft-530 Discord waitlist fail-soft (**#80** `waitlist.js?v=3`) **still live**. Waitlist e2e only after health **200**. **#82** unchanged (not Worker-live). |

None of the flip-row checks are a license to run the flip from this PR.

---

## 9. Explicit non-goals

| Do not | Why |
|--------|-----|
| Live-cut from this doc | Paper only. |
| Treat hop OPEN / hub NC+VW dual-run as cutover GO | Path OPEN ≠ Soft-530 five-row PASS ≠ Doc unfreeze ≠ `cloud.*` leave. |
| Point `cloud.*` tunnel / CNAME at McKing | Public `cloud.` stays on **Doc** until **Ben GO** + `status.php` parity vs Doc. Paper path is Tailscale Serve + `NEXTCLOUD_TRUSTED_DOMAINS` MagicDNS — **not** a CF cutover of `cloud.*`. |
| Publish McKing `/opt/mission-control` NC on Cloudflare | Lab/hub loopback-only (unpublished). McKing CF tunnel stays **`vault.` only**. |
| Recreate `vault.` ingress on Doc / move the Doc mission-control token for `vault.` | Dual-tunnel lock: `vault.` is **LIVE verified** on McKing (`cloudflared` → `localhost:8222`; `/api/config` **2026.6.0**, Chief verified). Lid-restore / KeepAlive must **not** recreate that ingress on Doc. Vault LIVE ≠ shop hostname leave ≠ Doc unfreeze. |
| Move the brochure to McKing / Doc / Pages from here | Worker `projectcar-brochure` stays. Pages git is a different, blocked plan. |
| Garage / Zone / Hatch fan-out | No Worker upload, no tunnel/DNS edit, no compose apply. |
| Unfreeze Doc / rebuild to tip | `doc-unfreeze.md` + Ben GO only. |
| Treat green **shop-os-ci** as GO | Git quality gate only. Not unfreeze. Not Soft-530 dual-run gate PASS. |
| Attach McKing to public CF during dual-run | Dual-run = Tailscale / staging only. Doc KeepAlive owns public `api.` / `ops.` / `app.` until the five-row gate PASSes. |
| Drop Soft-530 Discord fail-soft on the Worker | **#80** `waitlist.js?v=3` stays live on `projectcar-brochure` **during** the cut. |
| New public hostnames | Hostname **reuse**. |
| Invent McKing IPs, compose paths, or tokens | Not known in this paper; do not guess. |
| Cut `app.`, Member host, MC cockpit, CF↔GitHub, About P3-2/P3-3 | Other plans / locks. |
| Claim Soft-530 is an active outage | Restore **LIVE** 2026-09-11. Future lid-close **530 / 1033** still expected **while Doc is origin**. |

---

## Ownership (when someone later executes)

| Role | Owns | Does not own |
|------|------|----------------|
| **Ben** | Explicit unfreeze GO and (separately) cutover GO | Writing compose from this file |
| **Lead** | Doc KeepAlive today; later McKing shop containers + Tailscale / staging smoke + rollback processes | Cloudflare hostname / DNS edits |
| **Zone** | Tunnel hostname / DNS **after** GO + Soft-530 dual-run gate PASS; rollback = re-point cloudflared to Doc LaunchAgents | Starting McKing Docker; Doc `git pull` |
| **Lookout** | `projectcar-api-health-watch` on public `/health` — **N = 15** consecutive **200**s, zero CF **1033**, before any public cut (Ben may tune **N** 10–20) | Origin flip; compose |
| **Garage** | Brochure waitlist e2e **after** public health 200 | Tunnel, Docker, uvicorn / Next restarts |
| **Chief / plan-improve** | Standing review of this paper | Substituting for Ben’s GOs |

---

## Success criteria (none are true yet)

| # | Check | Expect when actually done |
|---|--------|---------------------------|
| 1 | Public names unchanged | `api.` / `ops.` / `app.` still the shop names; brochure still Worker |
| 2 | Origin is McKing Docker | shop-api + shop-web + cloudflared on McKing; Doc shop KeepAlive **retired only after** public PASS |
| 3 | BUILD_ID + digest parity | McKing compose matches the intended pin (`4cf8924` / `5swmVz` if still frozen, else post-`doc-unfreeze.md` id + matching image digests) |
| 4 | Lookout streak | Soft-530 dual-run gate: **N = 15** consecutive public `/health` **200**, **zero** CF **1033** (Ben may tune **N** 10–20) |
| 5 | CORS | Unchanged allowlist; waitlist OPTIONS still brochure Origin |
| 6 | Rollback path known | One-liner: re-point cloudflared to Doc LaunchAgents — agents still available until McKing public PASS |
| 7 | Brochure fail-soft | **#80** `waitlist.js?v=3` still live on Worker during the cut |

**None of these public-cutover checks are true today.** McKing path is **OPEN**; Doc KeepAlive still owns public `api.` / `ops.` / `app.`; Worker brochure + freeze + Soft-530 **LIVE**. Hop OPEN ≠ these rows.

---

## Locks (copy — do not weaken)

- Host split stays: customer = projectcar.ca / www (Worker). Management = **ops.** (temporary `app.` alias still live). API = `api.`.
- Doc frozen at `4cf8924` / `5swmVz` until Ben GO (`doc-unfreeze.md`). Hop OPEN ≠ unfreeze.
- Green shop-os-ci ≠ unfreeze ≠ McKing cut ≠ Soft-530 dual-run gate PASS.
- McKing path **OPEN** (sshd / docker / `/opt/mission-control`; hub dual-run NC+VW healthy on Doc+McKing). Hop OPEN ≠ cutover GO. Doc KeepAlive still owns public `api.` / `ops.` / `app.`.
- No public **shop** CF hostname leaves Doc until the five-row Soft-530 dual-run gate PASSes. Dual-run = Tailscale / staging only. Gate row 2 artifact when it lands: Doc dual-run evidence card (Tailscale / private only). Still no public McKing attach for shop. **Vault EXCLUDED** from this gate (already LIVE).
- Vault is **LIVE verified** on McKing (`cloudflared` → `localhost:8222`; `/api/config` **2026.6.0**, Chief verified). Dual-tunnel ownership is a **separate** living-ops row: Doc tunnel = `cloud.` + `api.` + `app.` + `ops.` only; McKing-only = `vault.projectcar.ca` (+ **unpublished** NC). Soft-530 five-row gate = Doc shop hosts only — **vault EXCLUDED**. Never move the Doc mission-control token for `vault.`; lid-restore / KeepAlive must **not** recreate `vault.` ingress on Doc. Vault LIVE ≠ shop hostname leave ≠ Doc unfreeze.
- **Dual-Nextcloud (paper):** public `cloud.projectcar.ca` stays on **Doc** until explicit **Ben GO**. McKing `/opt/mission-control` NC remains **lab/hub loopback-only** (unpublished). Paper path = Tailscale Serve HTTPS mirroring VW Serve at `lightning.tailbe8f55.ts.net` + `NEXTCLOUD_TRUSTED_DOMAINS` MagicDNS — **not** a Cloudflare cutover of `cloud.*`. Do **not** point `cloud.*` tunnel/CNAME at McKing until `status.php` parity vs Doc **and** Ben GO. #82 unchanged. Soft-530 companions **HOLD**. Vault LIVE unchanged.
- Rollback one-liner: re-point cloudflared to Doc LaunchAgents.
- Soft-530 Discord waitlist fail-soft (**#80** `waitlist.js?v=3`) stays on the Worker during the cut. **#82** unchanged.
- No live cut, no DNS/origin flip, no compose-down, no Garage/Zone fan-out from this file.
- Brochure Worker stays. No McKing-as-brochure.
- No Stripe. The shop is not open.
