# Security & Incident Response Playbook

**Last Updated:** 2026-08-16  
**Part of:** Project Car documentation hierarchy  
**Canonical:** `Coombzy/Project-Car` → `Docs/security-playbook.md`  
**Optional Desktop mirror:** `~/Desktop/Project Car/docs/` (not an authoring path)  
**Skill:** pointer only — do not dual-author here

Highest-priority child for *how* we respond. The original July 2026 concern (observed file movement, Android reset, lost 2FA) is the reason this file exists; it is **not** a claim of an open incident today. For live hub exposure rules see `mission-control-architecture.md` §11 and `website-webapp-specification.md`.

## Core Principles
- **Zero Trust**: Assume breach. No implicit trust between machines or agents.
- **Local-First**: Minimize cloud services. All sensitive operations stay on controlled hardware.
- **Daily Audits**: Automated where possible, reviewed by Porsche.
- **Rapid Response**: Code Mater (Android) provides field alerts. Porsche coordinates response.
- **Documentation**: Every incident logged in Mission Control (Nextcloud Notes or dedicated log).

## Agent Roles in Security
- **Porsche**: Central coordinator. Runs daily audits, analyzes logs, makes decisions, updates this playbook.
- **Lightning McKing**: Implements security tooling, hardens homelab/storage, runs heavy scans.
- **Doc Hudson**: Analyzes logs for anomalies, runs local LLMs for threat detection.
- **Code Mater**: Mobile early warning system. Monitors phone for unusual activity, sends alerts via Discord.

## Daily Audit Checklist (Automated where possible)
1. **File Integrity** — Check for unexpected file movement, new files in sensitive directories (use `find` or tools like `aide`/`tripwire` on Linux/macOS).
2. **Process Monitoring** — Look for unknown processes, high CPU/network on all machines.
3. **Network Scans** — Check for unexpected open ports, new devices on network.
4. **Authentication Logs** — Review login attempts, 2FA events, lost device status.
5. **Agent Health** — Verify all agents are responsive and not behaving anomalously.
6. **Nextcloud & Mission Control** — Check for unauthorized access or unusual sync activity.
7. **Android Device (Code Mater)** — Check for unusual apps, battery drain, location anomalies.

**Automation**: Porsche runs a daily heartbeat that executes the above and reports exceptions to Discord.

## Incident Response Playbook (Run in order)

### Phase 0: Detection
- Code Mater sends immediate Discord alert for:
  - Unusual battery drain
  - New unknown apps
  - Location anomalies
  - Failed 2FA or login attempts
- Porsche or Lightning detects anomaly during daily audit.

### Phase 1: Containment (0-5 minutes)
1. Porsche isolates affected machine (disable network, kill suspicious processes).
2. Code Mater triggers "safe mode" on Android (disable non-essential apps, enable airplane mode if needed).
3. Change all passwords / rotate keys from a clean machine.

### Phase 2: Investigation (5-60 minutes)
1. Lightning McKing creates forensic snapshot (memory dump, disk image where possible).
2. Doc Hudson analyzes logs with local LLMs for patterns.
3. Porsche reviews timeline in Mission Control.

### Phase 3: Eradication & Recovery
1. Wipe and re-image affected machine if compromise is confirmed.
2. Restore from known-good backup (air-gapped where possible).
3. Re-deploy agents with updated security keys.
4. Update this playbook with lessons learned.

### Phase 4: Post-Incident
- Full report written to Mission Control.
- All agents review changes.
- Upgrade priority list updated (e.g. faster move to new Android device for Code Mater).

## Tools & Techniques
- **macOS**: `fs_usage`, `lsof`, `netstat`, `launchctl`, Full Disk Access granted but watch for "operation not permitted" errors.
- **Linux/homelab**: `rsyslog`, `auditd`, `fail2ban`, `rkhunter`, ZFS snapshots.
- **Android**: Termux + `sshd`, Tasker automation, Hermes Agent for alerts.
- **Centralized**: Nextcloud for log storage, Porsche as the analyst.

## Prevention Standards
- All devices use strong, unique passphrases + hardware keys where possible.
- No persistent cloud logins except for controlled, monitored services.
- Regular backups with offline copies.
- Agent code signed and verified.
- Code Mater upgrade prioritized to a device with better on-device security features.

This playbook will be refined after every incident or audit finding.

---
**Maintained by:** Porsche + Doc  
**Canonical:** `Docs/security-playbook.md` on `Coombzy/Project-Car`  
**Related:** `master-overview-specification.md`, `agent-profiles-specification.md`, `mission-control-architecture.md`