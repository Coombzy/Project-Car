# Doc Hakosuka (M1 Max) — software baseline

**Updated:** 2026-09-21  
**Role:** Heavy local models / deep analysis. **Temporary Mission Control host** until McKing is home. Also hosts Shop API (`:8000`) + shop-web (`:3000`). **Not** the live brochure origin (Worker `projectcar-brochure` Direct Upload — `brochure-worker-deploy.md`). Not the travel edge host (that is Porsche). Camp target (after **Ben GO**): Doc also hosts public VW — [camp-vault-on-doc.md](camp-vault-on-doc.md).  
**Canonical:** `Coombzy/Project-Car` → `Docs/doc-software-baseline.md`

This file used to say “don’t dump the MC stack onto Doc.” That is **obsolete**. Locked host plan: Doc now → McKing later.

## Must install / verify

| Item | Why | Status |
|------|-----|--------|
| **Amphetamine** | Prevent sleep killing Hermes / shop API / shop-web / Docker hub / cloudflared. **CDM / lid-close:** session **started** is mitigation, not a guarantee. At **camp** (after vault-on-Doc GO) lid-close can 1033 **both** Soft-530 shop **and** vault. At **home-off**, Amphetamine off + Docs Mac off → Soft-530 **OPEN** is **EXPECTED** ([home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md)). | Session must stay **started** when Doc is supposed to be on |
| **Hermes gateway as service** | Survive reboot | Done (fleet Discord working) |
| **`DISCORD_ALLOW_BOTS=mentions`** + inline-mention gate | Fleet bot-to-bot in `#tire-shop` | Done |
| **Ollama** | Local heavy models | Done — `qwen3.6:35b`, `gemma4:26b` (2026-08-16) |
| **Homebrew + git + `gh` + `jq`** | Agent / ops basics | Done (`gh` as Coombzy) |
| **Docker Desktop** | Required while Doc hosts Nextcloud | Running — `mission-control` (3). Optional `project-car-website` compose is **local `:8088` preview only**, not production brochure |
| **Tailscale** | Remote reach from Porsche / Ben | Up — `docs-macbook-pro` `100.97.10.72` |
| **LaunchAgent `com.projectcar.shop-api`** | Shop API stay-up (KeepAlive) → uvicorn `:8000` | Live — wrapper `~/hermes-tools/mission-control/shop-api/run-shop-api.sh`. Lead owns this. See `api-stay-up.md` |
| **LaunchAgent `com.projectcar.shop-web`** | Ops / app UI stay-up (KeepAlive) → **`next start`** `:3000` | Live — wrapper `~/hermes-tools/mission-control/shop-web/run-shop-web.sh`. **Not** `next dev`. Lead owns this. See `shop-web-stay-up.md` |
| **Host cloudflared** | Public tunnels for `api.` + **LIVE `ops.`** + temporary `app.` | Live on Doc. Zone owns Cloudflare hostname / DNS rules |

## Strongly recommended

| Item | Why |
|------|-----|
| **coconutBattery** | Battery health / cycles |
| **AlDente** | Charge limit if this Mac stays plugged |
| **Cursor** or Grok Build | Coding IDE — either is enough |
| **Stats** (free) or **iStat Menus** | RAM / thermal under large models |

## Optional / elsewhere

| Item | Notes |
|------|--------|
| OrbStack / Colima | Not required — Docker Desktop is what the hub uses on Doc today |
| Matrix / Synapse | Deferred. Talk is enough |
| Headscale | **Not used.** Mesh is Tailscale |
| vLLM as daily driver | McKing / CUDA path — not default on this Mac |

## macOS settings (as important as apps)

- Prevent automatic sleep when plugged in
- Amphetamine session **actually started** for gateway / long Ollama / Docker / shop API / shop-web / cloudflared
- Hermes LaunchAgent so gateway survives lid/sleep policies
- Full Disk Access for Hermes if TCC blocks tools
- Separate Discord bot token (never Porsche’s)

## Lid-close / sleep

Doc is a MacBook (M1 Max). Lid close or host sleep stops or stalls origin processes and can drop the tunnel.

**Public symptom:** Cloudflare **502** or **530 / error 1033** (tunnel origin unreachable) on `api.projectcar.ca` / `ops.` / `app.`. Brochure waitlist `POST /waitlist` fails in the browser. Treat **1033** alongside **502** — both mean the edge cannot reach Doc.

The public brochure (Worker `projectcar-brochure`) does **not** go down when Doc sleeps. Waitlist still needs the API. See `api-stay-up.md`.

Amphetamine + plugged-in no-sleep plus LaunchAgent KeepAlive are mitigation, not a guarantee. Amphetamine **CDM** (session actually started) is the lid-close mitigation — installed-but-not-started still allows sleep.

**Home vs camp:** home-off Docs Mac **off** → Soft-530 **OPEN 530/1033** is **EXPECTED** (do **not** treat as failed CDM). Camp Doc **plugged + CDM** hosts Nextcloud; after [camp-vault-on-doc.md](camp-vault-on-doc.md) **Ben GO**, lid-close / CDM miss is a **coupled** Soft-530 + vault OPEN. Home Soft-530 **CLEAR** with lid **open** never scores the camp CDM lid-close soak. Matrix: [home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md).

If the lid is closed while Doc is supposed to be on, public API / ops / app are down until Doc is awake. Ordered wake after lid-close: `doc-lid-restore.md`. Do **not** queue that restore from intentional home-off ABSENT.

## Brochure is not Doc `:8088`

Production https://projectcar.ca / www is Cloudflare Worker **`projectcar-brochure`** Direct Upload of `apps/website/html` from `main`. Not the Doc `:8088` tunnel. Not `~/hermes-tools/project-car-website`. Optional local nginx in `apps/website/` still maps to `:8088` for preview only. Re-deploy: `brochure-worker-deploy.md`.

## Bring-up order (Doc already past this)

1. Portal + invite + intents — see Discord fleet notes in the `project-car` skill  
2. Hermes + home `#doc-garage`  
3. Amphetamine + power settings  
4. Local model stack (Ollama)  
5. Docker + `~/hermes-tools/mission-control`  
6. LaunchAgents `com.projectcar.shop-api` (uvicorn `:8000`) + `com.projectcar.shop-web` (`next start` `:3000`) + host cloudflared  
7. Tailscale + monitoring  
8. Smoke in `#doc-garage` then `#tire-shop`

Do not treat `project-car-website` / `:8088` as a production bring-up step.

## Pitfalls

- Machine “asleep” while Hermes is installed ≠ fleet chat working
- Lid-close / sleep → public **502** or **530 / error 1033** on tunneled hosts
- Grok Build alone is not the full baseline
- Reusing Porsche’s Discord token on Doc causes token lock / double replies
- Amphetamine installed but session not started still allows sleep (CDM is the started session, not the app icon)
- Home-off Soft-530 **OPEN** is **EXPECTED** — not a failed Amphetamine CDM incident
- Camp lid-close after vault-on-Doc GO 1033s shop **and** vault (coupled) — do not wake McKing / `lightning`
- Shop-web KeepAlive must be **`next start`**, not `next dev`
- **Do not** move Nextcloud onto Porsche “because Doc is a laptop”
- **Do not** follow retired `doc-nextcloud-headscale-setup-guide.md` (Headscale + Postgres)
- **Do not** treat Doc `:8088` as live projectcar.ca

Related: `home-lab-specification.md`, `home-vs-camp-doc-posture.md`, `camp-vault-on-doc.md`, `nextcloud-progress.md`, `agent-profiles-specification.md`, `mission-control-architecture.md`, `doc-lid-restore.md`, `api-stay-up.md`, `shop-web-stay-up.md`, `brochure-worker-deploy.md`
