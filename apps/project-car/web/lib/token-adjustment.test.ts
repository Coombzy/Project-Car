import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const pagePath = join(dirname(fileURLToPath(import.meta.url)), "../app/members/[id]/page.tsx");

const HINT = "Whole or cents, e.g. 100 or -1.50";

function adjustmentForm(source: string): string {
  const action = source.indexOf("action={adjustTokensAction}");
  assert.notEqual(action, -1, "adjust tokens form is missing");
  const formStart = source.lastIndexOf("<form", action);
  assert.notEqual(formStart, -1, "adjust tokens form is unopened");
  const formEnd = source.indexOf("</form>", action);
  assert.notEqual(formEnd, -1, "adjust tokens form is unclosed");
  return source.slice(formStart, formEnd + "</form>".length);
}

function amountInput(form: string): string {
  const tags = form.match(/<input\b[^>]*>/g) ?? [];
  const tag = tags.find((item) => /\bname="amount"/.test(item));
  assert.ok(tag, "adjust tokens form has no amount input");
  return tag;
}

function attr(tag: string, name: string): string | null {
  const match = tag.match(new RegExp(`\\b${name}=(?:\\{([^}]*)\\}|"([^"]*)")`));
  if (!match) {
    return null;
  }
  return (match[1] ?? match[2] ?? "").trim();
}

function html5Pattern(raw: string): RegExp {
  return new RegExp(`^(?:${raw})$`, "u");
}

describe("owner token adjustment field", () => {
  it("test_token_adjustment_amount_uses_decimal_mode_and_cents_pattern", () => {
    const source = readFileSync(pagePath, "utf8");
    const form = adjustmentForm(source);
    const amount = amountInput(form);

    assert.equal(attr(amount, "inputMode"), "decimal", `amount inputMode must be decimal (tag: ${amount})`);
    assert.match(form, new RegExp(HINT.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")));
    assert.equal(attr(amount, "title"), HINT, "invalid values must surface the hint in the browser");

    const rawPattern = attr(amount, "pattern");
    assert.ok(rawPattern, `amount input has no pattern (tag: ${amount})`);
    const pattern = html5Pattern(rawPattern);
    assert.equal(pattern.test("100"), true, `pattern ${rawPattern} must accept 100`);
    assert.equal(pattern.test("-1.50"), true, `pattern ${rawPattern} must accept -1.50`);
    assert.equal(pattern.test("abc"), false, `pattern ${rawPattern} must reject abc`);
    assert.equal(pattern.test("1.005"), false, `pattern ${rawPattern} must reject 1.005`);

    assert.match(amount, /\brequired\b/);
    assert.match(form, /action=\{adjustTokensAction\}/);
    assert.match(form, />\s*Post adjustment\s*</);
  });
});
