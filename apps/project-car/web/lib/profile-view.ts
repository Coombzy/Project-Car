/** Read-only display rows for `/member/profile`. */

export const PROFILE_MISSING = "Not on file";
export const WAIVER_UNSIGNED = "Not signed";

export type ProfileSource = {
  name: string;
  email: string;
  tier_name: string;
  status: string;
  phone: string | null;
  waiver_signed_at: string | null;
  waiver_version?: string | null;
  emergency_contact_name: string | null;
  emergency_contact_phone: string | null;
  token_balance: string;
  deposit_balance: string;
};

export type ProfileRow = {
  label: string;
  value: string;
};

function present(value: string | null | undefined): string | null {
  if (value == null) {
    return null;
  }
  const trimmed = value.trim();
  return trimmed === "" ? null : trimmed;
}

/** Same digits as `tokensLabel` in time.ts. Local so this file has no extension import. */
function balanceLabel(value: string): string {
  const amount = Number(value);
  if (Number.isNaN(amount)) {
    return value;
  }
  return Number.isInteger(amount) ? String(amount) : amount.toFixed(2);
}

function waiverValue(signedAt: string | null, version: string | null | undefined): string {
  if (present(signedAt) == null) {
    return WAIVER_UNSIGNED;
  }
  const waiverVersion = present(version);
  return waiverVersion == null ? "Signed" : `Signed · ${waiverVersion}`;
}

function emergencyValue(name: string | null, phone: string | null): string {
  const parts: string[] = [];
  const contactName = present(name);
  const contactPhone = present(phone);
  if (contactName) {
    parts.push(contactName);
  }
  if (contactPhone) {
    parts.push(contactPhone);
  }
  return parts.length === 0 ? PROFILE_MISSING : parts.join(" · ");
}

export function profileRows(member: ProfileSource): ProfileRow[] {
  return [
    { label: "Name", value: present(member.name) ?? PROFILE_MISSING },
    { label: "Email", value: present(member.email) ?? PROFILE_MISSING },
    { label: "Tier", value: present(member.tier_name) ?? PROFILE_MISSING },
    { label: "Status", value: present(member.status) ?? PROFILE_MISSING },
    { label: "Phone", value: present(member.phone) ?? PROFILE_MISSING },
    { label: "Waiver", value: waiverValue(member.waiver_signed_at, member.waiver_version) },
    {
      label: "Emergency contact",
      value: emergencyValue(member.emergency_contact_name, member.emergency_contact_phone),
    },
    { label: "Token balance", value: balanceLabel(member.token_balance) },
    { label: "Deposit balance", value: balanceLabel(member.deposit_balance) },
  ];
}
