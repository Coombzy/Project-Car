import assert from "node:assert/strict";
import { describe, it } from "node:test";

import {
  MEMBER_SHELL_ALIAS_COPY,
  MEMBER_SHELL_CUSTOMER_COPY,
  memberShellCopy,
} from "./member-shell-copy.ts";
import { isCustomerShopHost } from "./request-origin.ts";

function headers(init: Record<string, string>): Pick<Headers, "get"> {
  return new Headers(init);
}

function copyFor(init: Record<string, string>) {
  return memberShellCopy(isCustomerShopHost(headers(init)));
}

describe("memberShellCopy", () => {
  it("keeps the parked management-alias banner off the customer host", () => {
    const copy = memberShellCopy(false);
    assert.equal(copy.subtitle, "Member demo · parked");
    assert.equal(copy, MEMBER_SHELL_ALIAS_COPY);
    assert.match(copy.banner, /^Temporary Member demo on this management alias — customer bays 1–5\./);
    assert.match(copy.banner, /The shop is not open\./);
    assert.match(copy.banner, /not live pricing or Stripe/);
    assert.match(copy.banner, /Bay 6 is Owner-only/);
  });

  it("uses customer-host prep copy and does not say management alias", () => {
    const copy = memberShellCopy(true);
    assert.equal(copy, MEMBER_SHELL_CUSTOMER_COPY);
    assert.equal(copy.subtitle, "Customer-host Member surface (prep)");
    assert.match(copy.banner, /Customer-host Member surface \(prep\)/);
    assert.match(copy.banner, /Balance and schedule are primary/);
    assert.match(copy.banner, /Zone path-split is still pending/);
    assert.match(copy.banner, /Member is not live on this host/);
    assert.match(copy.banner, /Bay 6 is Owner-only/);
    assert.match(copy.banner, /The shop is not open/);
    assert.match(copy.banner, /not live pricing or Stripe/);
    assert.doesNotMatch(copy.subtitle, /management alias/i);
    assert.doesNotMatch(copy.banner, /management alias/i);
    assert.doesNotMatch(copy.subtitle, /parked/);
    assert.notEqual(copy.banner, MEMBER_SHELL_ALIAS_COPY.banner);
  });
});

describe("member shell copy follows the customer-host allowlist", () => {
  it("rewrites copy only for projectcar.ca and www", () => {
    for (const host of ["projectcar.ca", "www.projectcar.ca"]) {
      const copy = copyFor({
        "x-forwarded-host": host,
        "x-forwarded-proto": "https",
        host: "localhost:3000",
      });
      assert.equal(copy, MEMBER_SHELL_CUSTOMER_COPY, host);
    }

    const fromHostHeader = copyFor({
      host: "www.projectcar.ca",
      "x-forwarded-proto": "https",
    });
    assert.equal(fromHostHeader, MEMBER_SHELL_CUSTOMER_COPY);
  });

  it("keeps today's banner on ops, app, localhost, and api", () => {
    for (const host of ["ops.projectcar.ca", "app.projectcar.ca", "localhost:3000", "127.0.0.1:3000", "api.projectcar.ca"]) {
      const copy = copyFor({ host, "x-forwarded-proto": "https" });
      assert.equal(copy, MEMBER_SHELL_ALIAS_COPY, host);
      assert.match(copy.banner, /management alias/);
    }
  });

  it("does not treat a spoofed customer X-Forwarded-Host as the customer surface", () => {
    const copy = copyFor({
      "x-forwarded-host": "https://projectcar.ca/phish",
      host: "ops.projectcar.ca",
    });
    assert.equal(copy, MEMBER_SHELL_ALIAS_COPY);
  });
});
