import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, mkdirSync, readFileSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath, pathToFileURL } from "node:url";

const repoRoot = join(dirname(fileURLToPath(import.meta.url)), "..", "..", "..", "..");
const script = join(repoRoot, "scripts", "ui-proof.ts");
const packageJson = join(repoRoot, "apps", "project-car", "web", "package.json");

type GateModule = {
  SYSTEM_CHROME_CANDIDATES: readonly string[];
  findChrome: (plan: { files: string[]; directories: string[] }) => string | null;
  playwrightCacheRoots: (
    env: { PLAYWRIGHT_BROWSERS_PATH?: string; LOCALAPPDATA?: string },
    platform: string,
    home: string,
  ) => string[];
  searchPlan: (
    env: { HOME?: string; UI_PROOF_CHROME_PATHS?: string; PLAYWRIGHT_BROWSERS_PATH?: string },
    platform?: string,
  ) => { files: string[]; directories: string[] };
};

async function loadGate(): Promise<GateModule> {
  return (await import(pathToFileURL(script).href)) as GateModule;
}

function runGate(env: Record<string, string | undefined>) {
  const childEnv: NodeJS.ProcessEnv = { ...process.env };
  for (const [key, value] of Object.entries(env)) {
    if (value === undefined) {
      delete childEnv[key];
    } else {
      childEnv[key] = value;
    }
  }
  return spawnSync(process.execPath, ["--experimental-strip-types", script], {
    env: childEnv,
    encoding: "utf8",
  });
}

describe("ui proof chrome gate", () => {
  it("test_ui_proof_ci_missing_chrome_exits_nonzero", () => {
    const dir = mkdtempSync(join(tmpdir(), "ui-proof-ci-"));
    const missingA = join(dir, "no-chrome-a");
    const missingB = join(dir, "no-chrome-b");
    try {
      const result = runGate({
        CI: "true",
        UI_PROOF_CHROME_PATHS: `${missingA}:${missingB}`,
      });
      const output = `${result.stdout ?? ""}${result.stderr ?? ""}`;
      assert.notEqual(
        result.status,
        0,
        `CI=true with no Chrome exited ${String(result.status)}, expected non-zero\n${output}`,
      );
      assert.match(output, /Paths searched:/);
      assert.ok(output.includes(missingA), output);
      assert.ok(output.includes(missingB), output);
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });

  it("test_ui_proof_local_missing_chrome_prints_skipped", () => {
    const dir = mkdtempSync(join(tmpdir(), "ui-proof-local-"));
    const missing = join(dir, "no-chrome");
    try {
      const result = runGate({
        CI: undefined,
        UI_PROOF_CHROME_PATHS: missing,
      });
      assert.equal(result.status, 0, result.stderr);
      assert.match(result.stdout ?? "", /SKIPPED/);
      assert.equal((result.stderr ?? "").includes("Paths searched:"), false);
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });

  it("test_ui_proof_visual_script_invokes_the_gate", () => {
    const pkg = JSON.parse(readFileSync(packageJson, "utf8")) as { scripts?: { visual?: string } };
    assert.match(pkg.scripts?.visual ?? "", /scripts\/ui-proof\.ts/);
    const source = readFileSync(script, "utf8");
    assert.match(source, /playwrightBin/);
    assert.match(source, /\["test"\]/);
  });

  it("test_ui_proof_searches_system_chrome_and_playwright_cache", async () => {
    const gate = await loadGate();
    for (const path of [
      "/usr/bin/google-chrome",
      "/usr/bin/chromium",
      "/usr/bin/chromium-browser",
      "/usr/local/bin/google-chrome",
      "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]) {
      assert.ok(gate.SYSTEM_CHROME_CANDIDATES.includes(path), path);
    }
    const home = join(tmpdir(), "ui-proof-home");
    const plan = gate.searchPlan({ HOME: home }, "linux");
    assert.ok(plan.files.includes("/usr/bin/google-chrome"));
    assert.deepEqual(gate.playwrightCacheRoots({}, "linux", home), [join(home, ".cache", "ms-playwright")]);
    assert.deepEqual(gate.playwrightCacheRoots({}, "darwin", home), [
      join(home, "Library", "Caches", "ms-playwright"),
    ]);
    const custom = join(home, "browsers");
    assert.deepEqual(gate.playwrightCacheRoots({ PLAYWRIGHT_BROWSERS_PATH: custom }, "linux", home), [
      custom,
      join(home, ".cache", "ms-playwright"),
    ]);
    assert.deepEqual(gate.playwrightCacheRoots({ PLAYWRIGHT_BROWSERS_PATH: "0" }, "linux", home), [
      join(home, ".cache", "ms-playwright"),
    ]);
    assert.deepEqual(
      gate.playwrightCacheRoots({ LOCALAPPDATA: join(home, "Local") }, "win32", home),
      [join(home, "Local", "ms-playwright")],
    );
  });

  it("test_ui_proof_playwright_cache_file_counts_as_chromium", async () => {
    const gate = await loadGate();
    const dir = mkdtempSync(join(tmpdir(), "ui-proof-cache-"));
    const binary = join(dir, "chromium-1148", "chrome-linux", "chrome");
    try {
      mkdirSync(dirname(binary), { recursive: true });
      writeFileSync(binary, "");
      assert.equal(gate.findChrome({ files: [], directories: [dir] }), binary);
      assert.equal(gate.findChrome({ files: [join(dir, "missing")], directories: [] }), null);
      const real = join(dir, "real-chrome");
      const link = join(dir, "chromium-9", "chrome-linux", "chrome");
      writeFileSync(real, "");
      mkdirSync(dirname(link), { recursive: true });
      symlinkSync(real, link);
      assert.equal(gate.findChrome({ files: [], directories: [join(dir, "chromium-9")] }), link);
      const linux64 = join(dir, "chromium-1208", "chrome-linux64", "chrome");
      mkdirSync(dirname(linux64), { recursive: true });
      writeFileSync(linux64, "");
      assert.equal(gate.findChrome({ files: [], directories: [join(dir, "chromium-1208")] }), linux64);
      const mac = join(
        dir,
        "chromium-mac",
        "chrome-mac-arm64",
        "Google Chrome for Testing.app",
        "Contents",
        "MacOS",
        "Google Chrome for Testing",
      );
      mkdirSync(dirname(mac), { recursive: true });
      writeFileSync(mac, "");
      assert.equal(gate.findChrome({ files: [], directories: [join(dir, "chromium-mac")] }), mac);
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });
});
