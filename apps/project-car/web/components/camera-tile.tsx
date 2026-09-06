export function CameraTile({
  name,
  location,
  hint,
  primary,
}: {
  name: string;
  location: string;
  hint: string;
  primary?: boolean;
}) {
  return (
    <article className="card camera-tile">
      <div className="hoist-card-head">
        <h3>{name}</h3>
        <div className="hoist-pills">
          {primary ? <span className="pill pill-confirmed">Primary</span> : null}
          <span className="pill">No live feed</span>
        </div>
      </div>
      <div className="camera-frame" aria-hidden="true">
        <span>Placeholder · not a live camera</span>
      </div>
      <p className="muted">{location}</p>
      <p className="muted">{hint}</p>
    </article>
  );
}
