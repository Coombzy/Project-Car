/** Cancel stays off an active visit. The owner has one control. The member keeps pending and confirmed apart. */

export type CancelControl = "owner" | "member-pending" | "member-confirmed";

export function offersCancel(status: string, control: CancelControl): boolean {
  switch (control) {
    case "owner":
      return status === "pending" || status === "confirmed";
    case "member-pending":
      return status === "pending";
    case "member-confirmed":
      return status === "confirmed";
    default: {
      const unexpected: never = control;
      return unexpected;
    }
  }
}
