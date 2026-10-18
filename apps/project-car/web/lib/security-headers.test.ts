import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { createRequire, stripTypeScriptTypes } from "node:module";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath, pathToFileURL } from "node:url";

import { NextRequest } from "next/server.js";

import { SECURITY_HEADERS } from "./security-headers.ts";
import { CUSTOMER_HOST_OPS_LOGIN } from "./request-origin.ts";

const webRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const require = createRequire(join(webRoot, "package.json"));

const { pathToRegexp } = require("next/dist/compiled/path-to-regexp") as {
  pathToRegexp: (
    path: string,
    keys: unknown[],
    options: { strict: boolean; sensitive: boolean; delimiter: string },
  ) => { source: string };
};
const { normalizeRouteRegex } = require("next/dist/lib/load-custom-routes") as {
  normalizeRouteRegex: (regex: string) => string;
};
const { modifyRouteRegex } = require("next/dist/lib/redirect-status") as {
  modifyRouteRegex: (regex: string) => string;
};

const REQUIRED_SECURITY_HEADERS = [
  ["X-Content-Type-Options", "nosniff"],
  ["Referrer-Policy", "strict-origin-when-cross-origin"],
  ["X-Frame-Options", "DENY"],
  ["Permissions-Policy", "camera=(), microphone=(), geolocation=()"],
] as const;

const COVERED_PATHS = ["/", "/login", "/schedule", "/member/schedule", "/manifest.webmanifest"];

type HeaderRule = {
  source: string;
  headers?: Array<{ key: string; value: string }>;
};

type MiddlewareResponse = {
  status: number;
  headers: Headers;
};

function loadTranspiled(relativePath: string): Promise<{
  default?: { headers?: () => Promise<HeaderRule[]> | HeaderRule[] };
  middleware?: (request: NextRequest) => MiddlewareResponse;
}> {
  const abs = join(webRoot, relativePath);
  const dir = dirname(abs);
  let code = stripTypeScriptTypes(readFileSync(abs, "utf8"), { mode: "strip" });
  code = code.replace(/from\s+["'](\.[^"']+)["']/g, (_match, spec: string) => {
    const target = /\.(?:[cm]?[jt]s|json)$/.test(spec) ? spec : `${spec}.ts`;
    return `from "${pathToFileURL(resolve(dir, target)).href}"`;
  });
  code = code.replaceAll(
    'from "next/server"',
    `from "${pathToFileURL(join(webRoot, "node_modules/next/server.js")).href}"`,
  );
  const outFile = join(mkdtempSync(join(tmpdir(), "shop-web-security-headers-")), "module.mjs");
  writeFileSync(outFile, code);
  return import(pathToFileURL(outFile).href);
}

function sourceMatches(source: string, pathname: string): boolean {
  const compiled = pathToRegexp(source, [], {
    strict: true,
    sensitive: false,
    delimiter: "/",
  });
  const regex = new RegExp(normalizeRouteRegex(modifyRouteRegex(compiled.source)));
  return regex.test(pathname);
}

function headersForPath(rules: HeaderRule[], pathname: string): Map<string, string> {
  const matched = new Map<string, string>();
  for (const rule of rules) {
    if (!sourceMatches(rule.source, pathname)) {
      continue;
    }
    for (const header of rule.headers ?? []) {
      matched.set(header.key.toLowerCase(), header.value);
    }
  }
  return matched;
}

function assertSecurityHeaders(headers: { get(name: string): string | null }, where: string): void {
  for (const header of SECURITY_HEADERS) {
    assert.equal(headers.get(header.key), header.value, `${where} ${header.key}`);
  }
}

function request(url: string, host: string): NextRequest {
  return new NextRequest(url, {
    headers: {
      host,
      "x-forwarded-host": host,
      "x-forwarded-proto": url.startsWith("https:") ? "https" : "http",
    },
  });
}

describe("shop web security headers", () => {
  it("test_shop_web_security_headers", async () => {
    assert.deepEqual(
      SECURITY_HEADERS.map((header) => [header.key, header.value]),
      REQUIRED_SECURITY_HEADERS.map((header) => [header[0], header[1]]),
    );

    const configModule = await loadTranspiled("next.config.ts");
    const headersFn = configModule.default?.headers;
    assert.equal(typeof headersFn, "function");
    const rules = await headersFn();
    assert.ok(Array.isArray(rules));
    for (const pathname of COVERED_PATHS) {
      const applied = headersForPath(rules, pathname);
      for (const header of SECURITY_HEADERS) {
        assert.equal(applied.get(header.key.toLowerCase()), header.value, `${pathname} ${header.key}`);
      }
    }

    const middlewareModule = await loadTranspiled("middleware.ts");
    assert.equal(typeof middlewareModule.middleware, "function");
    const middleware = middlewareModule.middleware;

    const ownerLogin = middleware(request("http://localhost:3000/schedule", "localhost:3000"));
    assert.equal(ownerLogin.status, 307);
    assert.equal(ownerLogin.headers.get("location"), "http://localhost:3000/login?next=%2Fschedule");
    assertSecurityHeaders(ownerLogin.headers, "owner login redirect");

    const memberLogin = middleware(request("http://localhost:3000/member/schedule", "localhost:3000"));
    assert.equal(memberLogin.status, 307);
    assert.equal(
      memberLogin.headers.get("location"),
      "http://localhost:3000/member/login?next=%2Fmember%2Fschedule",
    );
    assertSecurityHeaders(memberLogin.headers, "member login redirect");

    const customerHost = middleware(request("https://projectcar.ca/schedule", "projectcar.ca"));
    assert.equal(customerHost.status, 307);
    assert.equal(customerHost.headers.get("location"), CUSTOMER_HOST_OPS_LOGIN);
    assertSecurityHeaders(customerHost.headers, "customer host redirect");

    const manifest = middleware(request("http://localhost:3000/manifest.webmanifest", "localhost:3000"));
    assert.equal(manifest.status, 200);
    assert.equal(manifest.headers.get("location"), null);
  });
});
