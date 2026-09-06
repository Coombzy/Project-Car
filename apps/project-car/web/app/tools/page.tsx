import { OwnerShell } from "../../components/owner-shell";
import { PlaceholderNote } from "../../components/placeholder-note";
import { handlePageError } from "../../lib/page";
import {
  SAMPLE_TOOL_INVENTORY,
  SAMPLE_TOOL_ORDERS,
  SAMPLE_TOOL_PLANNED,
  SAMPLE_TOOL_REQUESTS,
} from "../../lib/placeholders";
import { getMe } from "../../lib/shop-api";

export const dynamic = "force-dynamic";

export default async function OpsToolsPage() {
  try {
    const me = await getMe();
    return (
      <OwnerShell email={me.email} current="tools" wide>
        <OpsToolsBody />
      </OwnerShell>
    );
  } catch (error) {
    const message = await handlePageError(error);
    return (
      <OwnerShell current="tools" wide>
        <OpsToolsBody />
        <div className="banner error">{message}</div>
      </OwnerShell>
    );
  }
}

function OpsToolsBody() {
  return (
    <>
      <p className="eyebrow">Ops · placeholder</p>
      <h1>Tools</h1>
      <p className="lede">
        Breadth-first IA: inventory, orders, member requests, and planned
        purchases. Not live QR checkout or hardware. Schema may already have{" "}
        <code>tools</code>; this page is a stub so layout can be ironed out.
      </p>
      <PlaceholderNote>
        Four ops stubs — not a working inventory system. Member UI does not get
        this Tools section.
      </PlaceholderNote>

      <h2>Tool inventory</h2>
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>Tool</th>
              <th>Location</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {SAMPLE_TOOL_INVENTORY.map((row) => (
              <tr key={row.id}>
                <td>{row.name}</td>
                <td>{row.location}</td>
                <td>{row.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <h2>Tool orders</h2>
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>What</th>
              <th>Vendor</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {SAMPLE_TOOL_ORDERS.map((row) => (
              <tr key={row.id}>
                <td>{row.what}</td>
                <td>{row.vendor}</td>
                <td>{row.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <h2>Member tool requests</h2>
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>Who</th>
              <th>Request</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {SAMPLE_TOOL_REQUESTS.map((row) => (
              <tr key={row.id}>
                <td>{row.who}</td>
                <td>{row.what}</td>
                <td>{row.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <h2>Planned tool purchases</h2>
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>What</th>
              <th>Note</th>
              <th>When</th>
            </tr>
          </thead>
          <tbody>
            {SAMPLE_TOOL_PLANNED.map((row) => (
              <tr key={row.id}>
                <td>{row.what}</td>
                <td className="notes">{row.note}</td>
                <td>{row.when}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
