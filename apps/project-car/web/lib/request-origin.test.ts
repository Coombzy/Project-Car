import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { publicOrigin, publicUrl } from "./request-origin.ts";

function headers(init: Record<string, string>): Pick<Headers, "get"> {
  const store = new Headers(init);
  return store;
}

const listenUrl = "https://localhost:3000/";

describe("publicOrigin", () => {
  it("uses forwarded host and proto from the tunnel", () => {
    const origin = publicOrigin(
      headers({
        "x-forwarded-host": "app.projectcar.ca",
        "x-forwarded-proto": "https",
        host: "localhost:3000",
      }),
      listenUrl,
    );
    assert.equal(origin, "https://app.projectcar.ca");
  });

  it("uses Host + proto when X-Forwarded-Host is absent (cloudflared default)", () => {
    const origin = publicOrigin(
      headers({
        host: "app.projectcar.ca",
        "x-forwarded-proto": "https",
      }),
      listenUrl,
    );
    assert.equal(origin, "https://app.projectcar.ca");
  });

  it("keeps localhost when Doc hits :3000 with no forwarded host", () => {
    const origin = publicOrigin(headers({ host: "localhost:3000" }), "http://localhost:3000/");
    assert.equal(origin, "http://localhost:3000");
  });

  it("does not turn a proto-only tunnel request into https://localhost", () => {
    const origin = publicOrigin(
      headers({
        host: "app.projectcar.ca",
        "x-forwarded-proto": "https",
      }),
      listenUrl,
    );
    assert.notEqual(origin, "https://localhost:3000");
    assert.equal(origin, "https://app.projectcar.ca");
  });

  it("takes the first forwarded hop and ignores junk hosts", () => {
    const first = publicOrigin(
      headers({
        "x-forwarded-host": "app.projectcar.ca, other.example",
        "x-forwarded-proto": "https, http",
      }),
      listenUrl,
    );
    assert.equal(first, "https://app.projectcar.ca");

    const junk = publicOrigin(
      headers({
        "x-forwarded-host": "https://evil.example/phish",
        host: "localhost:3000",
      }),
      "http://localhost:3000/",
    );
    assert.equal(junk, "http://localhost:3000");
  });
});

describe("publicUrl", () => {
  it("builds /login?next=/ on the public host", () => {
    const login = publicUrl(
      headers({
        "x-forwarded-host": "app.projectcar.ca",
        "x-forwarded-proto": "https",
      }),
      listenUrl,
      "/login",
    );
    login.searchParams.set("next", "/");
    assert.equal(login.toString(), "https://app.projectcar.ca/login?next=%2F");
  });

  it("builds /login?next=/ on localhost for Doc demo", () => {
    const login = publicUrl(headers({ host: "localhost:3000" }), "http://localhost:3000/", "/login");
    login.searchParams.set("next", "/");
    assert.equal(login.toString(), "http://localhost:3000/login?next=%2F");
  });
});
