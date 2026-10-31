import type { PricingRule } from "../lib/config";
import { segmentCostLines, showSingleBandLabel } from "../lib/booking-segments";
import { fillApplies, overlayIsNonStandard, tokensLabel } from "../lib/time";

export function BookingCost({
  reservedTokens,
  pricingRule,
}: {
  reservedTokens: string;
  pricingRule?: PricingRule | null;
}) {
  const overlay = pricingRule && overlayIsNonStandard(pricingRule.advance_multiplier);
  const fill = pricingRule && fillApplies(pricingRule.fill_multiplier);
  const cost = pricingRule?.final_reserve_cost ?? reservedTokens;
  const singleBand = !pricingRule || showSingleBandLabel(pricingRule);
  return (
    <div className="booking-cost">
      <span className="token-badge">{tokensLabel(cost)} tok</span>
      {pricingRule && singleBand ? (
        <span className={`band-chip band-${pricingRule.band_id}`}>{pricingRule.band_label}</span>
      ) : null}
      {pricingRule && !singleBand
        ? (pricingRule.segments ?? []).map((segment) => (
            <span key={`${segment.band_id}-${segment.start}`} className={`band-chip band-${segment.band_id}`}>
              {segmentCostLines({ segments: [segment] })[0]}
            </span>
          ))
        : null}
      {overlay ? <span className="overlay-chip">{pricingRule.overlay_label}</span> : null}
      {fill ? <span className="fill-chip">{pricingRule.fill_label ?? "Fill"}</span> : null}
    </div>
  );
}
