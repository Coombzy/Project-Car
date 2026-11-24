import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { test } from "node:test";
import assert from "node:assert/strict";

const visualDir = dirname(fileURLToPath(import.meta.url));
const webRoot = dirname(visualDir);

test("start-api.sh exports SHOP_DEV_MODE defaulting to 1", () => {
  const sh = readFileSync(join(visualDir, "start-api.sh"), "utf8");
  assert.match(
    sh,
    /export SHOP_DEV_MODE="\$\{SHOP_DEV_MODE:-1\}"|export SHOP_DEV_MODE=1\b/,
  );
});

test("playwright API webServer env sets SHOP_DEV_MODE=1", () => {
  const cfg = readFileSync(join(webRoot, "playwright.config.ts"), "utf8");
  const apiAt = cfg.indexOf("bash visual/start-api.sh");
  assert.ok(apiAt >= 0, "API webServer command missing");
  const apiBlock = cfg.slice(apiAt);
  const nextAt = apiBlock.indexOf("npx next start");
  const apiOnly = nextAt === -1 ? apiBlock : apiBlock.slice(0, nextAt);
  assert.match(apiOnly, /SHOP_DEV_MODE:\s*"1"/);
});
