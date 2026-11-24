import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath, pathToFileURL } from "node:url";

const webRoot = join(dirname(fileURLToPath(import.meta.url)), "..");

function read(relative: string): string {
  const abs = join(webRoot, relative);
  assert.equal(existsSync(abs), true, `${relative} is missing`);
  return readFileSync(abs, "utf8");
}

describe("AUD-039 live regions", () => {
  it("test_aud039_banner_is_an_alert", () => {
    const banner = read("components/banner.tsx");
    assert.match(banner, /export function Banner/);
    assert.match(banner, /role="alert"/);
    assert.match(banner, /banner \$\{tone\}/);

    const thread = read("components/chat-thread.tsx");
    assert.match(thread, /from ["']\.\/banner["']/);
    assert.match(thread, /<Banner tone="error">\{error\}<\/Banner>/);
  });

  it("test_aud039_chat_live_region_sticks_near_bottom", async () => {
    const thread = read("components/chat-thread.tsx");
    assert.match(thread, /className="chat-messages"[^>]*aria-live="polite"/);
    assert.match(thread, /shouldStickToChatBottom\(/);
    assert.match(
      thread,
      /if \(node && stickRef\.current\) \{\s*node\.scrollTop = node\.scrollHeight;/,
    );

    const helper = await import(pathToFileURL(join(webRoot, "lib/chat-scroll.ts")).href);
    const stick = helper.shouldStickToChatBottom as (node: {
      scrollTop: number;
      scrollHeight: number;
      clientHeight: number;
    }) => boolean;
    assert.equal(helper.CHAT_STICK_PX, 80);
    const box = (scrollTop: number, scrollHeight = 1000, clientHeight = 400) => ({
      scrollTop,
      scrollHeight,
      clientHeight,
    });
    assert.equal(stick(box(600)), true);
    assert.equal(stick(box(520)), true);
    assert.equal(stick(box(519)), false);
    assert.equal(stick(box(0)), false);
    assert.equal(stick({ scrollTop: 0, scrollHeight: 200, clientHeight: 400 }), true);
  });

  it("test_aud039_own_send_sticks_when_scrolled_up", async () => {
    const thread = read("components/chat-thread.tsx");
    const helper = await import(pathToFileURL(join(webRoot, "lib/chat-scroll.ts")).href);
    const nearBottom = helper.shouldStickToChatBottom as (node: {
      scrollTop: number;
      scrollHeight: number;
      clientHeight: number;
    }) => boolean;

    const scroller = { scrollTop: 0, scrollHeight: 1000, clientHeight: 400 };
    assert.equal(nearBottom(scroller), false);

    const tickStart = thread.indexOf("const tick = async");
    const tickEnd = thread.indexOf("const timer = window.setInterval");
    assert.ok(tickStart !== -1 && tickEnd > tickStart);
    assert.doesNotMatch(thread.slice(tickStart, tickEnd), /stickRef\.current\s*=/);

    const start = thread.indexOf("async function onSubmit");
    const end = thread.indexOf("\n  return (", start);
    assert.ok(start !== -1 && end > start);
    const submit = thread.slice(start, end);
    const sent = submit.indexOf("await sendMessage");
    const paint = submit.indexOf("setMessages(", sent);
    assert.ok(sent !== -1 && paint > sent);
    const beforePaint = submit.slice(sent, paint);
    if (/stickRef\.current\s*=\s*true/.test(beforePaint)) {
      scroller.scrollTop = scroller.scrollHeight;
    }
    assert.equal(nearBottom(scroller), true);
  });
});
