import Link from "next/link";

import { OwnerShell } from "../components/owner-shell";
import { HoistHourStrip } from "../components/hoist-hour-strip";
import { PartsOrdersCard } from "../components/parts-orders-card";
import { TodoPanel } from "../components/todo-panel";
import { createTodoAction, deleteTodoAction, toggleTodoAction } from "./todos/actions";
import { getDashboard, getMe } from "../lib/shop-api";
import { handlePageError } from "../lib/page";
import { sortHoists } from "../lib/calendar";
import { formatShopDateTime, tokensLabel } from "../lib/time";

export const dynamic = "force-dynamic";

export default async function DashboardPage({
  searchParams,
}: {
  searchParams?: Promise<{ error?: string }>;
}) {
  const query = searchParams ? await searchParams : {};
  try {
    const [me, dash] = await Promise.all([getMe(), getDashboard()]);
    const hoists = sortHoists(dash.hoists);
    const bookedHours = dash.hoists.reduce((sum, hoist) => sum + hoist.next_hours.length, 0);
    const openTodos = dash.todos.filter((todo) => todo.status === "open").length;
    const openPos = dash.parts_orders.filter((row) => row.status !== "received").length;
    return (
      <OwnerShell email={me.email} current="home" wide>
        <div className="dash">
          <header className="dash-head">
            <div className="dash-title">
              <p className="eyebrow">Owner · demo</p>
              <h1>Shop dashboard</h1>
              <p className="lede">
                Next 24 hours on Bays 1–6 (Bay 6 is the Owner-only shop hoist). Times are
                America/Regina. Seeded sample data — the shop is not open.
              </p>
            </div>
            <div className="dash-metrics">
              <div className="metrics metrics-primary">
                <div className="metric">
                  <span className="eyebrow">Booked hours (24h)</span>
                  <b>{bookedHours}</b>
                </div>
                <div className="metric">
                  <span className="eyebrow">Open to-dos</span>
                  <b>{openTodos}</b>
                </div>
                <div className="metric">
                  <span className="eyebrow">Open POs</span>
                  <b>{openPos}</b>
                </div>
              </div>
              <p className="metrics-meta">
                <span>
                  <Link href="/waitlist">Waitlist</Link> {dash.waitlist_count}
                </span>
                <span>
                  <a href="#token-at-risk">Tokens at risk</a> {dash.token_at_risk.length}
                </span>
                <span>{dash.hoists.length} bays</span>
              </p>
            </div>
          </header>
          {query.error ? <div className="banner error">{query.error}</div> : null}

          <section className="dash-bays">
            <div className="section-head">
              <h2>Bays · next 24 hours</h2>
              <p className="muted">
                Window {formatShopDateTime(dash.window_start)} – {formatShopDateTime(dash.window_end)}{" "}
                ({dash.tz}).
              </p>
            </div>
            {hoists.length === 0 ? (
              <div className="banner empty">
                No hoists yet. Run <code>python -m app.seed</code> in the API.
              </div>
            ) : (
              <div className="hoist-grid hoist-grid-bays hoist-grid-owner">
                {hoists.map((hoist) => (
                  <HoistHourStrip
                    key={hoist.id}
                    hoist={hoist}
                    scheduleHref={`/schedule?view=week&hoist=${hoist.id}`}
                  />
                ))}
              </div>
            )}
          </section>

          <div className="dash-split">
            <PartsOrdersCard orders={dash.parts_orders} />
            <TodoPanel
              todos={dash.todos}
              calendar={dash.calendar}
              actions={{
                create: createTodoAction,
                toggle: toggleTodoAction,
                remove: deleteTodoAction,
              }}
              icsPath={(id) => `/todos/${id}/ics`}
              audience="owner"
            />
          </div>

          <section className="dash-risk" id="token-at-risk">
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
          </section>

          <p className="dash-links">
            <Link href="/waitlist">Open waitlist →</Link>
            {" · "}
            <Link href="/schedule">Open schedule →</Link>
            {" · "}
            <Link href="/parts">Open parts →</Link>
          </p>
        </div>
      </OwnerShell>
    );
  } catch (error) {
    const message = await handlePageError(error);
    return (
      <OwnerShell current="home" wide>
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
