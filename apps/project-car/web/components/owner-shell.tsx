import type { ReactNode } from "react";
import Link from "next/link";

import { logoutAction } from "../app/logout-action";

const NAV = [
  { href: "/", current: "home", label: "Dashboard" },
  { href: "/schedule", current: "schedule", label: "Schedule" },
  { href: "/members", current: "members", label: "Members" },
  { href: "/hoists", current: "hoists", label: "Hoists" },
  { href: "/waitlist", current: "waitlist", label: "Waitlist" },
  { href: "/tiers", current: "tiers", label: "Tiers" },
  { href: "/fill", current: "fill", label: "Fill gaps" },
] as const;

export type OwnerSection = (typeof NAV)[number]["current"];

export function OwnerShell({
  email,
  current,
  wide,
  children,
}: {
  email?: string;
  current: OwnerSection;
  wide?: boolean;
  children: ReactNode;
}) {
  return (
    <div className="shell">
      <header className="topbar">
        <div className="brand">
          <strong>Project Car</strong>
          <span>Management · Owner demo · app alias</span>
        </div>
        <nav className="nav">
          {NAV.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              aria-current={current === item.current ? "page" : undefined}
            >
              {item.label}
            </Link>
          ))}
          {email ? <span className="identity">{email}</span> : null}
          <form action={logoutAction}>
            <button className="ghost" type="submit">
              Sign out
            </button>
          </form>
        </nav>
      </header>
      <div className="demo-banner">
        Management demo on the current app.projectcar.ca alias (Doc). Intended
        host is ops.projectcar.ca — naming only, no DNS yet. Keep building
        calendar here. The shop is not open. This is not live pricing or
        payment.
      </div>
      <main className={wide ? "wide" : undefined}>{children}</main>
    </div>
  );
}
