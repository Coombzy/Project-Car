import { extraHoursLine, gstLine } from "../lib/booking-calendar";
import type { TokenTransaction } from "../lib/config";
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
        {rule.hours}h × 100 × {rule.band_multiplier} × {rule.advance_multiplier} = {tokensLabel(rule.final_reserve_cost)} · {rule.band_label}
      </span>
    );
  }
  return <span>—</span>;
}
