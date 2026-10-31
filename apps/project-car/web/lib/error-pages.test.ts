import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const webRoot = join(dirname(fileURLToPath(import.meta.url)), "..");

function readSource(relativePath: string): string {
  const abs = join(webRoot, relativePath);
  assert.equal(existsSync(abs), true, `${relativePath} is missing`);
  return readFileSync(abs, "utf8");
}

function dashboardHrefFrom(source: string): (pathname: string) => string {
  const match = source.match(
    /function dashboardHref\(pathname: string\): "\/" \| "\/member" \{[\s\S]*?\n\}/,
  );
  assert.ok(match, "not-found.tsx is missing dashboardHref");
  const js = match[0].replace("pathname: string", "pathname").replace(': "/" | "/member"', "");
  return new Function(`${js}\nreturn dashboardHref;`)() as (pathname: string) => string;
}

describe("shop error pages", () => {
  it("test_not_found_and_error_pages_use_the_shop_shell", () => {
    const notFound = readSource("app/not-found.tsx");
    const errorPage = readSource("app/error.tsx");
    const pages = readSource("visual/pages.spec.ts");

    assert.match(notFound, /That page is not here\./);
    assert.match(notFound, /OwnerShell/);
    assert.match(notFound, /window\.location\.pathname/);
    assert.match(notFound, /<Link href=\{dashboardHref\(pathname\)\}>Dashboard<\/Link>/);
    // Server HTML and the first client render must not ship the link. useState("")
    // makes dashboardHref return "/" for /member and /member/... until the effect.
    assert.match(
      notFound,
      /useState<string \| null>\(null\)/,
      "pathname stays unset until window.location.pathname is stored",
    );
    assert.doesNotMatch(
      notFound,
      /useState\(\s*""\s*\)/,
      'useState("") renders Dashboard href="/" before the effect',
    );
    assert.doesNotMatch(
      notFound,
      /<h1>That page is not here\.<\/h1>\s*<p className="lede">\s*<Link href=\{dashboardHref\(pathname\)\}>Dashboard<\/Link>/,
      "Dashboard link is in the first render",
    );
    assert.match(
      notFound,
      /\{typeof pathname === "string" \? \([\s\S]*?<Link href=\{dashboardHref\(pathname\)\}>Dashboard<\/Link>[\s\S]*?\) : null\}/,
      "Dashboard link renders only after pathname is a string",
    );
    assert.doesNotMatch(notFound, /error\.message|error\.stack/);

    const dashboardHref = dashboardHrefFrom(notFound);
    assert.equal(dashboardHref("/schedul"), "/");
    assert.equal(dashboardHref("/_not-found"), "/");
    assert.equal(dashboardHref("/members/missing"), "/");
    assert.equal(dashboardHref("/membership"), "/");
    assert.equal(dashboardHref(""), "/");
    assert.equal(dashboardHref("/member"), "/member");
    assert.equal(dashboardHref("/member/schedule"), "/member");
    assert.equal(dashboardHref("/member/nope"), "/member");

    assert.equal(
      errorPage.trimStart().startsWith('"use client"'),
      true,
      'error.tsx must start with "use client"',
    );
    assert.match(errorPage, /Something went wrong\. Try again\./);
    assert.match(errorPage, /OwnerShell/);
    assert.match(errorPage, /reset:\s*\(\)\s*=>\s*void/);
    assert.match(
      errorPage,
      /<button type="button" onClick=\{\(\) => reset\(\)\}>Try again<\/button>/,
    );
    assert.equal(errorPage.includes("error.message"), false, "error.tsx renders error.message");
    assert.equal(errorPage.includes("error.stack"), false, "error.tsx renders error.stack");
    assert.doesNotMatch(errorPage, /error\??\.(message|stack|digest)/);
    assert.doesNotMatch(errorPage, /\{error\}/);

    assert.match(pages, /name: "not-found", path: "\/no-such-page"/);
    assert.match(
      pages,
      /if \(path === "\/no-such-page"\) \{\s*expect\(response\?\.status\(\), path\)\.toBe\(404\);/,
    );
    assert.match(pages, /toBeLessThan\(400\)/);
    assert.match(pages, /That page is not here\./);
  });

  it("test_member_not_found_links_to_the_member_dashboard", async () => {
    let dashboardHref: (pathname: string) => "/" | "/member";
    try {
      ({ dashboardHref } = await import("./error-pages.ts"));
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      assert.fail(`lib/error-pages.ts must export dashboardHref (${message})`);
    }
    assert.equal(dashboardHref("/member"), "/member");
    assert.equal(dashboardHref("/member/nope"), "/member");
    assert.equal(dashboardHref("/member/schedule"), "/member");
    assert.equal(dashboardHref("/no-such-page"), "/");
    assert.equal(dashboardHref("/schedul"), "/");
    assert.equal(dashboardHref("/membership"), "/");
    assert.equal(dashboardHref("/members/missing"), "/");
    assert.equal(dashboardHref("/_not-found"), "/");
    assert.equal(dashboardHref(""), "/");

    const notFound = readSource("app/not-found.tsx");
    assert.match(notFound, /import \{ dashboardHref \} from "\.\.\/lib\/error-pages"/);
    assert.doesNotMatch(notFound, /function dashboardHref/);
    assert.match(notFound, /<Link href=\{dashboardHref\(pathname\)\}>Dashboard<\/Link>/);

    const pages = readSource("visual/pages.spec.ts");
    assert.match(pages, /page\.goto\("\/member\/nope", \{ waitUntil: "load" \}\)/);
    assert.match(pages, /toHaveAttribute\("href", "\/member"\)/);
    assert.match(pages, /This page could not be found\./);
    // shoot() must still fail when networkidle never arrives. A Timeout
    // swallow lets a hung shop request pass the API-error count.
    assert.match(pages, /await page\.waitForLoadState\("networkidle"\);/);
    assert.doesNotMatch(pages, /\/Timeout\/i\.test/);
  });
});
