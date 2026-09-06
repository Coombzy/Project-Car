import Link from "next/link";

import { BookingCost } from "../../components/booking-cost";
import { HoistHourStrip } from "../../components/hoist-hour-strip";
import { MemberShell } from "../../components/member-shell";
import { StatusPill } from "../../components/status-pill";
import { TodoPanel } from "../../components/todo-panel";
import { handleMemberPageError } from "../../lib/page";
import { getMemberDashboard, getMemberMe } from "../../lib/shop-api";
import { formatShopDateTime, tokensLabel } from "../../lib/time";
import {
  createMemberTodoAction,
  deleteMemberTodoAction,
  toggleMemberTodoAction,
} from "./todos/actions";

export const dynamic = "force-dynamic";

export default async function MemberHomePage({
  searchParams,
}: {
  searchParams?: Promise<{ error?: string }>;
}) {
  const query = searchParams ? await searchParams : {};
  try {
    const [me, dash] = await Promise.all([getMemberMe(), getMemberDashboard()]);
    const open = me.bookings.filter(
      (booking) =>
        booking.status === "pending" || booking.status === "confirmed" || booking.status === "active",
    );
    return (
      <MemberShell email={me.email} current="home" wide>
        <p className="eyebrow">Member · demo</p>
        <h1>Your shop</h1>
        <p className="lede">
          Balance, your to-dos, and the next 24 hours on bays you have booked.
          Customer bays only — Bay 6 is Owner-only. Temporary demo on this
          management alias. The shop is not open.
        </p>
        {query.error ? <div className="banner error">{query.error}</div> : null}

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
            <span className="eyebrow">Open to-dos</span>
            <b>{dash.todos.filter((todo) => todo.status === "open").length}</b>
          </div>
          <div className="metric">
            <span className="eyebrow">Your booked hours (24h)</span>
            <b>{dash.hoists.reduce((sum, hoist) => sum + hoist.next_hours.length, 0)}</b>
          </div>
        </div>

        <p>
          <Link href="/member/schedule">Book a customer bay →</Link>
        </p>

        <h2>Your bays · next 24 hours</h2>
        <p className="muted">
          Window {formatShopDateTime(dash.window_start)} – {formatShopDateTime(dash.window_end)}{" "}
          ({dash.tz}). Only bays with your bookings.
        </p>
        {dash.hoists.length === 0 ? (
          <div className="banner empty">
            You have no booked hours in the next 24 hours. Open the schedule to
            book a customer bay.
          </div>
        ) : (
          <div className="hoist-grid hoist-grid-bays">
            {dash.hoists.map((hoist) => (
              <HoistHourStrip
                key={hoist.id}
                hoist={hoist}
                scheduleHref={`/member/schedule?view=week&hoist=${hoist.id}`}
                linkMembers={false}
              />
            ))}
          </div>
        )}

        <TodoPanel
          todos={dash.todos}
          calendar={dash.calendar}
          actions={{
            create: createMemberTodoAction,
            toggle: toggleMemberTodoAction,
            remove: deleteMemberTodoAction,
          }}
          icsPath={(id) => `/member/todos/${id}/ics`}
          audience="member"
        />

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
        <h1>Your shop</h1>
        <div className="banner error">{message}</div>
      </MemberShell>
    );
  }
}
