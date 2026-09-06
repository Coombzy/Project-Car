import type { PricingRule } from "../lib/config";
import { overlayIsNonStandard, tokensLabel } from "../lib/time";

export function BookingCost({
  reservedTokens,
  pricingRule,
}: {
  reservedTokens: string;
  pricingRule?: PricingRule | null;
}) {
  const overlay = pricingRule && overlayIsNonStandard(pricingRule.advance_multiplier);
  return (
    <div className="booking-cost">
      <span className="token-badge">{tokensLabel(reservedTokens)} tok</span>
      {pricingRule ? (
        <span className={`band-chip band-${pricingRule.band_id}`}>{pricingRule.band_label}</span>
      ) : null}
      {overlay ? <span className="overlay-chip">{pricingRule.overlay_label}</span> : null}
    </div>
  );
}
