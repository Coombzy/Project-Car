import Link from "next/link";

import type { PartsOrder } from "../lib/config";
import { formatShopDateTime } from "../lib/time";
import { partsStatusLabel } from "../lib/todo-calendar";

const STATUS_CLASS: Record<PartsOrder["status"], string> = {
  ordered: "pill-pending",
  shipped: "pill-confirmed",
  in_transit: "urgency-medium",
  received: "pill-completed",
};

export function PartsOrdersCard({ orders }: { orders: PartsOrder[] }) {
  return (
    <section className="dash-panel">
      <h2>Parts orders</h2>
      <p className="muted">
        Most current shop POs. SKUs use the PT prefix. Statuses are stubs —
        not a live vendor feed. Full purchasing stays Later.
      </p>
      {orders.length === 0 ? (
        <div className="banner empty">
          No parts orders yet. Seed demo POs or open the Parts desk.
        </div>
      ) : (
        <div className="card">
          <table>
            <thead>
              <tr>
                <th>PO</th>
                <th>SKU</th>
                <th>What</th>
                <th>For</th>
                <th>Status</th>
                <th>Tracking</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((row) => (
                <tr key={row.id}>
                  <td>{row.po_number}</td>
                  <td className="notes">{row.sku ?? "—"}</td>
                  <td>
                    {row.what}
                    <div className="muted">{row.vendor}</div>
                  </td>
                  <td>{row.for_label}</td>
                  <td>
                    <span className={`pill ${STATUS_CLASS[row.status]}`}>
                      {partsStatusLabel(row.status)}
                    </span>
                    <div className="muted">
                      {row.status === "received" && row.received_at
                        ? `Received ${formatShopDateTime(row.received_at)}`
                        : row.eta_at
                          ? `ETA ${formatShopDateTime(row.eta_at)}`
                          : `Ordered ${formatShopDateTime(row.ordered_at)}`}
                    </div>
                  </td>
                  <td className="notes">{row.tracking ?? "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <p>
        <Link href="/parts">Open Parts desk →</Link>
      </p>
    </section>
  );
}
