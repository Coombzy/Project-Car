import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const webRoot = join(dirname(fileURLToPath(import.meta.url)), "..");

function readComponent(name: string): string {
  return readFileSync(join(webRoot, "components", name), "utf8");
}

function assertLabeledNav(source: string, label: string, className: string): void {
  const nav = source.match(new RegExp(`<nav\\b[^>]*aria-label="${label}"[^>]*>`));
  assert.ok(nav, `missing <nav aria-label="${label}">`);
  assert.match(nav[0], new RegExp(`className="${className}"`));
  assert.equal(nav[0].includes("tablist"), false, `${label} nav still names a tablist`);
}

describe("AUD-037 schedule and tools nav", () => {
  it("test_aud_037_view_toggles_are_navs_not_tablists", () => {
    const schedule = readComponent("schedule-toolbar.tsx");
    const tools = readComponent("inventory-kit-nav.tsx");

    for (const source of [schedule, tools]) {
      assert.equal(source.includes('role="tablist"'), false, 'role="tablist" wraps plain links');
      assert.equal(source.includes("role='tablist'"), false, "role='tablist' wraps plain links");
      assert.equal(source.includes('role="tab"'), false, "links must stay links, not role=tab");
    }

    assertLabeledNav(schedule, "Schedule view", "view-toggle");
    assert.match(schedule, /aria-current=\{view === "month" \? "page" : undefined\}/);
    assert.match(schedule, /aria-current=\{view === "week" \? "page" : undefined\}/);

    assertLabeledNav(tools, "Tool inventory", "view-toggle");
    assertLabeledNav(tools, "Bay kit", "view-toggle kit-bay-toggle");
    assert.match(tools, /aria-current=\{current !== CRIB_PREFIX \? "page" : undefined\}/);
    assert.match(tools, /aria-current=\{current === CRIB_PREFIX \? "page" : undefined\}/);
    assert.match(tools, /aria-current=\{current === bay \? "page" : undefined\}/);
  });
});
