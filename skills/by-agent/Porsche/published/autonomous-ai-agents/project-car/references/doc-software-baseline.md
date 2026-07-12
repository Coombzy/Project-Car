# Doc Hakosuka (M1 Max) — software baseline

**Updated:** 2026-07-12  
**Role:** Heavy local models / deep analysis. Not the travel edge host (that is Porsche).

## Must install / verify (when Doc is awake)

| Item | Why | Status |
|------|-----|--------|
| **Amphetamine** | Prevent sleep killing Hermes gateway / long model jobs | **Installed + running** (Ben confirmed 2026-07-12) — keep active for long jobs |
| **Hermes gateway as service** | `hermes gateway install && hermes gateway start` — survive reboot | Done (fleet Discord working) |
| **`DISCORD_ALLOW_BOTS=mentions`** | Fleet bot-to-bot in `#tire-shop` when @mentioned (default `none` ignores other bots) | Done |
| **Ollama and/or MLX** | Local heavy models (Doc’s primary job) | Done (`qwen3.6:35b`, `gemma4:26b`) |
| **Homebrew + git + `gh` + `jq`** | Agent/ops basics | Done (`gh` as Coombzy) |
| **Tailscale** (or current mesh) | Remote reach from Porsche / Ben | Verify still open |

## Strongly recommended

| Item | Why |
|------|-----|
| **coconutBattery** | Battery health / cycles |
| **AlDente** | Only if **MacBook** form factor (charge limit when always plugged) |
| **Cursor** if missing | Coding IDE; Doc may already have Grok build — Grok + Cursor is enough |
| **Stats** (free) or **iStat Menus** | RAM / thermal under large models |

## Optional / usually elsewhere

| Item | Notes |
|------|--------|
| OrbStack / Docker | Prefer Porsche (edge) or McKing (homelab) unless Doc will host containers |
| Full Nextcloud / Matrix stack | Travel default = Porsche; don’t dump MC stack onto Doc by default |

## macOS settings (as important as apps)

- Prevent automatic sleep when plugged in
- Amphetamine session active for gateway / long Ollama runs
- Hermes LaunchAgent/service so gateway survives lid/sleep policies
- Full Disk Access for Hermes if TCC blocks tools
- Separate Discord bot token (never Porsche’s)

## Bring-up order

1. Portal + invite + intents — see `discord-fleet-channels.md`  
2. Hermes + home `#doc-garage`  
3. Amphetamine + power settings  ✅ Amphetamine running  
4. Local model stack (Ollama/MLX)  
5. Mesh + monitoring  
6. Smoke in `#doc-garage` then `#tire-shop`

## Pitfalls

- Machine “asleep” while Hermes is installed ≠ fleet chat working  
- Grok build alone is not the full baseline  
- Reusing Porsche Discord token on Doc causes token lock / double replies  
- Amphetamine installed but session not started still allows sleep — confirm “Indefinitely” / app open during long jobs  
