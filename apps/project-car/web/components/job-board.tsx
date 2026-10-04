import { SAMPLE_JOBS } from "../lib/placeholders";
import { tokensLabel } from "../lib/time";

export function JobBoard({ audience }: { audience: "member" | "ops" }) {
  return (
    <>
      <div className="card" style={{ marginBottom: "1rem" }}>
        <p className="eyebrow">Pay model (locked)</p>
        <p className="lede" style={{ marginBottom: 0 }}>
          Ops posts the job and sets a <strong>token bounty</strong>. A member
          claims it and marks it done. Each of those stores a row. Done does
          not credit the token ledger. The amounts below stay the model lock,
          not a Stripe charge. The shop is not open.
        </p>
      </div>
      <p className="muted">
        {audience === "ops"
          ? "Sample rows. They are not stored claims. The shop is not open."
          : "Sample rows. Claim and done use the forms above. The shop is not open."}
      </p>
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>Task</th>
              <th>Kind</th>
              <th>Area</th>
              <th>When</th>
              <th>Token bounty</th>
              <th>On complete</th>
              <th>Note</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {SAMPLE_JOBS.map((job) => (
              <tr key={job.id}>
                <td>
                  <strong>{job.title}</strong>
                </td>
                <td>{job.kind}</td>
                <td>{job.area}</td>
                <td>{job.needed}</td>
                <td>
                  <span className="token-badge">
                    {tokensLabel(job.tokenBounty)} tokens
                  </span>
                </td>
                <td className="notes">
                  +{tokensLabel(job.tokenBounty)} to member ledger (stub)
                </td>
                <td className="notes">{job.note}</td>
                <td>
                  <button type="button" disabled>
                    Sample only
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
