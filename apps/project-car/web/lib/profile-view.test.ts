import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath, pathToFileURL } from "node:url";
import { crc32, inflateSync } from "node:zlib";

const libDir = dirname(fileURLToPath(import.meta.url));

type ProfileRow = { label: string; value: string };

type ProfileSource = {
  name: string;
  email: string;
  tier_name: string;
  status: string;
  phone: string | null;
  waiver_signed_at: string | null;
  waiver_version: string | null;
  emergency_contact_name: string | null;
  emergency_contact_phone: string | null;
  token_balance: string | number | null | undefined;
  deposit_balance: string | number | null | undefined;
};

function filled(overrides: Partial<ProfileSource> = {}): ProfileSource {
  return {
    name: "Ada Reyes",
    email: "ada.reyes@example.com",
    tier_name: "premium",
    status: "active",
    phone: "403-555-0101",
    waiver_signed_at: "2026-08-01T21:00:00.000Z",
    waiver_version: "2026-08-waiver",
    emergency_contact_name: "Luis Reyes",
    emergency_contact_phone: "403-555-0111",
    token_balance: "1500.00",
    deposit_balance: "0.00",
    ...overrides,
  };
}

async function loadRows(member: ProfileSource): Promise<{ rows?: ProfileRow[]; error?: string }> {
  try {
    const imported = await import(pathToFileURL(join(libDir, "profile-view.ts")).href);
    if (typeof imported.profileRows !== "function") {
      return { error: "profileRows is not a function" };
    }
    return { rows: imported.profileRows(member) as ProfileRow[] };
  } catch (error) {
    return { error: error instanceof Error ? error.message : String(error) };
  }
}

function valueOf(rows: ProfileRow[] | undefined, label: string): string | undefined {
  return rows?.find((row) => row.label === label)?.value;
}

function because(error: string | undefined, assertion: string): string {
  return error ? `${assertion} (${error})` : assertion;
}

const MEMBER_SHOTS = [
  "member-home",
  "member-cameras",
  "member-chat",
  "member-chat-room",
  "member-jobs",
  "member-parts",
  "member-schedule",
  "member-profile",
] as const;

const VIEWPORT: Record<string, readonly [number, number]> = {
  "390": [390, 844],
  "768": [768, 1024],
  "1440": [1440, 900],
};

function readRefPng(width: string, name: string): Buffer {
  const b64Path = join(libDir, "../visual/member-nav-ref", width, `${name}.b64`);
  assert.equal(existsSync(b64Path), true, `member visual ref missing: ${width}/${name}.b64`);
  return Buffer.from(readFileSync(b64Path, "utf8"), "base64");
}

function assertCompletePng(png: Buffer, width: number, height: number, label: string): void {
  const signature = "\x89PNG\r\n\x1a\n";
  assert.equal(png.subarray(0, 8).toString("latin1"), signature, `${label} is not a PNG`);
  let offset = 8;
  let sawIhdr = false;
  let sawIdat = false;
  let sawIend = false;
  const idat: Buffer[] = [];
  while (offset + 12 <= png.length) {
    const length = png.readUInt32BE(offset);
    const type = png.subarray(offset + 4, offset + 8);
    const dataEnd = offset + 8 + length;
    const chunkEnd = dataEnd + 4;
    assert.ok(chunkEnd <= png.length, `${label} truncated in ${type.toString("latin1")}`);
    const data = png.subarray(offset + 8, dataEnd);
    const stored = png.readUInt32BE(dataEnd);
    const computed = crc32(Buffer.concat([type, data])) >>> 0;
    assert.equal(computed, stored, `${label} CRC mismatch on ${type.toString("latin1")}`);
    const kind = type.toString("latin1");
    if (kind === "IHDR") {
      sawIhdr = true;
      assert.equal(data.readUInt32BE(0), width, `${label} width`);
      assert.equal(data.readUInt32BE(4), height, `${label} height`);
    } else if (kind === "IDAT") {
      sawIdat = true;
      idat.push(data);
    } else if (kind === "IEND") {
      sawIend = true;
      offset = chunkEnd;
      break;
    }
    offset = chunkEnd;
  }
  assert.equal(sawIhdr, true, `${label} missing IHDR`);
  assert.equal(sawIdat, true, `${label} missing IDAT`);
  assert.equal(sawIend, true, `${label} missing IEND`);
  assert.equal(offset, png.length, `${label} has bytes after IEND`);
  inflateSync(Buffer.concat(idat));
}

// A unified diff prefixes each added line with "+". A base64 line that
// already starts with "++" is stored as "+++...", and a decoder that treats
// "+++" as the file header drops it. That cut fails the IDAT CRC.
function bytesAfterDiffHeaderDecode(text: string): Buffer {
  const kept: string[] = [];
  for (const line of text.split("\n")) {
    if (line.length === 0) {
      continue;
    }
    const diffLine = `+${line}`;
    if (diffLine.startsWith("+++")) {
      continue;
    }
    kept.push(diffLine.slice(1));
  }
  return Buffer.from(kept.join(""), "base64");
}

describe("member profile view", () => {
  it("test_profile_rows_missing_phone_shows_not_on_file", async () => {
    const missing = await loadRows(filled({ phone: null }));
    assert.equal(
      valueOf(missing.rows, "Phone"),
      "Not on file",
      because(missing.error, "missing phone shows Not on file"),
    );

    const blank = await loadRows(filled({ phone: "   " }));
    assert.equal(
      valueOf(blank.rows, "Phone"),
      "Not on file",
      because(blank.error, "blank phone shows Not on file"),
    );

    const present = await loadRows(filled({ phone: " 403-555-0199 " }));
    assert.equal(valueOf(present.rows, "Phone"), "403-555-0199");
  });

  it("test_profile_rows_unsigned_waiver_shows_not_signed", async () => {
    const unsigned = await loadRows(
      filled({ waiver_signed_at: null, waiver_version: "2026-08-waiver" }),
    );
    assert.equal(
      valueOf(unsigned.rows, "Waiver"),
      "Not signed",
      because(unsigned.error, "waiver unsigned shows Not signed"),
    );

    const blank = await loadRows(filled({ waiver_signed_at: "  ", waiver_version: null }));
    assert.equal(valueOf(blank.rows, "Waiver"), "Not signed");
  });

  it("test_profile_rows_shows_the_member_record", async () => {
    const loaded = await loadRows(filled({ deposit_balance: "12.50" }));
    assert.deepEqual(
      loaded.rows?.map((row) => row.label),
      [
        "Name",
        "Email",
        "Tier",
        "Status",
        "Phone",
        "Waiver",
        "Emergency contact",
        "Token balance",
        "Deposit balance",
      ],
      because(loaded.error, "profile rows list the member record"),
    );
    assert.equal(valueOf(loaded.rows, "Name"), "Ada Reyes");
    assert.equal(valueOf(loaded.rows, "Email"), "ada.reyes@example.com");
    assert.equal(valueOf(loaded.rows, "Tier"), "premium");
    assert.equal(valueOf(loaded.rows, "Status"), "active");
    assert.equal(valueOf(loaded.rows, "Phone"), "403-555-0101");
    assert.equal(valueOf(loaded.rows, "Waiver"), "Signed · 2026-08-waiver");
    assert.equal(valueOf(loaded.rows, "Emergency contact"), "Luis Reyes · 403-555-0111");
    assert.equal(valueOf(loaded.rows, "Token balance"), "1500");
    assert.equal(valueOf(loaded.rows, "Deposit balance"), "12.50");

    const signedWithoutVersion = await loadRows(filled({ waiver_version: null }));
    assert.equal(valueOf(signedWithoutVersion.rows, "Waiver"), "Signed");
  });

  it("test_profile_rows_missing_emergency_contact_shows_not_on_file", async () => {
    const missing = await loadRows(
      filled({ emergency_contact_name: null, emergency_contact_phone: "  " }),
    );
    assert.equal(
      valueOf(missing.rows, "Emergency contact"),
      "Not on file",
      because(missing.error, "missing emergency contact shows Not on file"),
    );

    const nameOnly = await loadRows(
      filled({ emergency_contact_name: "Luis Reyes", emergency_contact_phone: null }),
    );
    assert.equal(valueOf(nameOnly.rows, "Emergency contact"), "Luis Reyes");

    const phoneOnly = await loadRows(
      filled({ emergency_contact_name: null, emergency_contact_phone: "403-555-0111" }),
    );
    assert.equal(valueOf(phoneOnly.rows, "Emergency contact"), "403-555-0111");
  });

  it("test_profile_rows_missing_balance_shows_not_on_file", async () => {
    const missing = await loadRows(filled({ token_balance: null, deposit_balance: null }));
    assert.equal(
      valueOf(missing.rows, "Token balance"),
      "Not on file",
      because(missing.error, "null token balance shows Not on file"),
    );
    assert.equal(
      valueOf(missing.rows, "Deposit balance"),
      "Not on file",
      because(missing.error, "null deposit balance shows Not on file"),
    );

    const absent = await loadRows(
      filled({ token_balance: undefined, deposit_balance: undefined }),
    );
    assert.equal(
      valueOf(absent.rows, "Token balance"),
      "Not on file",
      because(absent.error, "missing token balance shows Not on file"),
    );
    assert.equal(
      valueOf(absent.rows, "Deposit balance"),
      "Not on file",
      because(absent.error, "missing deposit balance shows Not on file"),
    );

    const blank = await loadRows(filled({ token_balance: "", deposit_balance: "" }));
    assert.equal(
      valueOf(blank.rows, "Token balance"),
      "Not on file",
      because(blank.error, "blank token balance shows Not on file"),
    );
    assert.equal(
      valueOf(blank.rows, "Deposit balance"),
      "Not on file",
      because(blank.error, "blank deposit balance shows Not on file"),
    );

    const whitespace = await loadRows(
      filled({ token_balance: "   ", deposit_balance: "   " }),
    );
    assert.equal(
      valueOf(whitespace.rows, "Token balance"),
      "Not on file",
      because(whitespace.error, "whitespace token balance shows Not on file"),
    );
    assert.equal(
      valueOf(whitespace.rows, "Deposit balance"),
      "Not on file",
      because(whitespace.error, "whitespace deposit balance shows Not on file"),
    );

    const zero = await loadRows(filled({ token_balance: "0.00", deposit_balance: "0" }));
    assert.equal(valueOf(zero.rows, "Token balance"), "0");
    assert.equal(valueOf(zero.rows, "Deposit balance"), "0");

    const zeroSwapped = await loadRows(filled({ token_balance: "0", deposit_balance: "0.00" }));
    assert.equal(valueOf(zeroSwapped.rows, "Token balance"), "0");
    assert.equal(valueOf(zeroSwapped.rows, "Deposit balance"), "0");
  });

  it("test_member_profile_page_is_read_only_and_points_at_chat", () => {
    const pagePath = join(libDir, "../app/member/profile/page.tsx");
    assert.equal(existsSync(pagePath), true, "member profile page is missing");
    const page = readFileSync(pagePath, "utf8");
    assert.match(page, /getMemberMe\(/);
    assert.match(page, /profileRows\(me\)/);
    assert.match(page, /Ask the shop to change this/);
    assert.match(page, /href="\/member\/chat"/);
    assert.doesNotMatch(page, /<form[\s>]/);
    assert.doesNotMatch(page, /<input[\s>]/);
    assert.doesNotMatch(page, /<textarea[\s>]/);
    assert.doesNotMatch(page, /<select[\s>]/);
    assert.doesNotMatch(page, /<button[\s>]/);
  });

  it("test_member_nav_has_profile_link", () => {
    const shell = readFileSync(join(libDir, "../components/member-shell.tsx"), "utf8");
    assert.match(shell, /href: "\/member\/profile", current: "profile", label: "Profile"/);
  });

  it("test_screenshot_walk_includes_member_profile", () => {
    const spec = readFileSync(join(libDir, "../visual/pages.spec.ts"), "utf8");
    const list = spec.match(/const MEMBER_PAGES: Shot\[\] = \[([\s\S]*?)\];/);
    assert.ok(list, "MEMBER_PAGES list is missing");
    assert.match(
      list[1],
      /\{ name: "member-profile", path: "\/member\/profile" \}/,
      "screenshot job must walk /member/profile",
    );
  });

  it("test_profile_rows_numeric_balance_matches_tokens_label", async () => {
    const time = await import(pathToFileURL(join(libDir, "time.ts")).href);
    assert.equal(typeof time.tokensLabel, "function");
    const tokensLabel = time.tokensLabel as (value: string | number) => string;
    const pairs: Array<[string | number, string | number]> = [
      [180.5, 100],
      [-1.5, 0],
      ["180.50", "12.50"],
      ["1500.00", "0.00"],
      ["nope", "12.5"],
    ];
    for (const [token, deposit] of pairs) {
      const loaded = await loadRows(filled({ token_balance: token, deposit_balance: deposit }));
      assert.equal(
        loaded.error,
        undefined,
        because(loaded.error, `balance ${String(token)} / ${String(deposit)} must render`),
      );
      assert.equal(valueOf(loaded.rows, "Token balance"), tokensLabel(token));
      assert.equal(valueOf(loaded.rows, "Deposit balance"), tokensLabel(deposit));
    }
  });

  it("test_member_nav_refs_are_complete_pngs", () => {
    for (const [width, [px, py]] of Object.entries(VIEWPORT)) {
      for (const name of MEMBER_SHOTS) {
        assertCompletePng(readRefPng(width, name), px, py, `${width}/${name}`);
      }
    }
  });

  it("test_member_nav_refs_survive_unified_diff", () => {
    for (const [width, [px, py]] of Object.entries(VIEWPORT)) {
      for (const name of MEMBER_SHOTS) {
        const b64Path = join(libDir, "../visual/member-nav-ref", width, `${name}.b64`);
        const text = readFileSync(b64Path, "utf8");
        const round = bytesAfterDiffHeaderDecode(text);
        assertCompletePng(round, px, py, `${width}/${name}`);
        assert.equal(round.equals(readRefPng(width, name)), true, `${width}/${name} diff decode changed bytes`);
      }
    }
  });

  it("test_visual_build_does_not_install_chromium", () => {
    const script = readFileSync(join(libDir, "../visual/build-web.sh"), "utf8");
    assert.doesNotMatch(script, /playwright install/, "visual build must not install a browser");
    assert.doesNotMatch(script, /chrome-headless-shell/);
    assert.doesNotMatch(script, /member-login/);
    assert.doesNotMatch(script, /member-detail/);
  });

  it("test_visual_build_compares_committed_member_screenshots", () => {
    const script = readFileSync(join(libDir, "../visual/build-web.sh"), "utf8");
    assert.doesNotMatch(
      script,
      /member-nav-ref/,
      "visual build must compare the committed screenshots, not replace them from member-nav-ref",
    );
    assert.doesNotMatch(
      script,
      /base64 -d/,
      "visual build must not decode screenshot bytes over visual/screenshots",
    );
    assert.match(script, /npm run build/);
    for (const [width, [px, py]] of Object.entries(VIEWPORT)) {
      for (const name of MEMBER_SHOTS) {
        const pngPath = join(libDir, "../visual/screenshots", width, `${name}.png`);
        assert.equal(
          existsSync(pngPath),
          true,
          `committed member screenshot missing: ${width}/${name}.png`,
        );
        const committed = readFileSync(pngPath);
        assertCompletePng(committed, px, py, `screenshots/${width}/${name}`);
        assert.equal(
          committed.equals(readRefPng(width, name)),
          true,
          `${width}/${name}.png is not the member-nav-ref capture`,
        );
      }
    }
    const config = readFileSync(join(libDir, "../playwright.config.ts"), "utf8");
    assert.match(config, /maxDiffPixelRatio:\s*0\.01/);
    assert.match(
      config,
      /snapshotPathTemplate:\s*"\{testDir\}\/screenshots\/\{projectName\}\/\{arg\}\{ext\}"/,
    );
    assert.doesNotMatch(config, /member-nav-ref/);
    const pages = readFileSync(join(libDir, "../visual/pages.spec.ts"), "utf8");
    assert.match(pages, /const MAX_LAYOUT_SHIFT = 0\.1/);
    assert.doesNotMatch(pages, /maxDiffPixelRatio/);
    const attributesPath = join(libDir, "../../../../.gitattributes");
    assert.equal(existsSync(attributesPath), true, "member screenshot diff attribute missing");
    const attributes = readFileSync(attributesPath, "utf8");
    for (const name of MEMBER_SHOTS) {
      assert.match(
        attributes,
        new RegExp(
          `^apps/project-car/web/visual/screenshots/\\*/${name}\\.png diff$`,
          "m",
        ),
        `${name}.png must diff as text so the pull request diff carries the bytes`,
      );
    }
  });
});
