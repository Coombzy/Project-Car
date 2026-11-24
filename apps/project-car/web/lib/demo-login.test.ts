import assert from "node:assert/strict";
import { afterEach, test } from "node:test";

import { showDemoLoginHints } from "./demo-login.ts";

afterEach(() => {
  delete process.env.SHOP_DEMO_LOGIN_HINTS;
});

test("showDemoLoginHints is true only when SHOP_DEMO_LOGIN_HINTS=true", () => {
  const previousNodeEnv = process.env.NODE_ENV;
  delete process.env.SHOP_DEMO_LOGIN_HINTS;
  try {
    process.env.NODE_ENV = "production";
    assert.equal(showDemoLoginHints(), false);
    process.env.NODE_ENV = "development";
    assert.equal(showDemoLoginHints(), false);
    process.env.SHOP_DEMO_LOGIN_HINTS = "1";
    assert.equal(showDemoLoginHints(), false);
    process.env.SHOP_DEMO_LOGIN_HINTS = "true";
    assert.equal(showDemoLoginHints(), true);
  } finally {
    if (previousNodeEnv === undefined) delete process.env.NODE_ENV;
    else process.env.NODE_ENV = previousNodeEnv;
  }
});
