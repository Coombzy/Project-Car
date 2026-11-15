/**Left side of the reserve equation. One band keeps hours × 100 × band. Mixed bands list each hour. */

export type ReserveSegment = {
  band_tokens: string;
};

export type ReserveMath = {
  hours: string;
  band_multiplier: string;
  advance_multiplier: string;
  fill_multiplier?: string;
  segments?: ReserveSegment[];
};

export function reserveFactors(rule: ReserveMath): string {
  const advance = rule.advance_multiplier;
  const fill = rule.fill_multiplier && rule.fill_multiplier !== "1" ? rule.fill_multiplier : "";
  const segments = rule.segments ?? [];
  const bands = new Set(segments.map((segment) => segment.band_tokens));
  if (segments.length > 1 && bands.size > 1) {
    const sum = segments.map((segment) => segment.band_tokens).join(" + ");
    const multipliers = [advance !== "1" ? advance : "", fill].filter((part) => part !== "");
    if (multipliers.length === 0) {
      return sum;
    }
    return `(${sum}) × ${multipliers.join(" × ")}`;
  }
  const fillPart = fill === "" ? "" : ` × ${fill}`;
  return `${rule.hours}h × 100 × ${rule.band_multiplier} × ${advance}${fillPart}`;
}
