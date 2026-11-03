import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const source = readFileSync(
  join(dirname(fileURLToPath(import.meta.url)), "../components/schedule-toolbar.tsx"),
  "utf8",
);

function thisWeekHref(toolbar: string): string {
  const label = toolbar.indexOf("This week");
  assert.notEqual(label, -1, "This week control is missing");
  const open = toolbar.lastIndexOf("<Link", label);
  const href = toolbar.slice(open, label).match(/href=\{(scheduleHref\([^)]*\))\}/);
  assert.ok(href, "This week link has no href");
  return href[1];
}

describe("schedule toolbar", () => {
  it("opens the current week from This week", () => {
    const href = thisWeekHref(source);
    assert.equal(href, 'scheduleHref(base, { view: "week", month })');
    assert.equal(href.includes("weekStart"), false);
    assert.equal(href.includes("view,"), false);
  });
});
