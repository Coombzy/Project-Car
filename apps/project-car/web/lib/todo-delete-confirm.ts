export const TODO_DELETE_EFFECT = "Delete this to-do? This cannot be undone.";

export type TodoDeletePhase = "idle" | "confirming";

export function todoDeleteClick(
  phase: TodoDeletePhase,
  click: "ask" | "confirm" | "cancel",
): { phase: TodoDeletePhase; submit: boolean } {
  switch (click) {
    case "ask":
      return { phase: "confirming", submit: false };
    case "cancel":
      return { phase: "idle", submit: false };
    case "confirm":
      return { phase: "confirming", submit: phase === "confirming" };
    default: {
      const unreachable: never = click;
      throw new Error(unreachable);
    }
  }
}
