import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath, pathToFileURL } from "node:url";

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

  it("test_member_profile_proof_does_not_use_screenshot_sidecar", () => {
    const self = readFileSync(fileURLToPath(import.meta.url), "utf8");
    const kept = [
      "test_profile_rows_missing_phone_shows_not_on_file",
      "test_profile_rows_unsigned_waiver_shows_not_signed",
      "test_profile_rows_shows_the_member_record",
      "test_profile_rows_missing_emergency_contact_shows_not_on_file",
      "test_profile_rows_missing_balance_shows_not_on_file",
      "test_member_profile_page_is_read_only_and_points_at_chat",
      "test_member_nav_has_profile_link",
      "test_screenshot_walk_includes_member_profile",
      "test_profile_rows_numeric_balance_matches_tokens_label",
    ];
    for (const name of kept) {
      assert.equal(self.includes(`it("${name}"`), true, `${name} must stay`);
    }
    const removed = [
      "test_member_nav_refs_are_complete_pngs",
      "test_member_nav_refs_survive_unified_diff",
      "test_visual_build_does_not_install_chromium",
      "test_visual_build_compares_committed_member_screenshots",
    ];
    for (const name of removed) {
      assert.equal(self.includes(`it("${name}"`), false, `${name} must be deleted`);
    }
    assert.equal(
      existsSync(join(libDir, "../visual/screenshots")),
      true,
      "keep the visual/screenshots refresh",
    );
    assert.equal(
      existsSync(join(libDir, "../visual/member-nav-ref")),
      false,
      "delete visual/member-nav-ref; screenshot proof is visual/screenshots",
    );
    const attributesPath = join(libDir, "../../../../.gitattributes");
    const attributes = existsSync(attributesPath) ? readFileSync(attributesPath, "utf8") : "";
    assert.doesNotMatch(
      attributes,
      /^apps\/project-car\/web\/visual\/screenshots\/\*\/member-.*\.png diff$/m,
      "delete .gitattributes rules that mark member screenshots as a text diff",
    );
    const pages = readFileSync(join(libDir, "../visual/pages.spec.ts"), "utf8");
    assert.match(pages, /const MAX_LAYOUT_SHIFT = 0\.1/);
    assert.doesNotMatch(pages, /maxDiffPixelRatio/);
    const config = readFileSync(join(libDir, "../playwright.config.ts"), "utf8");
    assert.match(config, /maxDiffPixelRatio:\s*0\.01/);
  });

});
