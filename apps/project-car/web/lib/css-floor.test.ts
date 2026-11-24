import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const css = readFileSync(
  join(dirname(fileURLToPath(import.meta.url)), "..", "app", "globals.css"),
  "utf8",
);

type Rule = { selector: string; body: string };

const DENSE = [
  ".chip-actions",
  ".todo-cal-actions",
  ".nav",
  ".nav-secondary",
  ".view-toggle",
  ".parts-status-form",
  ".demo-banner-dismiss",
  ".hour-slot",
  ".density-chip",
];

function rules(source: string): Rule[] {
  return [...source.replace(/\/\*[\s\S]*?\*\//g, "").matchAll(/([^{}]+)\{([^{}]*)\}/g)].map(
    (match) => ({ selector: match[1].replace(/\s+/g, " ").trim(), body: match[2] }),
  );
}

function parts(selector: string): string[] {
  return selector.split(",").map((part) => part.trim());
}

function reachesPastFields(selector: string): boolean {
  return parts(selector).some((part) => {
    if (!part.includes(":focus-visible")) {
      return false;
    }
    const rest = part.replaceAll(":focus-visible", "").trim();
    return rest === "" || rest === "*" || !/^(input|select|textarea)$/.test(rest);
  });
}

function mentions(selector: string, dense: string): boolean {
  return new RegExp(`\\.${dense.slice(1)}(?![\\w-])`).test(selector);
}

function targetPx(list: Rule[], names: string[]): number {
  let floor = 0;
  for (const rule of list) {
    const selected = parts(rule.selector).filter((part) => !part.includes("::"));
    if (!names.some((name) => selected.includes(name))) {
      continue;
    }
    for (const prop of ["min-height", "min-block-size", "height"]) {
      const match = rule.body.match(new RegExp(`(?:^|;)\\s*${prop}\\s*:\\s*(\\d+(?:\\.\\d+)?)px\\b`));
      if (match) {
        floor = Math.max(floor, Number(match[1]));
      }
    }
  }
  return floor;
}

function optsOut(list: Rule[], dense: string): boolean {
  return list.some((rule) => {
    if (!mentions(rule.selector, dense)) {
      return false;
    }
    const pseudo = parts(rule.selector).some((part) => part.includes("::before") || part.includes("::after"));
    if (pseudo && /content\s*:\s*none/.test(rule.body)) {
      return true;
    }
    const minH = rule.body.match(/min-height\s*:\s*([^;]+)/);
    return minH !== null && /^(?:0|0px|auto|unset|min-content|max-content)$/.test(minH[1].trim());
  });
}

describe("AUD-043 focus and target floor", () => {
  const parsed = rules(css);

  it("test_aud_043_focus_visible_reaches_past_fields", () => {
    const rule = parsed.find((item) => reachesPastFields(item.selector));
    assert.ok(rule, "no :focus-visible rule applies beyond input, select, and textarea");
    assert.match(rule.body, /outline(?:-color)?\s*:[^;]*var\(--focus\)/);
    const width = rule.body.match(/outline(?:-width)?\s*:\s*(\d+(?:\.\d+)?)px/);
    assert.ok(width !== null && Number(width[1]) >= 2, "focus outline is under 2px");
  });

  it("test_aud_043_button_and_link_targets_are_at_least_44px", () => {
    const button = targetPx(parsed, ["button", ".button"]);
    const link = targetPx(parsed, ["a"]);
    assert.ok(button >= 44, `button target is ${button}px`);
    assert.ok(link >= 44, `link target is ${link}px`);
  });

  it("test_aud_043_dense_groups_opt_out_of_the_44px_floor", () => {
    const missed = DENSE.filter((dense) => !optsOut(parsed, dense));
    assert.deepEqual(missed, []);
  });

  it("test_aud_043_44px_floor_is_coarse_pointer_only", () => {
    const src = css.replace(/\/\*[\s\S]*?\*\//g, "");
    const at = src.search(/@media\s*\(\s*pointer\s*:\s*coarse\s*\)\s*\{/);
    assert.ok(at >= 0, "44px floor is not under @media (pointer: coarse)");
    let depth = 1, i = src.indexOf("{", at) + 1;
    for (; depth > 0; i++) depth += src[i] === "{" ? 1 : src[i] === "}" ? -1 : 0;
    const block = src.slice(src.indexOf("{", at) + 1, i - 1);
    assert.match(block, /a\s*,\s*button\s*,\s*\.button\s*\{[^}]*min-height\s*:\s*44px/);
    assert.match(block, /min-height\s*:\s*auto/);
    assert.deepEqual(DENSE.filter((dense) => !mentions(block, dense)), []);
    assert.doesNotMatch(`${src.slice(0, at)}${src.slice(i)}`, /min-height\s*:\s*44px/);
  });
});
