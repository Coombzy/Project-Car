#!/usr/bin/env python3
"""Free this user's listeners on the shop visual ports.

Playwright starts the API with reuseExistingServer false. When
http://127.0.0.1:8000/health already answers, that start errors and the
screenshot job never runs. A previous visual run can leave uvicorn on
8000 and next on 3000. Stop those listeners after the web build, before
`npm run visual`. Do not flip reuseExistingServer and do not raise the
pixel or layout-shift caps.
"""

from __future__ import annotations

import os
import signal
import socket
import sys
import time

VISUAL_PORTS = (8000, 3000)
LISTEN_STATE = "0A"


def listen_inodes(tcp: str, tcp6: str, ports: tuple[int, ...]) -> dict[int, set[str]]:
    """Map each port to the socket inodes in LISTEN state in /proc/net text."""
    wanted = {port: set() for port in ports}
    for text in (tcp, tcp6):
        for inode, port in _listen_rows(text):
            if port in wanted:
                wanted[port].add(inode)
    return wanted


def _listen_rows(text: str):
    lines = text.splitlines()
    for line in lines[1:]:
        parts = line.split()
        if len(parts) < 10 or parts[3] != LISTEN_STATE:
            continue
        _addr, _sep, port_hex = parts[1].rpartition(":")
        if not port_hex:
            continue
        try:
            port = int(port_hex, 16)
        except ValueError:
            continue
        yield parts[9], port


def pids_holding(
    inodes: set[str],
    sockets_by_pid: dict[int, set[str]],
    exclude: set[int],
) -> list[int]:
    """Pids that hold one of `inodes`. `exclude` is never returned."""
    if not inodes:
        return []
    found: list[int] = []
    for pid, socks in sockets_by_pid.items():
        if pid in exclude:
            continue
        if inodes & socks:
            found.append(pid)
    return found


def _sockets_by_pid(exclude: set[int]) -> dict[int, set[str]]:
    found: dict[int, set[str]] = {}
    for name in os.listdir("/proc"):
        if not name.isdigit():
            continue
        pid = int(name)
        if pid in exclude:
            continue
        fd_dir = f"/proc/{pid}/fd"
        try:
            fds = os.listdir(fd_dir)
        except OSError:
            continue
        socks: set[str] = set()
        for fd in fds:
            try:
                target = os.readlink(f"{fd_dir}/{fd}")
            except OSError:
                continue
            if target.startswith("socket:[") and target.endswith("]"):
                socks.add(target[len("socket:[") : -1])
        if socks:
            found[pid] = socks
    return found


def port_open(port: int) -> bool:
    sock = socket.socket()
    sock.settimeout(0.4)
    try:
        sock.connect(("127.0.0.1", port))
    except OSError:
        return False
    finally:
        sock.close()
    return True


def _read_proc_net(name: str) -> str:
    try:
        with open(f"/proc/net/{name}", encoding="utf-8") as handle:
            return handle.read()
    except OSError:
        return ""


def _signal(pids: list[int], sig: int) -> None:
    for pid in pids:
        try:
            os.kill(pid, sig)
        except OSError:
            pass


def _busy(ports: tuple[int, ...]) -> list[int]:
    return [port for port in ports if port_open(port)]


def _targets(busy: list[int], exclude: set[int]) -> list[int]:
    by_port = listen_inodes(_read_proc_net("tcp"), _read_proc_net("tcp6"), VISUAL_PORTS)
    inodes: set[str] = set()
    for port in busy:
        inodes |= by_port.get(port, set())
    return pids_holding(inodes, _sockets_by_pid(exclude), exclude)


def main() -> int:
    exclude = {os.getpid(), os.getppid()}
    if not _busy(VISUAL_PORTS):
        return 0
    _signal(_targets(_busy(VISUAL_PORTS), exclude), signal.SIGTERM)
    for _ in range(20):
        if not _busy(VISUAL_PORTS):
            return 0
        time.sleep(0.1)
    _signal(_targets(_busy(VISUAL_PORTS), exclude), signal.SIGKILL)
    for _ in range(20):
        if not _busy(VISUAL_PORTS):
            return 0
        time.sleep(0.1)
    still = _busy(VISUAL_PORTS)
    print(
        "visual ports still in use: " + ", ".join(str(port) for port in still),
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
