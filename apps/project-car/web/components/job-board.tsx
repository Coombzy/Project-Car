import { SAMPLE_JOBS } from "../lib/placeholders";
import { tokensLabel } from "../lib/time";

export function JobBoard({ audience }: { audience: "member" | "ops" }) {
  return (
    <>
      <div className="card" style={{ marginBottom: "1rem" }}>
        <p className="eyebrow">Pay model (locked)</p>
        <p className="lede" style={{ marginBottom: 0 }}>
          Ops posts the job and sets a <strong>token bounty</strong>. A member
          claims it and completes the chore (cleaning, tool maintenance, random
          upkeep). Complete credits that bounty to the member’s{" "}
          <strong>append-only token ledger</strong> — same token system as hoist
          booking, not Stripe. Claim / complete stay Later; amounts below are
          the lock.
        </p>
      </div>
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
                    {audience === "ops"
                      ? "Post / assign (later)"
                      : "Claim / complete (later)"}
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
