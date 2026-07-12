# Porsche host: battery policy + Discord/gateway downtime notes

**Updated:** 2026-07-11

## Battery (always-plugged agent host)

### Policy (Ben)

| Item | Value |
|------|--------|
| Default hold | **60%** (AlDente Charge Limit) |
| Context | Plugged in all day at camp/work; rarely unplugged |
| Daily drain→full charge cycles | **No** (adds cycle wear) |
| Full charge | Only when mobility is needed (top-up) |
| Tool | AlDente Free is enough for hold + manual Discharge |

Chemistry: mid SoC (50–80%) is best for longevity while AC-powered. Prefer **hold** over yo-yo schedules. Ben accepted 60% after research (50% also fine for pure desk use; 80% is Apple’s native floor).

### Tooling facts

- Apple native Charge Limit (macOS Tahoe 26.4+, Apple silicon): **80–100% only** — cannot do 50/60.
  - https://support.apple.com/en-us/102338
- AlDente: `brew install --cask aldente` → `/Applications/AlDente.app`
- Bundle ID: `com.apphousekitchen.aldente-pro` (even free)
- Privileged helper required; only appears after **user admin password** on first run. App process alone does not enforce limits.
- Free: Charge Limiter + manual **Discharge**. Automatic Discharge / Schedule / reliable Shortcuts Set Charge Limit often need **Pro**.
- AlDente FAQ: leave system Charge Limit at 100%; avoid fighting Optimized Battery Charging.

### Agent workflow

1. `brew install --cask aldente` if missing.
2. Launch AlDente (process alone ≠ limits active).
3. Hand off helper install + slider **60%** + Launch at Login + **Discharge** (if SoC above target) to Ben — never type admin password.
4. Ask for a **neutral cue** when finished (“AlDente’s ready” / “battery’s set”) — **not** “helper done” (Ben: he’s not the helper).
5. Verify: `pgrep -lf AlDente`, helper under `/Library/PrivilegedHelperTools`, `pmset -g batt`.

### Session note 2026-07-11

AlDente 1.38 installed via Homebrew. Helper was **not** installed yet; battery was ~100% on AC (~99% health, ~97 cycles). Ben will approve helper after work at camp.

## Discord / gateway “are you there?” triage

1. `hermes status` + gateway PID / launchd KeepAlive
2. `~/.hermes/logs/gateway.log` and `update.log`
3. **`hermes update` intentionally SIGTERMs and restarts gateway** — brief Discord disconnect is expected
4. Paused security-audit crons are not the default outage cause
5. After restart, **stale Discord thread sessions may be pruned** — old threads can feel dead while the bot is online; try home channel / new thread
6. Hotel/guest Wi‑Fi DNS failures (`discord.com` nodename) also mimic gateway death

Logs that confirmed 2026-07-11: update stopped gateway ~04:38 MDT; Discord reconnected as Porsche#2334 within seconds.

Fleet channel map: `references/discord-fleet-channels.md`.
