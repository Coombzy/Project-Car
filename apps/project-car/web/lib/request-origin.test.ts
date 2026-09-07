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

  it("uses ops.projectcar.ca forwarded host (management, unchanged)", () => {
    const origin = publicOrigin(
      headers({
        "x-forwarded-host": "ops.projectcar.ca",
        "x-forwarded-proto": "https",
        host: "localhost:3000",
      }),
      listenUrl,
    );
    assert.equal(origin, "https://ops.projectcar.ca");
    assert.notEqual(origin, "https://localhost:3000");
  });

  it("uses projectcar.ca forwarded host + https (no localhost hop)", () => {
    const origin = publicOrigin(
      headers({
        "x-forwarded-host": "projectcar.ca",
        "x-forwarded-proto": "https",
        host: "localhost:3000",
      }),
      listenUrl,
    );
    assert.equal(origin, "https://projectcar.ca");
    assert.notEqual(origin, "https://localhost:3000");
    assert.notEqual(origin, "http://localhost:3000");
  });

  it("uses www.projectcar.ca forwarded host + https (no localhost hop)", () => {
    const origin = publicOrigin(
      headers({
        "x-forwarded-host": "www.projectcar.ca",
        "x-forwarded-proto": "https",
        host: "localhost:3000",
      }),
      listenUrl,
    );
    assert.equal(origin, "https://www.projectcar.ca");
    assert.notEqual(origin, "https://localhost:3000");
  });

  it("uses Host when X-Forwarded-Host is a customer host (cloudflared default)", () => {
    const apex = publicOrigin(
      headers({
        host: "projectcar.ca",
        "x-forwarded-proto": "https",
      }),
      listenUrl,
    );
    assert.equal(apex, "https://projectcar.ca");

    const www = publicOrigin(
      headers({
        host: "www.projectcar.ca",
        "x-forwarded-proto": "https",
      }),
      listenUrl,
    );
    assert.equal(www, "https://www.projectcar.ca");
  });

  it("rejects api.projectcar.ca as a shop-web redirect host", () => {
    const viaForwarded = publicOrigin(
      headers({
        "x-forwarded-host": "api.projectcar.ca",
        "x-forwarded-proto": "https",
        host: "localhost:3000",
      }),
      "http://localhost:3000/",
    );
    assert.equal(viaForwarded, "https://localhost:3000");
    assert.notEqual(viaForwarded, "https://api.projectcar.ca");

    const viaHostOnly = publicOrigin(
      headers({
        host: "api.projectcar.ca",
        "x-forwarded-proto": "https",
      }),
      "http://localhost:3000/",
    );
    assert.equal(viaHostOnly, "http://localhost:3000");
    assert.notEqual(viaHostOnly, "https://api.projectcar.ca");
  });

  it("rejects a well-formed but disallowed forwarded host", () => {
    const evil = publicOrigin(
      headers({
        "x-forwarded-host": "evil.example",
        "x-forwarded-proto": "https",
        host: "localhost:3000",
      }),
      "http://localhost:3000/",
    );
    assert.equal(evil, "https://localhost:3000");
    assert.notEqual(evil, "https://evil.example");

    const fallsThroughToAllowedHost = publicOrigin(
      headers({
        "x-forwarded-host": "evil.example",
        "x-forwarded-proto": "https",
        host: "app.projectcar.ca",
      }),
      listenUrl,
    );
    assert.equal(fallsThroughToAllowedHost, "https://app.projectcar.ca");

    const bothDisallowed = publicOrigin(
      headers({
        "x-forwarded-host": "evil.example",
        host: "api.projectcar.ca",
        "x-forwarded-proto": "https",
      }),
      "http://localhost:3000/",
    );
    assert.equal(bothDisallowed, "http://localhost:3000");
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

  it("builds /member/login?next=/member on projectcar.ca (no localhost hop)", () => {
    const login = publicUrl(
      headers({
        "x-forwarded-host": "projectcar.ca",
        "x-forwarded-proto": "https",
        host: "localhost:3000",
      }),
      listenUrl,
      "/member/login",
    );
    login.searchParams.set("next", "/member");
    assert.equal(login.toString(), "https://projectcar.ca/member/login?next=%2Fmember");
    assert.doesNotMatch(login.toString(), /localhost/);
  });

  it("builds /member/login?next=/member on www.projectcar.ca (no localhost hop)", () => {
    const login = publicUrl(
      headers({
        "x-forwarded-host": "www.projectcar.ca",
        "x-forwarded-proto": "https",
        host: "localhost:3000",
      }),
      listenUrl,
      "/member/login",
    );
    login.searchParams.set("next", "/member");
    assert.equal(login.toString(), "https://www.projectcar.ca/member/login?next=%2Fmember");
    assert.doesNotMatch(login.toString(), /localhost/);
  });

  it("builds /member on customer hosts when already logged in (redirect target)", () => {
    const apex = publicUrl(
      headers({
        "x-forwarded-host": "projectcar.ca",
        "x-forwarded-proto": "https",
      }),
      listenUrl,
      "/member",
    );
    assert.equal(apex.toString(), "https://projectcar.ca/member");

    const www = publicUrl(
      headers({
        host: "www.projectcar.ca",
        "x-forwarded-proto": "https",
      }),
      listenUrl,
      "/member",
    );
    assert.equal(www.toString(), "https://www.projectcar.ca/member");
  });

  it("does not mint a /member/login redirect to a disallowed host", () => {
    const rejected = publicUrl(
      headers({
        "x-forwarded-host": "api.projectcar.ca",
        "x-forwarded-proto": "https",
        host: "localhost:3000",
      }),
      "http://localhost:3000/",
      "/member/login",
    );
    rejected.searchParams.set("next", "/member");
    assert.equal(rejected.toString(), "https://localhost:3000/member/login?next=%2Fmember");
    assert.notEqual(rejected.origin, "https://api.projectcar.ca");
  });
});
