---
name: macos-security-hardening
description: "Hardening macOS for high-performance local AI workloads (Ollama, Hermes, local LLMs). Doc copy emphasizes always-on lab / large local models (not travel-host default)."
version: 1.4.0
author: Doc Hakosuka (always-on lab tailoring)
license: MIT
---

# macOS Security Hardening for AI Workloads

Class-level skill for auditing and hardening macOS systems running local AI agents and large language models. Strong security without sacrificing unified memory performance, Metal acceleration, or agent tool access.

**This install is tailored for Doc first** (always-on lab on M1 Max **64GB**). Porsche travel-host and McKing rows remain so fleet advice stays accurate — do **not** make travel-host the default workflow on this machine.

## When to use
- User asks for a security audit, hardening, lockdown, or threat review of a Mac
- Setting up Hermes / Ollama / Tailscale on a new or reinstalled Mac
- Post-purchase / post-repair / used-Mac hygiene
- Before enabling Remote Login, File Sharing, or exposing local model APIs
- **Always-on lab** (Doc) — use always-on-lab appendix
- Fleet hosts (Porsche travel PA, Doc always-on lab) — use **threat-model fork** below

## Core principles
- Preserve full performance of M-series unified memory and local inference.
- Grant AI tools (Terminal, Ollama, Hermes) necessary access (Full Disk Access) while limiting blast radius.
- Prefer non-destructive, reversible changes.
- **Default for Ben-facing interactive audits:** report first; apply fixes when Ben approves (or when autonomy is on **and** change is low-risk perms-only).
- Prioritize quick wins with zero or near-zero performance cost.
- Write a dated report to `~/Desktop/macOS-Security-Audit-YYYY-MM-DD.md` (never commit serial/UUID reports to public `Coombzy/Automation`).

## Fleet threat-model forks (same skill, different emphasis)

| Host | Threat bias | Extra focus | Auto-fix when autonomy on |
|------|-------------|-------------|----------------------------|
| **Doc** (always-on lab, large local models) | Local API exposure, long-lived agent tools, residual shop tools | Ollama **127.0.0.1 only**; Hermes perms; Amphetamine/stay-awake baseline; single Tailscale; model disk privacy | Same low-risk perms + Ollama bind check; still **gate** firewall/SIP/FileVault/Remote Login on Ben |
| **Porsche** (travel PA, often hotel/guest Wi‑Fi) | Theft, hostile LAN, gateway uptime, PA blast radius | Screen lock ≤60s; FileVault; no open shares; Discord/gateway health; AlDente ~60% on AC; pre-travel `~/.hermes` backup; captive-portal DNS triage | `chmod` 700/600 on `~/.hermes` secrets/DB/logs; confirm Ollama localhost if present |
| **McKing** (when online) | CUDA/LAN services, bulk storage | No unauthenticated model/serving binds on LAN; backup receive paths | Perms + listener audit |

Do **not** run identical “hotel paranoia” as the default on always-on lab, or force Doc lab bulk model surface onto travel host.

## Doc always-on lab workflow (default on this machine)

When auditing **this** Mac (or any Doc-class lab host), run the standard checks **plus** `references/always-on-lab.md`:

1. Ollama bind = localhost only; report any non-loopback listeners for model APIs.
2. Hermes 700/600 hygiene; state.db/logs often wrongly 644.
3. Stay-awake baseline (**Amphetamine installed + running** 2026-07-12) + single Tailscale.
4. Model disk / cache privacy under FileVault.
5. Low-risk auto-fix only; high-risk still Ben-gated.
6. Report — no serials in public repos.
7. Open ops: battery app still open — Amphetamine done. See `communication/Doc/Doc-Todo.md`.

## Typical workflow
1. **Baseline platform controls** — SIP, FileVault, Gatekeeper, firewall + stealth, Remote Login, Screen Sharing, software updates, Activation Lock / authenticated root.
2. **Network exposure** — non-loopback TCP listeners, AirPlay (`*:5000`/`*:7000` ControlCenter), Continuity (`rapportd`), sharing services, DNS.
3. **Tailscale / VPN** — single install only (prefer Tailscale.app on macOS), `tailscale debug prefs` (ShieldsUp, RouteAll, RunSSH), peer list, dual Homebrew vs App stacks.
4. **AI stack surface** — Ollama bind address (must stay `127.0.0.1`), Hermes `~/.hermes` perms (secrets 600; DB/logs often wrongly 644), profiles (`secure-ai`), local providers in config.
5. **Persistence & trust residue** — LaunchAgents/Daemons, system extensions, non-Apple kexts, TCC Full Disk Access / Accessibility / Input Monitoring.
6. **Used-device / shop hygiene** — admin group members, orphan share points (`sharing -l`), PhoneCheck/MacDiag-class tools, unknown Bluetooth pairings.
7. **Lock screen & recovery** — `sysadminctl -screenLock status` (flag delays ≥60s), Time Machine / backup destinations.
8. **Report** — severity-ranked findings + do-now / this-week / optional; do not apply changes unless asked (except low-risk autonomy path).

## Do-now hardening defaults (when user approves)
```bash
# Firewall + stealth
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setstealthmode on

# Remove common over-broad firewall allows (re-add only if needed)
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --remove /usr/bin/python3
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --remove /usr/bin/ruby
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --remove /usr/sbin/smbd
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --remove /usr/sbin/sshd-keygen-wrapper

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
- **Fleet git-safe mutual audits** (`Coombzy/Automation` is public): never copy security-audit reports, serials, 2FA/recovery notes, or full `~/.hermes` dumps into `backup/*/git-safe/`. Use skill **`fleet-mutual-improvement`** (canonical) for sanitized inventories only — not dual weekly audit runbooks.
- Auth failures for the local user GUID with Remote Login Off are usually failed sudo/password prompts, not remote SSH brute force — interpret before alarming.
- **Do not default Doc to travel-host checklists** — those live on Porsche; Doc uses always-on-lab.

## AI-specific threat model (quick)
| Threat | Mitigation |
|---|---|
| Prompt injection → local shell | `secure-ai` profile; supervise tool use; hard tool-loop stops on risky sessions |
| Compromised Tailnet peer | Shields up; tight ACLs; single Tailscale install |
| Stolen laptop | FileVault + Activation Lock + short screen lock |
| Local model API abuse | Ollama localhost only; no unauthenticated remote bind |
| Agent destructive actions | Backups (Time Machine / restic); separate profiles |
| Large model weight exfil path | FileVault; no public git of model caches/secrets |

## References
- `references/always-on-lab.md` — **Doc primary** checklist (Ollama bind, Hermes perms, stay-awake, model disk)
- `references/audit-commands.md` — full diagnostic command bank for audits
- `references/multi-device-risks.md` — Continuity, iCloud, Tailscale, Bluetooth multi-device notes
- `references/ai-stack-surface.md` — Hermes / Ollama / local-provider exposure checklist
