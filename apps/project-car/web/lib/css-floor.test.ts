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

function targetPx(list: Rule[], names: string[]): number {
  let floor = 0;
  for (const rule of list) {
    if (!names.some((name) => parts(rule.selector).includes(name))) {
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
    const button = targetPx(parsed, [
      "button",
      ".button",
      "button::before",
      ".button::before",
      "button::after",
      ".button::after",
    ]);
    const link = targetPx(parsed, ["a", "a::before", "a::after"]);
    assert.ok(button >= 44, `button target is ${button}px`);
    assert.ok(link >= 44, `link target is ${link}px`);
  });
});
