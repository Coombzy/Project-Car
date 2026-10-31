import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const visualDir = join(dirname(fileURLToPath(import.meta.url)), "../visual");
const buildWebPath = join(visualDir, "build-web.sh");

/** `shop-os-ci.yml` runs `npx playwright install --with-deps chromium` before this script. */
const PORT_CHECK = `
from free_visual_ports import VISUAL_PORTS, listen_inodes, pids_holding

assert VISUAL_PORTS == (8000, 3000)

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
found = listen_inodes(tcp, tcp6, VISUAL_PORTS)
assert found[8000] == {"111"}, found
assert found[3000] == {"444"}, found
assert "222" not in found[8000]
assert "333" not in found[8000]
assert "555" not in found[3000]
assert "666" not in found[8000]
pids = pids_holding({"111", "444"}, {5: {"111"}, 9: {"999"}, 7: {"444"}, 4: {"555"}}, {7})
assert sorted(pids) == [5], pids
empty = pids_holding(set(), {5: {"111"}}, set())
assert empty == []
`;

describe("visual/build-web.sh", () => {
  it("does not install Chromium", () => {
    const source = readFileSync(buildWebPath, "utf8");
    assert.equal(
      /^\s*npx playwright install\b/m.test(source),
      false,
      "build-web.sh must not run npx playwright install",
    );
    assert.match(source, /^npm run build\s*$/m);
  });

  it("stops listeners on port 8000 before Playwright starts", () => {
    const source = readFileSync(buildWebPath, "utf8");
    const buildAt = source.search(/^npm run build\s*$/m);
    const freeAt = source.search(/^python3 "\$VISUAL\/free_visual_ports\.py"\s*$/m);
    assert.ok(buildAt >= 0, "build-web.sh must run npm run build");
    assert.ok(
      freeAt > buildAt,
      "build-web.sh must free port 8000 after the build, before Playwright starts",
    );
    const proc = spawnSync("python3", ["-c", PORT_CHECK], {
      cwd: visualDir,
      encoding: "utf8",
    });
    assert.equal(proc.status, 0, `${proc.stderr ?? ""}\n${proc.stdout ?? ""}`);
  });
});
