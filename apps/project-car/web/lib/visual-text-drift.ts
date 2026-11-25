export const OFFICIAL_1440_BODY = {
  tokensAtRisk: "Tokens at risk 3",
  adaTokens: "156.25",
  bands: ["WEEKDAY DAY (BASE)", "WEEKDAY EVENING", "WEEKEND/FRI EVE", "LATE NIGHT"],
} as const;

const DRIFTED = ["Tokens at risk 1", "375", "OFF-PEAK", "NORMAL", "EVENING", "PEAK"] as const;

const REQUIRED = [
  OFFICIAL_1440_BODY.tokensAtRisk,
  OFFICIAL_1440_BODY.adaTokens,
  ...OFFICIAL_1440_BODY.bands,
];

function present(source: string, needle: string): boolean {
  const escaped = needle.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return new RegExp(`(?:^|[^A-Za-z0-9])${escaped}(?=$|[^A-Za-z0-9])`).test(source);
}

/** Missing official phrases, plus drifted labels still present after those phrases are removed. */
export function officialBodyDrift(source: string): string[] {
  const missing = REQUIRED.filter((text) => !source.includes(text));
  let rest = source;
  for (const text of REQUIRED) {
    rest = rest.split(text).join("\n");
  }
  return [...missing, ...DRIFTED.filter((label) => present(rest, label))];
}
