import assert from "node:assert/strict";
import { writeFileSync } from "node:fs";
import { register } from "node:module";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";
import { pathToFileURL } from "node:url";
import { ShopApiError } from "./config.ts";
const stub = join(tmpdir(), "pc-aud-054-headers.mjs");
const hook = join(tmpdir(), "pc-aud-054-hook.mjs");
writeFileSync(stub, "export async function cookies(){return{get(n){const v=globalThis.__shopJar?.get(n);return v===undefined?undefined:{value:v}}}}\n");
writeFileSync(hook, `const stub=${JSON.stringify(pathToFileURL(stub).href)};
export async function resolve(s,c,n){const p=c.parentURL??"";if(!p.includes("/lib/shop-api.ts")&&!p.includes("/lib/session.ts"))return n(s,c);if(s==="next/headers")return{url:stub,shortCircuit:true};if(s.startsWith(".")&&!/\\.[a-z]+$/.test(s))return n(s+".ts",c);return n(s,c)}\n`);
await register(pathToFileURL(hook).href);
const loaded = await import("./shop-api.ts");

test("AUD-054 apiClient(realm) covers owner and member", async () => {
  assert.equal(typeof loaded.apiClient, "function");
  globalThis.__shopJar = new Map([["pc_owner_session", "owner-token"], ["pc_member_session", "member-token"]]);
  const seen: { path: string; method: string; cookie: string | null; body?: unknown; signal?: AbortSignal }[] = [];
  const original = globalThis.fetch;
  const install = (offline = false) => {
    globalThis.fetch = async (input, init) => {
      if (offline) throw new Error("offline");
      const path = String(input).split("8000")[1] ?? "";
      seen.push({ path, method: init?.method ?? "GET", cookie: new Headers(init?.headers).get("cookie"), body: init?.body, signal: init?.signal ?? undefined });
      if (path.endsWith("/ics")) return new Response("ICS", { headers: { "content-disposition": 'attachment; filename="t.ics"' } });
      if (path.endsWith("/nope")) return new Response(JSON.stringify({ error: { code: "missing", message: "no" } }), { status: 404 });
      if ((init?.method ?? "GET") === "DELETE") return new Response(null, { status: 204 });
      return new Response(JSON.stringify({ ok: true }), { status: 200 });
    };
  };
  install();
  try {
    const owner = loaded.apiClient("owner");
    const member = loaded.apiClient("member");
    assert.deepEqual(await owner.get("/me", "load"), { ok: true });
    assert.ok(seen[0].cookie === "pc_owner_session=owner-token" && seen[0].signal instanceof AbortSignal);
    await member.post("/todos", "create", { title: "x" });
    assert.equal(`${seen[1].method} ${seen[1].cookie} ${seen[1].body}`, `POST pc_member_session=member-token ${JSON.stringify({ title: "x" })}`);
    await owner.patch("/todos/a", "edit", { done: true });
    assert.equal(seen[2].method, "PATCH");
    await member.del("/todos/a", "delete");
    assert.equal(`${seen[3].method} ${seen[3].cookie}`, "DELETE pc_member_session=member-token");
    assert.deepEqual(await owner.download("/x/ics", "dl", "fallback.ics"), { filename: "t.ics", body: "ICS" });
    await assert.rejects(() => member.get("/nope", "load"), (e: unknown) => e instanceof ShopApiError && e.status === 404 && e.code === "missing");
    install(true);
    await assert.rejects(() => owner.del("/x", "delete"), (e: unknown) => e instanceof ShopApiError && e.status === 503 && /Cannot reach shop API/.test(e.message));
    seen.length = 0;
    install();
    await loaded.deleteTodo("t1");
    await loaded.deleteMemberTodo("t2");
    await loaded.downloadTodoIcs("t1");
    await loaded.downloadMemberTodoIcs("t2");
    assert.deepEqual(seen.map((row) => [row.path, row.method, row.cookie]), [
      ["/todos/t1", "DELETE", "pc_owner_session=owner-token"], ["/todos/t2", "DELETE", "pc_member_session=member-token"],
      ["/todos/t1/ics", "GET", "pc_owner_session=owner-token"], ["/todos/t2/ics", "GET", "pc_member_session=member-token"],
    ]);
  } finally {
    globalThis.fetch = original;
  }
});
