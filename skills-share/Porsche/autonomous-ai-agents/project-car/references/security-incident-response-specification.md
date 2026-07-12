# Security & Incident Response Playbook

**Last Updated:** July 2026  
**Part of:** Project Car documentation hierarchy  
**Synchronized locations:**  
- Skill: `~/.hermes/skills/autonomous-ai-agents/project-car/references/security-playbook.md`  
- Desktop: `~/Desktop/Project-Car-Docs/security-playbook.md`

**Hardware Environment:** Heterogeneous fleet consisting of:
- **Linux/CachyOS machine** (Lightning McKing — i9-9900K + RTX 50801, primary homelab/storage, Arch-based with performance optimizations)
- **Two MacBooks** (Porsche on M4 Pro, Doc Hudson on M1 Max 32-core/64GB)
- **Android phone** (Code Mater on Nothing 3a Pro running Hermes Agent)

All procedures below are tailored to this mixed environment. Note chronic macOS "operation not permitted" errors even with Full Disk Access — use narrow paths and escalate to user when needed.

## Core Principles
- **Zero Trust**: Assume breach on any machine. No implicit trust.
- **Local-First**: Minimize cloud services. Sensitive operations stay on controlled hardware.
- **Daily Audits**: Automated where possible, reviewed by Porsche.
- **Rapid Response**: Code Mater provides field alerts via Discord. Porsche coordinates.
- **Documentation**: Every incident and audit logged in Mission Control (Nextcloud Notes or dedicated encrypted log).

## Agent Roles in Security
- **Porsche (M4 Pro)**: Central coordinator, runs daily audits, analyzes logs, makes routing decisions, updates this playbook.
- **Lightning McKing (CachyOS)**: Implements security tooling, hardens Linux storage/homelab, runs heavy scans and GPU-accelerated analysis.
- **Doc Hudson (M1 Max)**: Deep log analysis using local LLMs, anomaly detection, forensic reasoning.
- **Code Mater (Android + Hermes Agent)**: Mobile early warning system. Monitors device for anomalies, sends real-time Discord alerts, supports remote commands via bridge.

## Daily Audit Checklist (Automated where possible via Porsche heartbeat)
Run on all machines daily. Porsche aggregates results and reports exceptions to Discord (Turbocharger Springs).

### Linux/CachyOS (McKing)
- `auditd` logs, `rkhunter`, `clamav`, `fail2ban` status
- Check for unexpected processes (`ps aux`, `netstat -tuln`)
- Filesystem integrity (`aide` or custom scripts on key directories)
- ZFS/BTRFS snapshot validation
- Storage array health (SMART, RAID status)

### macOS (Porsche & Doc Hudson)
- `fs_usage`, `lsof`, `netstat`, `launchctl list`
- Check for unexpected login events (`log show --predicate 'eventMessage contains "login"'`)
- FileVault status, SIP status, `tmutil listlocalsnapshots`
- Watch for "operation not permitted" errors on Library paths — use scoped paths (`~/.hermes`, project dirs)
- `spctl --status` and Gatekeeper checks

### Android (Code Mater)
- Battery drain anomalies, unusual app permissions, new installed apps
- Hermes Agent health and log review
- ADB/Termux SSH access verification
- Location and network anomalies

**Automation**: Porsche heartbeat script runs platform-specific checks and consolidates output.

## Incident Response Playbook (Run in this order)

### Phase 0: Detection
Triggers:
- Code Mater sends Discord alert (unusual battery, new apps, location jumps, failed 2FA)
- Porsche audit finds anomaly on any machine
- Unexpected file movement (especially on macOS)

### Phase 1: Containment (0–5 minutes)
1. Porsche isolates affected machine:
   - Linux: `iptables -A INPUT -j DROP` or `ufw disable`
   - macOS: Disable WiFi/Ethernet or use `networksetup`
   - Android: Code Mater triggers airplane mode or Hermes "safe mode"
2. Kill suspicious processes (platform-specific commands logged).
3. Rotate all credentials from a clean machine (Porsche preferred).

### Phase 2: Investigation (5–60 minutes)
1. Lightning McKing creates forensic snapshot (Linux: `dd` or `rsync` of key dirs; macOS: `fs_usage` + Time Machine snapshot).
2. Doc Hudson analyzes logs with local LLMs for patterns.
3. Porsche builds timeline in Mission Control (Nextcloud).
4. Check all machines — compromise on one often indicates lateral movement.

### Phase 3: Eradication & Recovery
1. Wipe/re-image affected machine if root-level compromise confirmed.
2. Restore from known-good, air-gapped backup (CachyOS ZFS snapshots or macOS Time Machine).
3. Re-deploy agents with fresh keys and updated security baseline.
4. Update this playbook with lessons learned (new detection rules).

### Phase 4: Post-Incident
- Full report written to encrypted Mission Control note.
- All agents review changes.
- Update upgrade priority list (e.g. faster Code Mater replacement if Android is weak point).
- Test restored system thoroughly.

## Platform-Specific Tools
- **CachyOS/Linux**: `auditd`, `rkhunter`, `clamav`, `fail2ban`, `aide`, `zfs-auto-snapshot`, `netstat/ss`, `journalctl`
- **macOS**: `fs_usage`, `lsof`, `log`, `launchctl`, `fdesetup`, `tmutil`, `spctl`, `sip`
- **Android**: Termux (`sshd`, `top`, `logcat`), Tasker automation, ADB over WiFi, Hermes Agent logs, battery/permission monitors

## Prevention Standards
- Strong, unique passphrases + hardware security keys where possible.
- No unnecessary cloud logins.
- Regular, tested, air-gapped backups.
- Agent code signed and verified on deployment.
- Code Mater upgrade is high priority — target device with better on-device security, battery, and developer tools.
- Strict network segmentation between machines.

This playbook is living and will be updated after every incident or audit. All agents must be familiar with it.

---
**Maintained by:** Porsche  
**Synchronized in both locations per documentation policy.**  
**Related:** `master-overview.md`, `agent-profiles.md`, `high-level-apps-and-business.md`