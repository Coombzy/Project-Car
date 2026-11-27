import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { afterEach, describe, it } from "node:test";

import {
  PRIMARY_CAMERA_ID,
  SAMPLE_CAMERAS,
  primaryCamera,
  showDemoPlaceholders,
} from "./placeholders.ts";

const webRoot = join(import.meta.dirname, "..");
const flag = "NEXT_PUBLIC_SHOW_DEMO_PLACEHOLDERS";

function read(rel: string): string {
  return readFileSync(join(webRoot, rel), "utf8");
}

function body(rel: string): string {
  return read(rel).replace(/^[ \t]*import .*$/gm, "");
}

afterEach(() => {
  delete process.env[flag];
});

describe("primaryCamera", () => {
  it("test_primary_camera_is_the_primary_id", () => {
    const camera = primaryCamera();
    assert.equal(camera.id, PRIMARY_CAMERA_ID);
    assert.equal(camera.primary, true);
  });

  it("test_all_sample_camera_ids_are_unique", () => {
    const ids = SAMPLE_CAMERAS.map((c) => c.id);
    assert.equal(new Set(ids).size, ids.length);
  });
});

describe("showDemoPlaceholders", () => {
  it("defaults on and is off only for 0 or false", () => {
    const previousNodeEnv = process.env.NODE_ENV;
    delete process.env[flag];
    try {
      for (const nodeEnv of ["production", "development"]) {
        process.env.NODE_ENV = nodeEnv;
        delete process.env[flag];
        assert.equal(showDemoPlaceholders(), true, nodeEnv);
      }
      for (const off of ["0", "false", "FALSE", "  False  ", " 0 "]) {
        process.env[flag] = off;
        assert.equal(showDemoPlaceholders(), false, off);
      }
      for (const on of ["1", "true", "TRUE", "yes", "", "falsey", "00"]) {
        process.env[flag] = on;
        assert.equal(showDemoPlaceholders(), true, JSON.stringify(on));
      }
      const source = read("lib/placeholders.ts");
      const start = source.indexOf("function showDemoPlaceholders");
      assert.ok(start !== -1);
      assert.equal(source.slice(start).includes("NODE_ENV"), false);
    } finally {
      if (previousNodeEnv === undefined) delete process.env.NODE_ENV;
      else process.env.NODE_ENV = previousNodeEnv;
    }
  });
});

describe("job sample rows", () => {
  it("JobBoard and JobLedger render SAMPLE_JOBS only when the flag is on", () => {
    for (const rel of ["components/job-board.tsx", "components/job-ledger.tsx"]) {
      assert.match(
        read(rel),
        /import \{[^}]*showDemoPlaceholders[^}]*\} from ["']\.\.\/lib\/placeholders["']/,
        rel,
      );
      const source = body(rel);
      const call = source.indexOf("const showSamples = showDemoPlaceholders()");
      const sample = source.search(/SAMPLE_JOBS(\[|\.)/);
      assert.ok(call !== -1 && sample > call, rel);
    }

    const board = body("components/job-board.tsx");
    const boardOpen = board.indexOf("{showSamples ? (");
    assert.ok(board.indexOf("Pay model (locked)") < boardOpen);
    assert.match(board.slice(boardOpen), /SAMPLE_JOBS\.map[\s\S]*\) : \(/);

    const ledger = body("components/job-ledger.tsx");
    const open = ledger.indexOf('{showSamples && audience === "member" ? (');
    const close = ledger.indexOf(") : null}", open);
    const sample = ledger.search(/SAMPLE_JOBS(\[|\.)/);
    assert.ok(open !== -1 && close > open && sample > open && sample < close);
    assert.equal(ledger.slice(close).includes("SAMPLE_JOBS"), false);
    assert.ok(ledger.indexOf("events.map") > close);
  });
});

describe("inventory sample rows", () => {
  it("ToolCribLedger and MemberRequestDesk render SAMPLE_* only when the flag is on", () => {
    const rows = [
      ["components/tool-crib-ledger.tsx", "SAMPLE_CRIB_TOOLS"],
      ["components/member-request-desk.tsx", "SAMPLE_PARTS_STOCK"],
      ["components/member-request-desk.tsx", "SAMPLE_INVENTORY_REQUESTS"],
    ];
    for (const [rel, name] of rows) {
      assert.match(
        read(rel),
        /import \{[^}]*showDemoPlaceholders[^}]*\} from ["']\.\.\/lib\/placeholders["']/,
        rel,
      );
      const source = body(rel);
      const call = source.indexOf("const showSamples = showDemoPlaceholders()");
      const hits = [...source.matchAll(new RegExp(`${name}(\\[|\\.)`, "g"))];
      assert.ok(call !== -1 && hits.length > 0, `${rel} ${name}`);
      for (const hit of hits) {
        const at = hit.index ?? -1;
        const open = source.lastIndexOf("{showSamples ? (", at);
        const close = source.indexOf(") : null}", open);
        assert.ok(at > call && open !== -1 && at < close, `${rel} ${name}`);
      }
    }

    const desk = body("components/member-request-desk.tsx");
    const heading = desk.indexOf("Sample requests (not stored)");
    const open = desk.lastIndexOf("{showSamples ? (", heading);
    const close = desk.indexOf(") : null}", heading);
    assert.ok(heading > open && close > heading);
    assert.equal(desk.slice(close).includes("Sample requests (not stored)"), false);

    const rest = (rel: string) => body(rel).replace(/\{showSamples \? \([\s\S]*?\) : null\}/g, "");
    const crib = rest("components/tool-crib-ledger.tsx");
    assert.match(crib, /<input name="sku"/);
    assert.match(crib, /events\.map/);
    const ask = rest("components/member-request-desk.tsx");
    assert.match(ask, /<h2>Ask for a part<\/h2>/);
    assert.match(ask, /<form className="card request-form"/);
    assert.match(ask, /<input id="member-request-sku" name="sku" required/);
    assert.match(ask, /requests\.map/);
  });
});
