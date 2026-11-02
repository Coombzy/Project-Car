/**
 * UI proof browser gate.
 *
 * Missing Chrome/Chromium prints SKIPPED and exits 0, including when CI=true.
 * A found browser runs `playwright test` from apps/project-car/web.
 */
import { spawnSync } from "node:child_process";
import { existsSync, readdirSync, statSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const CHROME_FILE_NAMES = new Set([
  "chrome",
  "chromium",
  "chrome.exe",
  "Chromium",
  "google-chrome",
  "google-chrome-stable",
]);

const MAX_WALK_DEPTH = 8;

export const SYSTEM_CHROME_CANDIDATES = [
  "/usr/local/bin/google-chrome",
  "/usr/local/bin/google-chrome-stable",
  "/usr/local/bin/chromium",
  "/usr/local/bin/chromium-browser",
  "/usr/bin/google-chrome",
  "/usr/bin/google-chrome-stable",
  "/usr/bin/chromium",
  "/usr/bin/chromium-browser",
  "/opt/google/chrome/chrome",
  "/snap/bin/chromium",
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "/Applications/Chromium.app/Contents/MacOS/Chromium",
] as const;

type Env = {
  CI?: string;
  HOME?: string;
  USERPROFILE?: string;
  LOCALAPPDATA?: string;
  PLAYWRIGHT_BROWSERS_PATH?: string;
  UI_PROOF_CHROME_PATHS?: string;
};

export type SearchPlan = {
  files: string[];
  directories: string[];
};

function isRegularFile(path: string): boolean {
  try {
    return statSync(path).isFile();
  } catch {
    return false;
  }
}

function homeDir(env: Env): string {
  return env.HOME || env.USERPROFILE || homedir();
}

export function playwrightCacheRoots(env: Env, platform: string, home: string): string[] {
  const roots: string[] = [];
  const browsers = env.PLAYWRIGHT_BROWSERS_PATH;
  if (browsers && browsers !== "0") {
    roots.push(browsers);
  }
  if (platform === "darwin") {
    roots.push(join(home, "Library", "Caches", "ms-playwright"));
    return roots;
  }
  if (platform === "win32") {
    const local = env.LOCALAPPDATA || join(home, "AppData", "Local");
    roots.push(join(local, "ms-playwright"));
    return roots;
  }
  roots.push(join(home, ".cache", "ms-playwright"));
  return roots;
}

export function searchPlan(env: Env, platform: string = process.platform): SearchPlan {
  const override = env.UI_PROOF_CHROME_PATHS;
  if (override !== undefined) {
    return {
      files: override.split(":").filter((path) => path.length > 0),
      directories: [],
    };
  }
  const home = homeDir(env);
  return {
    files: [
      ...SYSTEM_CHROME_CANDIDATES,
      join(home, "Applications", "Google Chrome.app", "Contents", "MacOS", "Google Chrome"),
    ],
    directories: playwrightCacheRoots(env, platform, home),
  };
}

function walkChrome(root: string, depth: number): string | null {
  if (depth > MAX_WALK_DEPTH) {
    return null;
  }
  let entries;
  try {
    entries = readdirSync(root, { withFileTypes: true });
  } catch {
    return null;
  }
  for (const entry of entries) {
    if (entry.name === "node_modules") {
      continue;
    }
    const full = join(root, entry.name);
    if (entry.isDirectory()) {
      const nested = walkChrome(full, depth + 1);
      if (nested) {
        return nested;
      }
      continue;
    }
    if (entry.isFile() && CHROME_FILE_NAMES.has(entry.name)) {
      return full;
    }
  }
  return null;
}

export function findChrome(plan: SearchPlan): string | null {
  for (const file of plan.files) {
    if (isRegularFile(file)) {
      return file;
    }
  }
  for (const directory of plan.directories) {
    if (!existsSync(directory)) {
      continue;
    }
    const found = walkChrome(directory, 0);
    if (found) {
      return found;
    }
  }
  return null;
}

export function pathsSearched(plan: SearchPlan): string[] {
  return [...plan.files, ...plan.directories];
}

function repoRoot(): string {
  return join(dirname(fileURLToPath(import.meta.url)), "..");
}

function runVisual(): number {
  const webRoot = join(repoRoot(), "apps", "project-car", "web");
  const playwrightBin = join(webRoot, "node_modules", ".bin", "playwright");
  if (!existsSync(playwrightBin)) {
    process.stderr.write(
      `Chrome/Chromium was found, but ${playwrightBin} is missing. Run npm ci in apps/project-car/web.\n`,
    );
    return 1;
  }
  const result = spawnSync(playwrightBin, ["test"], {
    cwd: webRoot,
    stdio: "inherit",
    env: process.env,
  });
  return result.status ?? 1;
}

function invokedDirectly(): boolean {
  const entry = process.argv[1];
  if (!entry) {
    return false;
  }
  return pathToFileURL(resolve(entry)).href === import.meta.url;
}

function main(): number {
  const env = process.env as Env;
  const plan = searchPlan(env);
  const found = findChrome(plan);
  if (!found) {
    process.stdout.write("SKIPPED\n");
    return 0;
  }
  return runVisual();
}

if (invokedDirectly()) {
  process.exit(main());
}
