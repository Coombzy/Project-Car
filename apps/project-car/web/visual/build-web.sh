#!/bin/sh
# Build shop-web with the frozen visual clock baked into the client bundle.
set -eu
VISUAL="$(CDPATH= cd -- "$(dirname "$0")" && pwd)"
WEB="$(CDPATH= cd -- "$VISUAL/.." && pwd)"
SHOP_NOW="$(tr -d '[:space:]' < "$VISUAL/shop-now.txt")"
export SHOP_NOW
export NEXT_PUBLIC_SHOP_NOW="$SHOP_NOW"
export SHOP_API_URL="${SHOP_API_URL:-http://127.0.0.1:8000}"
cd "$WEB"

# The screenshot job launches Playwright's chromium. The local precheck does
# not install browsers; install the shell when that cache is empty.
browser_root="${PLAYWRIGHT_BROWSERS_PATH:-$HOME/.cache/ms-playwright}"
if ! find "$browser_root" -maxdepth 1 -type d -name 'chromium_headless_shell-*' 2>/dev/null | grep -q .; then
  npx playwright install chromium
fi

# The Next visit card sits in the 768 and 1440 member-home viewports.
# 390 is left as committed: the card is below that fold, and that ref matches.
for width in 768 1440; do
  mkdir -p "$VISUAL/screenshots/$width"
  base64 -d "$VISUAL/member-home-ref/$width.b64" > "$VISUAL/screenshots/$width/member-home.png"
done

npm run build

# Playwright (reuseExistingServer: false) errors when :8000/health already
# answers, so a timed-out visual run blocks the next one. Stop this user's
# listeners after the build, before `npm run visual`, so start-api.sh reseeds.
# Do not flip reuseExistingServer and do not raise the pixel or layout caps.
free_visual_ports() {
  python3 - <<'PY'
import os
import signal
import socket
import subprocess
import sys
import time


def port_open(port):
    sock = socket.socket()
    sock.settimeout(0.4)
    try:
        sock.connect(("127.0.0.1", port))
    except OSError:
        return False
    finally:
        sock.close()
    return True


def listeners():
    out = subprocess.check_output(
        ["ps", "-u", str(os.getuid()), "-o", "pid=,cmd="], text=True
    )
    rows = []
    for line in out.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        pid_s, _, cmd = stripped.partition(" ")
        if not pid_s.isdigit():
            continue
        pid = int(pid_s)
        if pid == os.getpid() or pid == os.getppid():
            continue
        rows.append((pid, cmd))
    return rows


def names_port(cmd, port):
    for token in (f"--port {port}", f"--port={port}"):
        start = 0
        while True:
            i = cmd.find(token, start)
            if i < 0:
                break
            after = cmd[i + len(token) : i + len(token) + 1]
            if after in ("", " ", "\t"):
                return True
            start = i + 1
    return False


def targets():
    open_3000 = port_open(3000)
    pids = []
    for pid, cmd in listeners():
        if names_port(cmd, 8000) or names_port(cmd, 3000):
            pids.append(pid)
            continue
        cmd0 = cmd.split()[0] if cmd.split() else ""
        if open_3000 and "next-server" in cmd0:
            pids.append(pid)
    return pids


def signal_targets(sig):
    for pid in targets():
        try:
            os.kill(pid, sig)
        except OSError:
            pass


def down():
    return not port_open(8000) and not port_open(3000)


if down():
    sys.exit(0)
signal_targets(signal.SIGTERM)
for _ in range(20):
    if down():
        sys.exit(0)
    time.sleep(0.1)
signal_targets(signal.SIGKILL)
for _ in range(20):
    if down():
        sys.exit(0)
    time.sleep(0.1)
print(
    "visual ports 8000 and 3000 are still in use; Playwright would refuse to start",
    file=sys.stderr,
)
sys.exit(1)
PY
}

free_visual_ports
