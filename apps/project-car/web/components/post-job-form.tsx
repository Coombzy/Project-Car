import { postJobAction } from "../app/jobs/actions";
import { JOB_BOUNTY_CAP } from "../lib/job-form";

export function PostJobForm() {
  return (
    <section className="card">
      <h2 style={{ marginTop: 0 }}>Post a job</h2>
      <p className="muted">
        Stores a shop job for members to claim. Above 0 tokens, at most {JOB_BOUNTY_CAP}, up to two
        decimals. Done does not credit the token ledger. The shop is not open.
      </p>
      <form action={postJobAction} className="stack-form">
        <label>
          Title
          <input name="title" required maxLength={200} placeholder="Sweep the bay" />
        </label>
        <label>
          Notes
          <textarea name="notes" rows={3} maxLength={2000} placeholder="Optional" />
        </label>
        <label>
          Bounty (tokens)
          <input
            name="bounty"
            required
            inputMode="decimal"
            min="0.01"
            max={JOB_BOUNTY_CAP}
            step="0.01"
            placeholder="25"
          />
        </label>
        <div className="actions">
          <button type="submit">Post a job</button>
        </div>
      </form>
    </section>
  );
}
