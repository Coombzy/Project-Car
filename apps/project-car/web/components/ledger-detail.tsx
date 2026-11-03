import { extraHoursLine, gstLine } from "../lib/booking-calendar";
import type { TokenTransaction } from "../lib/config";
import { reserveFactors } from "../lib/pricing-math";
import { tokensLabel } from "../lib/time";

export function LedgerDetail({ meta }: { meta: TokenTransaction["meta"] }) {
  const gst = gstLine(meta);
  if (gst) {
    return <span>{gst}</span>;
  }
  const extra = extraHoursLine(meta);
  if (extra) {
    return <span>{extra}</span>;
  }
  if (meta?.pricing_rule) {
    const rule = meta.pricing_rule;
    return (
      <span>
        {reserveFactors(rule)} = {tokensLabel(rule.final_reserve_cost)} · {rule.band_label} · {rule.overlay_label}
      </span>
    );
  }
  return <span>—</span>;
}
