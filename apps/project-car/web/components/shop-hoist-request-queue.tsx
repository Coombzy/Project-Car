import {
  approveShopHoistRequestAction,
  denyShopHoistRequestAction,
} from "../app/schedule/actions";
import type { ShopHoistRequest } from "../lib/config";
import { formatShopDateTime, tokensLabel } from "../lib/time";
import { ScheduleReturnFields, type ScheduleReturn } from "./schedule-return-fields";

export function ShopHoistRequestQueue({
  requests,
  returnTo,
}: {
  requests: ShopHoistRequest[];
  returnTo: ScheduleReturn;
}) {
  const pending = requests.filter((row) => row.status === "pending");

  return (
    <section className="card" id="shop-hoist-requests" style={{ marginTop: "1.4rem" }}>
      <h2>Shop hoist requests</h2>
      <p className="lede">
        Pending member requests for the shop hoist. Approve reserves the quoted tokens.
        Deny drops the row and does not take tokens.
      </p>
      {pending.length === 0 ? (
        <div className="banner empty">No pending shop-hoist requests.</div>
      ) : (
        pending.map((row) => (
          <article key={row.id} className="booking-chip">
            <strong>{row.member_name}</strong>
            <div>{row.hoist_name}</div>
            <div>
              {formatShopDateTime(row.start_at)}–{formatShopDateTime(row.end_at)}
            </div>
            <div>{tokensLabel(row.token_quote)} tokens</div>
            {row.notes ? <div className="muted">{row.notes}</div> : null}
            <div className="chip-actions">
              <form action={approveShopHoistRequestAction}>
                <ScheduleReturnFields returnTo={returnTo} />
                <input type="hidden" name="id" value={row.id} />
                <button type="submit">Approve</button>
              </form>
              <form action={denyShopHoistRequestAction}>
                <ScheduleReturnFields returnTo={returnTo} />
                <input type="hidden" name="id" value={row.id} />
                <button className="ghost" type="submit">
                  Deny
                </button>
              </form>
            </div>
          </article>
        ))
      )}
    </section>
  );
}
