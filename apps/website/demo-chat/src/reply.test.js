import assert from "node:assert/strict";
import test from "node:test";

import {
  APEX_AGENT_ID,
  allowedGatewayOrigin,
  allowedPageOrigin,
  cleanVisitorMessage,
  pickReply,
  scrubReply,
} from "./reply.js";

test("agent id is the demo bot and nothing else", () => {
  assert.equal(APEX_AGENT_ID, "3f6c46ec-6dee-4c88-a3a5-6c7c1dbc6765");
});

test("gateway origin is https cursor api only", () => {
  assert.equal(allowedGatewayOrigin("https://api2.cursor.sh"), "https://api2.cursor.sh");
  assert.equal(allowedGatewayOrigin("https://api2.cursor.sh/"), "https://api2.cursor.sh");
  assert.equal(allowedGatewayOrigin("https://api2.cursor.sh/api/sendPrompt"), null);
  assert.equal(allowedGatewayOrigin("http://api2.cursor.sh"), null);
  assert.equal(allowedGatewayOrigin("https://user:pw@api2.cursor.sh"), null);
  assert.equal(allowedGatewayOrigin("https://evil.cursorvm.com"), null);
  assert.equal(allowedGatewayOrigin("https://example.com"), null);
  assert.equal(allowedGatewayOrigin("https://api2.cursor.sh.evil.com"), null);
});

test("page origin is the brochure hosts only", () => {
  assert.equal(allowedPageOrigin("https://projectcar.ca"), true);
  assert.equal(allowedPageOrigin("https://www.projectcar.ca"), true);
  assert.equal(allowedPageOrigin("https://ops.projectcar.ca"), false);
  assert.equal(allowedPageOrigin("https://app.projectcar.ca"), false);
  assert.equal(allowedPageOrigin("https://evil.example"), false);
});

test("visitor message is a short single line", () => {
  assert.equal(cleanVisitorMessage("  hello\nthere "), "hello there");
  assert.equal(cleanVisitorMessage(""), null);
  assert.equal(cleanVisitorMessage("x".repeat(401)), null);
  assert.equal(cleanVisitorMessage({ message: "no" }), null);
});

test("pickReply returns only this nonce's assistant text", () => {
  const nonce = "11111111-1111-1111-1111-111111111111";
  const entries = [
    {
      kind: "message",
      role: "user",
      clientNonce: "22222222-2222-2222-2222-222222222222",
      requestId: "req-other",
      content: "other visitor secret",
    },
    {
      kind: "send-message",
      requestId: "req-other",
      message: { type: "text", content: "reply that must not leak" },
    },
    {
      kind: "message",
      role: "user",
      clientNonce: nonce,
      requestId: "req-mine",
      content: "hours?",
    },
    {
      kind: "send-message",
      requestId: "req-mine",
      message: { type: "text", content: "The shop is not open yet." },
    },
  ];
  assert.equal(pickReply(entries, nonce), "The shop is not open yet.");
  assert.equal(pickReply(entries, "22222222-2222-2222-2222-222222222222"), "reply that must not leak");
  assert.equal(pickReply(entries, "33333333-3333-3333-3333-333333333333"), null);
  assert.equal(pickReply(entries, "short"), null);
});

test("scrubReply drops credential-shaped text", () => {
  assert.equal(scrubReply("Join the waitlist."), "Join the waitlist.");
  assert.equal(scrubReply("Authorization: Bearer abc.def.ghi"), null);
  assert.equal(scrubReply("key sk-abcdefghij"), null);
});
