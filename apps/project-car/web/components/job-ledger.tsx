import { claimJobAction, markJobDoneAction } from "../app/member/jobs/actions";
import type { JobEvent } from "../lib/config";
import { SAMPLE_JOBS } from "../lib/placeholders";
import { formatShopDateTime } from "../lib/time";

function eventKindLabel(kind: JobEvent["kind"]): string {
  switch (kind) {
    case "claim":
      return "Claim";
    case "done":
      return "Done";
    default: {
      const exhaustive: never = kind;
      return exhaustive;
    }
  }
}

export function JobLedger({
  audience,
  events,
  error,
}: {
  audience: "member" | "ops";
  events: JobEvent[];
  error?: string;
}) {
  return (
    <>
      <h2>Stored claim and done</h2>
      <p className="muted">
        A claim stores one row. Marking the job done stores another row. Neither
        row credits the token ledger. The shop is not open.
      </p>
      {error ? <div className="banner error">{error}</div> : null}

      {audience === "member" ? (
        <>
          <div className="card">
            <h3>Claim a job</h3>
            <form action={claimJobAction} className="form-grid">
              <label>
                Job
                <select name="job_key" required defaultValue={SAMPLE_JOBS[0]?.id}>
                  {SAMPLE_JOBS.map((job) => (
                    <option key={job.id} value={job.id}>
                      {job.title}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Note
                <input name="note" placeholder="Optional" />
              </label>
              <div className="actions">
                <button type="submit">Store claim</button>
              </div>
            </form>
          </div>

          <div className="card">
            <h3>Mark a job done</h3>
            <form action={markJobDoneAction} className="form-grid">
              <label>
                Job
                <select name="job_key" required defaultValue={SAMPLE_JOBS[0]?.id}>
                  {SAMPLE_JOBS.map((job) => (
                    <option key={job.id} value={job.id}>
                      {job.title}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Note
                <input name="note" placeholder="Optional" />
              </label>
              <div className="actions">
                <button type="submit">Store done</button>
              </div>
            </form>
          </div>
        </>
      ) : null}

      {events.length === 0 ? (
        <div className="banner empty">No job claim or done stored yet.</div>
      ) : (
        <div className="card">
          <table>
            <thead>
              <tr>
                <th>When</th>
                <th>Kind</th>
                <th>Job</th>
                <th>Who</th>
                <th>Note</th>
              </tr>
            </thead>
            <tbody>
              {events.map((row) => (
                <tr key={row.id}>
                  <td>{formatShopDateTime(row.created_at)}</td>
                  <td>
                    <span className={`pill ${row.kind === "done" ? "pill-available" : "pill-confirmed"}`}>
                      {eventKindLabel(row.kind)}
                    </span>
                  </td>
                  <td>
                    <strong>{row.title}</strong>
                  </td>
                  <td>{row.member_name ?? "Member"}</td>
                  <td className="notes">{row.note ?? "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
}
