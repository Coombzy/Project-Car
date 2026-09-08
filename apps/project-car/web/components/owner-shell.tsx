import type { ReactNode } from "react";
import Link from "next/link";

import { logoutAction } from "../app/logout-action";
import { OwnerDemoBanner } from "./owner-demo-banner";

const PRIMARY_NAV = [
  { href: "/", current: "home", label: "Dashboard" },
  { href: "/schedule", current: "schedule", label: "Schedule" },
  { href: "/chat", current: "chat", label: "Chat" },
  { href: "/members", current: "members", label: "Members" },
] as const;

const SECONDARY_GROUPS = [
  {
    id: "inventory",
    label: "Inventory",
    items: [
      { href: "/parts", current: "parts", label: "Parts" },
      { href: "/tools", current: "tools", label: "Tools" },
    ],
  },
  {
    id: "floor",
    label: "Floor",
    items: [
      { href: "/jobs", current: "jobs", label: "Jobs" },
      { href: "/cameras", current: "cameras", label: "Cameras" },
      { href: "/hoists", current: "hoists", label: "Hoists" },
    ],
  },
  {
    id: "admin",
    label: "Admin",
    items: [
      { href: "/payments", current: "payments", label: "Payments" },
      { href: "/tiers", current: "tiers", label: "Tiers" },
      { href: "/fill", current: "fill", label: "Fill" },
      { href: "/waitlist", current: "waitlist", label: "Waitlist" },
    ],
  },
] as const;

export type OwnerSection =
  | (typeof PRIMARY_NAV)[number]["current"]
  | (typeof SECONDARY_GROUPS)[number]["items"][number]["current"];

function NavLink({
  href,
  label,
  current,
  section,
}: {
  href: string;
  label: string;
  current: OwnerSection;
  section: OwnerSection;
}) {
  return (
    <Link href={href} aria-current={current === section ? "page" : undefined}>
      {label}
    </Link>
  );
}

function SecondaryClusters({ current }: { current: OwnerSection }) {
  return (
    <>
      {SECONDARY_GROUPS.map((group) => (
        <div key={group.id} className="nav-cluster">
          <span className="nav-cluster-label">{group.label}</span>
          {group.items.map((item) => (
            <NavLink
              key={item.href}
              href={item.href}
              label={item.label}
              current={current}
              section={item.current}
            />
          ))}
        </div>
      ))}
    </>
  );
}

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
  const moreCurrent = SECONDARY_GROUPS.some((group) =>
    group.items.some((item) => item.current === current),
  );

  return (
    <div className="shell">
      <header className="owner-chrome">
        <div className="topbar">
          <div className="brand">
            <strong>Project Car</strong>
            <span>Owner · demo</span>
          </div>
          <nav className="nav nav-primary" aria-label="Primary">
            {PRIMARY_NAV.map((item) => (
              <NavLink
                key={item.href}
                href={item.href}
                label={item.label}
                current={current}
                section={item.current}
              />
            ))}
            <details className={`nav-more${moreCurrent ? " is-current" : ""}`}>
              <summary>
                More
                {moreCurrent ? <span className="sr-only"> (current section)</span> : null}
              </summary>
              <div className="nav-more-panel">
                <SecondaryClusters current={current} />
              </div>
            </details>
          </nav>
          <div className="topbar-end">
            {email ? <span className="identity">{email}</span> : null}
            <form action={logoutAction}>
              <button className="ghost" type="submit">
                Sign out
              </button>
            </form>
          </div>
        </div>
        <nav className="nav-secondary" aria-label="Shop tools">
          <SecondaryClusters current={current} />
        </nav>
      </header>
      <OwnerDemoBanner />
      <main className={wide ? "wide" : undefined}>{children}</main>
    </div>
  );
}
