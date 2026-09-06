import { OwnerShell } from "../../components/owner-shell";
import { StatusPill } from "../../components/status-pill";
import { handlePageError } from "../../lib/page";
import { getMe, listHoists } from "../../lib/shop-api";
import { createHoistAction, patchHoistAction } from "./actions";

export const dynamic = "force-dynamic";

export default async function HoistsPage({
  searchParams,
}: {
  searchParams: Promise<{ error?: string }>;
}) {
  try {
    const params = await searchParams;
    const [me, hoists] = await Promise.all([getMe(), listHoists()]);
    return (
      <OwnerShell email={me.email} current="hoists">
        <p className="eyebrow">GET /hoists</p>
        <h1>Hoists</h1>
        <p className="lede">
          Demo inventory is 6 bays — exactly one shop hoist for internal work.
          Shop work has priority on that bay. Occupied flips on check-in;
          complete frees the bay when nothing else is active.
        </p>
        {params.error ? <div className="banner error">{params.error}</div> : null}

        {hoists.length === 0 ? (
          <div className="banner empty">
            No hoists. Seed with <code>python -m app.seed</code> or add a bay below.
          </div>
        ) : (
          <div className="hoist-grid">
            {hoists.map((hoist) => (
              <article key={hoist.id} className="card hoist-card">
                <div className="hoist-card-head">
                  <h3>{hoist.name}</h3>
                  <div className="hoist-pills">
                    {hoist.is_shop ? <StatusPill value="shop" /> : null}
                    <StatusPill value={hoist.status} />
                  </div>
                </div>
                <form action={patchHoistAction}>
                  <input type="hidden" name="id" value={hoist.id} />
                  <label>
                    Location
                    <input name="location_label" defaultValue={hoist.location_label} />
                  </label>
                  <label>
                    Status
                    <select name="status" defaultValue={hoist.status}>
                      <option value="available">available</option>
                      <option value="occupied">occupied</option>
                      <option value="maintenance">maintenance</option>
                      <option value="locked">locked</option>
                    </select>
                  </label>
                  <label className="checkbox-row">
                    <input type="checkbox" name="is_shop" defaultChecked={hoist.is_shop} />
                    Shop hoist (internal / business work)
                  </label>
                  <div className="actions">
                    <button type="submit">Save bay</button>
                  </div>
                </form>
              </article>
            ))}
          </div>
        )}

        <section className="card" style={{ marginTop: "1.4rem" }}>
          <h2>Add hoist</h2>
          <form action={createHoistAction} className="form-grid">
            <label>
              Name
              <input name="name" required placeholder="Bay 4" />
            </label>
            <label>
              Location
              <input name="location_label" placeholder="West wall" />
            </label>
            <label>
              Status
              <select name="status" defaultValue="available">
                <option value="available">available</option>
                <option value="occupied">occupied</option>
                <option value="maintenance">maintenance</option>
                <option value="locked">locked</option>
              </select>
            </label>
            <label className="checkbox-row">
              <input type="checkbox" name="is_shop" />
              Shop hoist
            </label>
            <div className="actions" style={{ alignSelf: "end" }}>
              <button type="submit">Create hoist</button>
            </div>
          </form>
        </section>
      </OwnerShell>
    );
  } catch (error) {
    const message = await handlePageError(error);
    return (
      <OwnerShell current="hoists">
        <h1>Hoists</h1>
        <div className="banner error">{message}</div>
      </OwnerShell>
    );
  }
}
