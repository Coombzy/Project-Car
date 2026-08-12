# Code Mater / Android Integration Guide

**Last Updated:** 2026-07-09  
**Status:** Living draft (v1)  
**Owner:** Porsche (Scheduler/Planner)  
**Audience:** Ben (Coombsy), Porsche, Code Mater, Lightning McKing, Doc Hudson, Grok  
**Part of:** Project Car documentation hierarchy  

**Synchronized locations:**
- Skill: `~/.hermes/skills/autonomous-ai-agents/project-car/references/code-mater-android-integration-guide.md`
- Desktop: `~/Desktop/Project-Car-Docs/code-mater-android-integration-guide.md`
- GitHub: `Coombzy/Automation/Docs/code-mater-android-integration-guide.md`

Related: `agent-profiles-specification.md`, `ai-agents-constitution.md`, `integration-plan.md`, `security-playbook.md`, `home-lab-specification.md`, `mission-control-architecture.md`, `heartbeat-standards.md`.

---

## 1. Purpose

Define how **Code Mater** — the Android / phone agent — integrates with the fleet so Ben gets:

- Easiest mobile chat while welding / traveling (Android-first)  
- Constant schedule & todo updates via Discord + agents  
- Field capture (voice, photos, notes) into Mission Control  
- Security early warning after observed compromise patterns (phone hack/reset, 2FA loss)  
- Optional **remote execution on the phone** (Termux+SSH first) without turning the device into an untrusted free-for-all  

**Name:** Code Mater = “Mater” (reliable tow / rescue energy) + code/integration focus. Mobile glue for the fleet.

---

## 2. Role Definition

| Field | Spec |
|-------|------|
| **Agent name** | Code Mater |
| **Primary job** | Mobile integration, notifications, field data, security alerts, remote actions when bridge enabled |
| **Personality** | Helpful, reliable, quick-response; short messages; field-practical |
| **Supervisor** | Porsche (routes work; Ben is final authority especially on security) |
| **Does** | Alerts, lightweight checks, voice→task handoff, offline queue, bridge commands |
| **Does not** | Heavy coding, large local LLMs, GPU jobs, unconstrained host control of lab machines |

### Routing rules (from constitution)
- Mobile / real-time / field data → **Code Mater**  
- Planning / PA / coordination → **Porsche**  
- Deep analysis → **Doc**  
- Heavy code / storage / GPU → **McKing**  

---

## 3. Current Hardware

| Item | Current |
|------|---------|
| Device | **Nothing 3a Pro** (Android) |
| Hermes | Installed / running (communication path) |
| Upgrade priority | **High** (battery, thermals, on-device AI, security features) |
| Risk posture | Treat as **elevated compromise risk** until upgraded and hardened (prior Android reset / 2FA loss context) |

### Constraints (enforce in all designs)
- Battery life during long shifts  
- Thermal limits (no sustained heavy local models)  
- Unreliable northern job-site connectivity  
- Physical access risk (phone can be lost/stolen)  
- Lightweight tasks only on-device  

---

## 4. Capability Levels

Build in layers. Do not skip security basics to chase remote shell toys.

### Level 0 — Chat only (NOW)
- Hermes Agent on Android talks over **Discord**  
- Ben ↔ Code Mater ↔ Porsche coordination  
- No shell access to the phone from the lab  

**Status target:** Always keep this working even if higher levels break.

### Level 1 — Structured field capture
- Voice notes / short text → Discord or webhook → Porsche creates Mission Control tasks  
- Photo drop folder sync when online (Nextcloud Android client or staged upload)  
- Offline queue on device; flush when network returns  

### Level 2 — Security sentinel
- Local heuristics / Tasker profiles for: unusual battery drain, new admin apps, failed unlock spikes, SIM change if detectable  
- Immediate Discord alert to home channel  
- Optional “safe mode” actions (see §9)  

### Level 3 — Remote execution bridge (Termux + SSH)
- Porsche (or Ben) can run **scoped** commands in Termux over mesh/VPN SSH  
- Used for diagnostics, log pull, controlled automation — not open-ended root  

### Level 4 — Deep automation (optional)
- Tasker / MacroDroid + intents  
- ADB over Wi‑Fi (debug builds / trusted LAN only)  
- Native Hermes Android tool calling if/when client supports richer device APIs  

### Level 5 — Device upgrade + hardened baseline
- New flagship Android with better battery, security, developer options  
- Re-issue keys, full reinstall, assume clean device  

---

## 5. Communication Architecture

```
[Ben on site]
    |  Discord (primary)
    v
[Code Mater Hermes on Android]
    |
    +--> Discord Turbocharger Springs (fleet)
    |
    +--> (L1+) Webhook / Hermes / Porsche for task create
    |
    +--> (L3+) Termux sshd on mesh IP only
              ^
              |
         [Porsche / trusted admin]
```

### Channels
| Channel | Use |
|---------|-----|
| **Discord** | Primary Ben chat, alerts, fleet coordination |
| **GitHub Automation** | Optional status notes; not primary for phone |
| **Nextcloud app** | Files/calendar sync for human use; not the agent brain |
| **Matrix** | Future self-hosted notify path once MC Phase 1 ready |

### Access policy
Respond only to **Ben/Coombsy**, **Lightning**, **Doc** (and Porsche as coordinator).  
Ben decides major security actions.

---

## 6. Hermes on Android — Setup

Exact package/UI names may change; follow current Hermes Android install docs if they differ.

### 6.1 Install & identity
1. Install Hermes Agent on the Nothing 3a Pro  
2. Log in with the same fleet identity model as other agents (provider keys as appropriate)  
3. Create/use profile name: `codemater` (recommended) for isolated memory/skills  
4. Set personality/system notes: field agent, concise, security-aware, escalate to Porsche  

### 6.2 Discord gateway (critical)
1. Configure Discord bot token / gateway for Code Mater **or** shared fleet bot with clear routing — prefer **distinct bot or clear prefix** if multi-agent noise is high  
2. Allowlist Ben + fleet IDs only  
3. Verify: message from Android Discord app receives Code Mater reply  
4. Verify: Porsche can @/reach Code Mater in shared server  

### 6.3 Toolsets (keep lean)
Enable only what the phone needs:

```text
Recommended: messaging/discord path, lightweight web if needed, skills (read-only heavy)
Avoid on phone: unrestricted terminal against lab, huge browser automation, image gen, long coding loops
```

When Level 3 bridge exists, **remote shell runs inside Termux**, not by giving the cloud model full device admin by default.

### 6.4 Persistence
- Disable battery “kill background” for Hermes / Discord / Termux  
- Exempt from aggressive sleep for gateway process  
- Test overnight + “Do Not Disturb / work mode” scenarios  

---

## 7. Level 1 — Field Capture Workflows

### 7.1 Voice → task
1. Ben sends voice note or short voice-to-text in Discord to Code Mater  
2. Code Mater (or Porsche if Mater only relays) produces a structured task:  
   - Title  
   - Context  
   - Priority  
   - Due hint  
3. Porsche writes to Mission Control (`Deck` / `Notes` / `MissionControl/` paths) when hub is up  
4. Confirm back to Ben in one line  

**Offline:** Code Mater stores draft tasks locally (Termux file or Hermes memory) and flushes when online.

### 7.2 Photo / job site capture
- Prefer Nextcloud Android auto-upload to `ProjectCar/Jobs/inbox/`  
- Code Mater can remind Ben to tag job name  
- Do not auto-upload sensitive IDs/passwords  

### 7.3 Schedule nudge
- Porsche owns true calendar truth (Nextcloud)  
- Code Mater delivers **reminders and confirmations** only — avoid dual calendars drifting  

---

## 8. Level 3 — Termux + SSH Bridge (Preferred Remote Exec)

This is the recommended first remote-exec path.

### 8.1 Install on phone
1. Install **F-Droid** (optional but good for Termux ecosystem)  
2. Install **Termux** (and Termux:API if needed)  
3. In Termux:

```bash
pkg update && pkg upgrade
pkg install openssh git rsync coreutils termux-api
```

4. Set a strong password **or** (better) install Ben/Porsche public keys only:

```bash
passwd   # if using password temporarily
mkdir -p ~/.ssh
chmod 700 ~/.ssh
# append authorized_keys for Porsche/Ben only
chmod 600 ~/.ssh/authorized_keys
```

5. Start SSHD:

```bash
sshd
# note listening port — Termux often uses 8022
```

6. Find mesh/VPN IP (Tailscale/WireGuard) — **never expose sshd to full WAN**

### 8.2 Connect from Porsche

```bash
ssh -p 8022 -i ~/.ssh/codemater_phone <user>@<phone-mesh-ip>
```

Store as SSH config host `codemater`:

```sshconfig
Host codemater
  HostName <phone-mesh-ip>
  User ...
  Port 8022
  IdentityFile ~/.ssh/codemater_phone
  IdentitiesOnly yes
```

### 8.3 What remote commands are allowed

**Allow (examples)**
- `termux-battery-status`  
- Disk/memory summaries  
- Tail Hermes/Termux logs  
- Flush queued field notes to rsync target  
- Run a **signed/known** script from `~/codemater/bin/`  

**Deny by policy**
- Blind `rm -rf`  
- Exfiltrating full photo rolls without Ben  
- Installing unknown packages without Ben  
- Disabling lock screen / security settings remotely  
- Anything that bypasses device encryption  

### 8.4 Command wrapper pattern (recommended)
Maintain an allowlist script on the phone:

```bash
~/codemater/bin/safe-run <verb>
# verbs: battery | health | queue-flush | logs | safe-mode
```

Porsche calls `safe-run` only — not arbitrary shell — until trust is high.

### 8.5 Keep sshd up
- Termux boot script / Termux:Boot (if used) to start `sshd`  
- Or Tasker “on Wi‑Fi connected to home/mesh” → start sshd  
- Alert Discord if sshd unexpected down when Ben is home  

---

## 9. Security Sentinel & Safe Mode

Aligned with `security-playbook.md`.

### 9.1 Alert triggers (immediate Discord)
- Unusual battery drain  
- New unknown apps especially with accessibility/admin privileges  
- Failed unlock / auth anomalies if observable  
- SIM / number change signals if available  
- Unexpected USB debug enablement  
- Failed 2FA / account recovery attempts Ben reports  

### 9.2 Safe mode actions (Ben-approved playbook)
On confirmed or high-confidence threat:

1. Notify Discord `#home` / security channel with timestamp  
2. Disable non-essential automations  
3. Suggest/enable airplane mode if physical threat  
4. Pause remote sshd  
5. Porsche opens `MissionControl/Incidents/` note  
6. Ben decides wipe / reinstall / key rotation  

### 9.3 Daily lightweight audit (phone)
- Hermes responsive?  
- Discord connected?  
- Termux sshd expected state?  
- Free storage / battery health summary  
- Unauthorized device admin apps list (manual or dumpsys where permitted)  

Report **exceptions only** to Discord to avoid noise.

### 9.4 Assumptions
- Device may be lost or seized — full-disk encryption + strong lock required  
- Do not store long-lived cloud admin passwords in plain Termux files  
- Prefer hardware-backed keys / passkeys where possible after upgrade  

---

## 10. Optional Paths: Tasker & ADB

### 10.1 Tasker
Use for:
- On connect to mesh Wi‑Fi → start sshd  
- Low battery → Discord notify via webhook  
- Work geofence → DND + agent quiet hours  
- Share intent → queue field note  

Keep profiles documented in `~/codemater/tasker-export/` (backed up to Nextcloud).

### 10.2 ADB over Wi‑Fi
- **Trusted LAN/mesh only**  
- Disable when not actively debugging  
- Never leave `adb tcpip` open on public networks  
- Prefer wireless debugging pairing with rotating ports on modern Android  

ADB is a **power tool for Ben/Porsche setup**, not the primary always-on agent channel.

---

## 11. Integration with Mission Control & Fleet

| Integration | Mechanism | Phase |
|-------------|-----------|-------|
| Chat with Ben | Discord | L0 |
| Task create | Discord → Porsche → MC Deck/Notes | L1 |
| File drop | Nextcloud Android client | L1 |
| Incident notes | Porsche writes MC Incidents from Mater alerts | L2 |
| Remote diagnostics | SSH `safe-run` | L3 |
| Calendar truth | Nextcloud; Mater only reminds | all |
| Heartbeats | Mater does **not** run heavy MC heartbeats; Porsche owns those | all |

### Data classification on phone
- **OK offline cache:** non-secret todos, public job notes  
- **Minimize:** client PII, payment data, raw 2FA seeds  
- **Never:** lab root credentials, unencrypted export of password managers  

---

## 12. Mobile Workflow Standards (for Ben)

1. **One chat home:** Discord for agent talk while working  
2. **Short commands:** “remind 3pm fuel”, “log job site X arrival”, “alert Porsche battery weird”  
3. **Confirmations:** Mater replies in ≤ few lines  
4. **Quiet hours:** optional work-site mode reduces non-critical pings  
5. **Escalation:** security language (“compromised”, “unknown app”, “2FA”) always pages Porsche + Ben hard  

### Example interactions
```text
Ben: voice note "need dual-cert TIG coupons for Friday"
Mater: Queued task → Porsche. Priority normal. Confirm?

Ben: battery feels wrong after install
Mater: SECURITY: flagging drain anomaly. Pausing nonessential automation. Porsche notified.
```

---

## 13. Upgrade Recommendations

**Why upgrade:** better battery for 12h+ days, stronger security updates, more RAM for Hermes, cleaner OEM policy for background agents, better thermal headroom.

**Target class (research at purchase time):**
- Flagship or strong mid-flagship Android with long support window  
- Excellent battery + efficient SoC  
- Predictable developer options / unlock policy if needed  
- Preference for devices that play well with Termux + reliable background work  

**Candidates to evaluate when buying:** Pixel (update longevity), Nothing flagship, Samsung (Tasker/DeX ecosystem) — re-check 2026 reviews for battery and policy.

**Migration checklist**
1. New device encrypt + lock setup  
2. Fresh Hermes install + new profile  
3. New SSH keypair; retire old phone keys  
4. Discord allowlist unchanged  
5. Wipe old device after cutover  
6. Update this doc + agent-profiles hardware table  

---

## 14. Phased Bring-Up Checklist

### Phase CM-0 — Chat reliable
- [ ] Hermes installed and logged in  
- [ ] Discord allowlist correct  
- [ ] Reply latency acceptable on LTE and job Wi‑Fi  
- [ ] Battery exemptions set  
- [ ] Ben can use as primary field chat  

### Phase CM-1 — Capture
- [ ] Voice/text → task handoff to Porsche documented and tested  
- [ ] Nextcloud auto-upload folder working  
- [ ] Offline queue + flush tested (airplane mode drill)  

### Phase CM-2 — Sentinel
- [ ] Alert templates for battery/apps/auth  
- [ ] Discord security path verified  
- [ ] Safe-mode steps written and dry-run (without breaking phone)  
- [ ] Daily exception-only audit  

### Phase CM-3 — SSH bridge
- [ ] Termux + openssh installed  
- [ ] Key-only auth from Porsche  
- [ ] Mesh-only reachability  
- [ ] `safe-run` allowlist verbs live  
- [ ] sshd auto-start policy chosen  
- [ ] No WAN exposure confirmed (`nmap` from outside mesh)  

### Phase CM-4 — Hardened / upgraded device
- [ ] Hardware upgrade decision  
- [ ] Clean install + key rotation  
- [ ] Risk posture lowered in security playbook  

---

## 15. Failure Modes

| Failure | Behavior |
|---------|----------|
| No network | Queue messages/tasks locally; sync later |
| Discord down | Local log; retry; optional SMS only if Ben pre-approves another path |
| Hermes crash | Ben uses raw Discord to Porsche; Mater restarts on unlock |
| SSH unreachable | Fall back to L0/L1; do not open WAN ports to “fix” it |
| Phone stolen | Ben remote-wipe via Google/OEM; rotate all tokens; revoke SSH keys; Discord alert |
| False security alert | Mater labels confidence; Porsche dedupes; tune thresholds |

---

## 16. Open Decisions

1. Separate Discord bot for Code Mater vs shared fleet bot  
2. Tailscale vs WireGuard for phone mesh enrollment  
3. Termux:Boot vs Tasker for sshd persistence  
4. Exact allowlist verbs for `safe-run` v1  
5. Nextcloud official app vs FolderSync for photo pipeline  
6. Device upgrade model + budget timing  
7. Whether SMS fallback is ever allowed (security tradeoff)  

---

## 17. Immediate Next Actions

| # | Action | Owner |
|---|--------|-------|
| 1 | Confirm Hermes+Discord L0 reliability on Nothing 3a Pro for a full work day | Ben + Code Mater |
| 2 | Set battery/background exemptions | Ben |
| 3 | Define task handoff format with Porsche (template message) | Porsche |
| 4 | Install Termux + key-only sshd on mesh only | Ben + Porsche |
| 5 | Implement `safe-run` with `battery` + `health` verbs | Porsche / Mater |
| 6 | Dry-run security alert → Discord → incident note | Porsche |
| 7 | Start upgrade shortlist (3 devices) when Ben ready | Porsche research |

---

## 18. Document Maintenance

- **Maintained by:** Porsche  
- **Update when:** device changes, bridge level changes, security incidents, Discord/bot topology changes  
- **Sync:** skill + Desktop + GitHub `Docs/` together  
- **After incidents:** append lessons to security playbook **and** this guide  

---

**Approved by:** _(pending Ben)_  
**Maintained by:** Porsche  

*Living document — promote `safe-run` verb list and exact package versions once the phone bridge is live.*
