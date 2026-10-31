"""The visual build must not install a browser, and it must free port 8000."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
VISUAL = ROOT / "apps" / "project-car" / "web" / "visual"
BUILD_WEB = VISUAL / "build-web.sh"
FREER = VISUAL / "free_visual_ports.py"


def test_build_web_does_not_install_chromium_and_frees_port_8000() -> None:
    script = BUILD_WEB.read_text(encoding="utf-8")
    assert "npx playwright install" not in script, "build-web.sh must not run npx playwright install"
    build_at = script.find("\nnpm run build\n")
    free_line = 'python3 "$VISUAL/free_visual_ports.py"'
    free_at = script.find("\n" + free_line + "\n")
    assert build_at >= 0, "build-web.sh must run npm run build"
    assert free_at > build_at, "build-web.sh must free port 8000 after the build, before Playwright starts"

    spec = importlib.util.spec_from_file_location("free_visual_ports", FREER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.VISUAL_PORTS == (8000, 3000)

    tcp = """  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode
   0: 0100007F:1F40 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 111 1 0000000000000000 100 0 0 10 0
   1: 0100007F:1F40 00000000:0000 01 00000000:00000000 00:00000000 00000000     0        0 222 1 0000000000000000 100 0 0 10 0
   2: 00000000:0050 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 333 1 0000000000000000 100 0 0 10 0
   3: 0100007F:1F41 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 666 1 0000000000000000 100 0 0 10 0
"""
    tcp6 = """  sl  local_address                         remote_address                        st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode
   0: 00000000000000000000000000000000:0BB8 00000000000000000000000000000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 444 1 0000000000000000 100 0 0 10 0
   1: 00000000000000000000000000000000:0BC2 00000000000000000000000000000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 555 1 0000000000000000 100 0 0 10 0
"""
    found = module.listen_inodes(tcp, tcp6, module.VISUAL_PORTS)
    assert found[8000] == {"111"}, found
    assert found[3000] == {"444"}, found
    assert "222" not in found[8000]
    assert "333" not in found[8000]
    assert "555" not in found[3000]
    assert "666" not in found[8000]
    pids = module.pids_holding({"111", "444"}, {5: {"111"}, 9: {"999"}, 7: {"444"}, 4: {"555"}}, {7})
    assert sorted(pids) == [5], pids
    assert module.pids_holding(set(), {5: {"111"}}, set()) == []
