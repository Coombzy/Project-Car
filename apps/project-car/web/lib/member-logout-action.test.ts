import assert from "node:assert/strict";
import { register } from "node:module";
import { test } from "node:test";

const HOOK = `
const bodies = new Map([
  ["next/navigation", \`export function redirect(url) {
  if (globalThis.__redirectThrows) throw new Error("NEXT_REDIRECT");
  globalThis.__redirects.push(url);
}\`],
  ["../../lib/session", \`export async function clearMemberSessionCookie() {
  globalThis.__cookieClears++;
}\`],
  ["../../lib/shop-api", \`export async function logoutMember() {
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

register("data:text/javascript," + encodeURIComponent(HOOK), { parentURL: import.meta.url });

type State = {
  __redirects: string[];
  __cookieClears: number;
  __logoutFails: boolean;
  __redirectThrows: boolean;
};
const state = globalThis as unknown as State;

function reset(logoutFails: boolean, redirectThrows = false) {
  state.__redirects = [];
  state.__cookieClears = 0;
  state.__logoutFails = logoutFails;
  state.__redirectThrows = redirectThrows;
}

const actionModule = import("../app/member/logout-action.ts");

test("clears the cookie and redirects when logoutMember resolves", async () => {
  reset(false);
  const { memberLogoutAction } = await actionModule;
  await memberLogoutAction();
  assert.equal(state.__cookieClears, 1);
  assert.deepEqual(state.__redirects, ["/member/login"]);
});

test("still clears the cookie and redirects when logoutMember rejects", async () => {
  reset(true);
  const { memberLogoutAction } = await actionModule;
  await memberLogoutAction();
  assert.equal(state.__cookieClears, 1);
  assert.deepEqual(state.__redirects, ["/member/login"]);
});

test("a redirect thrown after the cookie is cleared is not swallowed", async () => {
  reset(false, true);
  const { memberLogoutAction } = await actionModule;
  await assert.rejects(() => memberLogoutAction(), /NEXT_REDIRECT/);
  assert.equal(state.__cookieClears, 1);
});
