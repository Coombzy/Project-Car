import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const webRoot = join(dirname(fileURLToPath(import.meta.url)), "..");
const specPath = join(webRoot, "visual/pages.spec.ts");
const calendarPath = join(webRoot, "components/week-hoist-calendars.tsx");

describe("owner schedule visual settle", () => {
  it("hour slots do not prefetch and the schedule shoot outlives the 800ms settle", () => {
    const spec = readFileSync(specPath, "utf8");
    assert.match(spec, /const MAX_LAYOUT_SHIFT = 0\.1;/);
    assert.match(spec, /const SETTLE_MS = 800;/);
    assert.match(spec, /await page\.waitForLoadState\("networkidle"\)/);
    assert.match(spec, /await page\.waitForTimeout\(SETTLE_MS\)/);
    assert.equal(spec.includes("maxDiffPixelRatio"), false);
    assert.match(spec, /if \(shot\.path === "\/schedule"\) \{\s*test\.setTimeout\(120_000\);/);

    const calendar = readFileSync(calendarPath, "utf8");
    const slotAt = calendar.indexOf("className={`hour-slot");
    assert.ok(slotAt >= 0, "hour-slot link is missing");
    assert.match(
      calendar.slice(slotAt, slotAt + 400),
      /prefetch=\{false\}/,
      "hour-slot links must not prefetch; each one is a distinct dynamic /schedule URL",
    );
  });
});
