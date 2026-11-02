import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const webRoot = join(dirname(fileURLToPath(import.meta.url)), "..");
const page = readFileSync(join(webRoot, "app/members/[id]/page.tsx"), "utf8");
const actions = readFileSync(join(webRoot, "app/members/actions.ts"), "utf8");

describe("manual token change", () => {
  it("requires a reason and sends it with the adjustment", () => {
    const formStart = page.indexOf("action={adjustTokensAction}");
    const form = page.slice(page.lastIndexOf("<form", formStart), page.indexOf("</form>", formStart));
    assert.match(form, /name="reason"/);
    assert.match(form, /required/);
    assert.match(actions, /formData\.get\("reason"\)/);
    assert.match(actions, /reason/);
  });
});
