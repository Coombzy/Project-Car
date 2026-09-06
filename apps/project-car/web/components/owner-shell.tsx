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
          <span>Shop OS · Owner demo</span>
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
        Demo shop OS — sample members, hoists, and bookings so you can walk the
        product. The shop is not open. This is not live pricing or payment.
      </div>
      <main className={wide ? "wide" : undefined}>{children}</main>
    </div>
  );
}
