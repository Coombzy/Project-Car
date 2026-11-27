import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

/** PC #282 part 11. On main these six screens still say America/Regina. */
const root = join(dirname(fileURLToPath(import.meta.url)), "..");

const screens = [
  "app/fill/page.tsx",
  "app/member/schedule/page.tsx",
  "app/page.tsx",
  "app/tiers/page.tsx",
  "components/create-booking-form.tsx",
  "components/member-booking-form.tsx",
] as const;

function source(rel: string): string {
  return readFileSync(join(root, rel), "utf8");
}

describe("PC282 part 11 Mountain Time labels", () => {
  it("six screens say Mountain Time", () => {
    const missing = screens.filter((rel) => !source(rel).includes("Mountain Time"));
    assert.deepEqual(missing, []);
  });
});
