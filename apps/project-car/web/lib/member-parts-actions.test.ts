// Stubs next/navigation, next/cache and lib/shop-api through a module resolve
// hook, so the action's redirects and API calls are observable.
import assert from "node:assert/strict";
import { mkdirSync, writeFileSync } from "node:fs";
import { register } from "node:module";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";
import { pathToFileURL } from "node:url";

const mocks: { calls: unknown[]; redirects: string[]; failure: unknown } =
  (globalThis as Record<string, any>).partsMocks ??= { calls: [], redirects: [], failure: null };

const dir = join(tmpdir(), `member-parts-actions-${process.pid}`);
mkdirSync(dir, { recursive: true });
writeFileSync(join(dir, "navigation.mjs"), "export function redirect(url) { globalThis.partsMocks.redirects.push(url); throw new Error('redirect ' + url); }\n");
writeFileSync(join(dir, "cache.mjs"), "export function revalidatePath() {}\n");
writeFileSync(join(dir, "config.mjs"), "export class ShopApiError extends Error {}\n");
writeFileSync(join(dir, "shop-api.mjs"), "export async function createMemberPartsRequest(body) { globalThis.partsMocks.calls.push(body); if (globalThis.partsMocks.failure) throw globalThis.partsMocks.failure; }\n");
writeFileSync(join(dir, "hook.mjs"), `import { pathToFileURL } from "node:url";
const stubs = new Map([["next/navigation", "navigation.mjs"], ["next/cache", "cache.mjs"], ["../../../lib/config", "config.mjs"], ["../../../lib/shop-api", "shop-api.mjs"]].map(([s, f]) => [s, pathToFileURL(${JSON.stringify(dir)} + "/" + f).href]));
export async function resolve(specifier, context, nextResolve) {
  const url = stubs.get(specifier);
  if (url && context.parentURL?.includes("/apps/project-car/web/")) return { url, shortCircuit: true };
  return nextResolve(specifier, context);
}
`);
await register(pathToFileURL(join(dir, "hook.mjs")).href);

const { createMemberPartsRequestAction } = await import("../app/member/parts/actions.ts");
const { ShopApiError } = await import(pathToFileURL(join(dir, "config.mjs")).href);

function form(sku?: string): FormData {
  const data = new FormData();
  if (sku !== undefined) data.set("sku", sku);
  return data;
}
const reset = (): void => { mocks.calls = []; mocks.redirects = []; mocks.failure = null; };

test("a blank sku never reaches the API", async () => {
  for (const sku of [undefined, "", "   "]) {
    reset();
    await assert.rejects(() => createMemberPartsRequestAction(form(sku)));
    assert.deepEqual(mocks.calls, [], `sku ${JSON.stringify(sku)} reached the API`);
    assert.equal(mocks.redirects[0], "/member/parts?error=missing_sku");
  }
});

test("the API error text never reaches the query string", async () => {
  reset();
  mocks.failure = new ShopApiError("internal secret");
  await assert.rejects(() => createMemberPartsRequestAction(form("PT-OIL-5W30-012")));
  assert.equal(mocks.redirects[0], "/member/parts?error=parts_request_failed");
});

test("a real sku reaches the API trimmed, then redirects to the list", async () => {
  reset();
  await assert.rejects(() => createMemberPartsRequestAction(form("  PT-OIL-5W30-012  ")));
  assert.deepEqual(mocks.calls, [{ sku: "PT-OIL-5W30-012", note: undefined }]);
  assert.equal(mocks.redirects[0], "/member/parts");
});
