// No sibling imports: node --test loads this file as ESM and will not resolve
// extensionless paths. The shapes match PricingRule / PricingSegment in config.ts.

export type SegmentLine = {
  band_id: string;
  band_label: string;
  band_multiplier: string;
  hours: string;
  tokens: string;
  start?: string;
};

export type SegmentRule = {
  hours: string;
  band_multiplier: string;
  advance_multiplier: string;
  final_reserve_cost: string;
  band_label: string;
  overlay_label: string;
  segments?: SegmentLine[] | null;
};

export function segmentRowKey(segment: { band_id: string; start: string }): string {
  return `${segment.band_id}-${segment.start}`;
}

function tokenText(value: string): string {
  const amount = Number(value);
  if (Number.isNaN(amount)) {
    return value;
  }
  return Number.isInteger(amount) ? String(amount) : amount.toFixed(2);
}

export function segmentCostLines(rule: Pick<SegmentRule, "segments">): string[] {
  const segments = rule.segments ?? [];
  return segments.map(
    (segment) =>
      `${segment.band_label} · ${segment.hours}h × ${segment.band_multiplier} · ${segment.tokens}`,
  );
}

export function spansBands(rule: Pick<SegmentRule, "segments">): boolean {
  const ids = new Set((rule.segments ?? []).map((segment) => segment.band_id));
  return ids.size > 1;
}

export function showSingleBandLabel(rule: Pick<SegmentRule, "segments">): boolean {
  return !spansBands(rule);
}

export function segmentTotalLine(rule: Pick<SegmentRule, "final_reserve_cost">): string {
  return `Total · ${rule.final_reserve_cost}`;
}

export function quoteSegmentLines(rule: SegmentRule): string[] {
  const lines = segmentCostLines(rule);
  if (lines.length === 0) {
    return lines;
  }
  return [...lines, segmentTotalLine(rule)];
}

export function pricingRuleSummary(rule: SegmentRule): string {
  if (!spansBands(rule)) {
    return `${rule.hours}h × 100 × ${rule.band_multiplier} × ${rule.advance_multiplier} = ${tokenText(rule.final_reserve_cost)} · ${rule.band_label} · ${rule.overlay_label}`;
  }
  return [...segmentCostLines(rule), segmentTotalLine(rule), rule.overlay_label].join(" · ");
}
