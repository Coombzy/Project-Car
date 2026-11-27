import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, it } from "node:test";
import { pathSegment } from "./shop-path.ts";

const shopApiPath = join(dirname(fileURLToPath(import.meta.url)), "shop-api.ts");

describe("pathSegment", () => {
  it("keeps a UUID and a plain tier name the same", () => {
    const id = "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11";
    assert.equal(pathSegment(id), id);
    assert.equal(pathSegment(id), encodeURIComponent(id));
    assert.equal(pathSegment("Weekend"), "Weekend");
    assert.equal(pathSegment("Weekend"), encodeURIComponent("Weekend"));
  });

  it("encodes reserved characters as one segment", () => {
    assert.equal(pathSegment("a b"), "a%20b");
    assert.equal(pathSegment("a/b"), "a%2Fb");
    assert.equal(pathSegment("a?b"), "a%3Fb");
    assert.equal(pathSegment("a#b"), "a%23b");
    assert.equal(pathSegment("100%"), "100%25");
    assert.equal(pathSegment("../x"), "..%2Fx");
  });

  it("throws on empty, dot, and dot-dot", () => {
    for (const value of ["", ".", ".."]) {
      assert.throws(() => pathSegment(value), {
        name: "Error",
        message: "Bad path segment.",
      });
    }
  });
});

describe("shop-api request paths", () => {
  it("does not interpolate a raw id or name segment", () => {
    const source = readFileSync(shopApiPath, "utf8");
    assert.match(source, /\/tiers\/\$\{pathSegment\(name\)\}/);
    assert.match(source, /\/members\/\$\{pathSegment\(id\)\}/);
    assert.match(source, /\/bookings\/\$\{pathSegment\(id\)\}\/cancel/);
    assert.equal(source.match(/\/\$\{(?:id|name)\}/g), null);
  });
});
