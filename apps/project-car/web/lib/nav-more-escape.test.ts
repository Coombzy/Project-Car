import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

import { handleNavMoreKeydown } from "./nav-more-escape.ts";

const shell = readFileSync(
  join(dirname(fileURLToPath(import.meta.url)), "../components/owner-shell.tsx"),
  "utf8",
);

function menu(open: boolean, hasSummary = true) {
  const summary = {
    hits: 0,
    focus() {
      summary.hits += 1;
    },
  };
  return {
    open,
    summary,
    querySelector(selector: string) {
      return selector === "summary" && hasSummary ? summary : null;
    },
  };
}

function key(name: string, node: ReturnType<typeof menu> | null): boolean {
  let prevented = false;
  handleNavMoreKeydown(
    {
      key: name,
      preventDefault() {
        prevented = true;
      },
    },
    node,
  );
  return prevented;
}

describe("R175 owner More menu Escape", () => {
  it("test_r175_escape_closes_open_more_and_focuses_summary", () => {
    const open = menu(true);
    assert.equal(key("Escape", open), true);
    assert.equal(open.open, false);
    assert.equal(open.summary.hits, 1);

    const shut = menu(false);
    assert.equal(key("Escape", shut), false);
    assert.equal(shut.open, false);
    assert.equal(shut.summary.hits, 0);

    for (const name of ["Enter", " ", "Tab", "ArrowDown", "Esc"]) {
      const still = menu(true);
      assert.equal(key(name, still), false, name);
      assert.equal(still.open, true, name);
      assert.equal(still.summary.hits, 0, name);
    }

    const bare = menu(true, false);
    assert.equal(key("Escape", bare), true);
    assert.equal(bare.open, false);
    assert.equal(key("Escape", null), false);
  });

  it("test_r175_owner_shell_wires_escape_on_the_more_details", () => {
    const block = shell.slice(shell.indexOf("<details"), shell.indexOf("</details>"));
    assert.equal(shell.startsWith('"use client";\n'), true);
    assert.match(shell, /from ["']\.\.\/lib\/nav-more-escape["']/);
    assert.match(block, /className=\{`nav-more/);
    assert.match(block, /<summary>\s*More/);
    assert.match(block, /onKeyDown=\{/);
    assert.match(block, /handleNavMoreKeydown\(event, event\.currentTarget\)/);
    assert.equal((shell.match(/<details/g) ?? []).length, 1);
    assert.equal(shell.includes("onClick"), false);
    for (const label of ["Dashboard", "Schedule", "Chat", "Members", "Sign out"]) {
      assert.ok(shell.includes(label), label);
    }
  });
});
