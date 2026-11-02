import Link from "next/link";

import { MemberShell } from "../../../components/member-shell";
import { handleMemberPageError } from "../../../lib/page";
import { profileRows } from "../../../lib/profile-view";
import { getMemberMe } from "../../../lib/shop-api";

export const dynamic = "force-dynamic";

export default async function MemberProfilePage() {
  try {
    const me = await getMemberMe();
    const rows = profileRows(me);
    return (
      <MemberShell email={me.email} current="profile">
        <p className="eyebrow">Member · demo</p>
        <h1>Profile</h1>
        <p className="lede">
          Your membership record. Read-only. Ask the shop to change a field.
          The shop is not open.
        </p>
        <div className="card">
          <table>
            <tbody>
              {rows.map((row) => (
                <tr key={row.label}>
                  <th scope="row">{row.label}</th>
                  <td>{row.value}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p>
          <Link href="/member/chat">Ask the shop to change this</Link>
        </p>
      </MemberShell>
    );
  } catch (error) {
    const message = await handleMemberPageError(error);
    return (
      <MemberShell current="profile">
        <p className="eyebrow">Member · demo</p>
        <h1>Profile</h1>
        <div className="banner error">{message}</div>
      </MemberShell>
    );
  }
}
