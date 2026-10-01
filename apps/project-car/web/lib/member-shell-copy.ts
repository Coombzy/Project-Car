/**
 * Brand subtitle + demo banner for MemberShell.
 *
 * Customer hosts (`projectcar.ca` / `www.projectcar.ca`) get prep copy.
 * Ops, the temporary `app.` alias, and localhost keep the parked
 * management-alias demo. Zone path-split is still pending — this copy
 * does not mark Member live on the customer host.
 */
export type MemberShellCopy = {
  subtitle: string;
  banner: string;
};

/** Ops / temporary `app.` / localhost — unchanged parked demo wording. */
export const MEMBER_SHELL_ALIAS_COPY: MemberShellCopy = {
  subtitle: "Member demo · parked",
  banner:
    "Temporary Member demo on this management alias — customer bays 1–5. " +
    "Home shows your to-dos and only bays you booked in the next 24 hours. " +
    "Customer app is projectcar.ca. Intended management host is " +
    "ops.projectcar.ca. Parts is a request desk (PT / TC SKUs), not " +
    "checkout. Job board (token bounties) and the primary shop camera are " +
    "labeled placeholders. Bay 6 is Owner-only. The shop is not " +
    "open. This is not live pricing or Stripe.",
};

/**
 * Customer-host prep. Balance + schedule are the primary surface.
 * Does not say the request is on a management alias.
 */
export const MEMBER_SHELL_CUSTOMER_COPY: MemberShellCopy = {
  subtitle: "Customer-host Member surface (prep)",
  banner:
    "Customer-host Member surface (prep) on projectcar.ca and www.projectcar.ca. " +
    "Balance and schedule are primary. Zone path-split is still pending, so " +
    "Member is not live on this host. Customer bays 1–5. Home shows your " +
    "to-dos and only bays you booked in the next 24 hours. Parts is a request " +
    "desk (PT / TC SKUs), not checkout. Job board (token bounties) and the " +
    "primary shop camera are labeled placeholders. Bay 6 is Owner-only. The " +
    "shop is not open. This is not live pricing or Stripe.",
};

export function memberShellCopy(customerHost: boolean): MemberShellCopy {
  return customerHost ? MEMBER_SHELL_CUSTOMER_COPY : MEMBER_SHELL_ALIAS_COPY;
}
