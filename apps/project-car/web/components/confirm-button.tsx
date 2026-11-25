"use client";

import { useState } from "react";

import { TODO_DELETE_EFFECT, todoDeleteClick, type TodoDeletePhase } from "../lib/todo-delete-confirm";

export function ConfirmButton({ className = "ghost" }: { className?: string }) {
  const [phase, setPhase] = useState<TodoDeletePhase>("idle");
  if (phase === "idle") {
    return (
      <button className={className} type="button" onClick={() => setPhase(todoDeleteClick("idle", "ask").phase)}>
        Delete
      </button>
    );
  }
  return (
    <span className="todo-delete-confirm" style={{ display: "grid", gap: "0.35rem", maxWidth: "9rem" }}>
      <span className="muted">{TODO_DELETE_EFFECT}</span>
      <span className="todo-cal-actions">
        <button className={className} type="button" onClick={() => setPhase(todoDeleteClick(phase, "cancel").phase)}>
          Cancel
        </button>
        <button
          className={className}
          type="submit"
          onClick={(event) => {
            if (!todoDeleteClick(phase, "confirm").submit) event.preventDefault();
          }}
        >
          Delete
        </button>
      </span>
    </span>
  );
}
