import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { contentDispositionForIcs } from "./ics-filename.ts";

describe("contentDispositionForIcs", () => {
  it("test_r171_content_disposition_uses_a_safe_ics_name", () => {
    const uuidName = "project-car-todo-550e8400-e29b-41d4-a716-446655440000.ics";
    const fallbackName = "todo-550e8400-e29b-41d4-a716-446655440000.ics";
    const split = 'a"; filename="evil.exe';
    const injected = "todo\r\nX-Injected: 1.ics";
    const path = "../../etc/passwd";
    const quotedId = 'ab"cd';

    assert.equal(contentDispositionForIcs(uuidName), `attachment; filename="${uuidName}"`);
    assert.equal(contentDispositionForIcs(fallbackName), `attachment; filename="${fallbackName}"`);
    assert.equal(contentDispositionForIcs(split), 'attachment; filename="afilenameevil.exe.ics"');
    assert.equal(contentDispositionForIcs(injected), 'attachment; filename="todoX-Injected1.ics"');
    assert.equal(contentDispositionForIcs(path), 'attachment; filename="passwd.ics"');
    assert.equal(contentDispositionForIcs("..\\..\\etc\\passwd"), 'attachment; filename="passwd.ics"');
    assert.equal(contentDispositionForIcs(`todo-${quotedId}.ics`), 'attachment; filename="todo-abcd.ics"');
    assert.equal(contentDispositionForIcs(`todo-${path}.ics`), 'attachment; filename="passwd.ics"');
    assert.equal(contentDispositionForIcs("notes"), 'attachment; filename="notes.ics"');
    assert.equal(contentDispositionForIcs("FILE.ICS"), 'attachment; filename="FILE.ics"');
    assert.equal(contentDispositionForIcs("caf\u00e9 notes.ics"), 'attachment; filename="cafnotes.ics"');
    assert.equal(contentDispositionForIcs(""), 'attachment; filename="todo.ics"');
    assert.equal(contentDispositionForIcs('"'), 'attachment; filename="todo.ics"');
    assert.equal(contentDispositionForIcs("///"), 'attachment; filename="todo.ics"');
    assert.equal(contentDispositionForIcs(".."), 'attachment; filename="todo.ics"');
    assert.equal(contentDispositionForIcs("\r\n"), 'attachment; filename="todo.ics"');

    for (const value of [split, injected, path, `todo-${quotedId}.ics`, `todo-${path}.ics`]) {
      const disposition = contentDispositionForIcs(value);
      assert.match(disposition, /^attachment; filename="[A-Za-z0-9][A-Za-z0-9._-]*\.ics"$/);
      assert.equal(disposition.includes("\r"), false);
      assert.equal(disposition.includes("\n"), false);
      assert.equal(disposition.includes("\\"), false);
      assert.equal(disposition.includes("/"), false);
      assert.equal(disposition.includes(value), false);
    }
  });
});
