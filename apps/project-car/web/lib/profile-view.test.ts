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
  token_balance: string;
  deposit_balance: string;
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

  it("test_visual_member_pages_include_profile", () => {
    const spec = readFileSync(join(libDir, "../visual/pages.spec.ts"), "utf8");
    const list = spec.match(/const MEMBER_PAGES: Shot\[\] = \[([\s\S]*?)\];/);
    assert.ok(list, "MEMBER_PAGES list is missing");
    assert.match(
      list[1],
      /\{ name: "member-profile", path: "\/member\/profile" \}/,
      "screenshot job must walk /member/profile",
    );
  });
});
