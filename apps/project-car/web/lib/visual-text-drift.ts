export const OFFICIAL_1440_BODY = {
  tokensAtRisk: "Tokens at risk 1",
  adaTokens: "375.00",
  bands: ["OFF-PEAK", "NORMAL", "EVENING", "PEAK"],
} as const;

const DRIFTED = [
  "Tokens at risk 3",
  "156.25",
  "WEEKDAY DAY (BASE)",
  "WEEKDAY EVENING",
  "WEEKEND",
  "FRI EVE",
  "LATE NIGHT",
  "EARLY MORNING",
] as const;

const REQUIRED = [
  OFFICIAL_1440_BODY.tokensAtRisk,
  OFFICIAL_1440_BODY.adaTokens,
  ...OFFICIAL_1440_BODY.bands,
];

function present(source: string, needle: string): boolean {
  const escaped = needle.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return new RegExp(`(?:^|[^A-Za-z0-9])${escaped}(?=$|[^A-Za-z0-9])`).test(source);
}

/** Missing official phrases, plus stale labels that are still in the body. */
export function officialBodyDrift(source: string): string[] {
  const missing = REQUIRED.filter((text) => !present(source, text));
  const drifted = DRIFTED.filter((label) => present(source, label));
  return [...missing, ...drifted];
}
