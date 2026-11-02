import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const webRoot = join(dirname(fileURLToPath(import.meta.url)), "..");
const cardPath = join(webRoot, "components/owner-booking-card.tsx");
const actionsPath = join(webRoot, "app/schedule/actions.ts");

function activeCompleteForm(source: string): string {
  const branch = source.indexOf('booking.status === "active"');
  assert.notEqual(branch, -1, "active booking branch is missing");
  const formStart = source.indexOf("<form", branch);
  assert.notEqual(formStart, -1, "active booking has no complete form");
  const formEnd = source.indexOf("</form>", formStart);
  assert.notEqual(formEnd, -1, "active complete form is unclosed");
  return source.slice(formStart, formEnd + "</form>".length);
}

function inputTag(form: string, name: string): string {
  const tags = form.match(/<input\b[^>]*>/g) ?? [];
  const tag = tags.find((item) => new RegExp(`\\bname="${name}"`).test(item));
  assert.ok(tag, `complete form has no ${name} input`);
  return tag;
}

function attr(tag: string, name: string): string | null {
  const match = tag.match(new RegExp(`\\b${name}=(?:\\{([^}]*)\\}|"([^"]*)")`));
  if (!match) {
    return null;
  }
  return (match[1] ?? match[2] ?? "").trim();
}

describe("owner complete booking", () => {
  it("test_complete_card_posts_zero_unused_tokens", () => {
    const card = readFileSync(cardPath, "utf8");
    const form = activeCompleteForm(card);
    const unused = inputTag(form, "unused_tokens");

    assert.equal(attr(unused, "type"), "hidden", `unused tokens must be pinned at 0 (tag: ${unused})`);
    assert.equal(attr(unused, "value"), "0", "complete must post unused_tokens 0");
    assert.equal(attr(unused, "defaultValue"), null, "unused tokens must not be an editable default");
    assert.equal(attr(unused, "max"), null, "unused tokens must not offer the reserve as a max");
    assert.doesNotMatch(unused, /reserved_tokens/);
    assert.doesNotMatch(form, /type="number"/);
    assert.doesNotMatch(form, /Unused/);
    assert.match(form, /action=\{completeBookingAction\}/);
    assert.match(form, />\s*Complete\s*</);

    const cancelAt = card.indexOf("action={cancelBookingAction}");
    assert.notEqual(cancelAt, -1, "cancel action is missing");
    const cancelFormStart = card.lastIndexOf("<form", cancelAt);
    const cancelFormEnd = card.indexOf("</form>", cancelAt);
    const cancelForm = card.slice(cancelFormStart, cancelFormEnd);
    assert.equal(cancelForm.includes('name="unused_tokens"'), false, "cancel must not post unused tokens");
    assert.match(cancelForm, />\s*Cancel\s*</);

    const actions = readFileSync(actionsPath, "utf8");
    const completeAt = actions.indexOf("function completeBookingAction");
    assert.notEqual(completeAt, -1, "completeBookingAction is missing");
    const completeFn = actions.slice(completeAt, actions.indexOf("export async function", completeAt + 1));
    assert.match(completeFn, /formData\.get\("unused_tokens"\)/);
    assert.match(completeFn, /completeBooking\(/);
  });
});
