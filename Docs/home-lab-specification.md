# Home Lab Specification

**Last Updated:** 2026-09-07  
**Status:** Living spec  
**Canonical:** `Coombzy/Project-Car` → `Docs/home-lab-specification.md`

Host lock for the lab: who runs what **now**, who takes it **later**, and what is **not** on these machines. Product live/next/later stays in [STATUS.md](STATUS.md). This file is the machine map.

Do **not** restore the July skill / Desktop draft blindly — it still has Porsche hosting Nextcloud and Doc as the public `projectcar.ca` origin. Those are wrong.

---

## Host lock

| Machine | Hardware | Role now | Role later |
|---------|----------|----------|------------|
| **Doc** (Hakosuka) | M1 Max, 64 GB | Temporary Mission Control hub (Nextcloud, Vaultwarden sibling) + Shop API `:8000` (`api.projectcar.ca`) + shop-web `:3000` (`ops.` + temporary `app.`). Heavy local models / overflow. **Not** the public brochure origin. | Inference / overflow after the hub moves |
| **McKing** (`lil-cachy`) | i9-9900K + RTX 5080, target 30–50 TB, CachyOS | **Not** hosting the hub. Last tailnet check in [nextcloud-progress.md](nextcloud-progress.md) (2026-08-16): **offline**. Do not start the migrate. | Permanent hub, off-box backups, GPU / vLLM |
| **Porsche** | M4 Pro, 24 GB | Travel **client** — NC Desktop + Bitwarden over Tailscale. Coordinator, not a server. | Same. **Never** the Nextcloud server |
| **Code Mater** | Android + Hermes | Discord field agent | Termux / SSH only after a Ben security review |

**Locked plan:** Doc now → McKing later. Travel default is reach Doc (then McKing) over **Tailscale**. Do **not** move Nextcloud onto Porsche because Doc is a laptop.

---

## Doc — what it hosts

Doc is the temporary Mission Control host **and** the Shop OS origin. It is **not** the public brochure origin.

### Mission Control hub

Runtime: `~/hermes-tools/mission-control` (compose project `mission-control`). Stay out of git — secrets + data live there.

| Service | Detail | Notes |
|---------|--------|--------|
| Nextcloud | **30.0.17.2** on host **`:8080`** (Files, Talk, Calendar, Deck, Forms, Photos, Passwords) | Last live re-check 2026-08-16 — [nextcloud-progress.md](nextcloud-progress.md) |
| MariaDB **11.4** + Redis **7** | NC DB / cache only | Shop Postgres is a **separate** compose (`infra/compose` — shop DB only; it does not start the API) |
| Vaultwarden sibling | Intended `127.0.0.1:8222` (+ local Caddy `:8443`) | Last check 2026-08-16: **compose down**. Do not invent it as live. |
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

Private Mission Control stays **off** these public shop hosts.

### What Doc does **not** host

- **Public `projectcar.ca` / www.** Live origin is the Cloudflare Worker (below). Not a Doc tunnel. Not `:8088`.
- **Production brochure compose.** Optional `apps/website/` nginx (or leftover `~/hermes-tools/project-car-website`) on **`:8088`** is **local preview only**.
- **McKing’s later job.** Permanent hub / storage / GPU wait until `lil-cachy` is on the tailnet.

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

| Layer | Use |
|-------|-----|
| **Tailscale** | Private reach to the hub. Doc last recorded as `docs-macbook-pro` `100.97.10.72` ([doc-software-baseline.md](doc-software-baseline.md), [nextcloud-progress.md](nextcloud-progress.md)). Porsche / Ben join as clients. **Headscale is not used.** |
| **Host cloudflared** (on Doc) | Public tunnels for **`api.`** + **LIVE `ops.`** + temporary **`app.`** only. Zone owns hostname / DNS rules. Lead confirms the process is up after wake. |
| **Worker** | Apex / www brochure — **not** this tunnel. |

Do **not** expose Nextcloud or Vaultwarden on the naked marketing domain without Access. Prefer Tailscale for NC. VW, when up, binds `127.0.0.1:8222` only.

---

## Stay-up and lid-close

Doc is a MacBook. Lid close or host sleep stops or stalls origin processes and can drop the tunnel. Amphetamine + plugged-in no-sleep + LaunchAgent KeepAlive are **mitigation, not a guarantee** ([doc-software-baseline.md](doc-software-baseline.md)).

**Public symptom on tunneled hosts** (`api.` / `ops.` / `app.`): Cloudflare **502** or **530 / error 1033**. Soft morning 530s are expected lid-close — stay quiet and restore when Doc is reachable.

**Brochure / www do not go down** when Doc sleeps.

| Need | Doc |
|------|-----|
| Ordered Lead wake (cloudflared → shop-api → shop-web `next start` → smoke) | [doc-lid-restore.md](doc-lid-restore.md) |
| API KeepAlive / health / ownership | [api-stay-up.md](api-stay-up.md) |
| shop-web KeepAlive / rebuild / `BUILD_ID` | [shop-web-stay-up.md](shop-web-stay-up.md) |

Do not treat a morning 1033 as a product break, an edge flip, or a reason to start Pages git / Member GO.

---

## Software on Doc (pointer)

Apps and macOS sleep settings live in [doc-software-baseline.md](doc-software-baseline.md). Short lock: Amphetamine session **started**; Docker Desktop for the hub; Ollama for heavy models; Hermes gateway as a service; Homebrew / `gh` / `jq`; **do not** reuse Porsche’s Discord token on Doc.

Bring-up order (Doc is already past this) is in that baseline. Do **not** treat `project-car-website` / `:8088` as a production step.

---

## Do not start from this spec

| Item | Why |
|------|-----|
| **Mission Control cockpit** | Needs **Ben GO**. Booking-live hold is already satisfied. |
| **Classic Pages git** | Plan only; blocked on CF ↔ GitHub auth; outranked by Member host. Direct Upload stays live. |
| **Member host / Zone path-split** | Plan only — [member-host-cutover.md](member-host-cutover.md), [member-zone-edge.md](member-zone-edge.md). **Ben GO.** No Garage / Zone / Hatch from here. |
| **Doc → McKing migrate** | Wait until `lil-cachy` is on the tailnet. |
| **Cut the `app.` alias** | `ops.` is already LIVE. Ben cuts DNS. |
| **n8n, Matrix, Apex sidecar** | Banned / deferred. |

---

## Related

| Doc | Why |
|-----|-----|
| [STATUS.md](STATUS.md) | What’s live / next / locked on the product |
| [doc-software-baseline.md](doc-software-baseline.md) | Doc apps, LaunchAgents, sleep |
| [nextcloud-progress.md](nextcloud-progress.md) | Last live hub check (no secrets). Public-site rows there can be stale — brochure lock is this file + STATUS |
| [platform-architecture.md](platform-architecture.md) | Monorepo, stack, runtime vs git |
| [integration-plan.md](integration-plan.md) | How MC, shop OS, agents, and the lab connect |
| [mission-control-architecture.md](mission-control-architecture.md) | Ben-only cockpit (parked) |
| [website-webapp-specification.md](website-webapp-specification.md) | Domain + brochure architecture |
| [brochure-worker-deploy.md](brochure-worker-deploy.md) | Standing Worker upload |
| [doc-lid-restore.md](doc-lid-restore.md) · [api-stay-up.md](api-stay-up.md) · [shop-web-stay-up.md](shop-web-stay-up.md) | Lid-close 530 / 1033 |
| [agent-profiles-specification.md](agent-profiles-specification.md) | Hardware + jobs (coordinator ≠ hub host) |
| [deployment-guide.md](deployment-guide.md) | Index of stay-up / deploy runbooks |

**Maintained in** `Docs/` on `Coombzy/Project-Car`.
