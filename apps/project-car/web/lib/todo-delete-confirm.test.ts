import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const webRoot = join(dirname(fileURLToPath(import.meta.url)), "..");

function source(path: string): string {
  return readFileSync(join(webRoot, path), "utf8");
}

function removeForm(panel: string): string {
  const start = panel.indexOf("<form action={actions.remove}>");
  assert.notEqual(start, -1, "remove form");
  const end = panel.indexOf("</form>", start);
  assert.ok(end > start, "remove form end");
  return panel.slice(start, end);
}

describe("AUD-042 confirm before deleting a to-do", () => {
  it("test_aud042_remove_form_uses_confirm_not_a_bare_submit", () => {
    const panel = source("components/todo-panel.tsx");
    const form = removeForm(panel);
    assert.equal(form.includes('type="submit"'), false, "remove form still submits on the first click");
    assert.equal(
      /<button\b[^>]*>\s*Delete\s*<\/button>/.test(form),
      false,
      "remove form still has a bare Delete button",
    );
    assert.match(panel, /import \{ ConfirmButton \} from "\.\/confirm-button"/);
    assert.match(form, /<ConfirmButton\b/);
    assert.match(form, /type="hidden" name="id" value=\{todo\.id\}/);
    assert.match(form, /action=\{actions\.remove\}/);
  });

  it("test_aud042_first_click_does_not_submit_confirm_does", async () => {
    const helper = await import("./todo-delete-confirm.ts");
    assert.equal(helper.TODO_DELETE_EFFECT, "Delete this to-do? This cannot be undone.");

    const asked = helper.todoDeleteClick("idle", "ask");
    assert.equal(asked.submit, false);
    assert.equal(asked.phase, "confirming");

    const askedAgain = helper.todoDeleteClick(asked.phase, "ask");
    assert.equal(askedAgain.submit, false);
    assert.equal(askedAgain.phase, "confirming");

    assert.equal(helper.todoDeleteClick("idle", "confirm").submit, false);

    const confirmed = helper.todoDeleteClick("confirming", "confirm");
    assert.equal(confirmed.submit, true);
    assert.equal(confirmed.phase, "confirming");

    const cancelled = helper.todoDeleteClick("confirming", "cancel");
    assert.equal(cancelled.submit, false);
    assert.equal(cancelled.phase, "idle");

    const cancelIdle = helper.todoDeleteClick("idle", "cancel");
    assert.equal(cancelIdle.submit, false);
    assert.equal(cancelIdle.phase, "idle");

    const control = source("components/confirm-button.tsx");
    assert.match(control, /from "\.\.\/lib\/todo-delete-confirm"/);
    assert.match(control, /\{TODO_DELETE_EFFECT\}/);
    const controlButtons = [...control.matchAll(/<button\b[\s\S]*?<\/button>/g)].map((match) => match[0]);
    const ask = controlButtons.find((button) => button.includes('todoDeleteClick("idle", "ask")'));
    const confirm = controlButtons.find((button) => button.includes('todoDeleteClick(phase, "confirm")'));
    const cancel = controlButtons.find((button) => button.includes('todoDeleteClick(phase, "cancel")'));
    assert.ok(ask, "ask control");
    assert.match(ask, /type="button"/);
    assert.doesNotMatch(ask, /type="submit"/);
    assert.match(ask, />\s*Delete\s*</);
    assert.ok(confirm, "confirm control");
    assert.match(confirm, /type="submit"/);
    assert.match(confirm, /preventDefault\(\)/);
    assert.match(confirm, />\s*Delete\s*</);
    assert.ok(cancel, "cancel control");
    assert.match(cancel, /type="button"/);
    assert.doesNotMatch(cancel, /type="submit"/);
    assert.match(cancel, />\s*Cancel\s*</);
  });
});
