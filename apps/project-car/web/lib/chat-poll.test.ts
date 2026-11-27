import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";
import { shouldSkipChatPoll } from "./chat-poll.ts";

function pollIntervalCallback(source: string): string {
  const start = source.indexOf("setInterval(");
  assert.notEqual(start, -1, "ChatThread has no setInterval");
  const end = source.indexOf("POLL_MS", start);
  assert.ok(end > start, "setInterval is not tied to POLL_MS");
  return source.slice(start, end);
}

describe("chat poll", () => {
  it("test_chat_poll_skips_when_in_flight", () => {
    assert.equal(shouldSkipChatPoll({ inFlight: true, hidden: false }), true);
    assert.equal(shouldSkipChatPoll({ inFlight: false, hidden: true }), true);
    assert.equal(shouldSkipChatPoll({ inFlight: true, hidden: true }), true);
    assert.equal(shouldSkipChatPoll({ inFlight: false, hidden: false }), false);
  });

  it("test_chat_thread_calls_shouldSkipChatPoll_in_poll_ms_interval", () => {
    const thread = readFileSync(
      join(dirname(fileURLToPath(import.meta.url)), "../components/chat-thread.tsx"),
      "utf8",
    );
    assert.match(
      thread,
      /import\s*\{[^}]*\bshouldSkipChatPoll\b[^}]*\}\s*from\s*["']\.\.\/lib\/chat-poll["']/,
    );
    assert.match(pollIntervalCallback(thread), /\bshouldSkipChatPoll\s*\(/);
  });
});
