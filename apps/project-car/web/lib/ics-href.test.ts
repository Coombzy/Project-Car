import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

import { safeIcsHref } from "./ics-href.ts";

const ORIGIN = "https://shop.example";
const TODO_ID = "550e8400-e29b-41d4-a716-446655440000";

describe("safeIcsHref", () => {
  it("test_r172_safe_ics_href_rejects_off_origin", () => {
    assert.equal(safeIcsHref("/todos/1/ics", ORIGIN), "/todos/1/ics");
    assert.equal(safeIcsHref("/member/todos/1/ics", ORIGIN), "/member/todos/1/ics");
    assert.equal(safeIcsHref(`${ORIGIN}/todos/1/ics`, ORIGIN), "/todos/1/ics");
    assert.equal(safeIcsHref(`${ORIGIN}/member/todos/1/ics`, ORIGIN), "/member/todos/1/ics");
    assert.equal(safeIcsHref(`/todos/${TODO_ID}/ics`, ORIGIN), `/todos/${TODO_ID}/ics`);
    assert.equal(
      safeIcsHref(`/member/todos/${TODO_ID}/ics`, ORIGIN),
      `/member/todos/${TODO_ID}/ics`,
    );
    assert.equal(
      safeIcsHref("http://127.0.0.1/todos/1/ics", "http://127.0.0.1"),
      "/todos/1/ics",
    );
    assert.equal(
      safeIcsHref("http://127.0.0.1:3000/member/todos/1/ics", "http://127.0.0.1:3000"),
      "/member/todos/1/ics",
    );

    assert.equal(safeIcsHref("https://evil.example/todos/1/ics", ORIGIN), null);
    assert.equal(safeIcsHref("http://127.0.0.1/todos/1/ics", ORIGIN), null);
    assert.equal(safeIcsHref("http://127.0.0.1/todos/1/ics", "http://127.0.0.1:3000"), null);
    assert.equal(safeIcsHref("//evil.example/todos/1/ics", ORIGIN), null);
    assert.equal(safeIcsHref("//shop.example/todos/1/ics", ORIGIN), null);
    assert.equal(safeIcsHref("javascript:alert(1)", ORIGIN), null);
    assert.equal(safeIcsHref("/\\evil.example", ORIGIN), null);
    assert.equal(safeIcsHref("/login", ORIGIN), null);
    assert.equal(safeIcsHref("/todos/1", ORIGIN), null);
    assert.equal(safeIcsHref("/todos/%2e%2e/ics", ORIGIN), null);
    assert.equal(safeIcsHref("/%2f%2fevil.example/todos/1/ics", ORIGIN), null);
  });
});

describe("CopyEventButton", () => {
  it("test_r172_copy_event_uses_safe_ics_href", () => {
    const source = readFileSync(
      join(dirname(fileURLToPath(import.meta.url)), "../components/copy-event-button.tsx"),
      "utf8",
    );
    assert.equal(source.includes("safeIcsHref(icsHref,"), true);
    assert.equal(source.includes("fetch(icsHref"), false);
    assert.equal(source.includes('cache: "no-store"'), true);
    assert.equal(source.includes('rel="noopener noreferrer"'), true);
    assert.equal(source.includes("Add a due date to export."), true);
    assert.equal(source.includes("window.setTimeout(() => setCopied(false), 2000)"), true);
  });
});
