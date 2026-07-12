---
name: macos-security-hardening
description: "Hardening macOS for high-performance local AI workloads (Ollama, Hermes, local LLMs) while maintaining fluid multi-device operation."
version: 1.1.0
author: Doc Hakosuka
license: MIT
---

# macOS Security Hardening for AI Workloads

Class-level skill for auditing and hardening macOS systems running local AI agents and large language models. Strong security without sacrificing unified memory performance, Metal acceleration, or agent tool access.

## When to use
- User asks for a security audit, hardening, lockdown, or threat review of a Mac
- Setting up Hermes / Ollama / Tailscale on a new or reinstalled Mac
- Post-purchase / post-repair / used-Mac hygiene
- Before enabling Remote Login, File Sharing, or exposing local model APIs

## Core principles
- Preserve full performance of M-series unified memory and local inference.
- Grant AI tools (Terminal, Ollama, Hermes) necessary access (Full Disk Access) while limiting blast radius.
- Prefer non-destructive, reversible changes. **Default = audit/report first; only apply fixes when user approves.**
- Prioritize quick wins with zero or near-zero performance cost.
- Write a dated report to `~/Desktop/macOS-Security-Audit-YYYY-MM-DD.md`.

## Typical workflow
1. **Baseline platform controls** — SIP, FileVault, Gatekeeper, firewall + stealth, Remote Login, Screen Sharing, software updates, Activation Lock / authenticated root.
2. **Network exposure** — non-loopback TCP listeners, AirPlay (`*:5000`/`*:7000` ControlCenter), Continuity (`rapportd`), sharing services, DNS.
3. **Tailscale / VPN** — single install only (prefer Tailscale.app on macOS), `tailscale debug prefs` (ShieldsUp, RouteAll, RunSSH), peer list, dual Homebrew vs App stacks.
4. **AI stack surface** — Ollama bind address (must stay `127.0.0.1`), Hermes `~/.hermes` perms (secrets 600; DB/logs often wrongly 644), profiles (`secure-ai`), local providers in config.
5. **Persistence & trust residue** — LaunchAgents/Daemons, system extensions, non-Apple kexts, TCC Full Disk Access / Accessibility / Input Monitoring.
6. **Used-device / shop hygiene** — admin group members, orphan share points (`sharing -l`), PhoneCheck/MacDiag-class tools, unknown Bluetooth pairings.
7. **Lock screen & recovery** — `sysadminctl -screenLock status` (flag delays ≥60s), Time Machine / backup destinations.
8. **Report** — severity-ranked findings + do-now / this-week / optional; do not apply changes unless asked.

## Do-now hardening defaults (when user approves)
```bash
# Firewall + stealth
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setstealthmode on

# Remove common over-broad firewall allows (re-add only if needed)
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --remove /usr/bin/python3
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --remove /usr/bin/ruby
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --remove /usr/sbin/smbd
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --remove /usr/libexec/sshd-keygen-wrapper

# Hermes perms
chmod 700 ~/.hermes
chmod 600 ~/.hermes/state.db ~/.hermes/.env ~/.hermes/auth.json ~/.hermes/config.yaml 2>/dev/null
chmod 600 ~/.hermes/logs/*.log 2>/dev/null

# One Tailscale stack (Homebrew userspace is the usual duplicate)
brew services stop tailscale 2>/dev/null
# optional inbound hardening:
# tailscale set --shields-up

brew analytics off
sudo chmod 755 "/Users/Shared/SC Info" 2>/dev/null
```
GUI (user must click): Lock Screen → password immediately; Sharing all off; AirPlay Receiver off; Privacy → remove MacDiag/PhoneCheck; Bluetooth forget unknowns.

Isolated Hermes profile:
```bash
hermes profile create secure-ai
```

## High-signal checks (always run)
```bash
csrutil status
fdesetup status
spctl --status
/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
/usr/libexec/ApplicationFirewall/socketfilterfw --getstealthmode
/usr/libexec/ApplicationFirewall/socketfilterfw --listapps
systemsetup -getremotelogin 2>/dev/null || true
sysadminctl -screenLock status
lsof -iTCP -sTCP:LISTEN -P -n
sharing -l
dscl . -read /Groups/admin GroupMembership
systemextensionsctl list
kextstat 2>/dev/null | grep -v com.apple || true
tailscale status 2>/dev/null; tailscale debug prefs 2>/dev/null | head -40
ls -la ~/.hermes/.env ~/.hermes/auth.json ~/.hermes/state.db 2>/dev/null
```

## Pitfalls
- **Never revoke Full Disk Access from Terminal** while Hermes/Ollama are mid-task.
- **Do not enable Lockdown Mode** without testing AI workflows first (breaks some Continuity/web features).
- Avoid blanket `tccutil reset All` unless ready to re-grant everything.
- **Ollama must stay on 127.0.0.1** — never recommend `0.0.0.0` / LAN bind without auth reverse proxy. Do not put Ollama on Tailscale raw.
- **Dual Tailscale** (App system extension + Homebrew `tailscaled --tun=userspace-networking`) is common and bad — consolidate to App.
- **Firewall allowlist ≠ service running** — python3/ruby/smbd/sshd-wrapper may still be *allowed* incoming; remove stale allows.
- **PhoneCheck / MacDiag residue** on used or shop-serviced Macs: orphan admin membership (`phonecheck`), guest R/W share points for deleted homes, TCC grants for `com.macdiag.app` even after app deleted. Always check `sharing -l`, admin group, FDA/Accessibility/Input Monitoring.
- **Screen lock delay of 300s** is too long for AI laptops — require immediate or ≤60s.
- **Hermes `state.db` and logs** often created as 644 — chmod after audits; sessions can contain paths/prompt snippets.
- **AirPlay Receiver** shows as ControlCenter LISTEN on `*:5000` and `*:7000` — treat as LAN exposure.
- Report may include serial/UUID — mark sensitive; do not commit to public repos.
- **Fleet git-safe mutual audits** (`Coombzy/Automation` is public): never copy security-audit reports, serials, 2FA/recovery notes, or full `~/.hermes` dumps into `backup/*/git-safe/`. Use skill `fleet-mutual-audit` for sanitized inventories only.
- Auth failures for the local user GUID with Remote Login Off are usually failed sudo/password prompts, not remote SSH brute force — interpret before alarming.

## AI-specific threat model (quick)
| Threat | Mitigation |
|---|---|
| Prompt injection → local shell | `secure-ai` profile; supervise tool use; hard tool-loop stops on risky sessions |
| Compromised Tailnet peer | Shields up; tight ACLs; single Tailscale install |
| Stolen laptop | FileVault + Activation Lock + short screen lock |
| Local model API abuse | Ollama localhost only; no unauthenticated remote bind |
| Agent destructive actions | Backups (Time Machine / restic); separate profiles |

## References
- `references/audit-commands.md` — full diagnostic command bank for audits
- `references/multi-device-risks.md` — Continuity, iCloud, Tailscale, Bluetooth multi-device notes
- `references/ai-stack-surface.md` — Hermes / Ollama / local-provider exposure checklist
