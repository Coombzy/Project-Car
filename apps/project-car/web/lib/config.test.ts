import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { ShopApiError, parseApiError, shopApiUrl } from "./config.ts";

const DEFAULT_SHOP_API_URL = "http://127.0.0.1:8000";

// Each case sets SHOP_API_URL and puts the previous value back, including when it was unset.
function withShopApiUrl(value: string | undefined, run: () => void): void {
  const previous = process.env.SHOP_API_URL;
  try {
    if (value === undefined) {
      delete process.env.SHOP_API_URL;
    } else {
      process.env.SHOP_API_URL = value;
    }
    run();
  } finally {
    if (previous === undefined) {
      delete process.env.SHOP_API_URL;
    } else {
      process.env.SHOP_API_URL = previous;
    }
  }
}

function shopApiUrlFor(value: string | undefined): string {
  const previous = process.env.SHOP_API_URL;
  let actual = "";
  withShopApiUrl(value, () => {
    actual = shopApiUrl();
  });
  assert.equal(process.env.SHOP_API_URL, previous);
  return actual;
}

describe("shopApiUrl", () => {
  it("test_shop_api_url_empty_falls_back_to_the_default", () => {
    const base = shopApiUrlFor("");
    assert.deepEqual(
      {
        base,
        hoists: `${base}/hoists`,
        // A value that is only slashes is empty once trailing slashes are removed.
        slashOnly: shopApiUrlFor("/"),
        slashes: shopApiUrlFor("///"),
      },
      {
        base: DEFAULT_SHOP_API_URL,
        hoists: `${DEFAULT_SHOP_API_URL}/hoists`,
        slashOnly: DEFAULT_SHOP_API_URL,
        slashes: DEFAULT_SHOP_API_URL,
      },
    );
  });

  it("test_shop_api_url_whitespace_falls_back_to_the_default", () => {
    const blanks = [" ", "   ", "\n", "\t", "\n\t", " \t\n "];
    const actual = Object.fromEntries(
      blanks.map((value) => [JSON.stringify(value), shopApiUrlFor(value)]),
    );
    const expected = Object.fromEntries(
      blanks.map((value) => [JSON.stringify(value), DEFAULT_SHOP_API_URL]),
    );
    assert.deepEqual(actual, expected);
  });

  it("test_shop_api_url_strips_every_trailing_slash", () => {
    const doubled = shopApiUrlFor("http://host:8000//");
    assert.deepEqual(
      {
        doubled,
        hoists: `${doubled}/hoists`,
        tripled: shopApiUrlFor("http://host:8000///"),
        path: shopApiUrlFor("http://host:8000/shop//"),
      },
      {
        doubled: "http://host:8000",
        hoists: "http://host:8000/hoists",
        tripled: "http://host:8000",
        path: "http://host:8000/shop",
      },
    );
  });

  it("test_shop_api_url_trims_surrounding_spaces", () => {
    assert.deepEqual(
      {
        paddedDefault: shopApiUrlFor("  http://127.0.0.1:8000  "),
        paddedSlashes: shopApiUrlFor("  http://host:8000//  "),
        tabs: shopApiUrlFor("\thttp://10.1.2.3:9000\n"),
      },
      {
        paddedDefault: DEFAULT_SHOP_API_URL,
        paddedSlashes: "http://host:8000",
        tabs: "http://10.1.2.3:9000",
      },
    );
  });

  it("test_shop_api_url_real_value_and_ci_default_stay", () => {
    // One trailing slash already worked on main. Keep that, and do not touch a real value.
    assert.deepEqual(
      {
        unset: shopApiUrlFor(undefined),
        ci: shopApiUrlFor("http://127.0.0.1:8000"),
        oneSlash: shopApiUrlFor("http://127.0.0.1:8000/"),
        pathOneSlash: shopApiUrlFor("http://host:8000/shop/"),
        host: shopApiUrlFor("http://10.1.2.3:9000"),
        path: shopApiUrlFor("https://api.example:8443/shop"),
      },
      {
        unset: DEFAULT_SHOP_API_URL,
        ci: "http://127.0.0.1:8000",
        oneSlash: DEFAULT_SHOP_API_URL,
        pathOneSlash: "http://host:8000/shop",
        host: "http://10.1.2.3:9000",
        path: "https://api.example:8443/shop",
      },
    );
  });
});

describe("parseApiError", () => {
  it("test_parse_api_error_reads_the_error_envelope", () => {
    const error = parseApiError(
      404,
      { error: { code: "not_found", message: "Hoist is missing." } },
      "Request failed.",
    );
    assert.equal(error.status, 404);
    assert.equal(error.code, "not_found");
    assert.equal(error.message, "Hoist is missing.");
    assert.equal(error.name, "ShopApiError");
    assert.ok(error instanceof ShopApiError);
    assert.ok(error instanceof Error);
  });

  it("test_parse_api_error_body_with_no_error_uses_the_fallback", () => {
    const missing = parseApiError(500, { detail: "nope" }, "Shop API failed.");
    const empty = parseApiError(500, {}, "Shop API failed.");
    assert.deepEqual(
      { status: missing.status, code: missing.code, message: missing.message, name: missing.name },
      { status: 500, code: "http_error", message: "Shop API failed.", name: "ShopApiError" },
    );
    assert.deepEqual(
      { status: empty.status, code: empty.code, message: empty.message },
      { status: 500, code: "http_error", message: "Shop API failed." },
    );
  });

  it("test_parse_api_error_null_body_uses_the_fallback", () => {
    const error = parseApiError(503, null, "Cannot reach shop API.");
    assert.equal(error.status, 503);
    assert.equal(error.code, "http_error");
    assert.equal(error.message, "Cannot reach shop API.");
    assert.equal(error.name, "ShopApiError");
  });

  it("test_parse_api_error_non_object_body_uses_the_fallback", () => {
    const fromString = parseApiError(502, "upstream exploded", "Shop API failed.");
    const fromNumber = parseApiError(502, 0, "Shop API failed.");
    assert.deepEqual(
      {
        status: fromString.status,
        code: fromString.code,
        message: fromString.message,
        name: fromString.name,
      },
      { status: 502, code: "http_error", message: "Shop API failed.", name: "ShopApiError" },
    );
    assert.deepEqual(
      { status: fromNumber.status, code: fromNumber.code, message: fromNumber.message },
      { status: 502, code: "http_error", message: "Shop API failed." },
    );
  });
});

describe("ShopApiError", () => {
  it("test_shop_api_error_fields", () => {
    const error = new ShopApiError(409, "conflict", "That hour is taken.");
    assert.equal(error.status, 409);
    assert.equal(error.code, "conflict");
    assert.equal(error.message, "That hour is taken.");
    assert.equal(error.name, "ShopApiError");
    assert.ok(error instanceof Error);
    assert.ok(error instanceof ShopApiError);
  });
});
