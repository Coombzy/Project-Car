# Home Lab Specification

**Last Updated:** 2026-09-21  
**Status:** Living spec  
**Canonical:** `Coombzy/Project-Car` → `Docs/home-lab-specification.md`

Host lock for the lab: who runs what **now**, who takes it **later**, and what is **not** on these machines. Product live/next/later stays in [STATUS.md](STATUS.md). This file is the machine map. Home vs camp Doc power: [home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md). Camp vault-on-Doc (paper — **Ben GO**): [camp-vault-on-doc.md](camp-vault-on-doc.md).

Do **not** restore the July skill / Desktop draft blindly — it still has Porsche hosting Nextcloud and Doc as the public `projectcar.ca` origin. Those are wrong. Do **not** restore the 2026-08-16 stamp that locked McKing as offline `lil-cachy` — McKing identity is **`lightning`** (Omarchy). **`vault.projectcar.ca`** is the intended public Vaultwarden hostname.

---

## Host lock

| Machine | Hardware | Role now | Role later |
|---------|----------|----------|------------|
| **Doc** (Hakosuka) | M1 Max, 64 GB | Temporary Mission Control hub (Nextcloud; local VW sibling if compose is up) + Shop API `:8000` (`api.projectcar.ca`) + shop-web `:3000` (`ops.` + temporary `app.`). Heavy local models / overflow. **Not** the public brochure origin. **Camp target** (after **Ben GO** + Zone retarget): Doc hosts **NC + public VW**. | Inference / overflow after the hub moves. Camp hub while McKing sleeps. |
| **McKing** (`lightning`) | i9-9900K + RTX 5080, target 30–50 TB, **Omarchy** | Home/lab vault host — intended public **`vault.projectcar.ca`** (VW). **Not** the public shop CF origin (`api.` / `ops.` / `app.` stay on Doc). Old `lil-cachy` / 2026-08-16 **offline** stamp is **superseded**. When `lightning` is **ABSENT**, vault Soft-530 / **1033** is **expected quiet**. | Permanent hub, off-box backups, GPU / vLLM. At **camp**, McKing **may sleep**. |
| **Porsche** | M4 Pro, 24 GB | Travel **client** — NC Desktop + Bitwarden over Tailscale. Coordinator, not a server. | Same. **Never** the Nextcloud server |
| **Code Mater** | Android + Hermes | Discord field agent | Termux / SSH only after a Ben security review |

**Locked plan:** Doc now for public shop CF + temp NC hub → McKing later for permanent hub. Public **vault** intended hostname is **`vault.projectcar.ca`** (home/lab = McKing / `lightning`; **camp** after **Ben GO** = Doc + Zone retarget — [camp-vault-on-doc.md](camp-vault-on-doc.md)). Travel default is reach Doc (then McKing) over **Tailscale**. Do **not** move Nextcloud onto Porsche because Doc is a laptop.

Camp cutover ≠ auto-GO ≠ Zone execute from this spec. Soft-530 independence is **home/lab only**.

---

## Doc — what it hosts

Doc is the temporary Mission Control host **and** the Shop OS origin. It is **not** the public brochure origin.

### Mission Control hub

Runtime: `~/hermes-tools/mission-control` (compose project `mission-control`). Stay out of git — secrets + data live there.

| Service | Detail | Notes |
|---------|--------|--------|
| Nextcloud | **30.0.17.2** on host **`:8080`** (Files, Talk, Calendar, Deck, Forms, Photos, Passwords) | Last live re-check 2026-08-16 — [nextcloud-progress.md](nextcloud-progress.md) |
| MariaDB **11.4** + Redis **7** | NC DB / cache only | Shop Postgres is a **separate** compose (`infra/compose` — shop DB only; it does not start the API) |
| Vaultwarden sibling | Intended `127.0.0.1:8222` (+ local Caddy `:8443`) | Local sibling if compose is up. **Not** automatically public `vault.`. Intended public hostname is **`vault.projectcar.ca`** (home/lab McKing; camp Doc after **Ben GO** + Zone retarget). 2026-08-16 “compose down” is a stale probe, not the host lock. |
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
- **Public `vault.projectcar.ca` at home/lab.** Intended McKing / `lightning` VW hostname. Do **not** recreate `vault.` ingress on Doc without [camp-vault-on-doc.md](camp-vault-on-doc.md) **Ben GO** + Zone retarget.
- **McKing’s later job.** Permanent hub / storage / GPU. Identity is **`lightning`** (Omarchy), not offline `lil-cachy`. At camp, McKing **may sleep**.

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

Do **not** expose Nextcloud or Vaultwarden on the naked marketing domain without Access. Prefer Tailscale for NC. Intended public VW hostname is **`vault.projectcar.ca`** (home/lab McKing / `lightning`; camp Doc after **Ben GO** + Zone retarget). Local Doc VW, when up, still binds `127.0.0.1:8222` until that GO.

---

## Stay-up and lid-close

Doc is a MacBook. Lid close or host sleep stops or stalls origin processes and can drop the tunnel. Amphetamine + plugged-in no-sleep + LaunchAgent KeepAlive are **mitigation, not a guarantee** ([doc-software-baseline.md](doc-software-baseline.md)).

**Public symptom on tunneled shop hosts** (`api.` / `ops.` / `app.`): Cloudflare **502** or **530 / error 1033**. Soft morning 530s are expected lid-close when Doc is supposed to be on — stay quiet and restore when Doc is reachable. **Home-off** (Docs Mac intentionally off): Soft-530 **OPEN** is **EXPECTED** — [home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md).

**Brochure / www do not go down** when Doc sleeps.

**Home/lab vault:** when `lightning` is **ABSENT**, public `vault.projectcar.ca` Soft-530 / **1033** is **expected quiet** — do **not** wake McKing. Soft-530 shop and vault fail **independently** at home/lab.

**Camp (after Ben GO + Zone retarget):** Doc hosts NC + VW. Vault **does** go down when Doc sleeps. Soft-530 + vault couple on Doc lid / Amphetamine CDM / KeepAlive — [camp-vault-on-doc.md](camp-vault-on-doc.md). `lightning` **ABSENT** stays expected quiet (McKing may sleep).

| Need | Doc |
|------|-----|
| Ordered Lead wake (cloudflared → shop-api → shop-web `next start` → smoke) | [doc-lid-restore.md](doc-lid-restore.md) — home-off ABSENT does **not** queue this |
| Home vs camp Soft-530 matrix (home-off OPEN = **EXPECTED**) | [home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md) |
| Camp vault on Doc (paper — **Ben GO** then Zone `vault.` retarget only; rollback Zone → McKing) | [camp-vault-on-doc.md](camp-vault-on-doc.md) |
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
| **Doc → McKing migrate** | Identity is `lightning` (Omarchy), not offline `lil-cachy`. Still not an auto-migrate. |
| **Recreate `vault.` ingress on Doc without camp Ben GO** | Home/lab public vault stays McKing / `lightning` until [camp-vault-on-doc.md](camp-vault-on-doc.md) **Ben GO** + Zone retarget. Never auto-cutover. Rollback is Zone → McKing. |
| **Wake McKing because `lightning` is ABSENT** | Vault Soft-530 / **1033** while `lightning` **ABSENT** = **expected quiet**. |
| **Cut the `app.` alias** | `ops.` is already LIVE. Ben cuts DNS. |
| **n8n, Matrix, Apex sidecar** | Banned / deferred. |

---

## Related

| Doc | Why |
|-----|-----|
| [STATUS.md](STATUS.md) | What’s live / next / locked on the product |
| [home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md) | Home Soft-530 OPEN when Docs Mac off = **EXPECTED**; camp Doc plugged + CDM hosts NC |
| [camp-vault-on-doc.md](camp-vault-on-doc.md) | Camp interim: Doc hosts NC+VW; **Ben GO** then Zone `vault.` retarget only; rollback Zone → McKing |
| [doc-software-baseline.md](doc-software-baseline.md) | Doc apps, LaunchAgents, sleep, Amphetamine CDM |
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
