import { CameraTile } from "../../../components/camera-tile";
import { MemberShell } from "../../../components/member-shell";
import { PlaceholderNote } from "../../../components/placeholder-note";
import { handleMemberPageError } from "../../../lib/page";
import { primaryCamera } from "../../../lib/placeholders";
import { getMemberMe } from "../../../lib/shop-api";

export const dynamic = "force-dynamic";

export default async function MemberCamerasPage() {
  try {
    const me = await getMemberMe();
    return (
      <MemberShell email={me.email} current="cameras">
        <MemberCamerasBody />
      </MemberShell>
    );
  } catch (error) {
    const message = await handleMemberPageError(error);
    return (
      <MemberShell current="cameras">
        <MemberCamerasBody />
        <div className="banner error">{message}</div>
      </MemberShell>
    );
  }
}

function MemberCamerasBody() {
  const camera = primaryCamera();
  return (
    <>
      <p className="eyebrow">Customer-facing · placeholder</p>
      <h1>Shop camera</h1>
      <p className="lede">
        Members get the <strong>primary shop camera</strong> only. Ops sees
        every camera, door entry logs, and AI collection. This tile is not a
        live Frigate feed. Occupancy hints never override the booking calendar.
      </p>
      <PlaceholderNote>
        One primary camera — sample frame only. Not a live feed. Door logs and
        other cameras stay on the ops surface.
      </PlaceholderNote>
      <CameraTile
        name={camera.name}
        location={camera.location}
        hint={camera.hint}
        primary
      />
    </>
  );
}
