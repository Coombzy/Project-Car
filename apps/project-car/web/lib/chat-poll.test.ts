import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { shouldSkipChatPoll } from "./chat-poll.ts";

describe("chat poll", () => {
  it("test_chat_poll_skips_when_in_flight", () => {
    assert.equal(shouldSkipChatPoll({ inFlight: true, hidden: false }), true);
    assert.equal(shouldSkipChatPoll({ inFlight: false, hidden: true }), true);
    assert.equal(shouldSkipChatPoll({ inFlight: true, hidden: true }), true);
    assert.equal(shouldSkipChatPoll({ inFlight: false, hidden: false }), false);
  });
});
