import { OwnerShell } from "../../components/owner-shell";
import { handlePageError } from "../../lib/page";
import { getMe, listTiers } from "../../lib/shop-api";
import { tokensLabel } from "../../lib/time";
import { patchTierAction } from "./actions";

export const dynamic = "force-dynamic";

export default async function TiersPage({
  searchParams,
}: {
  searchParams: Promise<{ error?: string }>;
}) {
  try {
    const params = await searchParams;
    const [me, tiers] = await Promise.all([getMe(), listTiers()]);
    return (
      <OwnerShell email={me.email} current="tiers">
        <p className="eyebrow">GET /tiers</p>
        <h1>Tiers / settings</h1>
        <p className="lede">
          Basic, Pro, and Weekly are placeholders — names and allowances are
          data. These are not published live prices. The shop is not open.
        </p>
        {params.error ? <div className="banner error">{params.error}</div> : null}

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
                <div className="form-grid">
                  <label>
                    Display name
                    <input name="display_name" defaultValue={tier.display_name} required />
                  </label>
                  <label>
                    Placeholder price
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
