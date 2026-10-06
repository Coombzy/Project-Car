import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const pagePath = join(dirname(fileURLToPath(import.meta.url)), "../app/tiers/page.tsx");

const SEEDED_LEDE =
  "Basic and Premium are seeded placeholders — names and allowances are data. These are not live prices. The shop is not open.";

function ledeText(source: string): string {
  const match = source.match(/<p className="lede">([\s\S]*?)<\/p>/);
  assert.ok(match, "tiers page is missing the lede");
  return match[1].replace(/\s+/g, " ").trim();
}

describe("tiers page copy", () => {
  it("test_tiers_copy_names_basic_and_premium", () => {
    const source = readFileSync(pagePath, "utf8");
    const retired = ["Pro", "Weekly"].filter((name) => new RegExp(`\\b${name}\\b`).test(source));
    assert.deepEqual(retired, [], `tiers page still names retired tiers: ${retired.join(", ")}`);
    assert.equal(ledeText(source), SEEDED_LEDE);
    assert.match(source, /name="price"/);
    assert.match(source, /name="included_tokens"/);
    assert.match(source, /name="booking_window_days"/);
    assert.match(source, /name="max_simultaneous_bookings"/);
    assert.match(source, /name="notes"/);
  });
});
