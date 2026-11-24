import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, it } from "node:test";

import { NextRequest } from "next/server.js";

import { EDGE_CLIENT_IP_HEADER, loginForwardHeaders } from "./login-forward.ts";

const webRoot = join(import.meta.dirname, "..");
/** Tests only. Production reads SHOP_PROXY_SECRET from the environment. */
const DUMMY_SECRET = "dummy-shop-proxy-secret";

function read(rel: string): string {
  return readFileSync(join(webRoot, rel), "utf8");
}

function functionBody(source: string, name: string): string {
  const marker = `export async function ${name}(`;
  const start = source.indexOf(marker);
  assert.notEqual(start, -1, `${name} is exported`);
  const next = source.indexOf("\nexport ", start + marker.length);
  return source.slice(start, next === -1 ? source.length : next);
}

describe("AUD-010", () => {
  it("builds both shop headers from a Next request with CF-Connecting-IP", () => {
    assert.equal(EDGE_CLIENT_IP_HEADER, "CF-Connecting-IP");
    for (const [ip, secret] of [
      ["203.0.113.44", DUMMY_SECRET],
      ["2001:db8::10", ` ${DUMMY_SECRET} `],
    ] as const) {
      const request = new NextRequest("https://ops.projectcar.ca/login", {
        headers: { "CF-Connecting-IP": ip },
      });
      assert.deepEqual(loginForwardHeaders(request, secret), {
        "X-Shop-Client-IP": ip,
        "X-Shop-Proxy-Secret": DUMMY_SECRET,
      });
    }
    const bare = new NextRequest("https://ops.projectcar.ca/login");
    assert.deepEqual(loginForwardHeaders(bare, "  "), {});
  });

  it("owner and member login actions send both headers", () => {
    const api = read("lib/shop-api.ts");
    for (const name of ["loginOwner", "loginMember"]) {
      const body = functionBody(api, name);
      assert.match(body, /forwardHeaders:\s*Record<string,\s*string>/);
      assert.match(body, /\.\.\.forwardHeaders/);
    }
    for (const [rel, call] of [
      ["app/login/actions.ts", "loginOwner"],
      ["app/member/login/actions.ts", "loginMember"],
    ] as const) {
      const source = read(rel);
      assert.match(
        source,
        /const forward = loginForwardHeaders\(\{ headers: await headers\(\) \}, process\.env\.SHOP_PROXY_SECRET \?\? ""\);/,
      );
      assert.match(source, new RegExp(`const token = await ${call}\\(email, password, forward\\);`));
      assert.equal(source.includes(DUMMY_SECRET), false, rel);
    }
    for (const rel of ["lib/login-forward.ts", "lib/shop-api.ts"]) {
      assert.equal(read(rel).includes(DUMMY_SECRET), false, rel);
    }
  });
});
