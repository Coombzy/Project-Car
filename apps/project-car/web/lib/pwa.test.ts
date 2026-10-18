import assert from "node:assert/strict";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { createRequire } from "node:module";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath, pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);

const webRoot = join(dirname(fileURLToPath(import.meta.url)), "..");

describe("shop web manifest", () => {
  it("test_shop_web_manifest_is_installable", async () => {
    const manifestPath = join(webRoot, "app", "manifest.ts");
    assert.equal(existsSync(manifestPath), true, "manifest file is missing");

    const manifestModule = await import(pathToFileURL(manifestPath).href);
    assert.equal(typeof manifestModule.default, "function");
    const manifest = manifestModule.default();

    assert.equal(manifest.name, "Project Car Shop OS");
    assert.equal(manifest.start_url, "/");
    assert.equal(manifest.display, "standalone");
    assert.equal(manifest.background_color, "#0b0c0e");

    const css = readFileSync(join(webRoot, "app", "globals.css"), "utf8");
    const background = css.match(/--bg:\s*(#[0-9a-fA-F]{6})/);
    assert.ok(background, "shop --bg token is missing");
    assert.equal(manifest.background_color, background[1]);

    const layout = readFileSync(join(webRoot, "app", "layout.tsx"), "utf8");
    assert.match(layout, /title:\s*"Project Car · Shop OS"/);
    assert.match(layout, /manifest:\s*"\/manifest\.webmanifest"/);
    assert.match(layout, /<body>\{children\}<\/body>/);
    assert.doesNotMatch(layout, /serviceWorker|service-worker/);
    assert.doesNotMatch(readFileSync(manifestPath, "utf8"), /serviceWorker|service-worker/);

    for (const relativePath of [
      "public/sw.js",
      "public/service-worker.js",
      "app/sw.ts",
      "app/sw.js",
      "app/service-worker.ts",
    ]) {
      assert.equal(existsSync(join(webRoot, relativePath)), false, relativePath);
    }
  });
});

type ManifestIcon = {
  src: string;
  type?: string;
};

type WebManifest = {
  icons?: ManifestIcon[];
  name?: string;
  start_url?: string;
  display?: string;
};

type AssetKind = "json" | "image";

type UnsignedResponse = {
  status: number;
  location: string | null;
  kind: AssetKind | "redirect";
  contentType: string | null;
  bodyText: string | null;
};

type LoadedMiddleware = {
  matches: (pathname: string) => boolean;
  run: (url: string, host: string) => { status: number; location: string | null };
};

const OWNER_HOST = "ops.projectcar.ca";
const CUSTOMER_HOST = "projectcar.ca";

function iconPathname(src: string): string {
  if (src.startsWith("/")) {
    return src.split(/[?#]/)[0] ?? src;
  }
  return new URL(src, "https://ops.projectcar.ca/").pathname;
}

function installAssetPaths(manifest: WebManifest): string[] {
  const paths = ["/manifest.webmanifest"];
  for (const icon of manifest.icons ?? []) {
    paths.push(iconPathname(icon.src));
  }
  return paths;
}

function imageContentType(pathname: string, declared: string | undefined): string {
  if (declared && declared.startsWith("image/")) {
    return declared;
  }
  if (pathname.endsWith(".svg")) {
    return "image/svg+xml";
  }
  if (pathname.endsWith(".jpg") || pathname.endsWith(".jpeg")) {
    return "image/jpeg";
  }
  if (pathname.endsWith(".webp")) {
    return "image/webp";
  }
  if (pathname.endsWith(".gif")) {
    return "image/gif";
  }
  if (pathname.endsWith(".ico")) {
    return "image/x-icon";
  }
  return "image/png";
}

function iconBytes(pathname: string): Buffer {
  const relative = pathname.replace(/^\//, "");
  const candidates = [join(webRoot, "public", relative), join(webRoot, "app", relative)];
  const file = candidates.find((candidate) => existsSync(candidate));
  assert.ok(file, `${pathname} icon file is missing`);
  return readFileSync(file);
}

function serveInstallAsset(pathname: string, manifest: WebManifest): UnsignedResponse {
  if (pathname === "/manifest.webmanifest") {
    return {
      status: 200,
      location: null,
      kind: "json",
      contentType: "application/manifest+json",
      bodyText: JSON.stringify(manifest),
    };
  }
  const icon = (manifest.icons ?? []).find((item) => iconPathname(item.src) === pathname);
  assert.ok(icon, `${pathname} is not an icon on the manifest`);
  const bytes = iconBytes(pathname);
  assert.ok(bytes.length > 8, `${pathname} icon is empty`);
  return {
    status: 200,
    location: null,
    kind: "image",
    contentType: imageContentType(pathname, icon.type),
    bodyText: null,
  };
}

// middleware.ts imports next/server, which this ESM test runner does not resolve.
// Compile that same source and call it the way Next would for an unsigned request.
function loadMiddleware(): { loaded: LoadedMiddleware; cleanup: () => void } {
  const ts = require("typescript") as {
    transpileModule: (
      source: string,
      options: { compilerOptions: Record<string, number>; fileName: string },
    ) => { outputText: string };
    ModuleKind: { CommonJS: number };
    ScriptTarget: { ES2022: number };
  };
  const nextServer = require.resolve("next/server");
  const { NextRequest } = require("next/server") as {
    NextRequest: new (url: string, init?: { headers?: Record<string, string> }) => {
      headers: { get(name: string): string | null };
    };
  };
  const { getMiddlewareMatchers } = require("next/dist/build/analysis/get-page-static-info") as {
    getMiddlewareMatchers: (matcher: string[], nextConfig: Record<string, never>) => { regexp: string }[];
  };
  const { getMiddlewareRouteMatcher } = require("next/dist/shared/lib/router/utils/middleware-route-matcher") as {
    getMiddlewareRouteMatcher: (matchers: { regexp: string }[]) => (pathname: string) => boolean;
  };
  const dir = mkdtempSync(join(tmpdir(), "shop-manifest-mw-"));
  const files = ["lib/config.ts", "lib/request-origin.ts", "lib/security-headers.ts", "middleware.ts"];
  for (const relative of files) {
    const source = readFileSync(join(webRoot, relative), "utf8");
    let js = ts.transpileModule(source, {
      compilerOptions: {
        module: ts.ModuleKind.CommonJS,
        target: ts.ScriptTarget.ES2022,
      },
      fileName: relative,
    }).outputText;
    js = js.replaceAll(`require("next/server")`, `require(${JSON.stringify(nextServer)})`);
    js = js.replaceAll(/require\("(\.\/[^"]+)"\)/g, (_match, spec: string) => `require("${spec}.cjs")`);
    const out = join(dir, relative.replace(/\.ts$/, ".cjs"));
    mkdirSync(dirname(out), { recursive: true });
    writeFileSync(out, js);
  }
  const compiled = require(join(dir, "middleware.cjs")) as {
    middleware: (request: InstanceType<typeof NextRequest>) => {
      status: number;
      headers: { get(name: string): string | null };
    };
    config: { matcher: string[] };
  };
  const matches = getMiddlewareRouteMatcher(getMiddlewareMatchers(compiled.config.matcher, {}));
  return {
    loaded: {
      matches,
      run(url: string, host: string) {
        const request = new NextRequest(url, {
          headers: {
            host,
            "x-forwarded-host": host,
            "x-forwarded-proto": "https",
          },
        });
        assert.equal(request.headers.get("cookie"), null);
        const response = compiled.middleware(request);
        return { status: response.status, location: response.headers.get("location") };
      },
    },
    cleanup() {
      rmSync(dir, { recursive: true, force: true });
    },
  };
}

function unsignedResponse(
  pathname: string,
  host: string,
  manifest: WebManifest,
  loaded: LoadedMiddleware,
): UnsignedResponse {
  const url = `https://${host}${pathname}`;
  if (!loaded.matches(pathname)) {
    return serveInstallAsset(pathname, manifest);
  }
  const response = loaded.run(url, host);
  if (response.location || (response.status >= 300 && response.status < 400)) {
    return {
      status: response.status,
      location: response.location,
      kind: "redirect",
      contentType: null,
      bodyText: null,
    };
  }
  const served = serveInstallAsset(pathname, manifest);
  return { ...served, status: response.status };
}

describe("unsigned manifest fetch", () => {
  it("test_unsigned_manifest_request_is_not_redirected", async () => {
    const manifestModule = await import(pathToFileURL(join(webRoot, "app", "manifest.ts")).href);
    const manifest = manifestModule.default() as WebManifest;
    const paths = installAssetPaths(manifest);
    const { loaded, cleanup } = loadMiddleware();
    try {
      for (const host of [OWNER_HOST, CUSTOMER_HOST]) {
        for (const pathname of paths) {
          const response = unsignedResponse(pathname, host, manifest, loaded);
          assert.equal(
            response.status,
            200,
            `${host} ${pathname} redirected to ${response.location ?? "(no location)"}`,
          );
          assert.equal(response.location, null);
          if (pathname === "/manifest.webmanifest") {
            assert.equal(response.kind, "json");
            assert.match(response.contentType ?? "", /json/);
            const body = JSON.parse(response.bodyText ?? "") as WebManifest;
            assert.equal(body.name, "Project Car Shop OS");
            assert.equal(body.start_url, "/");
            assert.equal(body.display, "standalone");
            continue;
          }
          assert.equal(response.kind, "image");
          assert.match(response.contentType ?? "", /^image\//);
        }
      }

      const schedule = unsignedResponse("/schedule", OWNER_HOST, manifest, loaded);
      assert.equal(schedule.status, 307);
      assert.equal(schedule.location, "https://ops.projectcar.ca/login?next=%2Fschedule");

      const customerHome = unsignedResponse("/", CUSTOMER_HOST, manifest, loaded);
      assert.equal(customerHome.status, 307);
      assert.equal(customerHome.location, "https://ops.projectcar.ca/login");
    } finally {
      cleanup();
    }
  });
});
