# Doc Hakosuka (M1 Max) — software baseline

**Updated:** 2026-07-11  
**Role:** Heavy local models / deep analysis. Not the travel edge host (that is Porsche).

## Must install / verify (when Doc is awake)

| Item | Why |
|------|-----|
| **Amphetamine** | Prevent sleep killing Hermes gateway / long model jobs |
| **Hermes gateway as service** | `hermes gateway install && hermes gateway start` — survive reboot |
| **`DISCORD_ALLOW_BOTS=mentions`** | Fleet bot-to-bot in `#tire-shop` when @mentioned (default `none` ignores other bots) |
| **Ollama and/or MLX** | Local heavy models (Doc’s primary job) |
| **Homebrew + git + `gh` + `jq`** | Agent/ops basics |
| **Tailscale** (or current mesh) | Remote reach from Porsche / Ben |

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
- Hermes LaunchAgent/service so gateway survives lid/sleep policies
- Full Disk Access for Hermes if TCC blocks tools
- Separate Discord bot token (never Porsche’s)

## Bring-up order

1. Portal + invite + intents — see `discord-fleet-channels.md`  
2. Hermes + home `#doc-garage`  
3. Amphetamine + power settings  
4. Local model stack (Ollama/MLX)  
5. Mesh + monitoring  
6. Smoke in `#doc-garage` then `#tire-shop`

## Pitfalls

- Machine “asleep” while Hermes is installed ≠ fleet chat working  
- Grok build alone is not the full baseline  
- Reusing Porsche Discord token on Doc causes token lock / double replies  
