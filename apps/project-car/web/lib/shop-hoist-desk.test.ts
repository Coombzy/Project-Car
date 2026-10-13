import assert from "node:assert/strict";
import { mkdirSync, writeFileSync } from "node:fs";
import { register } from "node:module";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { test } from "node:test";
import { fileURLToPath, pathToFileURL } from "node:url";

import { formatShopDateTime, tokensLabel } from "./time.ts";

const webRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const ADA_ID = "11111111-1111-4111-8111-111111111111";
const SAM_ID = "22222222-2222-4222-8222-222222222222";
const OVERLAP_MESSAGE = "That hour is already booked. This approval did not take tokens.";

type FetchCall = { method: string; path: string; status: string | null };

type RequestRow = {
  record: "shop_hoist_request";
  id: string;
  member_id: string;
  member_name: string;
  hoist_id: string;
  hoist_name: string;
  start_at: string;
  end_at: string;
  status: "pending" | "approved" | "denied";
  token_quote: string;
  notes: string | null;
  created_by_kind: "human";
  created_by_id: string;
  created_at: string;
};

type HostNode = {
  type: string;
  props: Record<string, unknown> & { children?: unknown };
};

type SchedulePage = (props: {
  searchParams: Promise<Record<string, string | undefined>>;
}) => Promise<unknown>;

const adaStart = "2026-10-09T15:00:00.000Z";
const adaEnd = "2026-10-09T17:00:00.000Z";
const samStart = "2026-10-10T18:00:00.000Z";
const samEnd = "2026-10-10T19:00:00.000Z";

function requestRow(row: Pick<RequestRow, "id" | "member_name" | "start_at" | "end_at" | "token_quote">): RequestRow {
  return {
    record: "shop_hoist_request",
    member_id: "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
    hoist_id: "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
    hoist_name: "Bay 6",
    status: "pending",
    notes: null,
    created_by_kind: "human",
    created_by_id: "member",
    created_at: row.start_at,
    ...row,
  };
}

function isElement(node: unknown): node is { type: unknown; props?: { children?: unknown } } {
  return Boolean(node) && typeof node === "object" && "$$typeof" in (node as object) && "type" in (node as object);
}

function isHookError(error: unknown): boolean {
  const message = error instanceof Error ? error.message : String(error);
  return /hook|dispatcher|useState|useEffect|useContext|useMemo|useRef|useId/i.test(message);
}

function childList(children: unknown): unknown[] {
  if (children == null || typeof children === "boolean") {
    return [];
  }
  return Array.isArray(children) ? children : [children];
}

async function expand(node: unknown, depth = 0): Promise<unknown> {
  assert.ok(depth < 40, "schedule tree expanded too deeply");
  if (node == null || typeof node === "boolean") {
    return null;
  }
  if (typeof node === "string" || typeof node === "number") {
    return String(node);
  }
  if (Array.isArray(node)) {
    const expanded = [];
    for (const child of node) {
      expanded.push(await expand(child, depth + 1));
    }
    return expanded;
  }
  if (!isElement(node)) {
    return null;
  }
  if (typeof node.type === "function") {
    let rendered: unknown;
    try {
      rendered = (node.type as (props: unknown) => unknown)(node.props);
      if (rendered && typeof (rendered as Promise<unknown>).then === "function") {
        rendered = await rendered;
      }
    } catch (error) {
      if (!isHookError(error)) {
        throw error;
      }
      rendered = node.props?.children ?? null;
    }
    return expand(rendered, depth + 1);
  }
  if (typeof node.type === "symbol") {
    return expand(node.props?.children, depth + 1);
  }
  const children = await expand(node.props?.children, depth + 1);
  return { type: node.type, props: { ...node.props, children } } satisfies HostNode;
}

function walk(node: unknown, visit: (node: HostNode) => void): void {
  if (node == null || typeof node === "boolean" || typeof node === "string" || typeof node === "number") {
    return;
  }
  if (Array.isArray(node)) {
    for (const child of node) {
      walk(child, visit);
    }
    return;
  }
  const host = node as HostNode;
  if (typeof host.type !== "string") {
    return;
  }
  visit(host);
  walk(host.props.children, visit);
}

function textOf(node: unknown): string {
  if (node == null || typeof node === "boolean") {
    return "";
  }
  if (typeof node === "string" || typeof node === "number") {
    return String(node);
  }
  if (Array.isArray(node)) {
    return node.map((child) => textOf(child)).join("");
  }
  const host = node as HostNode;
  return textOf(host.props?.children);
}

function hosts(node: unknown, type: string): HostNode[] {
  const found: HostNode[] = [];
  walk(node, (host) => {
    if (host.type === type) {
      found.push(host);
    }
  });
  return found;
}

function inputValue(form: HostNode, name: string): string | null {
  const input = hosts(form, "input").find((field) => field.props.name === name);
  if (!input || input.props.value == null) {
    return null;
  }
  return String(input.props.value);
}

function buttonLabel(form: HostNode): string {
  const button = hosts(form, "button")[0];
  return button ? textOf(button).trim() : "";
}

function deskForms(tree: unknown, label: "Approve" | "Deny"): HostNode[] {
  return hosts(tree, "form").filter((form) => typeof form.props.action === "function" && buttonLabel(form) === label);
}

function containsNode(node: unknown, target: HostNode): boolean {
  if (node === target) {
    return true;
  }
  if (node == null || typeof node !== "object") {
    return false;
  }
  if (Array.isArray(node)) {
    return node.some((child) => containsNode(child, target));
  }
  const host = node as HostNode;
  return containsNode(host.props?.children, target);
}

function rowAround(tree: unknown, form: HostNode, memberName: string): HostNode {
  let best: HostNode | null = null;
  let bestLength = Number.POSITIVE_INFINITY;
  walk(tree, (host) => {
    if (host === form || !containsNode(host, form)) {
      return;
    }
    const text = textOf(host);
    if (!text.includes(memberName) || text.length >= bestLength) {
      return;
    }
    best = host;
    bestLength = text.length;
  });
  assert.ok(best, `no schedule row listed ${memberName} with this action`);
  return best;
}

function redirectLocation(error: unknown): string | null {
  if (!error || typeof error !== "object" || !("digest" in error)) {
    return null;
  }
  const digest = (error as { digest?: unknown }).digest;
  if (typeof digest !== "string" || !digest.startsWith("NEXT_REDIRECT;")) {
    return null;
  }
  return digest.split(";").slice(2, -2).join(";");
}

async function installDeskLoader(): Promise<void> {
  const dir = join(tmpdir(), `shop-hoist-desk-${process.pid}`);
  mkdirSync(dir, { recursive: true });
  const headersUrl = pathToFileURL(join(dir, "headers.mjs"));
  const cacheUrl = pathToFileURL(join(dir, "cache.mjs"));
  writeFileSync(
    join(dir, "headers.mjs"),
    `export async function cookies() {
  return {
    get(name) {
      return name === "pc_owner_session" ? { name, value: "owner-session" } : undefined;
    },
    set() {},
    delete() {},
  };
}
export async function headers() { return new Headers(); }
export async function draftMode() { return { isEnabled: false, enable() {}, disable() {} }; }
`,
  );
  writeFileSync(
    join(dir, "cache.mjs"),
    `export function revalidatePath() {}
export function revalidateTag() {}
export function unstable_cache(fn) { return fn; }
export function unstable_noStore() {}
`,
  );
  const hookPath = join(dir, "hook.mjs");
  writeFileSync(
    hookPath,
    `import { createRequire } from "node:module";
import { existsSync, readFileSync } from "node:fs";
import { fileURLToPath, pathToFileURL } from "node:url";

const require = createRequire(${JSON.stringify(join(webRoot, "package.json"))});
const ts = require("typescript");
const headersUrl = ${JSON.stringify(headersUrl.href)};
const cacheUrl = ${JSON.stringify(cacheUrl.href)};

function fromWebSource(parentURL) {
  return Boolean(parentURL && parentURL.includes("/apps/project-car/web/") && !parentURL.includes("/node_modules/"));
}

function resolveRelative(specifier, parentURL) {
  const exts = [".tsx", ".ts", ".jsx", ".js", ".mjs"];
  if (exts.some((ext) => specifier.endsWith(ext))) {
    const exact = new URL(specifier, parentURL);
    if (existsSync(fileURLToPath(exact))) {
      return exact.href;
    }
  }
  for (const ext of exts) {
    const candidate = new URL(specifier + ext, parentURL);
    if (existsSync(fileURLToPath(candidate))) {
      return candidate.href;
    }
  }
  return null;
}

export async function resolve(specifier, context, nextResolve) {
  if (fromWebSource(context.parentURL) && specifier === "next/headers") {
    return { url: headersUrl, shortCircuit: true };
  }
  if (fromWebSource(context.parentURL) && specifier === "next/cache") {
    return { url: cacheUrl, shortCircuit: true };
  }
  if (specifier.startsWith(".") && fromWebSource(context.parentURL)) {
    const resolved = resolveRelative(specifier, context.parentURL);
    if (resolved) {
      return { url: resolved, shortCircuit: true };
    }
  }
  try {
    return await nextResolve(specifier, context);
  } catch (error) {
    if (error && error.code === "ERR_MODULE_NOT_FOUND" && !specifier.endsWith(".js")) {
      return nextResolve(specifier + ".js", context);
    }
    throw error;
  }
}

export async function load(url, context, nextLoad) {
  if (url.startsWith("file:") && url.includes("/apps/project-car/web/") && !url.includes("/node_modules/") && (url.endsWith(".ts") || url.endsWith(".tsx"))) {
    const source = readFileSync(fileURLToPath(url), "utf8");
    const transpiled = ts.transpileModule(source, {
      compilerOptions: {
        target: ts.ScriptTarget.ES2022,
        module: ts.ModuleKind.ESNext,
        jsx: ts.JsxEmit.ReactJSX,
        esModuleInterop: true,
      },
      fileName: url.endsWith(".tsx") ? "desk.tsx" : "desk.ts",
    });
    return { format: "module", source: transpiled.outputText, shortCircuit: true };
  }
  return nextLoad(url, context);
}
`,
  );
  await register(pathToFileURL(hookPath).href, pathToFileURL(join(webRoot, "package.json")));
}

async function loadSchedulePage(): Promise<SchedulePage> {
  await installDeskLoader();
  // The page is TSX. Node's type stripper does not transform JSX, so this
  // import has to follow the loader registered above.
  const loaded = await import("../app/schedule/page.tsx");
  return loaded.default as SchedulePage;
}

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json" },
  });
}

test("test_schedule_page_offers_approve_and_deny", async () => {
  const store = [
    requestRow({
      id: ADA_ID,
      member_name: "Ada Reyes",
      start_at: adaStart,
      end_at: adaEnd,
      token_quote: "180.50",
    }),
    requestRow({
      id: SAM_ID,
      member_name: "Sam Okonkwo",
      start_at: samStart,
      end_at: samEnd,
      token_quote: "90",
    }),
  ];
  const calls: FetchCall[] = [];
  const originalFetch = globalThis.fetch;
  const originalError = console.error;
  console.error = (...args: unknown[]) => {
    const message = args.map((part) => String(part)).join(" ");
    if (message.includes("Invalid hook call")) {
      return;
    }
    originalError(...args);
  };
  globalThis.fetch = async (input, init) => {
    const url = new URL(typeof input === "string" ? input : input instanceof URL ? input.href : input.url);
    const method = (init?.method ?? "GET").toUpperCase();
    const status = url.searchParams.get("status");
    calls.push({ method, path: url.pathname, status });
    if (method === "GET" && url.pathname === "/me") {
      return jsonResponse({ role: "owner", email: "owner@projectcar.ca" });
    }
    if (method === "GET" && url.pathname === "/hoists") {
      return jsonResponse([
        {
          id: "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
          name: "Bay 6",
          location_label: "Shop hoist",
          status: "available",
          is_shop: true,
          created_at: adaStart,
          updated_at: adaStart,
        },
        {
          id: "cccccccc-cccc-4ccc-8ccc-cccccccccccc",
          name: "Bay 1",
          location_label: "Floor",
          status: "available",
          is_shop: false,
          created_at: adaStart,
          updated_at: adaStart,
        },
      ]);
    }
    if (method === "GET" && url.pathname === "/members") {
      return jsonResponse([
        {
          id: "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
          name: "Ada Reyes",
          email: "ada.reyes@example.com",
          phone: null,
          tier_name: "basic",
          status: "active",
          waiver_signed_at: null,
          waiver_version: null,
          emergency_contact_name: null,
          emergency_contact_phone: null,
          token_balance: "1500",
          deposit_balance: "0",
          created_at: adaStart,
          updated_at: adaStart,
        },
      ]);
    }
    if (method === "GET" && url.pathname === "/bookings") {
      return jsonResponse([]);
    }
    if (method === "GET" && url.pathname === "/shop-hoist-requests") {
      const rows = status ? store.filter((row) => row.status === status) : store;
      return jsonResponse(rows);
    }
    const decision = url.pathname.match(/^\/shop-hoist-requests\/([^/]+)\/(approve|deny)$/);
    if (decision && method === "POST") {
      const id = decision[1];
      const action = decision[2];
      const row = store.find((item) => item.id === id);
      if (!row) {
        return jsonResponse({ error: { code: "not_found", message: "Request not found." } }, 404);
      }
      if (action === "approve") {
        return jsonResponse(
          { error: { code: "hoist_overlap", message: OVERLAP_MESSAGE } },
          409,
        );
      }
      row.status = "denied";
      return jsonResponse({
        request_id: row.id,
        status: "denied",
        action: "deny",
        booking_id: null,
        token_balance: "1500",
      });
    }
    return jsonResponse(
      { error: { code: "not_mocked", message: `No mock for ${method} ${url.pathname}` } },
      500,
    );
  };

  try {
    const SchedulePage = await loadSchedulePage();
    const render = async (error?: string) => {
      const tree = await expand(
        await SchedulePage({
          searchParams: Promise.resolve(error ? { error } : {}),
        }),
      );
      return tree;
    };

    const first = await render();
    const pageText = textOf(first);
    assert.match(pageText, /Month heat-map/, `schedule page did not render (${calls.map((call) => call.path).join(", ")})`);
    const approve = deskForms(first, "Approve");
    const deny = deskForms(first, "Deny");
    assert.deepEqual(
      approve.map((form) => inputValue(form, "id")).sort(),
      [ADA_ID, SAM_ID],
      "schedule page did not offer Approve on each pending shop-hoist request",
    );
    assert.deepEqual(
      deny.map((form) => inputValue(form, "id")).sort(),
      [ADA_ID, SAM_ID],
      "schedule page did not offer Deny on each pending shop-hoist request",
    );
    assert.ok(
      calls.some((call) => call.method === "GET" && call.path === "/shop-hoist-requests" && call.status === "pending"),
      "schedule page did not load pending shop-hoist requests",
    );

    const samDeny = deny.find((form) => inputValue(form, "id") === SAM_ID);
    assert.ok(samDeny, "missing Deny for Sam Okonkwo");
    const samText = textOf(rowAround(first, samDeny, "Sam Okonkwo"));
    assert.match(samText, /Sam Okonkwo/);
    assert.match(samText, /Bay 6/);
    assert.match(samText, new RegExp(tokensLabel("90")));
    assert.match(samText, new RegExp(formatShopDateTime(samStart).replace(/[.*+?^${}()|[\]\\]/g, "\\$&")));
    assert.match(samText, new RegExp(formatShopDateTime(samEnd).replace(/[.*+?^${}()|[\]\\]/g, "\\$&")));

    const denyBody = new FormData();
    for (const field of hosts(samDeny, "input")) {
      if (typeof field.props.name === "string") {
        denyBody.set(field.props.name, String(field.props.value ?? ""));
      }
    }
    let denyRedirect: unknown;
    try {
      await (samDeny.props.action as (formData: FormData) => Promise<void>)(denyBody);
    } catch (error) {
      denyRedirect = error;
    }
    const denyLocation = redirectLocation(denyRedirect);
    assert.ok(denyLocation?.startsWith("/schedule"), "Deny did not return to the schedule");
    assert.equal(new URL(denyLocation ?? "", "http://schedule.local").searchParams.get("error"), null);
    assert.ok(
      calls.some((call) => call.method === "POST" && call.path === `/shop-hoist-requests/${SAM_ID}/deny`),
      "Deny did not call the staff deny route",
    );

    const afterDeny = await render();
    assert.equal(
      deskForms(afterDeny, "Deny").some((form) => inputValue(form, "id") === SAM_ID),
      false,
      "a denied shop-hoist request stayed in the queue",
    );
    assert.equal(
      deskForms(afterDeny, "Approve").some((form) => inputValue(form, "id") === ADA_ID),
      true,
      "the other pending request left the queue when Sam was denied",
    );
    assert.doesNotMatch(textOf(afterDeny), /Sam Okonkwo/);

    const adaApprove = deskForms(afterDeny, "Approve").find((form) => inputValue(form, "id") === ADA_ID);
    assert.ok(adaApprove, "missing Approve for Ada Reyes");
    const adaText = textOf(rowAround(afterDeny, adaApprove, "Ada Reyes"));
    assert.match(adaText, /Ada Reyes/);
    assert.match(adaText, /Bay 6/);
    assert.match(adaText, new RegExp(tokensLabel("180.50").replace(".", "\\.")));
    assert.match(adaText, new RegExp(formatShopDateTime(adaStart).replace(/[.*+?^${}()|[\]\\]/g, "\\$&")));
    assert.match(adaText, new RegExp(formatShopDateTime(adaEnd).replace(/[.*+?^${}()|[\]\\]/g, "\\$&")));

    const approveBody = new FormData();
    for (const field of hosts(adaApprove, "input")) {
      if (typeof field.props.name === "string") {
        approveBody.set(field.props.name, String(field.props.value ?? ""));
      }
    }
    let approveRedirect: unknown;
    try {
      await (adaApprove.props.action as (formData: FormData) => Promise<void>)(approveBody);
    } catch (error) {
      approveRedirect = error;
    }
    const approveLocation = redirectLocation(approveRedirect);
    assert.ok(approveLocation?.startsWith("/schedule"), "Approve did not return to the schedule");
    const approveError = new URL(approveLocation ?? "", "http://schedule.local").searchParams.get("error");
    assert.equal(approveError, OVERLAP_MESSAGE);
    assert.ok(
      calls.some((call) => call.method === "POST" && call.path === `/shop-hoist-requests/${ADA_ID}/approve`),
      "Approve did not call the staff approve route",
    );

    const withBanner = await render(approveError ?? undefined);
    const banner = hosts(withBanner, "div").find((node) => {
      const className = String(node.props.className ?? "");
      return className.split(/\s+/).includes("banner") && className.split(/\s+/).includes("error");
    });
    assert.equal(banner ? textOf(banner).trim() : "", OVERLAP_MESSAGE);
    assert.equal(
      deskForms(withBanner, "Approve").some((form) => inputValue(form, "id") === ADA_ID),
      true,
      "a failed approval dropped the pending request",
    );
  } finally {
    globalThis.fetch = originalFetch;
    console.error = originalError;
  }
});
