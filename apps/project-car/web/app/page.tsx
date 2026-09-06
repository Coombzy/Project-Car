import Link from "next/link";

import { OwnerShell } from "../components/owner-shell";
import { StatusPill } from "../components/status-pill";
import { getDashboard, getMe } from "../lib/shop-api";
import { handlePageError } from "../lib/page";
import { BookingCost } from "../components/booking-cost";
import { formatShopDateTime, formatShopTime, tokensLabel } from "../lib/time";

export const dynamic = "force-dynamic";

export default async function DashboardPage() {
  try {
    const [me, dash] = await Promise.all([getMe(), getDashboard()]);
    return (
      <OwnerShell email={me.email} current="home">
        <p className="eyebrow">Owner · demo</p>
        <h1>Shop dashboard</h1>
        <p className="lede">
          Today&apos;s bays (6 hoists, one shop-priority), bookings, waitlist,
          and members running low on tokens. Seeded sample data — not a live
          shop.
        </p>
        <div className="metrics">
          <div className="metric">
            <span className="eyebrow">Hoists</span>
            <b>{dash.hoists.length}</b>
          </div>
          <div className="metric">
            <span className="eyebrow">Today&apos;s bookings</span>
            <b>{dash.today_bookings.length}</b>
          </div>
          <div className="metric">
            <span className="eyebrow">Waitlist</span>
            <b>{dash.waitlist_count}</b>
          </div>
          <div className="metric">
            <span className="eyebrow">Tokens at risk</span>
            <b>{dash.token_at_risk.length}</b>
          </div>
        </div>

        <h2>Hoists</h2>
        {dash.hoists.length === 0 ? (
          <div className="banner empty">
            No hoists yet. Run <code>python -m app.seed</code> in the API.
          </div>
        ) : (
          <div className="hoist-grid">
            {dash.hoists.map((hoist) => (
              <article key={hoist.id} className="card hoist-card">
                <div className="hoist-card-head">
                  <h3>{hoist.name}</h3>
                  <div className="hoist-pills">
                    {hoist.is_shop ? <StatusPill value="shop" /> : null}
                    <StatusPill value={hoist.status} />
                  </div>
                </div>
                <p className="muted">{hoist.location_label || "No location label"}</p>
                {hoist.current_booking ? (
                  <p>
                    On bay: <strong>{hoist.current_booking.member_name}</strong>
                    <br />
                    <span className="muted">
                      {formatShopTime(hoist.current_booking.start_at)}–
                      {formatShopTime(hoist.current_booking.end_at)}
                    </span>
                  </p>
                ) : (
                  <p className="muted">No active booking right now.</p>
                )}
                <p>
                  <Link href="/hoists">Manage hoists →</Link>
                </p>
              </article>
            ))}
          </div>
        )}

        <h2>Today&apos;s bookings</h2>
        {dash.today_bookings.length === 0 ? (
          <div className="banner empty">Nothing on the board for today.</div>
        ) : (
          <div className="card">
            <table>
              <thead>
                <tr>
                  <th>When</th>
                  <th>Member</th>
                  <th>Hoist</th>
                  <th>Status</th>
                  <th>Tokens</th>
                </tr>
              </thead>
              <tbody>
                {dash.today_bookings.map((booking) => (
                  <tr key={booking.id}>
                    <td>
                      {formatShopTime(booking.start_at)}–{formatShopTime(booking.end_at)}
                      <div className="muted">{formatShopDateTime(booking.start_at)}</div>
                    </td>
                    <td>
                      {booking.member_id ? (
                        <Link href={`/members/${booking.member_id}`}>{booking.member_name}</Link>
                      ) : (
                        booking.member_name
                      )}
                      {booking.kind === "shop" ? (
                        <>
                          {" "}
                          <StatusPill value="shop" />
                        </>
                      ) : null}
                    </td>
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

        <h2>Token-at-risk members</h2>
        {dash.token_at_risk.length === 0 ? (
          <div className="banner empty">No active members under 2 tokens.</div>
        ) : (
          <div className="card">
            <table>
              <thead>
                <tr>
                  <th>Member</th>
                  <th>Tier</th>
                  <th>Tokens</th>
                </tr>
              </thead>
              <tbody>
                {dash.token_at_risk.map((member) => (
                  <tr key={member.id}>
                    <td>
                      <Link href={`/members/${member.id}`}>{member.name}</Link>
                      <div className="muted">{member.email}</div>
                    </td>
                    <td>{member.tier_name}</td>
                    <td>{tokensLabel(member.token_balance)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <p>
          <Link href="/waitlist">Open waitlist →</Link>
          {" · "}
          <Link href="/schedule">Open week schedule →</Link>
        </p>
      </OwnerShell>
    );
  } catch (error) {
    const message = await handlePageError(error);
    return (
      <OwnerShell current="home">
        <p className="eyebrow">Owner · demo</p>
        <h1>Shop dashboard</h1>
        <div className="banner error">{message}</div>
        <p>
          Confirm the API is up at <code>SHOP_API_URL</code> (default{" "}
          <code>http://127.0.0.1:8000</code>) and that demo data is seeded.
        </p>
      </OwnerShell>
    );
  }
}
