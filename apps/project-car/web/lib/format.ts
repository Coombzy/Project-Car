const HOURS = /^(-?)(\d+)(?:\.(\d+))?$/;

const LEDGER_KIND_LABELS: Readonly<Record<string, string>> = {
  booking_reserve: "Booking hold",
  booking_debit: "Booking debit",
  booking_refund: "Booking refund",
  monthly_allocation: "Monthly grant",
  admin_adjustment: "Owner adjustment",
  token_purchase: "Token purchase",
};

export function formatHours(value: string): string {
  const match = HOURS.exec(value.trim());
  if (!match) {
    return `${value.trim()} h`;
  }
  const sign = match[1];
  const whole = match[2];
  const fraction = (match[3] ?? "").replace(/0+$/, "");
  const amount = fraction.length > 0 ? `${sign}${whole}.${fraction}` : `${sign}${whole}`;
  return `${amount} h`;
}

export function tierName(slug: string, tiers: ReadonlyArray<{ slug: string; name: string }>): string {
  const tier = tiers.find((row) => row.slug === slug);
  return tier ? tier.name : slug;
}

export function ledgerKindLabel(kind: string): string {
  return LEDGER_KIND_LABELS[kind] ?? kind;
}
