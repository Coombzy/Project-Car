# Multi-device risks (AI Mac + Tailscale + Continuity)

## Tailscale
- Prefer **one** client on macOS: official **Tailscale.app** (system network extension).
- Homebrew `tailscaled --tun=userspace-networking` often runs in parallel via LaunchAgent — stop it.
- Check prefs: `ShieldsUp`, `RouteAll`, `RunSSH`, `ExitNode*`.
  - ShieldsUp false = accepts inbound from tailnet (OK only with tight ACLs).
  - RouteAll true = intentional subnet routing only.
  - RunSSH false until keys + Tailscale SSH policy are deliberate.
- Compromised peer (e.g. always-on Linux box) is lateral-movement risk to the Mac.
- Do not advertise Ollama/Hermes ports on the tailnet without auth.

## Continuity / local discovery
- `rapportd` listening on `*:<highport>` is normal Continuity surface.
- AirPlay Receiver = ControlCenter on `*:5000` and `*:7000` — disable on untrusted LANs.
- AirDrop: Contacts Only or Off when traveling.
- Bluetooth: remove previous-owner pairings (random headphone names are a signal).

## iCloud / Apple ID
- Activation Lock should stay enabled for theft recovery.
- Review devices list after used-Mac setup or shop visit.
- iCloud-synced agent notes/secrets need intentional scope (prefer local `~/.hermes` with tight perms).

## SSH across fleet (Ben’s preferred path)
- Prefer simple SSH **over Tailscale**, not public WAN SSH.
- Keep Remote Login Off until keys exist; then keys-only, no password auth on public interfaces.
- Generate `~/.ssh` only when enabling; document AllowUsers if multi-account.

## Hermes multi-machine
- Profiles isolate skills/cron/memories — use `secure-ai` (or similar) for sensitive sessions.
- Don’t share world-readable `state.db` across users; chmod 700 `~/.hermes`.
- Local Ollama custom provider should stay `http://127.0.0.1:11434/v1`.

## Used-device / repair-shop residue
- Admin group may still list `phonecheck` after home deletion.
- Share points can keep guest R/W on Public folders — `sharing -l`.
- MacDiag (`com.macdiag.app`) may retain FDA + Accessibility + Input Monitoring after uninstall.
- Treat shop service as a credential-rotation event if untrusted.
