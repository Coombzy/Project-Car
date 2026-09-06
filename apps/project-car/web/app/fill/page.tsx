import { OwnerShell } from "../../components/owner-shell";
import { handlePageError } from "../../lib/page";
import { getMe, listFillOutbox, previewFill } from "../../lib/shop-api";
import { formatShopDateTime, formatShopTime, tokensLabel } from "../../lib/time";
import { notifyFillAction } from "./actions";

export const dynamic = "force-dynamic";

export default async function FillPage({
  searchParams,
}: {
  searchParams: Promise<{ error?: string; notice?: string }>;
}) {
  try {
    const params = await searchParams;
    const [me, preview, outbox] = await Promise.all([getMe(), previewFill(), listFillOutbox()]);
    return (
      <OwnerShell email={me.email} current="fill">
        <p className="eyebrow">GET /fill/preview · America/Regina</p>
        <h1>Fill the gaps</h1>
        <p className="lede">
          Next-day open hours on customer bays only (shop hoist excluded). Discount
          is 10–25% from how empty tomorrow is — more open hours, higher discount.
          Tokens only. Not a public price. The shop is not open.
        </p>
        {params.error ? <div className="banner error">{params.error}</div> : null}
        {params.notice ? <div className="banner empty">{params.notice}</div> : null}

        <section className="card">
          <div className="hoist-card-head">
            <h2>Tomorrow {preview.target_date}</h2>
            <span className={`pill urgency-${preview.urgency}`}>{preview.urgency}</span>
          </div>
          <p className="muted">
            Window {formatShopTime(preview.window_start)}–{formatShopTime(preview.window_end)}{" "}
            {preview.tz}. Source: {preview.source}. {preview.bay_count} customer bay
            {preview.bay_count === 1 ? "" : "s"}.
          </p>
          <dl className="fill-stats">
            <div>
              <dt>Open hours</dt>
              <dd>{tokensLabel(preview.open_hours)}</dd>
            </div>
            <div>
              <dt>Booked</dt>
              <dd>{tokensLabel(preview.booked_hours)}</dd>
            </div>
            <div>
              <dt>Capacity</dt>
              <dd>{tokensLabel(preview.capacity_hours)}</dd>
            </div>
            <div>
              <dt>Suggested discount</dt>
              <dd>{tokensLabel(preview.discount_pct)}%</dd>
            </div>
            <div>
              <dt>Fill factor</dt>
              <dd>× {tokensLabel(preview.fill_multiplier)}</dd>
            </div>
          </dl>
          {preview.gaps.length === 0 ? (
            <p className="muted">No customer-bay openings tomorrow in the fill window.</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Bay</th>
                  <th>Open</th>
                  <th>Hours</th>
                </tr>
              </thead>
              <tbody>
                {preview.gaps.map((gap) => (
                  <tr key={`${gap.hoist_id}-${gap.start_at}`}>
                    <td>{gap.hoist_name}</td>
                    <td>
                      {formatShopTime(gap.start_at)}–{formatShopTime(gap.end_at)}
                    </td>
                    <td>{tokensLabel(gap.hours)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>

        <section className="card" style={{ marginTop: "1.4rem" }}>
          <h2>Notify active members</h2>
          <p className="lede">
            Email uses SMTP when configured, otherwise a durable stub that records
            sent. SMS and push adapters are stubs for Twilio / Inbox later. Dry-run
            writes the outbox without publishing the offer.
          </p>
          <form action={notifyFillAction} className="stack-form">
            <div className="form-grid">
              <label>
                Discount % (10–25)
                <input
                  name="discount_pct"
                  type="number"
                  min="10"
                  max="25"
                  step="0.01"
                  defaultValue={tokensLabel(preview.discount_pct)}
                />
              </label>
              <label>
                Channels
                <span className="channel-row">
                  <label className="inline-check">
                    <input type="checkbox" name="email" defaultChecked /> Email
                  </label>
                  <label className="inline-check">
                    <input type="checkbox" name="sms" /> SMS (stub)
                  </label>
                  <label className="inline-check">
                    <input type="checkbox" name="push" /> Push (stub)
                  </label>
                </span>
              </label>
            </div>
            <div className="actions">
              <button type="submit" name="mode" value="dry_run">
                Dry-run
              </button>
              <button type="submit" name="mode" value="send" disabled={!preview.applies}>
                Publish and send
              </button>
            </div>
          </form>
        </section>

        <section className="card" style={{ marginTop: "1.4rem" }}>
          <h2>Outbox</h2>
          {outbox.length === 0 ? (
            <p className="muted">No notification rows yet.</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>When</th>
                  <th>Channel</th>
                  <th>To</th>
                  <th>Status</th>
                  <th>Subject</th>
                </tr>
              </thead>
              <tbody>
                {outbox.map((row) => (
                  <tr key={row.id}>
                    <td>{formatShopDateTime(row.created_at)}</td>
                    <td>{row.channel}</td>
                    <td>{row.to_address ?? "—"}</td>
                    <td>
                      {row.status}
                      {row.last_error ? ` · ${row.last_error}` : ""}
                    </td>
                    <td className="notes">{row.subject ?? "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>
      </OwnerShell>
    );
  } catch (error) {
    const message = await handlePageError(error);
    return (
      <OwnerShell current="fill">
        <p className="eyebrow">Fill the gaps</p>
        <h1>Fill the gaps</h1>
        <div className="banner error">{message}</div>
      </OwnerShell>
    );
  }
}
