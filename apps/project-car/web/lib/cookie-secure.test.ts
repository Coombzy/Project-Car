import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { createRequire, stripTypeScriptTypes } from "node:module";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath, pathToFileURL } from "node:url";

import { cookieSecure } from "./cookie-secure.ts";

const require = createRequire(fileURLToPath(import.meta.url));
const { ResponseCookies } = require("next/dist/compiled/@edge-runtime/cookies/index.js") as {
  ResponseCookies: new (headers: Headers) => {
    set(options: { name: string; value: string; path?: string; secure?: boolean }): unknown;
    delete(nameOrOptions: string | { name: string; path?: string; secure?: boolean }): unknown;
  };
};

const libDir = dirname(fileURLToPath(import.meta.url));

type CookieCall = {
  op: "set" | "delete";
  arg: unknown;
};

type SessionCookies = {
  writeSessionCookie: (value: string, maxAge?: number) => Promise<void>;
  clearSessionCookie: () => Promise<void>;
  writeMemberSessionCookie: (value: string, maxAge?: number) => Promise<void>;
  clearMemberSessionCookie: () => Promise<void>;
  calls: CookieCall[];
};

function loadSession(): Promise<SessionCookies> {
  const dir = mkdtempSync(join(tmpdir(), "cookie-secure-delete-"));
  const sinkUrl = pathToFileURL(join(dir, "cookies-sink.mjs")).href;
  writeFileSync(
    join(dir, "cookies-sink.mjs"),
    [
      "export const calls = [];",
      "export async function cookies() {",
      "  return {",
      "    get() { return undefined; },",
      "    set(arg) { calls.push({ op: 'set', arg }); },",
      "    delete(arg) { calls.push({ op: 'delete', arg }); },",
      "  };",
      "}",
      "",
    ].join("\n"),
  );
  let code = stripTypeScriptTypes(readFileSync(join(libDir, "session.ts"), "utf8"), { mode: "strip" });
  code = code.replace(/from\s+["']next\/headers["']/, `from ${JSON.stringify(sinkUrl)}`);
  code = code.replace(/from\s+["'](\.[^"']+)["']/g, (_match, spec: string) => {
    const target = /\.(?:[cm]?[jt]s)$/.test(spec) ? spec : `${spec}.ts`;
    return `from ${JSON.stringify(pathToFileURL(resolve(libDir, target)).href)}`;
  });
  const outFile = join(dir, "session.mjs");
  writeFileSync(outFile, code);
  return import(pathToFileURL(outFile).href).then(async (mod) => {
    const sink = (await import(sinkUrl)) as { calls: CookieCall[] };
    return {
      writeSessionCookie: mod.writeSessionCookie,
      clearSessionCookie: mod.clearSessionCookie,
      writeMemberSessionCookie: mod.writeMemberSessionCookie,
      clearMemberSessionCookie: mod.clearMemberSessionCookie,
      calls: sink.calls,
    };
  });
}

function headerFor(call: CookieCall): string {
  const headers = new Headers();
  const jar = new ResponseCookies(headers);
  if (call.op === "set") {
    jar.set(call.arg as { name: string; value: string; path?: string; secure?: boolean });
  } else if (typeof call.arg === "string") {
    jar.delete(call.arg);
  } else {
    jar.delete(call.arg as { name: string; path?: string; secure?: boolean });
  }
  const lines = headers.getSetCookie();
  assert.equal(lines.length, 1);
  return lines[0] ?? "";
}

function cookieShape(header: string): {
  name: string;
  path: string | undefined;
  secure: boolean;
  expiresMs: number | null;
} {
  const [pair, ...attrs] = header.split(";").map((part) => part.trim());
  const eq = pair.indexOf("=");
  assert.notEqual(eq, -1);
  const name = pair.slice(0, eq);
  let path: string | undefined;
  let secure = false;
  let expiresMs: number | null = null;
  for (const attr of attrs) {
    const split = attr.indexOf("=");
    if (split === -1) {
      if (attr.toLowerCase() === "secure") {
        secure = true;
      }
      continue;
    }
    const key = attr.slice(0, split).toLowerCase();
    const value = attr.slice(split + 1);
    if (key === "path") {
      path = value;
    } else if (key === "expires") {
      expiresMs = Date.parse(value);
    }
  }
  return { name, path, secure, expiresMs };
}

async function withCookieEnv(
  env: { SHOP_COOKIE_SECURE?: string; SHOP_MEMBER_COOKIE_PATH_SCOPED?: string; NODE_ENV?: string },
  run: () => Promise<void>,
): Promise<void> {
  const keys = ["SHOP_COOKIE_SECURE", "SHOP_MEMBER_COOKIE_PATH_SCOPED", "NODE_ENV"] as const;
  const previous = new Map(keys.map((key) => [key, process.env[key]]));
  for (const key of keys) {
    const value = env[key];
    if (value === undefined) {
      delete process.env[key];
    } else {
      process.env[key] = value;
    }
  }
  try {
    await run();
  } finally {
    for (const [key, value] of previous) {
      if (value === undefined) {
        delete process.env[key];
      } else {
        process.env[key] = value;
      }
    }
  }
}

async function assertDeleteMatchesWrite(
  session: SessionCookies,
  write: () => Promise<void>,
  clear: () => Promise<void>,
  expected: { secure: boolean; path: string },
): Promise<void> {
  session.calls.length = 0;
  await write();
  const setCall = session.calls.find((call) => call.op === "set");
  assert.ok(setCall);
  session.calls.length = 0;
  await clear();
  const deleteCall = session.calls.find((call) => call.op === "delete");
  assert.ok(deleteCall);
  const written = cookieShape(headerFor(setCall));
  const cleared = cookieShape(headerFor(deleteCall));
  assert.equal(written.secure, expected.secure);
  assert.equal(written.path, expected.path);
  assert.equal(cleared.name, written.name);
  assert.equal(cleared.path, written.path);
  assert.equal(cleared.secure, written.secure);
  assert.ok(cleared.expiresMs !== null && cleared.expiresMs < Date.now());
}

describe("cookieSecure", () => {
  it("is true when SHOP_COOKIE_SECURE=true (KeepAlive next dev on HTTPS)", () => {
    assert.equal(cookieSecure({ SHOP_COOKIE_SECURE: "true" }), true);
  });

  it("is true when NODE_ENV=production", () => {
    assert.equal(cookieSecure({ NODE_ENV: "production" }), true);
  });

  it("is true when both flags are set", () => {
    assert.equal(cookieSecure({ SHOP_COOKIE_SECURE: "true", NODE_ENV: "production" }), true);
  });

  it("is false for local http when unset", () => {
    assert.equal(cookieSecure({}), false);
  });

  it("is false when SHOP_COOKIE_SECURE is not the string true", () => {
    assert.equal(cookieSecure({ SHOP_COOKIE_SECURE: "false" }), false);
    assert.equal(cookieSecure({ SHOP_COOKIE_SECURE: "1" }), false);
  });
});

describe("session cookie deletion", () => {
  it("sends the same name, path, and Secure flag on delete as on write", async () => {
    const session = await loadSession();

    await withCookieEnv({ SHOP_COOKIE_SECURE: "true", NODE_ENV: "test" }, async () => {
      await assertDeleteMatchesWrite(
        session,
        () => session.writeSessionCookie("owner-token"),
        () => session.clearSessionCookie(),
        { secure: true, path: "/" },
      );
      await assertDeleteMatchesWrite(
        session,
        () => session.writeMemberSessionCookie("member-token"),
        () => session.clearMemberSessionCookie(),
        { secure: true, path: "/" },
      );
    });

    await withCookieEnv(
      { SHOP_COOKIE_SECURE: "true", SHOP_MEMBER_COOKIE_PATH_SCOPED: "true", NODE_ENV: "test" },
      async () => {
        await assertDeleteMatchesWrite(
          session,
          () => session.writeMemberSessionCookie("member-token"),
          () => session.clearMemberSessionCookie(),
          { secure: true, path: "/member" },
        );
      },
    );

    await withCookieEnv({ SHOP_COOKIE_SECURE: "false", NODE_ENV: "test" }, async () => {
      await assertDeleteMatchesWrite(
        session,
        () => session.writeSessionCookie("owner-token"),
        () => session.clearSessionCookie(),
        { secure: false, path: "/" },
      );
      await assertDeleteMatchesWrite(
        session,
        () => session.writeMemberSessionCookie("member-token"),
        () => session.clearMemberSessionCookie(),
        { secure: false, path: "/" },
      );
    });
  });
});
