import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const webRoot = join(dirname(fileURLToPath(import.meta.url)), "..");
const page = readFileSync(join(webRoot, "app/members/[id]/page.tsx"), "utf8");
const actions = readFileSync(join(webRoot, "app/members/actions.ts"), "utf8");

describe("owner records a signup's money and sign-in", () => {
  it("records a stand-in token purchase with GST and sets a sign-in password", () => {
    assert.match(page, /name="payment_id"/);
    assert.match(page, /name="tokens"/);
    assert.match(page, /name="subtotal_cad"/);
    assert.match(page, /GST/);
    assert.match(page, /STANDIN/);
    assert.match(page, /name="password"/);
    assert.match(page, /minLength=\{12\}/);
    assert.match(actions, /recordTokenPurchase/);
    assert.match(actions, /setMemberPassword/);
  });
});
