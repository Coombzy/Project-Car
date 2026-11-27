import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, it } from "node:test";

const webRoot = join(import.meta.dirname, "..");

function read(rel: string): string {
  return readFileSync(join(webRoot, rel), "utf8");
}

function functionBody(source: string, name: string): string {
  const marker = `function ${name}`;
  const start = source.indexOf(marker);
  assert.notEqual(start, -1, `${name} is defined`);
  const rest = source.slice(start + marker.length);
  const boundary = rest.search(/\n(?:export )?(?:async )?function /);
  const end = boundary === -1 ? source.length : start + marker.length + boundary;
  return source.slice(start, end);
}

const HELPER_SIGNAL = /signal:\s*init\.signal\s*\?\?\s*AbortSignal\.timeout\(\s*10_000\s*\)/;
const LOGIN_SIGNAL = /signal:\s*AbortSignal\.timeout\(\s*10_000\s*\)/;
const CANNOT_REACH =
  /parseApiError\(\s*503,\s*null,\s*`Cannot reach shop API at \$\{shopApiUrl\(\)\}\.`\s*\)/;

describe("AUD-049", () => {
  it("all four fetch sites pass a 10s abort signal", () => {
    const api = read("lib/shop-api.ts");
    assert.equal((api.match(/fetch\s*\(/g) ?? []).length, 4);

    for (const name of ["shopFetch", "memberFetch"] as const) {
      const body = functionBody(api, name);
      assert.equal((body.match(/fetch\s*\(/g) ?? []).length, 1, name);
      assert.match(body, HELPER_SIGNAL, name);
    }

    for (const name of ["loginOwner", "loginMember"] as const) {
      const body = functionBody(api, name);
      assert.equal((body.match(/fetch\s*\(/g) ?? []).length, 1, name);
      assert.match(body, LOGIN_SIGNAL, name);
      assert.match(body, /forwardHeaders:\s*Record<string,\s*string>/);
      assert.match(body, /\.\.\.forwardHeaders/);
    }
  });

  it("abort and network failures still map to parseApiError 503 cannot-reach", () => {
    const api = read("lib/shop-api.ts");
    for (const name of ["shopJson", "memberJson", "loginOwner", "loginMember"] as const) {
      assert.match(functionBody(api, name), CANNOT_REACH, name);
    }
  });
});
