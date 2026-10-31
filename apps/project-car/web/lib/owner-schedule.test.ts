import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const source = readFileSync(
  join(dirname(fileURLToPath(import.meta.url)), "../components/owner-lane-grid.tsx"),
  "utf8",
);

describe("owner schedule", () => {
  it("shows every hour on a wide screen and keeps this day's visits", () => {
    assert.match(source, /every hour/);
    assert.match(source, /length: 24/);
    assert.equal(source.includes("index + 6"), false);
    assert.match(source, /hour < 6/);
    const phoneAt = source.indexOf("@media (max-width: 767px)");
    assert.notEqual(phoneAt, -1);
    const phoneOnly = source.slice(phoneAt);
    assert.match(phoneOnly, /\.owner-lanes \.night \{ display: none; \}/);
    const beforePhone = source.slice(0, phoneAt);
    assert.equal(beforePhone.includes(".owner-lanes .night { display: none; }"), false);
    const wide = source.slice(source.indexOf("@media (min-width: 768px)"));
    assert.equal(wide.includes(".owner-list { display: none; }"), false);
    assert.match(wide, /\.owner-grid \{ display: block; \}/);
  });
});
