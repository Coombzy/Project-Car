# Porsche travel-host security appendix (M4 Pro PA)

Threat bias: **theft, hostile hotel/guest Wi‑Fi, gateway uptime, PA tool blast radius** — not Doc’s always-on lab model surface.

## Before travel (same day or night before)

- [ ] FileVault on; Activation Lock expected for Apple ID
- [ ] Screen lock **immediate or ≤60s**; require password on wake
- [ ] Sharing: File Sharing, Remote Login, Remote Management, Screen Sharing **off** unless Ben explicitly needs one path
- [ ] AirPlay Receiver off (ControlCenter often listens `*:5000`/`*:7000`)
- [ ] Backup `~/.hermes` (exclude huge caches) to encrypted destination Ben already uses — do not invent new cloud sinks
- [ ] Confirm Discord gateway starts after reboot (`hermes status` / launchd or user service as configured)
- [ ] AlDente: hold **~60%** on AC at camp/work; top to 100% only for mobility days
- [ ] Note hotel Wi‑Fi DNS failures can look like “Discord down” — test DNS before long recovery

## On hostile / guest LAN

- Prefer **Tailscale** (single install: App preferred) for mesh; avoid dual Homebrew userspace + App
- Do **not** bind Ollama (if installed) to non-localhost
- Avoid enabling Remote Login “just for this hotel”
- Prefer known networks; treat captive portals as untrusted
- If gateway dies: check DNS → `hermes status` → logs → brief Ben; don’t thrash updates on flaky captive portals

## PA blast radius

- Hermes `terminal.backend: local` + full tools = high impact under prompt injection
- For untrusted pasted content / web scrapes: prefer tighter tool use, hard tool-loop stops, or `secure-ai` profile when Ben wants isolation
- Never put security-incident detail, 2FA recovery, or serials into public `Coombzy/Automation` git-safe packs
- Work around macOS TCC (`Operation not permitted` on `~/.ssh` / sometimes `~/.gitconfig`) with `gh` / narrow paths — **do not re-nag Ben** for Full Disk Access every time

## Auto-fix when autonomy on (low risk only)

```bash
chmod 700 ~/.hermes
chmod 600 ~/.hermes/state.db ~/.hermes/.env ~/.hermes/auth.json ~/.hermes/config.yaml 2>/dev/null
chmod 600 ~/.hermes/logs/*.log 2>/dev/null
# If Ollama present: confirm loopback only (report if not)
lsof -iTCP:11434 -sTCP:LISTEN -P -n 2>/dev/null || true
```

**Still gate on Ben:** firewall policy changes, SIP, FileVault off/on, Remote Login on, Lockdown Mode, broad `tccutil reset`.

## Gateway / “are you offline?” quick triage

1. Local DNS to `discord.com`
2. `hermes status` / gateway PID
3. `~/.hermes/logs/gateway.log` / `update.log`
4. Remember: `hermes update` restarts gateway by design (brief disconnect)
5. Stale Discord threads can feel dead while bot is healthy — try home channel

## Report fields (travel audit)

Include: network type (hotel/home/camp), Tailscale up?, sharing services, screen lock, FileVault, Hermes perms, listeners non-loopback, gateway health. **No serials/UUIDs in public git.**
