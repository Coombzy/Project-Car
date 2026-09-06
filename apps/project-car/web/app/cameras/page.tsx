import { CameraTile } from "../../components/camera-tile";
import { OwnerShell } from "../../components/owner-shell";
import { PlaceholderNote } from "../../components/placeholder-note";
import { handlePageError } from "../../lib/page";
import {
  SAMPLE_AI_EVENTS,
  SAMPLE_CAMERAS,
  SAMPLE_DOOR_LOGS,
} from "../../lib/placeholders";
import { getMe } from "../../lib/shop-api";

export const dynamic = "force-dynamic";

export default async function OpsCamerasPage() {
  try {
    const me = await getMe();
    return (
      <OwnerShell email={me.email} current="cameras" wide>
        <OpsCamerasBody />
      </OwnerShell>
    );
  } catch (error) {
    const message = await handlePageError(error);
    return (
      <OwnerShell current="cameras" wide>
        <OpsCamerasBody />
        <div className="banner error">{message}</div>
      </OwnerShell>
    );
  }
}

function OpsCamerasBody() {
  return (
    <>
      <p className="eyebrow">Ops · placeholder</p>
      <h1>Cameras, door logs, AI</h1>
      <p className="lede">
        Ops can view every shop camera, plus door entry logs and AI collection
        stubs. Members only see the primary shop camera. Frigate (or an
        equivalent NVR) is the later tie-in for feeds and AI events. Occupancy
        is a hint, not bay source of truth. No live NVR in this slice.
      </p>
      <PlaceholderNote>
        Placeholder tiles and stub tables — not live Frigate, not live door
        hardware, not Twilio. Door logs stay ops-only.
      </PlaceholderNote>

      <h2>Every camera</h2>
      <div className="hoist-grid">
        {SAMPLE_CAMERAS.map((camera) => (
          <CameraTile
            key={camera.id}
            name={camera.name}
            location={camera.location}
            hint={camera.hint}
            primary={camera.primary}
          />
        ))}
      </div>

      <h2>Door entry logs</h2>
      <p className="muted">
        Ops-only. Sample rows — NFC / FOB readers are still out of v1.
      </p>
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>When</th>
              <th>Who</th>
              <th>Door</th>
              <th>Result</th>
            </tr>
          </thead>
          <tbody>
            {SAMPLE_DOOR_LOGS.map((row) => (
              <tr key={row.id}>
                <td>{row.at}</td>
                <td>{row.who}</td>
                <td>{row.door}</td>
                <td>{row.result}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <h2>AI camera collection</h2>
      <p className="muted">
        Frigate-style event stubs. Hint, not source of truth for hoist occupancy.
      </p>
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>When</th>
              <th>Camera</th>
              <th>Kind</th>
              <th>Note</th>
            </tr>
          </thead>
          <tbody>
            {SAMPLE_AI_EVENTS.map((row) => (
              <tr key={row.id}>
                <td>{row.at}</td>
                <td>{row.camera}</td>
                <td>{row.kind}</td>
                <td className="notes">{row.note}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
