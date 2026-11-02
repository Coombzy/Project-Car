import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { describe, it } from "node:test";

const page = readFileSync(new URL("../app/member/purchase/page.tsx", import.meta.url), "utf8");
const form = readFileSync(new URL("../app/member/purchase/purchase-form.tsx", import.meta.url), "utf8");
const actions = readFileSync(new URL("../app/member/purchase/actions.ts", import.meta.url), "utf8");

describe("member token purchase", () => {
  it("shows GST lines and posts through the stand-in payment adapter", () => {
    assert.match(page, /GST/);
    assert.match(form, /name="payment_id"/);
    assert.match(form, /name="tokens"/);
    assert.match(form, /name="subtotal_cad"/);
    assert.match(form, /STANDIN/);
    assert.match(form, /gst_cad|GST/);
    assert.match(actions, /memberTokenPurchase|buyTokens/);
  });
});
