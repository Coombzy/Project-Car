import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { stripTypeScriptTypes } from "node:module";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath, pathToFileURL } from "node:url";

import { ShopApiError } from "./config.ts";

const libDir = dirname(fileURLToPath(import.meta.url));
const webRoot = resolve(libDir, "..");

type RedirectError = Error & { path?: string };

type RedirectSink = { calls: string[] };
type CookieSink = { deletes: unknown[] };

const NAVIGATION = [
  "export const calls = [];",
  "export function redirect(path) {",
  "  calls.push(path);",
  "  const error = new Error('NEXT_REDIRECT');",
  "  error.path = path;",
  "  throw error;",
  "}",
  "",
].join("\n");

const PAGE_COOKIES = [
  "export async function cookies() {",
  "  return {",
  "    get() { return undefined; },",
  "    set() { throw new Error('Cookies can only be modified in a Server Action or Route Handler.'); },",
  "    delete() { throw new Error('Cookies can only be modified in a Server Action or Route Handler.'); },",
  "  };",
  "}",
  "",
].join("\n");

const ROUTE_COOKIES = [
  "export const deletes = [];",
  "export async function cookies() {",
  "  return {",
  "    get() { return undefined; },",
  "    set(arg) { deletes.push(arg); },",
  "    delete(arg) { deletes.push(arg); },",
  "  };",
  "}",
  "",
].join("\n");

function rewriteRelatives(code: string, fromDir: string): string {
  return code.replace(/from\s+["'](\.[^"']+)["']/g, (_match, spec: string) => {
    const target = /\.(?:[cm]?[jt]s)$/.test(spec) ? spec : `${spec}.ts`;
    return `from ${JSON.stringify(pathToFileURL(resolve(fromDir, target)).href)}`;
  });
}

function writeStripped(dir: string, name: string, source: string, fromDir: string): string {
  const file = join(dir, name);
  writeFileSync(file, rewriteRelatives(stripTypeScriptTypes(source, { mode: "strip" }), fromDir));
  return pathToFileURL(file).href;
}

async function loadPage(): Promise<{
  handlePageError: (error: unknown) => Promise<string>;
  handleMemberPageError: (error: unknown) => Promise<string>;
  redirects: string[];
}> {
  const dir = mkdtempSync(join(tmpdir(), "page-error-"));
  writeFileSync(join(dir, "navigation.mjs"), NAVIGATION);
  writeFileSync(join(dir, "headers.mjs"), PAGE_COOKIES);
  const navigationHref = pathToFileURL(join(dir, "navigation.mjs")).href;
  const headersHref = pathToFileURL(join(dir, "headers.mjs")).href;
  let session = readFileSync(join(libDir, "session.ts"), "utf8");
  session = session.replace(/from\s+["']next\/headers["']/, `from ${JSON.stringify(headersHref)}`);
  const sessionHref = writeStripped(dir, "session.mjs", session, libDir);
  let page = readFileSync(join(libDir, "page.ts"), "utf8");
  page = page.replace(/from\s+["']next\/navigation["']/, `from ${JSON.stringify(navigationHref)}`);
  page = page.replace(/from\s+["']\.\/session["']/, `from ${JSON.stringify(sessionHref)}`);
  const pageHref = writeStripped(dir, "page.mjs", page, libDir);
  const mod = (await import(pageHref)) as {
    handlePageError: (error: unknown) => Promise<string>;
    handleMemberPageError: (error: unknown) => Promise<string>;
  };
  const sink = (await import(navigationHref)) as RedirectSink;
  return { ...mod, redirects: sink.calls };
}

async function loadRoute(sourcePath: string): Promise<{ redirects: string[]; deletes: unknown[] }> {
  const dir = mkdtempSync(join(tmpdir(), "session-route-"));
  writeFileSync(join(dir, "navigation.mjs"), NAVIGATION);
  writeFileSync(join(dir, "headers.mjs"), ROUTE_COOKIES);
  const navigationHref = pathToFileURL(join(dir, "navigation.mjs")).href;
  const headersHref = pathToFileURL(join(dir, "headers.mjs")).href;
  let session = readFileSync(join(libDir, "session.ts"), "utf8");
  session = session.replace(/from\s+["']next\/headers["']/, `from ${JSON.stringify(headersHref)}`);
  const sessionHref = writeStripped(dir, "session.mjs", session, libDir);
  const routeDir = dirname(sourcePath);
  let route = readFileSync(sourcePath, "utf8");
  route = route.replace(/from\s+["']next\/navigation["']/, `from ${JSON.stringify(navigationHref)}`);
  route = route.replace(/from\s+["'](?:\.\.\/)+lib\/session["']/, `from ${JSON.stringify(sessionHref)}`);
  const routeHref = writeStripped(dir, "route.mjs", route, routeDir);
  const mod = (await import(routeHref)) as { GET: () => Promise<void> };
  await assert.rejects(() => mod.GET(), (error: unknown) => {
    assert.equal(typeof (error as RedirectError).path, "string");
    return true;
  });
  const redirects = ((await import(navigationHref)) as RedirectSink).calls;
  const deletes = ((await import(headersHref)) as CookieSink).deletes;
  return { redirects, deletes };
}

function api(status: number): ShopApiError {
  return new ShopApiError(status, "unauthorized", `message ${status}`);
}

describe("handlePageError session redirect", () => {
  it("sends an expired owner session to the route that clears the cookie", async () => {
    const page = await loadPage();
    await assert.rejects(
      () => page.handlePageError(api(401)),
      (error: unknown) => (error as RedirectError).path === "/session/expired",
    );
    assert.deepEqual(page.redirects, ["/session/expired"]);
  });

  it("sends an expired member session to the member route", async () => {
    const page = await loadPage();
    for (const status of [401, 403]) {
      page.redirects.length = 0;
      await assert.rejects(
        () => page.handleMemberPageError(api(status)),
        (error: unknown) => (error as RedirectError).path === "/member/session/expired",
      );
    }
  });

  it("returns the shop message for a non-session error and does not redirect", async () => {
    const page = await loadPage();
    assert.equal(await page.handlePageError(api(500)), "message 500");
    assert.equal(
      await page.handleMemberPageError(new Error("boom")),
      "Something went wrong talking to the shop API.",
    );
    assert.deepEqual(page.redirects, []);
  });
});

describe("session expired routes", () => {
  it("clears the owner cookie and opens the session login", async () => {
    const route = await loadRoute(join(webRoot, "app/session/expired/route.ts"));
    assert.equal(route.deletes.length, 1);
    assert.deepEqual(route.redirects, ["/login?reason=session"]);
  });

  it("clears the member cookie and opens the member session login", async () => {
    const route = await loadRoute(join(webRoot, "app/member/session/expired/route.ts"));
    assert.equal(route.deletes.length, 1);
    assert.deepEqual(route.redirects, ["/member/login?reason=session"]);
  });
});
