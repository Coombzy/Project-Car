import { InventoryKitNav } from "../../components/inventory-kit-nav";
import { OwnerShell } from "../../components/owner-shell";
import { PlaceholderNote } from "../../components/placeholder-note";
import { handlePageError } from "../../lib/page";
import {
  BAY_KITS,
  CRIB_PREFIX,
  SAMPLE_CRIB_TOOLS,
  SAMPLE_INVENTORY_REQUESTS,
  SAMPLE_TOOL_ORDERS,
  SAMPLE_TOOL_PLANNED,
  bayKitItems,
  checkoutLabel,
  parseKitParam,
} from "../../lib/inventory";
import { getMe } from "../../lib/shop-api";

export const dynamic = "force-dynamic";

export default async function OpsToolsPage({
  searchParams,
}: {
  searchParams: Promise<{ kit?: string }>;
}) {
  const kit = parseKitParam((await searchParams).kit);
  try {
    const me = await getMe();
    return (
      <OwnerShell email={me.email} current="tools" wide>
        <OpsToolsBody kit={kit} />
      </OwnerShell>
    );
  } catch (error) {
    const message = await handlePageError(error);
    return (
      <OwnerShell current="tools" wide>
        <OpsToolsBody kit={kit} />
        <div className="banner error">{message}</div>
      </OwnerShell>
    );
  }
}

function OpsToolsBody({ kit }: { kit: ReturnType<typeof parseKitParam> }) {
  const bay = kit === CRIB_PREFIX ? null : BAY_KITS[kit];
  const bayRows = bay ? bayKitItems(bay.prefix) : [];

  return (
    <>
      <p className="eyebrow">Ops · placeholder</p>
      <h1>Tools</h1>
      <p className="lede">
        Locked prefixes: <strong>B1–B6</strong> are resident bay hand-tool kits
        (one kit per hoist). <strong>B6</strong> is the shop hoist bay — same
        B-scheme, never <code>SH</code>. <strong>TC</strong> is the tool crib
        (checkout / return / overdue stub). Not live QR or hardware. Schema may
        already have <code>tools</code>; these lists are labeled demo SKUs.
      </p>
      <PlaceholderNote>
        Placeholder inventory — not a working checkout system. Member UI does
        not get this Tools section. Members may <em>request</em> a crib tool
        from <code>/member/parts</code>. Consumables (<code>CM</code>) stay
        Later.
      </PlaceholderNote>

      <InventoryKitNav current={kit} />

      {bay ? (
        <>
          <h2>
            {bay.prefix} · {bay.hoist}
            {bay.shopHoist ? " (shop hoist)" : ""}
          </h2>
          <p className="muted">
            {bay.location}. Resident kit — tools stay on the bay cart. They do
            not check out through the crib.
          </p>
          <div className="card">
            <table>
              <thead>
                <tr>
                  <th>SKU</th>
                  <th>Tool</th>
                  <th>Category</th>
                  <th>State</th>
                  <th>Note</th>
                </tr>
              </thead>
              <tbody>
                {bayRows.map((row) => (
                  <tr key={row.sku}>
                    <td className="sku">{row.sku}</td>
                    <td>{row.name}</td>
                    <td>{row.category}</td>
                    <td>
                      <span
                        className={`pill ${
                          row.state === "missing" ? "pill-overdue" : "pill-available"
                        }`}
                      >
                        {row.state === "missing" ? "Missing (stub)" : "Resident"}
                      </span>
                    </td>
                    <td className="notes">{row.note}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      ) : (
        <>
          <h2>Tool crib · TC</h2>
          <p className="muted">
            Specialty tools. Checkout / return / overdue is a stub — no QR,
            no hardware, no due-date mail.
          </p>
          <div className="card">
            <table>
              <thead>
                <tr>
                  <th>SKU</th>
                  <th>Tool</th>
                  <th>Checkout</th>
                  <th>Who</th>
                  <th>Due</th>
                  <th>Note</th>
                </tr>
              </thead>
              <tbody>
                {SAMPLE_CRIB_TOOLS.map((row) => (
                  <tr key={row.sku}>
                    <td className="sku">{row.sku}</td>
                    <td>{row.name}</td>
                    <td>
                      <span
                        className={`pill ${
                          row.checkout === "available"
                            ? "pill-available"
                            : row.checkout === "overdue"
                              ? "pill-overdue"
                              : "pill-confirmed"
                        }`}
                      >
                        {checkoutLabel(row.checkout)}
                      </span>
                    </td>
                    <td>{row.who ?? "—"}</td>
                    <td>{row.due ?? "—"}</td>
                    <td className="notes">{row.note}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}

      <h2>Tool orders</h2>
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>SKU</th>
              <th>What</th>
              <th>Vendor</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {SAMPLE_TOOL_ORDERS.map((row) => (
              <tr key={row.id}>
                <td className="sku">{row.sku ?? "—"}</td>
                <td>{row.what}</td>
                <td>{row.vendor}</td>
                <td>{row.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <h2>Member tool requests</h2>
      <p className="muted">
        Crib (TC) and part (PT) requests from the member desk. Not commerce.
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
            {SAMPLE_INVENTORY_REQUESTS.filter((row) => row.kind === "crib_tool").map(
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

      <h2>Planned tool purchases</h2>
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>SKU hint</th>
              <th>What</th>
              <th>Note</th>
              <th>When</th>
            </tr>
          </thead>
          <tbody>
            {SAMPLE_TOOL_PLANNED.map((row) => (
              <tr key={row.id}>
                <td className="sku">{row.skuHint}</td>
                <td>{row.what}</td>
                <td className="notes">{row.note}</td>
                <td>{row.when}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <p className="muted cm-later">
        Consumables prefix <code>CM</code> is locked for later (shop towels,
        rags, tape). Do not build a full CM desk in this slice.
      </p>
    </>
  );
}
