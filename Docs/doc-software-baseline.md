# Doc Hakosuka (M1 Max) — software baseline

**Updated:** 2026-08-16  
**Role:** Heavy local models / deep analysis. **Also the temporary Mission Control + projectcar.ca host** until McKing is home. Not the travel edge host (that is Porsche).  
**Canonical:** `Coombzy/Project-Car` → `Docs/doc-software-baseline.md`

This file used to say “don’t dump the MC stack onto Doc.” That is **obsolete**. Locked host plan: Doc now → McKing later.

## Must install / verify

| Item | Why | Status (checked 2026-08-16) |
|------|-----|------------------------------|
| **Amphetamine** | Prevent sleep killing Hermes gateway / long model jobs / Docker hub | **Running** (process present) |
| **Hermes gateway as service** | Survive reboot | Done (fleet Discord working) |
| **`DISCORD_ALLOW_BOTS=mentions`** + inline-mention gate | Fleet bot-to-bot in `#tire-shop` | Done |
| **Ollama** | Local heavy models | Done — `qwen3.6:35b`, `gemma4:26b` |
| **Homebrew + git + `gh` + `jq`** | Agent / ops basics | Done (`gh` as Coombzy) |
| **Docker Desktop** | Required while Doc hosts NC + site | Running — `mission-control` (3) + `project-car-website` (2) |
| **Tailscale** | Remote reach from Porsche / Ben | Up — `docs-macbook-pro` `100.97.10.72` |

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
- Amphetamine session **actually started** for gateway / long Ollama / Docker
- Hermes LaunchAgent so gateway survives lid/sleep policies
- Full Disk Access for Hermes if TCC blocks tools
- Separate Discord bot token (never Porsche’s)

## Bring-up order (Doc already past this)

1. Portal + invite + intents — see Discord fleet notes in the `project-car` skill  
2. Hermes + home `#doc-garage`  
3. Amphetamine + power settings  
4. Local model stack (Ollama)  
5. Docker + `~/hermes-tools/mission-control` + `project-car-website`  
6. Tailscale + monitoring  
7. Smoke in `#doc-garage` then `#tire-shop`

## Pitfalls

- Machine “asleep” while Hermes is installed ≠ fleet chat working
- Grok Build alone is not the full baseline
- Reusing Porsche’s Discord token on Doc causes token lock / double replies
- Amphetamine installed but session not started still allows sleep
- **Do not** move Nextcloud onto Porsche “because Doc is a laptop”
- **Do not** follow retired `doc-nextcloud-headscale-setup-guide.md` (Headscale + Postgres)

Related: `home-lab-specification.md`, `nextcloud-progress.md`, `agent-profiles-specification.md`, `mission-control-architecture.md`
