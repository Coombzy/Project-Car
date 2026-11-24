import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";
import ts from "typescript";

const pagePath = join(
  dirname(fileURLToPath(import.meta.url)),
  "..",
  "app",
  "member",
  "jobs",
  "page.tsx",
);

type Props = Record<string, unknown>;

// Harness: transpile the .tsx to CommonJS, swap its imports for stubs, and
// record the props MemberShell receives. Node's type stripping has no JSX.
async function renderPage(me: unknown, events: unknown): Promise<Props> {
  const shells: Props[] = [];
  const classNames: string[] = [];
  const MemberShell = { name: "MemberShell" };
  const React = {
    Fragment: "Fragment",
    createElement: (type: unknown, props: Props | null, ...children: unknown[]) => {
      if (type === MemberShell) shells.push(props ?? {});
      if (typeof props?.className === "string") classNames.push(props.className);
      return { type, props, children };
    },
  };
  const stubs: Record<string, unknown> = {
    "../../../components/job-board": { JobBoard: null },
    "../../../components/job-ledger": { JobLedger: null },
    "../../../components/member-shell": { MemberShell },
    "../../../components/placeholder-note": { PlaceholderNote: null },
    "../../../lib/page": { handleMemberPageError: async () => "shop unavailable" },
    "../../../lib/shop-api": {
      getMemberMe: () => (me instanceof Error ? Promise.reject(me) : Promise.resolve(me)),
      listMemberJobEvents: () =>
        events instanceof Error ? Promise.reject(events) : Promise.resolve(events),
    },
  };
  const js = ts.transpileModule(readFileSync(pagePath, "utf8"), {
    compilerOptions: { jsx: "react", module: "commonjs", target: "es2022", esModuleInterop: true },
  }).outputText;
  const exports: Props = {};
  new Function("exports", "require", "React", js)(exports, (id: string) => stubs[id], React);
  await (exports.default as (p: Props) => Promise<unknown>)({ searchParams: Promise.resolve({}) });
  assert.equal(shells.length, 1, "exactly one MemberShell renders");
  return { ...shells[0], classNames };
}

describe("MemberJobsPage member email", () => {
  it("keeps the email when listMemberJobEvents fails", async () => {
    const shell = await renderPage({ email: "ada@example.com" }, new Error("shop down"));
    assert.equal(shell.email, "ada@example.com");
    assert.deepEqual(shell.classNames, ["banner error"]);
  });

  it("renders no email when getMemberMe fails", async () => {
    const shell = await renderPage(new Error("no session"), []);
    assert.equal(shell.email, undefined);
    assert.equal(shell.current, "jobs");
    assert.deepEqual(shell.classNames, ["banner error"]);
  });
});
