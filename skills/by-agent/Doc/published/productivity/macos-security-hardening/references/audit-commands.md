# Audit command bank (macOS AI workstation)

Run non-destructively. Prefer batching independent reads. Redact secrets in reports.

## Platform baseline
```bash
sw_vers; uname -a
csrutil status
fdesetup status
spctl --status --verbose
softwareupdate --list 2>&1 | head -40
sysadminctl -screenLock status
# FileVault recovery principals
fdesetup list 2>&1
# Authenticated root / activation (Apple Silicon)
csrutil authenticated-root status 2>&1
system_profiler SPHardwareDataType 2>&1 | grep -iE 'Serial|UUID|Activation'
```

## Firewall
```bash
FW=/usr/libexec/ApplicationFirewall/socketfilterfw
$FW --getglobalstate
$FW --getstealthmode
$FW --getblockall
$FW --getallowsigned
$FW --getallowsignedapp
$FW --listapps
```

## Sharing / remote access
```bash
systemsetup -getremotelogin 2>&1
sharing -l 2>&1
# Screen Sharing service presence
launchctl print system/com.apple.screensharing 2>&1 | head -15
# Orphan admin members (used-device hygiene)
dscl . -read /Groups/admin GroupMembership
dscl . -list /Users UniqueID | awk '$2>=500'
```

## Listeners (LAN exposure)
```bash
lsof -iTCP -sTCP:LISTEN -P -n
# Non-loopback only
lsof -iTCP -sTCP:LISTEN -P -n | grep -v '127.0.0.1\|\[::1\]' || true
# AirPlay often: ControlCenter *:5000 *:7000
# Continuity: rapportd high port
```

## Tailscale
```bash
which tailscale; tailscale status
tailscale debug prefs 2>&1 | head -60
# Dual install smell
ps aux | grep -i tailscale | grep -v grep
ls ~/Library/LaunchAgents/*tail* 2>/dev/null
systemextensionsctl list
```

## Persistence
```bash
ls -la ~/Library/LaunchAgents/ /Library/LaunchAgents/ /Library/LaunchDaemons/ 2>/dev/null
kextstat 2>/dev/null | grep -v com.apple || true
systemextensionsctl list
crontab -l 2>&1
osascript -e 'tell application "System Events" to get the name of every login item' 2>&1
```

## TCC (may need Full Disk Access for system DB)
```bash
# User TCC
sqlite3 ~/Library/Application\ Support/com.apple.TCC/TCC.db \
  "SELECT service, client, auth_value FROM access WHERE auth_value>0;" 2>&1 | head -80
# System TCC (sudo)
sudo sqlite3 /Library/Application\ Support/com.apple.TCC/TCC.db \
  "SELECT service, client, auth_value FROM access WHERE auth_value>0;" 2>&1 | head -80
# Watch for: com.macdiag.app, unknown FDA/Accessibility/ListenEvent
```

## Hermes / Ollama (AI stack)
```bash
ls -la ~/.hermes/ ~/.hermes/.env ~/.hermes/auth.json ~/.hermes/config.yaml ~/.hermes/state.db 2>/dev/null
# Key names only from .env
grep -E '^[A-Z0-9_]+=' ~/.hermes/.env 2>/dev/null | cut -d= -f1
lsof -iTCP -sTCP:LISTEN -P -n | grep -i ollama || true
curl -sS --max-time 2 http://127.0.0.1:11434/api/tags | head -c 200; echo
# Expect 127.0.0.1 only — flag any 0.0.0.0/LAN bind
```

## Bluetooth / continuity hygiene
```bash
system_profiler SPBluetoothDataType 2>&1 | head -50
# Forget unknown paired devices in GUI
```

## Backups
```bash
tmutil destinationinfo 2>&1
tmutil latestbackup 2>&1 | head -5
```

## Report path
`~/Desktop/macOS-Security-Audit-YYYY-MM-DD.md` — include severity, evidence, fix, do-now vs later.
