import { OwnerShell } from "../../components/owner-shell";
import { PlanOffer } from "../../components/plan-offer";
import { handlePageError } from "../../lib/page";
import { getMe, listTiers } from "../../lib/shop-api";
import { tokensLabel } from "../../lib/time";
import {
  grantPeriodAllocationAction,
  listPricingSettings,
  patchPricingAction,
  patchTierAction,
  type PricingMultiplier,
} from "./actions";

export const dynamic = "force-dynamic";

export default async function TiersPage({
  searchParams,
}: {
  searchParams: Promise<{ error?: string; granted?: string; skipped?: string }>;
}) {
  try {
    const params = await searchParams;
    const notice = allocationNotice(params.granted, params.skipped);
    const [me, tiers, pricing] = await Promise.all([getMe(), listTiers(), listPricingSettings()]);
    return (
      <OwnerShell email={me.email} current="tiers">
        <p className="eyebrow">GET /tiers</p>
        <h1>Tiers / settings</h1>
        <p className="lede">
          Basic and Premium are seeded placeholders — names and allowances are
          data. These are not live prices. The shop is not open.
        </p>
        {params.error ? <div className="banner error">{params.error}</div> : null}
        {notice ? <div className="banner">{notice}</div> : null}

        <form action={grantPeriodAllocationAction} className="card" style={{ marginBottom: "0.9rem" }}>
          <div className="hoist-card-head">
            <h2 style={{ marginTop: 0 }}>Period allotment</h2>
          </div>
          <p className="muted">
            Grants each active member their tier included tokens once for this
            calendar month (Mountain Time). A second click this month inserts
            nothing. This button is the trigger. There is no background job. No
            Stripe. The shop is not open.
          </p>
          <div className="actions">
            <button type="submit">Grant this month</button>
          </div>
        </form>

        <form action={patchPricingAction} className="card" style={{ marginBottom: "0.9rem" }}>
          <div className="hoist-card-head">
            <h2 style={{ marginTop: 0 }}>Band and overlay multipliers</h2>
          </div>
          <p className="muted">
            Seeded placeholders. A quote after an edit uses the stored multiplier.
            Cancel and complete keep the number locked on the booking. Not live prices.
            The shop is not open.
          </p>
          <p className="eyebrow">Bands</p>
          <div className="form-grid" style={{ gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))" }}>
            {pricing.bands.map((row) => (
              <MultiplierField key={row.id} prefix="band" row={row} />
            ))}
          </div>
          <p className="eyebrow" style={{ marginTop: "0.85rem" }}>Overlays</p>
          <div className="form-grid" style={{ gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))" }}>
            {pricing.overlays.map((row) => (
              <MultiplierField key={row.id} prefix="overlay" row={row} />
            ))}
          </div>
          <div className="actions">
            <button type="submit">Save multipliers</button>
          </div>
        </form>

        {tiers.length === 0 ? (
          <div className="banner empty">No tiers. Run API migrations, then seed.</div>
        ) : (
          <div className="tier-list">
            {tiers.map((tier) => (
              <form key={tier.name} action={patchTierAction} className="card">
                <input type="hidden" name="name" value={tier.name} />
                <div className="hoist-card-head">
                  <h2>{tier.display_name}</h2>
                  <span className="muted">{tier.name}</span>
                </div>
                <PlanOffer plan={tier} framed={false} />
                <div className="form-grid">
                  <label>
                    Display name
                    <input name="display_name" defaultValue={tier.display_name} required />
                  </label>
                  <label>
                    Price, CAD per month, before GST
                    <input name="price" defaultValue={tokensLabel(tier.price)} />
                  </label>
                  <label>
                    Included tokens
                    <input
                      name="included_tokens"
                      type="number"
                      min="0"
                      defaultValue={tier.included_tokens}
                    />
                  </label>
                  <label>
                    Booking window (days)
                    <input
                      name="booking_window_days"
                      type="number"
                      min="1"
                      defaultValue={tier.booking_window_days}
                    />
                  </label>
                  <label>
                    Max simultaneous
                    <input
                      name="max_simultaneous_bookings"
                      type="number"
                      min="1"
                      defaultValue={tier.max_simultaneous_bookings}
                    />
                  </label>
                  <label>
                    Notes
                    <input name="notes" defaultValue={tier.notes ?? ""} />
                  </label>
                </div>
                <div className="actions">
                  <button type="submit">Save {tier.display_name}</button>
                </div>
              </form>
            ))}
          </div>
        )}
      </OwnerShell>
    );
  } catch (error) {
    const message = await handlePageError(error);
    return (
      <OwnerShell current="tiers">
        <h1>Tiers</h1>
        <div className="banner error">{message}</div>
      </OwnerShell>
    );
  }
}

function allocationNotice(granted: string | undefined, skipped: string | undefined): string | null {
  if (!granted || !/^\d+$/.test(granted)) {
    return null;
  }
  const skippedCount = skipped && /^\d+$/.test(skipped) ? skipped : "0";
  return `Granted ${granted} this month. ${skippedCount} already had this month's allotment.`;
}

function MultiplierField({ prefix, row }: { prefix: "band" | "overlay"; row: PricingMultiplier }) {
  return (
    <label>
      {row.label}
      <input
        name={`${prefix}:${row.id}`}
        inputMode="decimal"
        defaultValue={tokensLabel(row.multiplier)}
        required
      />
    </label>
  );
}
