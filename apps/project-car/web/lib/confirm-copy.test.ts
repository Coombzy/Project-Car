import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { grantConfirmText, multiplierConfirmText } from "./confirm-copy.ts";

describe("R125 confirm copy", () => {
  it("names a plural grant before it runs", () => {
    assert.equal(grantConfirmText(23, 400), "Grant 400 tokens to 23 active members?");
  });

  it("uses member when the grant count is one", () => {
    assert.equal(grantConfirmText(1, 100), "Grant 100 tokens to 1 active member?");
  });

  it("uses token when the grant amount is one", () => {
    assert.equal(grantConfirmText(23, 1), "Grant 1 token to 23 active members?");
  });

  it("uses token and member when both counts are one", () => {
    assert.equal(grantConfirmText(1, 1), "Grant 1 token to 1 active member?");
  });

  it("names both multiplier values before the change", () => {
    assert.equal(multiplierConfirmText(1, 1.2), "Change the multiplier from 1 to 1.2?");
  });
});
