import type { ReactNode } from "react";
import Link from "next/link";

import { memberLogoutAction } from "../app/member/logout-action";

const NAV = [
  { href: "/member", current: "home", label: "Balance" },
  { href: "/member/schedule", current: "schedule", label: "Schedule" },
] as const;

export type MemberSection = (typeof NAV)[number]["current"];

export function MemberShell({
  email,
  current,
  wide,
  children,
}: {
  email?: string;
  current: MemberSection;
  wide?: boolean;
  children: ReactNode;
}) {
  return (
    <div className="shell">
      <header className="topbar">
        <div className="brand">
          <strong>Project Car</strong>
          <span>Member demo · parked</span>
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
          <form action={memberLogoutAction}>
            <button className="ghost" type="submit">
              Sign out
            </button>
          </form>
        </nav>
      </header>
      <div className="demo-banner">
        Temporary Member demo on this management alias — customer bays 1–5.
        Customer app is projectcar.ca. Intended management host is
        ops.projectcar.ca. The shop hoist is Owner-only. The shop is not open.
      </div>
      <main className={wide ? "wide" : undefined}>{children}</main>
    </div>
  );
}
