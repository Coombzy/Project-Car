import { SAMPLE_JOBS } from "../lib/placeholders";

export function JobBoard({ audience }: { audience: "member" | "ops" }) {
  return (
    <div className="card">
      <table>
        <thead>
          <tr>
            <th>Task</th>
            <th>Area</th>
            <th>When</th>
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
              <td>{job.area}</td>
              <td>{job.needed}</td>
              <td className="notes">{job.note}</td>
              <td>
                <button type="button" disabled>
                  {audience === "ops" ? "Assign (later)" : "Claim (later)"}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
