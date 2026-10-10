import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath, pathToFileURL } from "node:url";

const libDir = dirname(fileURLToPath(import.meta.url));

function intervalCallback(source: string): string {
  const start = source.indexOf("setInterval(");
  assert.notEqual(start, -1, "ChatThread has no setInterval");
  const end = source.indexOf("POLL_MS", start);
  assert.ok(end > start, "setInterval is not tied to POLL_MS");
  return source.slice(start, end);
}

describe("chat poll", () => {
  it("test_chat_poll_skips_when_in_flight", async () => {
    const thread = readFileSync(join(libDir, "../components/chat-thread.tsx"), "utf8");
    const callback = intervalCallback(thread);
    assert.match(callback, /shouldSkipChatPoll\(/, "interval callback has no in-flight guard");
    assert.match(thread, /from ["']\.\.\/lib\/chat-poll["']/);

    const helper = await import(pathToFileURL(join(libDir, "chat-poll.ts")).href);
    assert.equal(typeof helper.shouldSkipChatPoll, "function");
    assert.equal(helper.shouldSkipChatPoll({ inFlight: true, hidden: false }), true);
    assert.equal(helper.shouldSkipChatPoll({ inFlight: false, hidden: true }), true);
    assert.equal(helper.shouldSkipChatPoll({ inFlight: true, hidden: true }), true);
    assert.equal(helper.shouldSkipChatPoll({ inFlight: false, hidden: false }), false);
  });
});
