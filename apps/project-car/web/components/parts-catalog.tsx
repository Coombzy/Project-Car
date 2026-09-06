import { SAMPLE_PARTS } from "../lib/placeholders";

export function PartsCatalog({ audience }: { audience: "member" | "ops" }) {
  return (
    <div className="hoist-grid">
      {SAMPLE_PARTS.map((part) => (
        <article key={part.id} className="card">
          <div className="hoist-card-head">
            <h3>{part.name}</h3>
            <span className="pill pill-pending">{part.status}</span>
          </div>
          <p className="muted">{part.note}</p>
          <div className="actions">
            <button type="button" disabled>
              {audience === "ops" ? "Purchase desk (later)" : "Purchase (later)"}
            </button>
          </div>
        </article>
      ))}
    </div>
  );
}
