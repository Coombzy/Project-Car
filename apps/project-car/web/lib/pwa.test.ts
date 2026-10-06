import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath, pathToFileURL } from "node:url";

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
