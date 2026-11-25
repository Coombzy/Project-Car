export const OFFICIAL_1440_BODY = {
  tokensAtRisk: "Tokens at risk 1",
  adaTokens: "375.00",
  bands: ["OFF-PEAK", "NORMAL", "EVENING", "PEAK"],
} as const;

const DRIFTED_1440 = [
  "Tokens at risk 3",
  "156.25",
  "WEEKDAY DAY (BASE)",
  "WEEKDAY EVENING",
  "WEEKEND",
  "FRI EVE",
  "LATE NIGHT",
  "EARLY MORNING",
] as const;

function present(source: string, needle: string): boolean {
  const escaped = needle.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const re = new RegExp(`(?<![A-Za-z0-9-])${escaped}(?![A-Za-z0-9-])`, "g");
  for (const match of source.matchAll(re)) {
    const at = match.index ?? 0;
    const prefix = /^[A-Za-z]+$/.test(needle) ? /([A-Za-z]+) $/.exec(source.slice(0, at))?.[1] : "";
    if (prefix && DRIFTED_1440.some((label) => label.startsWith(`${prefix} ${needle}`))) continue;
    return true;
  }
  return false;
}

/** Missing official phrases, plus stale labels still present in the body. */
export function officialBodyDrift(source: string): string[] {
  const required = [OFFICIAL_1440_BODY.tokensAtRisk, OFFICIAL_1440_BODY.adaTokens, ...OFFICIAL_1440_BODY.bands];
  return [...required.filter((text) => !present(source, text)), ...officialStaleHits(source)];
}

/** Stale labels still in the body. Case-folded so a title-case label still counts. */
export function officialStaleHits(source: string): string[] {
  const folded = source.toUpperCase();
  return DRIFTED_1440.filter((label) => present(folded, label.toUpperCase()));
}
