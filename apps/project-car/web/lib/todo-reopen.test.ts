import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const webRoot = join(dirname(fileURLToPath(import.meta.url)), "..");

function source(path: string): string {
  return readFileSync(join(webRoot, path), "utf8");
}

describe("done to-dos stay on the panel for Reopen", () => {
  it("test_done_rows_stay_on_the_panel_for_reopen", () => {
    const panel = source("components/todo-panel.tsx");
    const owner = source("app/page.tsx");
    const member = source("app/member/page.tsx");
    const ownerActions = source("app/todos/actions.ts");
    const memberActions = source("app/member/todos/actions.ts");

    assert.match(panel, /todos\.filter\(\(todo\) => todo\.status === "done"\)/);
    assert.match(panel, /\[\.\.\.open, \.\.\.done\]/);
    assert.match(panel, /name="status" value=\{todo\.status\}/);
    assert.match(panel, /todo\.status === "done" \? "Reopen" : "Done"/);
    assert.match(owner, /todos=\{dash\.todos\}/);
    assert.match(member, /todos=\{dash\.todos\}/);
    assert.match(ownerActions, /=== "done" \? "open" : "done"/);
    assert.match(memberActions, /=== "done" \? "open" : "done"/);
  });
});
