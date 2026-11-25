import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { fetchTimeoutSignal, shopApiTimeoutMs } from "./fetch-timeout.ts";

const ENV = "SHOP_API_TIMEOUT_MS";
const DEFAULT_MS = 10_000;

async function withShopApiTimeout(value: string | undefined, run: () => Promise<void> | void): Promise<void> {
  const previous = process.env[ENV];
  if (value === undefined) {
    delete process.env[ENV];
  } else {
    process.env[ENV] = value;
  }
  try {
    await run();
  } finally {
    if (previous === undefined) {
      delete process.env[ENV];
    } else {
      process.env[ENV] = previous;
    }
  }
}

function whenAborted(signal: AbortSignal): Promise<void> {
  if (signal.aborted) {
    return Promise.resolve();
  }
  return new Promise((resolve) => {
    // AbortSignal.timeout does not keep the event loop alive on its own.
    const hold = setTimeout(() => {}, 30_000);
    signal.addEventListener(
      "abort",
      () => {
        clearTimeout(hold);
        resolve();
      },
      { once: true },
    );
  });
}

describe("R69 shop API fetch timeout", () => {
  it("uses 10000 when unset, empty, zero, negative, or non-numeric", async () => {
    const fallbacks: Array<string | undefined> = [undefined, "", " ", "0", "0.0", "-1", "abc"];
    for (const value of fallbacks) {
      await withShopApiTimeout(value, () => {
        assert.equal(shopApiTimeoutMs(), DEFAULT_MS, JSON.stringify(value));
      });
    }
  });

  it("uses a positive SHOP_API_TIMEOUT_MS", async () => {
    await withShopApiTimeout("250", () => {
      assert.equal(shopApiTimeoutMs(), 250);
    });
  });

  it("aborts a stalled wait after a short override", { timeout: 2_000 }, async () => {
    await withShopApiTimeout("40", async () => {
      const signal = fetchTimeoutSignal();
      assert.equal(signal.aborted, false);
      await whenAborted(signal);
      assert.equal(signal.aborted, true);
      assert.equal(signal.reason.name, "TimeoutError");
    });
  });

  it("lets the caller abort win, and still times out if the caller stays open", { timeout: 2_000 }, async () => {
    await withShopApiTimeout("10000", () => {
      const caller = new AbortController();
      const reason = new Error("caller");
      const signal = fetchTimeoutSignal(caller.signal);
      assert.equal(fetchTimeoutSignal(null).aborted, false);
      assert.equal(signal.aborted, false);
      caller.abort(reason);
      assert.equal(signal.aborted, true);
      assert.equal(signal.reason, reason);
    });

    await withShopApiTimeout("40", async () => {
      const caller = new AbortController();
      const signal = fetchTimeoutSignal(caller.signal);
      await whenAborted(signal);
      assert.equal(caller.signal.aborted, false);
      assert.equal(signal.reason.name, "TimeoutError");
    });

    await withShopApiTimeout("10000", () => {
      const caller = new AbortController();
      const reason = new Error("already");
      caller.abort(reason);
      const signal = fetchTimeoutSignal(caller.signal);
      assert.equal(signal.aborted, true);
      assert.equal(signal.reason, reason);
    });
  });
});
