import { SAMPLE_JOBS } from "../lib/placeholders";
import { tokensLabel } from "../lib/time";

export function JobBoard({ audience }: { audience: "member" | "ops" }) {
  return (
    <div className="card">
      <table>
        <thead>
          <tr>
            <th>Task</th>
            <th>Kind</th>
            <th>Area</th>
            <th>When</th>
            <th>Token bounty</th>
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
              <td>{tokensLabel(job.tokenBounty)}</td>
              <td className="notes">{job.note}</td>
              <td>
                <button type="button" disabled>
                  {audience === "ops" ? "Post / assign (later)" : "Claim (later)"}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
