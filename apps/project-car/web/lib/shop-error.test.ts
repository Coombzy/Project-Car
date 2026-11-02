import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { ShopApiError } from "./config.ts";
import { isMemberSessionError, isOwnerSessionError, shopErrorMessage } from "./shop-error.ts";

const FALLBACK = "Something went wrong talking to the shop API.";
const api = (status: number) => new ShopApiError(status, "code", `message ${status}`);
// Same keys as a ShopApiError, but not one: must never leak its message or log anyone out.
const lookalike = { status: 401, code: "ECONNREFUSED", message: "internal db host 10.0.0.5" };
const notApi: unknown[] = [new Error("boom"), "just a string", lookalike];

describe("shopErrorMessage", () => {
  it("returns the ShopApiError message, even with a custom fallback", () => {
    assert.equal(shopErrorMessage(api(404)), "message 404");
    assert.equal(shopErrorMessage(api(500), "custom"), "message 500");
  });

  it("returns the fallback for anything else", () => {
    for (const error of notApi) {
      assert.equal(shopErrorMessage(error), FALLBACK);
      assert.equal(shopErrorMessage(error, "custom"), "custom");
    }
  });
});

describe("session errors", () => {
  const cases: [number, boolean, boolean][] = [
    [401, true, true],
    [403, false, true],
    [404, false, false],
    [500, false, false],
  ];
  for (const [status, owner, member] of cases) {
    it(`ShopApiError ${status}: owner=${owner} member=${member}`, () => {
      assert.equal(isOwnerSessionError(api(status)), owner);
      assert.equal(isMemberSessionError(api(status)), member);
    });
  }

  it("anything that is not a ShopApiError is never a session error", () => {
    for (const error of notApi) {
      assert.equal(isOwnerSessionError(error), false);
      assert.equal(isMemberSessionError(error), false);
    }
  });
});
