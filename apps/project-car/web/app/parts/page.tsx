import { OwnerShell } from "../../components/owner-shell";
import { PlaceholderNote } from "../../components/placeholder-note";
import type { PartsOrder, PartsRequest } from "../../lib/config";
import { SAMPLE_INVENTORY_REQUESTS, SAMPLE_PARTS_STOCK, partsReorderState } from "../../lib/inventory";
import { handlePageError } from "../../lib/page";
import { getMe, listPartsOrders, listPartsRequests } from "../../lib/shop-api";
import { formatShopDateTime } from "../../lib/time";
import { partsStatusLabel } from "../../lib/todo-calendar";
import { decidePartsRequestAction, patchPartsOrderAction } from "./actions";

export const dynamic = "force-dynamic";

const ORDER_STATUSES: PartsOrder["status"][] = ["ordered", "shipped", "in_transit", "received"];

export default async function OpsPartsPage({
  searchParams,
}: {
  searchParams?: Promise<{ error?: string }>;
}) {
  const query = searchParams ? await searchParams : {};
  try {
    const [me, requests, orders] = await Promise.all([
      getMe(),
      listPartsRequests(),
      listPartsOrders(),
    ]);
    return (
      <OwnerShell email={me.email} current="parts" wide>
        <OpsPartsBody requests={requests} orders={orders} error={query.error} />
      </OwnerShell>
    );
  } catch (error) {
    const message = await handlePageError(error);
    return (
      <OwnerShell current="parts" wide>
        <OpsPartsBody requests={[]} orders={[]} />
        <div className="banner error">{message}</div>
      </OwnerShell>
    );
  }
}

function requestStatusLabel(status: PartsRequest["status"]): string {
  switch (status) {
    case "open":
      return "Open";
    case "fulfilled":
      return "Fulfilled";
    case "declined":
      return "Declined";
    default: {
      const neverStatus: never = status;
      return neverStatus;
    }
  }
}

function OpsPartsBody({
  requests,
  orders,
  error,
}: {
  requests: PartsRequest[];
  orders: PartsOrder[];
  error?: string;
}) {
  return (
    <>
      <p className="eyebrow">Ops · placeholder</p>
      <h1>Parts — shop stock</h1>
      <p className="lede">
        <strong>PT</strong> is parts inventory: on-hand qty, reorder point, POs,
        and member requests. Distinct from bay kits (B1–B6) and the tool crib
        (TC). Distinct from the customer request desk on{" "}
        <code>/member/parts</code>. Full checkout and eBay stay Later. Flag{" "}
        <code>pc.marketplace</code> stays off. No Stripe. The shop is not open.
      </p>
      {error ? <div className="banner error">{error}</div> : null}
      <PlaceholderNote>
        PT stock qty is a stub — not a price list and not the member catalog.
        Purchase orders are the stored <code>parts_orders</code> rows, the same
        rows as the dashboard. Member-facing parts stay requests-only on the
        customer surface. Consumables (<code>CM</code>) stay Later.
      </PlaceholderNote>

      <h2>PT stock</h2>
      <p className="muted">
        Qty / reorder are stubs. Rows at or below the reorder point are marked.
        Example SKU <code>PT-OIL-5W30-012</code>.
      </p>
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>SKU</th>
              <th>What</th>
              <th>Qty</th>
              <th>Reorder</th>
              <th>Status</th>
              <th>Note</th>
            </tr>
          </thead>
          <tbody>
            {SAMPLE_PARTS_STOCK.map((row) => {
              const state = partsReorderState(row);
              return (
                <tr key={row.sku} className={state === "reorder" ? "reorder-row" : undefined}>
                  <td className="sku">{row.sku}</td>
                  <td>{row.name}</td>
                  <td>
                    {row.qty} {row.unit}
                  </td>
                  <td>
                    {row.reorderPoint} {row.unit}
                  </td>
                  <td>
                    <span
                      className={`pill ${
                        state === "reorder" ? "pill-overdue" : "pill-available"
                      }`}
                    >
                      {state === "reorder" ? "Reorder (stub)" : "In stock (stub)"}
                    </span>
                  </td>
                  <td className="notes">{row.note}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <h2>Purchase orders</h2>
      <p className="muted">
        Stored shop POs, including <code>PT-PO-1045</code> when it is seeded.
        Same rows as the dashboard parts strip. Set status here — not a live
        vendor feed, and not a cart.
      </p>
      {orders.length === 0 ? (
        <div className="banner empty">No parts orders stored yet.</div>
      ) : (
        <div className="card">
          <table>
            <thead>
              <tr>
                <th>PO</th>
                <th>SKU</th>
                <th>What</th>
                <th>Vendor</th>
                <th>For</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((row) => (
                <tr key={row.id}>
                  <td>{row.po_number}</td>
                  <td className="sku">{row.sku ?? "—"}</td>
                  <td>{row.what}</td>
                  <td>{row.vendor || "—"}</td>
                  <td>{row.for_label || "—"}</td>
                  <td>
                    <form className="parts-status-form" action={patchPartsOrderAction}>
                      <input type="hidden" name="id" value={row.id} />
                      <select
                        name="status"
                        defaultValue={row.status}
                        aria-label={`Status for ${row.po_number}`}
                      >
                        {ORDER_STATUSES.map((status) => (
                          <option key={status} value={status}>
                            {partsStatusLabel(status)}
                          </option>
                        ))}
                      </select>
                      <button type="submit">Save</button>
                    </form>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <h2>Stored parts requests</h2>
      <p className="muted">
        Rows members stored from the request desk. Fulfill or decline is the
        status they see. Not a storefront and not a tool checkout. The shop is
        not open.
      </p>
      {requests.length === 0 ? (
        <div className="banner empty">No parts requests stored yet.</div>
      ) : (
        <div className="card">
          <table>
            <thead>
              <tr>
                <th>Who</th>
                <th>SKU</th>
                <th>Note</th>
                <th>Status</th>
                <th>Stored</th>
                <th>Decision</th>
              </tr>
            </thead>
            <tbody>
              {requests.map((row) => (
                <tr key={row.id}>
                  <td>{row.member_name ?? "Member"}</td>
                  <td className="sku">{row.sku}</td>
                  <td>{row.note ?? "—"}</td>
                  <td>{requestStatusLabel(row.status)}</td>
                  <td>{formatShopDateTime(row.created_at)}</td>
                  <td>
                    <div className="parts-status-form">
                      <form action={decidePartsRequestAction}>
                        <input type="hidden" name="id" value={row.id} />
                        <input type="hidden" name="status" value="fulfilled" />
                        <button type="submit">Fulfill</button>
                      </form>
                      <form action={decidePartsRequestAction}>
                        <input type="hidden" name="id" value={row.id} />
                        <input type="hidden" name="status" value="declined" />
                        <button type="submit" className="ghost">
                          Decline
                        </button>
                      </form>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <h2>Sample member requests (not stored)</h2>
      <p className="muted">
        Placeholder part asks. They are not rows in the parts-request table.
      </p>
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>Who</th>
              <th>SKU</th>
              <th>Request</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {SAMPLE_INVENTORY_REQUESTS.filter((row) => row.kind === "part").map(
              (row) => (
                <tr key={row.id}>
                  <td>{row.who}</td>
                  <td className="sku">{row.sku}</td>
                  <td>{row.what}</td>
                  <td>{row.status}</td>
                </tr>
              ),
            )}
          </tbody>
        </table>
      </div>

      <p className="muted cm-later">
        Consumables prefix <code>CM</code> (towels, rags, tape) is documented
        for later. Example shape <code>CM-TW-001</code> — not a stock desk here.
      </p>
    </>
  );
}
