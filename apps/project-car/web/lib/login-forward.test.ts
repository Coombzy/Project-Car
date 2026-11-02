import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { loginForwardHeaders } from "./login-forward.ts";

function headers(values: Record<string, string>): { get(name: string): string | null } {
  return {
    get(name: string) {
      return values[name.toLowerCase()] ?? null;
    },
  };
}

describe("loginForwardHeaders", () => {
  it("sends the Cloudflare IP with the proxy secret", () => {
    const forwarded = loginForwardHeaders(headers({ "cf-connecting-ip": "203.0.113.10" }), {
      SHOP_PROXY_SECRET: "p".repeat(32),
    });
    assert.deepEqual(forwarded, {
      "X-Shop-Client-IP": "203.0.113.10",
      "X-Shop-Proxy-Secret": "p".repeat(32),
    });
  });

  it("sends nothing without the secret", () => {
    const forwarded = loginForwardHeaders(headers({ "cf-connecting-ip": "203.0.113.10" }), {});
    assert.deepEqual(forwarded, {});
  });

  it("sends nothing without a client IP", () => {
    const forwarded = loginForwardHeaders(headers({}), { SHOP_PROXY_SECRET: "p".repeat(32) });
    assert.deepEqual(forwarded, {});
  });
});
