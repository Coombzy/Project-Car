import type { PricingRule } from "../lib/config";
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
  return (
    <div className="booking-cost">
      <span className="token-badge">{tokensLabel(cost)} tok</span>
      {pricingRule ? (
        <span className={`band-chip band-${pricingRule.band_id}`}>{pricingRule.band_label}</span>
      ) : null}
      {overlay ? <span className="overlay-chip">{pricingRule.overlay_label}</span> : null}
      {fill ? <span className="fill-chip">{pricingRule.fill_label ?? "Fill"}</span> : null}
    </div>
  );
}
