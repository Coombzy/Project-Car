import { OwnerShell } from "../../components/owner-shell";
import { PlaceholderNote } from "../../components/placeholder-note";
import { handlePageError } from "../../lib/page";
import { SAMPLE_MEMBERSHIP_PAYMENTS, SAMPLE_PARTS_PAYMENTS } from "../../lib/placeholders";
import { getMe } from "../../lib/shop-api";

export const dynamic = "force-dynamic";

export default async function OpsPaymentsPage() {
  try {
    const me = await getMe();
    return (
      <OwnerShell email={me.email} current="payments" wide>
        <OpsPaymentsBody />
      </OwnerShell>
    );
  } catch (error) {
    const message = await handlePageError(error);
    return (
      <OwnerShell current="payments" wide>
        <OpsPaymentsBody />
        <div className="banner error">{message}</div>
      </OwnerShell>
    );
  }
}

function OpsPaymentsBody() {
  return (
    <>
      <p className="eyebrow">Ops · placeholder</p>
      <h1>Payments / billing ledger</h1>
      <p className="lede">
        Ops tracks <strong>membership payments</strong> and{" "}
        <strong>parts payments</strong>. AI watches almost all of that by
        default; humans get alerted on exceptions, not every normal payment.
        Full Stripe stays Later. No live charges. The shop is not open.
      </p>
      <PlaceholderNote>
        Billing stub — sample rows only. Not Stripe. Exception row is labeled so
        the AI-alert model is visible. Token job bounties live on the job board
        ledger, not here.
      </PlaceholderNote>

      <h2>Membership payments</h2>
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>Who</th>
              <th>Kind</th>
              <th>Amount</th>
              <th>AI / ops</th>
            </tr>
          </thead>
          <tbody>
            {SAMPLE_MEMBERSHIP_PAYMENTS.map((row) => (
              <tr key={row.id}>
                <td>{row.who}</td>
                <td>{row.kind}</td>
                <td>{row.amount}</td>
                <td>{row.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <h2>Parts payments</h2>
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>Who</th>
              <th>Kind</th>
              <th>Amount</th>
              <th>AI / ops</th>
            </tr>
          </thead>
          <tbody>
            {SAMPLE_PARTS_PAYMENTS.map((row) => (
              <tr key={row.id}>
                <td>{row.who}</td>
                <td>{row.kind}</td>
                <td>{row.amount}</td>
                <td>{row.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
