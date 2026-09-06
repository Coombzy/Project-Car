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
          <span>Shop OS · Member demo</span>
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
        Member self-serve demo — your token balance and customer bays (1–5). The
        shop hoist is Owner-only. The shop is not open. This is not live pricing
        or payment.
      </div>
      <main className={wide ? "wide" : undefined}>{children}</main>
    </div>
  );
}
