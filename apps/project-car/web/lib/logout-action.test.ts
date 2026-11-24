import assert from "node:assert/strict";
import { register } from "node:module";
import { test } from "node:test";

// A loader hook swaps the three imports in app/logout-action.ts for stubs that
// record what they were asked to do. The stub bodies run on the main thread.
const HOOK_SOURCE = `
const bodies = new Map([
  ["next/navigation", \`export function redirect(url) {
  if (globalThis.__redirectThrows) throw new Error("NEXT_REDIRECT");
  globalThis.__redirects.push(url);
}\`],
  ["../lib/session", \`export async function clearSessionCookie() {
  globalThis.__cookieClears++;
}\`],
  ["../lib/shop-api", \`export async function logoutOwner() {
  if (globalThis.__logoutFails) throw new Error("shop offline");
}\`],
]);

export async function resolve(specifier, context, nextResolve) {
  const body = bodies.get(specifier);
  if (body !== undefined) {
    return { url: "data:text/javascript," + encodeURIComponent(body), shortCircuit: true };
  }
  return nextResolve(specifier, context);
}
`;

register("data:text/javascript," + encodeURIComponent(HOOK_SOURCE), { parentURL: import.meta.url });

type State = {
  __redirects: string[];
  __cookieClears: number;
  __logoutFails: boolean;
  __redirectThrows: boolean;
};

const state = globalThis as unknown as State;

function resetState(logoutFails: boolean) {
  state.__redirects = [];
  state.__cookieClears = 0;
  state.__logoutFails = logoutFails;
  state.__redirectThrows = false;
}

const actionModule = import("../app/logout-action.ts");

test("logoutAction clears the cookie and redirects when the shop call succeeds", async () => {
  resetState(false);
  const { logoutAction } = await actionModule;
  await logoutAction();
  assert.equal(state.__cookieClears, 1);
  assert.deepEqual(state.__redirects, ["/login"]);
});

test("logoutAction still clears the cookie and redirects when the shop call rejects", async () => {
  resetState(true);
  const { logoutAction } = await actionModule;
  await logoutAction();
  assert.equal(state.__cookieClears, 1);
  assert.deepEqual(state.__redirects, ["/login"]);
});

test("a redirect thrown after the cookie is cleared is not swallowed", async () => {
  resetState(false);
  state.__redirectThrows = true;
  const { logoutAction } = await actionModule;
  await assert.rejects(() => logoutAction(), /NEXT_REDIRECT/);
  assert.equal(state.__cookieClears, 1);
});
