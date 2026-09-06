import Link from "next/link";

import { BookingCost } from "../../components/booking-cost";
import { MemberShell } from "../../components/member-shell";
import { StatusPill } from "../../components/status-pill";
import { handleMemberPageError } from "../../lib/page";
import { getMemberMe } from "../../lib/shop-api";
import { formatShopDateTime, tokensLabel } from "../../lib/time";

export const dynamic = "force-dynamic";

export default async function MemberHomePage() {
  try {
    const me = await getMemberMe();
    const open = me.bookings.filter(
      (booking) =>
        booking.status === "pending" || booking.status === "confirmed" || booking.status === "active",
    );
    return (
      <MemberShell email={me.email} current="home">
        <p className="eyebrow">Member · demo</p>
        <h1>Your tokens</h1>
        <p className="lede">
          Balance is a cached ledger sum. Book customer bays 1–5 within your
          {` ${me.tier_name} `}
          window. The shop hoist is Owner-only. Sample data — the shop is not
          open.
        </p>

        <div className="metrics">
          <div className="metric">
            <span className="eyebrow">Balance</span>
            <b>{tokensLabel(me.token_balance)}</b>
          </div>
          <div className="metric">
            <span className="eyebrow">Tier</span>
            <b>{me.tier_name}</b>
          </div>
          <div className="metric">
            <span className="eyebrow">Period allotment</span>
            <b>{tokensLabel(me.included_tokens)}</b>
          </div>
          <div className="metric">
            <span className="eyebrow">Booking window</span>
            <b>{me.booking_window_days}d</b>
          </div>
        </div>

        <p>
          <Link href="/member/schedule">Book a customer bay →</Link>
        </p>

        <h2>Open bookings</h2>
        {open.length === 0 ? (
          <div className="banner empty">No pending, confirmed, or active bookings.</div>
        ) : (
          <div className="card">
            <table>
              <thead>
                <tr>
                  <th>When</th>
                  <th>Bay</th>
                  <th>Status</th>
                  <th>Reserved</th>
                </tr>
              </thead>
              <tbody>
                {open.map((booking) => (
                  <tr key={booking.id}>
                    <td>{formatShopDateTime(booking.start_at)}</td>
                    <td>{booking.hoist_name}</td>
                    <td>
                      <StatusPill value={booking.status} />
                    </td>
                    <td>
                      <BookingCost
                        reservedTokens={booking.reserved_tokens}
                        pricingRule={booking.pricing_rule}
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <h2>Token ledger</h2>
        {me.tokens.length === 0 ? (
          <div className="banner empty">No ledger rows yet.</div>
        ) : (
          <div className="card">
            <table>
              <thead>
                <tr>
                  <th>When</th>
                  <th>Kind</th>
                  <th>Amount</th>
                  <th>Note</th>
                  <th>Pricing</th>
                </tr>
              </thead>
              <tbody>
                {me.tokens.map((row) => (
                  <tr key={row.id}>
                    <td>{formatShopDateTime(row.created_at)}</td>
                    <td>{row.kind}</td>
                    <td>{tokensLabel(row.amount)}</td>
                    <td className="notes">{row.note ?? "—"}</td>
                    <td className="notes">
                      {row.meta?.pricing_rule
                        ? `${row.meta.pricing_rule.hours}h × 100 × ${row.meta.pricing_rule.band_multiplier} × ${row.meta.pricing_rule.advance_multiplier} = ${tokensLabel(row.meta.pricing_rule.final_reserve_cost)} · ${row.meta.pricing_rule.band_label} · ${row.meta.pricing_rule.overlay_label}`
                        : "—"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </MemberShell>
    );
  } catch (error) {
    const message = await handleMemberPageError(error);
    return (
      <MemberShell current="home">
        <p className="eyebrow">Member · demo</p>
        <h1>Your tokens</h1>
        <div className="banner error">{message}</div>
      </MemberShell>
    );
  }
}
