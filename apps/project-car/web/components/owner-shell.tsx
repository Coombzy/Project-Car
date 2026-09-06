import type { ReactNode } from "react";
import Link from "next/link";

import { logoutAction } from "../app/logout-action";

export function OwnerShell({
  email,
  current,
  children,
}: {
  email?: string;
  current: "home" | "waitlist";
  children: ReactNode;
}) {
  return (
    <div className="shell">
      <header className="topbar">
        <div className="brand">
          <strong>Project Car</strong>
          <span>Shop OS · Owner</span>
        </div>
        <nav className="nav">
          <Link href="/" aria-current={current === "home" ? "page" : undefined}>
            Dashboard
          </Link>
          <Link
            href="/waitlist"
            aria-current={current === "waitlist" ? "page" : undefined}
          >
            Waitlist
          </Link>
          {email ? <span className="identity">{email}</span> : null}
          <form action={logoutAction}>
            <button className="ghost" type="submit">
              Sign out
            </button>
          </form>
        </nav>
      </header>
      <main>{children}</main>
    </div>
  );
}
