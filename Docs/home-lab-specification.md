# Home Lab Specification

**Last Updated:** 2026-09-11  
**Status:** Living spec  
**Canonical:** `Coombzy/Project-Car` → `Docs/home-lab-specification.md`

Host lock for the lab: who runs what **now**, who takes it **later**, and what is **not** on these machines. Product live/next/later stays in [STATUS.md](STATUS.md). This file is the machine map. Dual-tunnel + vault LIVE match STATUS (2026-09-11). Shop CF cutover stays **paper**. Dual-Nextcloud lock: public `cloud.projectcar.ca` stays on **Doc** until explicit **Ben GO**; McKing `/opt/mission-control` NC is **lab/hub loopback-only** (unpublished).

Do **not** restore the July skill / Desktop draft blindly — it still has Porsche hosting Nextcloud and Doc as the public `projectcar.ca` origin. Those are wrong. Do **not** restore the 2026-08-16 stamp that locked McKing as offline `lil-cachy` and Vaultwarden as Doc compose-down — that contradicts live dual-tunnel reality.

---

## Host lock

| Machine | Hardware | Role now | Role later |
|---------|----------|----------|------------|
| **Doc** (Hakosuka) | M1 Max, 64 GB | Temporary Mission Control hub (Nextcloud; local VW sibling if compose is up — **not** public `vault.`) + Shop API `:8000` (`api.projectcar.ca`) + shop-web `:3000` (`ops.` + temporary `app.`). Doc tunnel = **`cloud.` + `api.` + `app.` + `ops.` only** (shop Soft-530 / KeepAlive). **Public `cloud.projectcar.ca` stays on Doc** until explicit **Ben GO**. Heavy local models / overflow. **Not** the public brochure origin. **Not** public `vault.projectcar.ca`. | Inference / overflow after the hub moves. Shop KeepAlive backup until the Soft-530 five-row **shop** gate PASSes |
| **McKing** (`lightning`) | i9-9900K + RTX 5080, target 30–50 TB, CachyOS / Omarchy | Path **OPEN** 2026-09-11 ~10:32 (sshd / docker / `/opt/mission-control`). Hub dual-run **NC+VW healthy** on Doc+McKing. Public **`vault.projectcar.ca` LIVE** — McKing `cloudflared` → `localhost:8222` (Vaultwarden `/alive` Lead **200** prefer; `/api/config` **2026.6.0**, Chief verified). McKing `/opt/mission-control` NC is **lab/hub loopback-only** (**unpublished** — not on the McKing CF tunnel). **Not** public shop CF origin (`api.` / `ops.` / `app.` stay on Doc). Old `lil-cachy` / 2026-08-16 **offline** stamp is **superseded**. | Permanent hub, off-box backups, GPU / vLLM. Shop-host later **only after** Soft-530 five-row gate PASS — paper: [mcking-shop-host-cutover.md](mcking-shop-host-cutover.md). Public `cloud.*` leave is a **separate** Ben GO + `status.php` parity gate — **not** a Tailscale Serve stand-up |
| **Porsche** | M4 Pro, 24 GB | Travel **client** — NC Desktop + Bitwarden over Tailscale. Coordinator, not a server. | Same. **Never** the Nextcloud server |
| **Code Mater** | Android + Hermes | Discord field agent | Termux / SSH only after a Ben security review |

**Locked plan:** Doc now for public shop CF + temp NC hub → McKing later for permanent hub **and** shop origins (paper). Public **vault** ingress is **already McKing**. Public **`cloud.projectcar.ca` stays on Doc** until explicit **Ben GO**. McKing NC stays **unpublished** (loopback-only). Travel default is reach Doc (then McKing) over **Tailscale**. Do **not** move Nextcloud onto Porsche because Doc is a laptop.

Hop OPEN ≠ shop cutover GO ≠ Doc unfreeze ≠ `cloud.*` leave. Vault LIVE ≠ shop hostname leave ≠ McKing NC publish.

---

## Doc — what it hosts

Doc is the temporary Mission Control host **and** the Shop OS origin. It is **not** the public brochure origin. It is **not** the public vault origin.

### Mission Control hub

Runtime: `~/hermes-tools/mission-control` (compose project `mission-control`). Stay out of git — secrets + data live there.

| Service | Detail | Notes |
|---------|--------|-------|
| Nextcloud | **30.0.17.2** on host **`:8080`** (Files, Talk, Calendar, Deck, Forms, Photos, Passwords) | **Public `cloud.projectcar.ca` stays here** until explicit **Ben GO**. Hub dual-run **NC+VW healthy** on Doc+McKing (2026-09-11) does **not** move `cloud.*`. Older 2026-08-16 probe: [nextcloud-progress.md](nextcloud-progress.md) |
| MariaDB **11.4** + Redis **7** | NC DB / cache only | Shop Postgres is a **separate** compose (`infra/compose` — shop DB only; it does not start the API) |
| Vaultwarden sibling (local) | Intended `127.0.0.1:8222` (+ local Caddy `:8443`) | Dual-run sibling if compose is up. **Not** public `vault.projectcar.ca`. Public vault is **McKing-only** (`cloudflared` → `localhost:8222`; `/api/config` **2026.6.0**). 2026-08-16 “compose down” is **superseded**. Do **not** recreate `vault.` ingress on Doc. |
| Hub LaunchAgent | `ai.mission-control.hub` | Start/backup scripts in the runtime tree |
| NC backups | `~/Desktop/Mission-Control/backups/nextcloud/` | Local on Doc today; McKing off-box is later |

Shop members **never** get Nextcloud accounts. n8n is banned. Matrix / Synapse is deferred — Talk is enough.

The **Mission Control cockpit** (`apps/mission-control/`) still needs **Ben GO**. Do not start it from this spec. Owner + Member booking already live on Doc does **not** unlock the cockpit.

### Shop OS on Doc

| Process | Stay-up | Public hostname | Origin |
|---------|---------|-----------------|--------|
| Shop API (uvicorn FastAPI) | LaunchAgent **`com.projectcar.shop-api`** → `~/hermes-tools/mission-control/shop-api/run-shop-api.sh` → **`:8000`** | `api.projectcar.ca` | Host **cloudflared** on Doc. **Lead owns** `:8000`. |
| Shop UI (Next.js) | LaunchAgent **`com.projectcar.shop-web`** → `~/hermes-tools/mission-control/shop-web/run-shop-web.sh` → **`next start`** **`:3000`** | **`ops.projectcar.ca` LIVE** (staff-on-shift, not Owner-only) + temporary **`app.projectcar.ca`** alias | Same cloudflared. Tunnel origin **`http://127.0.0.1:3000`** (not bare `localhost`). |

KeepAlive on shop-web **must** be **`next start`**, not `next dev`. `next dev` flaps (EADDRINUSE / KeepAlive loops). Learn that from [shop-web-stay-up.md](shop-web-stay-up.md), not by repeating the outage.

`app.` stays until Ben cuts that DNS. Do not remove the alias from this file.

Doc KeepAlive = `com.projectcar.cloudflared` + shop-api + shop-web. **Vault is OUT** of this set.

Private Mission Control stays **off** these public shop hosts.

### What Doc does **not** host

- **Public `projectcar.ca` / www.** Live origin is the Cloudflare Worker (below). Not a Doc tunnel. Not `:8088`.
- **Public `vault.projectcar.ca`.** McKing-only LIVE. Doc lid-restore / LaunchAgent KeepAlive must **not** recreate `vault.` ingress on Doc.
- **Production brochure compose.** Optional `apps/website/` nginx (or leftover `~/hermes-tools/project-car-website`) on **`:8088`** is **local preview only**.
- **McKing’s later shop-host job.** Public `api.` / `ops.` / `app.` stay on Doc until the Soft-530 five-row **shop** gate PASSes. Hop OPEN / hub NC+VW dual-run / vault LIVE do **not** pass that gate.

---

## McKing — what it hosts

McKing (`lightning`) is on the path. It is **not** the public shop CF origin.

| Surface | Reality now | Notes |
|---------|-------------|-------|
| **Path** | **OPEN** 2026-09-11 ~10:32 America/Edmonton | sshd / docker / `/opt/mission-control`. Hop OPEN ≠ shop cutover GO ≠ Doc unfreeze. |
| **Hub dual-run** | **NC+VW healthy** on Doc+McKing | Local hub, not a shop CF leave. **Not** a `cloud.*` leave. |
| **Public vault** | **`vault.projectcar.ca` LIVE** | McKing `cloudflared` → `localhost:8222`. `/alive` Lead **200** (prefer); `/api/config` **2026.6.0** (Chief verified). |
| **Hub NC (McKing)** | **lab/hub loopback-only — unpublished** | `/opt/mission-control` NC. **Not** on the McKing CF tunnel (that tunnel stays **`vault.` only**). Paper path: Tailscale Serve HTTPS mirroring VW Serve at `lightning.tailbe8f55.ts.net` + `NEXTCLOUD_TRUSTED_DOMAINS` MagicDNS. **Not** a Cloudflare cutover of `cloud.*`. |
| **Shop CF** | **Not** McKing | `api.` / `ops.` / `app.` stay Doc KeepAlive. Paper: [mcking-shop-host-cutover.md](mcking-shop-host-cutover.md). |
| **Tailnet Frigate + Jellyfin** | Lab on McKing Tailnet (Frigate **0.17.2**) | **Not** Shop OS `/cameras` live. Does **not** flip `pc.cameras`. Later cameras placeholder stays **Later**. No camera wiring from this stand-up. |

Do **not** invent McKing as offline `lil-cachy`. Do **not** invent public shop hostnames on McKing. Do **not** treat Tailnet Frigate / Jellyfin as Shop OS cameras. Do **not** publish McKing NC on `cloud.*` / Cloudflare.

---

## Brochure — not on Doc

| Piece | Reality |
|-------|---------|
| Git SSOT | `apps/website/html` on `main` |
| **Live origin** | Cloudflare Worker **`projectcar-brochure`** Direct Upload |
| Public hosts | https://projectcar.ca and https://www.projectcar.ca |
| Re-deploy | [brochure-worker-deploy.md](brochure-worker-deploy.md) — Zone uploads after Garage merges HTML |
| Optional local | `:8088` preview only — **not** production |
| Classic Pages git | **Plan only** — [brochure-pages-cutover.md](brochure-pages-cutover.md). Blocked on Cloudflare ↔ GitHub auth. **Outranked** by STATUS Next #1 (Member host). **Do not start.** |
| Apex sidecar | **Deferred.** Do not revive. |

Waitlist on Membership / Contact is a browser `POST` to `https://api.projectcar.ca/waitlist`. The Worker serves static HTML. If Doc is asleep, the **brochure stays up**; the waitlist form fails honestly until the API is back.

Older “Doc hosts projectcar.ca” / “Cloudflare Tunnel → `:8088`” lines (July drafts, stale nextcloud-progress public-site rows) are **superseded**. This file + STATUS + [doc-software-baseline.md](doc-software-baseline.md) win.

---

## Mesh and tunnels

**Dual-tunnel ownership (separate living-ops row — not the shop CF cutover).** Canonical lock: [STATUS.md](STATUS.md) Live / Locks.

| Tunnel | Hostnames | Origin / role |
|--------|-----------|----------------|
| **Doc tunnel** | **`cloud.` + `api.` + `app.` + `ops.` only** | Shop Soft-530 / KeepAlive (plus `cloud.`). Public **`cloud.projectcar.ca` stays on Doc** until explicit **Ben GO**. Public shop names stay on Doc until the Soft-530 five-row **shop** gate PASSes. That gate is **Doc shop hosts only** — **vault EXCLUDED**. |
| **McKing-only tunnel** | **`vault.projectcar.ca` — LIVE verified** (+ **unpublished** NC, not a tunnel hostname) | McKing `cloudflared` → **`localhost:8222`**. `/alive` Lead **200** (prefer); `/api/config` **2026.6.0** (Chief verified). Not the Doc mission-control token. Not shop `api.` / `ops.` / `app.`. McKing NC is **not** on this tunnel. |
| **Tailscale** | Private reach to the hub | Doc last recorded as `docs-macbook-pro` `100.97.10.72` ([doc-software-baseline.md](doc-software-baseline.md), [nextcloud-progress.md](nextcloud-progress.md)). Porsche / Ben join as clients. **Headscale is not used.** McKing path is **OPEN** (`lightning`). Paper for McKing NC: **Tailscale Serve HTTPS** mirroring VW Serve at `lightning.tailbe8f55.ts.net` + `NEXTCLOUD_TRUSTED_DOMAINS` MagicDNS — **not** a `cloud.*` CF cutover. |
| **Worker** | Apex / www brochure | **Not** either tunnel. |

Do **not** expose Nextcloud on the naked marketing domain without Access. Prefer Tailscale for NC. Public VW is **`vault.projectcar.ca` on McKing** — not a Doc tunnel hostname. Do **not** point the `cloud.*` tunnel or CNAME at McKing until a dual-run acceptance gate PASSes (McKing `status.php` parity vs Doc `status.php`) **and** explicit **Ben GO**.

### Dual-Nextcloud paper path (not a `cloud.*` CF cutover)

**Lock.** Public `cloud.projectcar.ca` stays on **Doc** until explicit **Ben GO**. McKing `/opt/mission-control` NC stays **lab/hub loopback-only** (unpublished). Dual-tunnel matrix **unchanged**: Doc = `cloud.` / `api.` / `app.` / `ops.`; McKing = `vault.` (+ unpublished NC).

**Paper path** (later execute — **not** this fold): Tailscale Serve HTTPS for McKing NC, mirroring VW Serve at `lightning.tailbe8f55.ts.net`, plus `NEXTCLOUD_TRUSTED_DOMAINS` MagicDNS hostnames. This is **not** a Cloudflare cutover of `cloud.*`. Checklist: [mcking-shop-host-cutover.md](mcking-shop-host-cutover.md) Dual-Nextcloud ownership.

| Gate | Pass | Fail |
|------|------|------|
| **Doc owns public `cloud.`** | `cloud.projectcar.ca` still Doc tunnel until **Ben GO** | Do not retarget tunnel / CNAME |
| **McKing NC unpublished** | Loopback / Tailscale Serve only — **not** on McKing CF tunnel | Do not add NC to `vault.` tunnel or mint `cloud.` on McKing |
| **`status.php` parity (before any later `cloud.*` leave)** | McKing `status.php` matches Doc `status.php` (installed, not maintenance, version) | Hub “NC+VW healthy” / hop OPEN / vault LIVE / Serve stand-up alone are **not** PASS |

#82 gate unchanged. Soft-530 companions **HOLD**. Vault LIVE unchanged.

---

## Stay-up and lid-close

Doc is a MacBook. Lid close or host sleep stops or stalls origin processes and can drop the **Doc** tunnel. Amphetamine + plugged-in no-sleep + LaunchAgent KeepAlive are **mitigation, not a guarantee** ([doc-software-baseline.md](doc-software-baseline.md)).

**Public symptom on Doc shop hosts** (`cloud.` / `api.` / `ops.` / `app.`): Cloudflare **502** or **530 / error 1033**. Soft morning 530s are expected lid-close — stay quiet and restore when Doc is reachable.

**Brochure / www do not go down** when Doc sleeps.

**Vault does not go down** when Doc sleeps. `vault.projectcar.ca` is McKing-only. Soft-530 / `api.` `/health` can stay **green while vault dies**.

| Need | Doc |
|------|-----|
| Ordered Lead wake (cloudflared → shop-api → shop-web `next start` → smoke) | [doc-lid-restore.md](doc-lid-restore.md) — **vault is OUT**. Must **not** recreate `vault.` ingress on Doc |
| API KeepAlive / health / ownership | [api-stay-up.md](api-stay-up.md) |
| shop-web KeepAlive / rebuild / `BUILD_ID` | [shop-web-stay-up.md](shop-web-stay-up.md) |
| Soft-530 five-row **shop** gate (before any public shop CF hostname leaves Doc) | [mcking-shop-host-cutover.md](mcking-shop-host-cutover.md) — **`cloud.` / `api.` / `app.` / `ops.` only; vault EXCLUDED** |
| Lookout Soft-530 watch (`api.` `/health`) | STATUS Live — **resumed** (`enabled:true`). Shop hosts only |
| Lookout vault flip watch (`/alive` every **5m**) | STATUS Live — **LIVE/armed** (`enabled:true`, Lookout confirmed). Fallback `/api/config` if `/alive` 404s. Flip-only alerts: **Chief + Lead only** on **200↔non-200**; **never Ben**; never mutate. **Vault watch ≠ Soft-530 / Doc lid-restore** |

Do not treat a morning 1033 as a product break, an edge flip, a shop CF cutover GO, or a reason to start Pages git / Member GO.

---

## Software on Doc (pointer)

Apps and macOS sleep settings live in [doc-software-baseline.md](doc-software-baseline.md). Short lock: Amphetamine session **started**; Docker Desktop for the hub; Ollama for heavy models; Hermes gateway as a service; Homebrew / `gh` / `jq`; **do not** reuse Porsche’s Discord token on Doc.

Bring-up order (Doc is already past this) is in that baseline. Do **not** treat `project-car-website` / `:8088` as a production step.

---

## Do not start from this spec (anti-goals)

| Item | Why |
|------|-----|
| **Mission Control cockpit** | Needs **Ben GO**. Booking-live hold is already satisfied. |
| **Classic Pages git** | Plan only; blocked on CF ↔ GitHub auth; outranked by Member host. Direct Upload stays live. |
| **Member host / Zone path-split** | Plan only — [member-host-cutover.md](member-host-cutover.md), [member-zone-edge.md](member-zone-edge.md). **Ben GO.** No Garage / Zone / Hatch from here. |
| **Shop CF hostname leave (McKing shop-host cutover)** | **Paper only.** Hop OPEN ≠ shop cutover GO ≠ Doc unfreeze. Soft-530 five-row gate = **Doc shop hosts only** (`cloud.` / `api.` / `app.` / `ops.`) — **vault EXCLUDED**. Vault LIVE / hub NC+VW dual-run / hop OPEN do **not** pass that gate. [mcking-shop-host-cutover.md](mcking-shop-host-cutover.md). |
| **Point `cloud.*` tunnel / CNAME at McKing** | Public `cloud.projectcar.ca` stays on **Doc** until explicit **Ben GO**. McKing `/opt/mission-control` NC stays **unpublished**. Do **not** retarget `cloud.*` until a dual-run acceptance gate PASSes: McKing `status.php` parity vs Doc `status.php`. Hub dual-run healthy / hop OPEN / vault LIVE / Tailscale Serve stand-up do **not** pass that gate. Paper path is Tailscale Serve + MagicDNS trusted domains — **not** a Cloudflare cutover of `cloud.*`. |
| **Publish McKing NC on Cloudflare** | McKing CF tunnel stays **`vault.` only**. Unpublished NC ≠ public `cloud.*`. |
| **Recreate `vault.` ingress on Doc** | Vault is **OUT** of [doc-lid-restore.md](doc-lid-restore.md) and Doc LaunchAgent KeepAlive. Public `vault.` stays McKing-only. Never move the Doc mission-control token for `vault.`. |
| **Treat vault flip watch as Soft-530** | Lookout vault `/alive` watch is **LIVE/armed** and **separate**. Soft-530 / `api.` `/health` can stay green while vault dies. |
| **Cut the `app.` alias** | `ops.` is already LIVE. Ben cuts DNS. |
| **n8n, Matrix, Apex sidecar** | Banned / deferred. |
| **Wire Shop OS `/cameras` from McKing Frigate / Jellyfin** | Tailnet Frigate **0.17.2** + Jellyfin lab ≠ Shop OS `/cameras` live. Does **not** flip `pc.cameras`. Later Frigate / cameras placeholder stays **Later**. No camera wiring from this stand-up. |

---

## Related

| Doc | Why |
|-----|-----|
| [STATUS.md](STATUS.md) | What’s live / next / locked on the product. Dual-tunnel + vault LIVE + vault flip watch **LIVE/armed**. Dual-Nextcloud: public `cloud.` on Doc until Ben GO; McKing NC unpublished |
| [mcking-shop-host-cutover.md](mcking-shop-host-cutover.md) | Shop CF cutover **paper**. Soft-530 five-row = shop hosts only. Dual-Nextcloud paper: Tailscale Serve + MagicDNS trusted domains — **not** a `cloud.*` CF cutover |
| [doc-software-baseline.md](doc-software-baseline.md) | Doc apps, LaunchAgents, sleep |
| [nextcloud-progress.md](nextcloud-progress.md) | Older hub probe (no secrets). 2026-08-16 public-site / offline-McKing rows can be stale — brochure + dual-tunnel lock is this file + STATUS |
| [platform-architecture.md](platform-architecture.md) | Monorepo, stack, runtime vs git |
| [integration-plan.md](integration-plan.md) | How MC, shop OS, agents, and the lab connect |
| [mission-control-architecture.md](mission-control-architecture.md) | Ben-only cockpit (parked). Tip-fold matches this dual-tunnel + vault LIVE lock (VW not Doc compose host; shop CF paper; Soft-530 five-row = Doc shop hosts only) |
| [website-webapp-specification.md](website-webapp-specification.md) | Domain + brochure architecture |
| [brochure-worker-deploy.md](brochure-worker-deploy.md) | Standing Worker upload |
| [doc-lid-restore.md](doc-lid-restore.md) · [api-stay-up.md](api-stay-up.md) · [shop-web-stay-up.md](shop-web-stay-up.md) | Lid-close 530 / 1033 — **vault OUT** of lid-restore / Doc KeepAlive |
| [agent-profiles-specification.md](agent-profiles-specification.md) | Hardware + jobs (coordinator ≠ hub host) |
| [deployment-guide.md](deployment-guide.md) | Index of stay-up / deploy runbooks |

**Maintained in** `Docs/` on `Coombzy/Project-Car`.
