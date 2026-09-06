"use client";

import { useState } from "react";

import type { Todo } from "../lib/config";
import { googleTemplateUrl } from "../lib/todo-calendar";

export function CopyEventButton({
  todo,
  icsHref,
}: {
  todo: Todo;
  icsHref: string;
}) {
  const [copied, setCopied] = useState(false);
  const google = googleTemplateUrl(todo);

  async function copyEvent() {
    try {
      const response = await fetch(icsHref, { cache: "no-store" });
      if (!response.ok) {
        return;
      }
      const text = await response.text();
      await navigator.clipboard.writeText(text);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 2000);
    } catch {
      setCopied(false);
    }
  }

  if (!todo.due_at) {
    return <span className="muted">Add a due date to export.</span>;
  }

  return (
    <span className="todo-cal-actions">
      <a className="button ghost" href={icsHref}>
        ICS
      </a>
      <button className="ghost" type="button" onClick={copyEvent}>
        {copied ? "Copied" : "Copy event"}
      </button>
      {google ? (
        <a className="button ghost" href={google} target="_blank" rel="noreferrer">
          Google
        </a>
      ) : null}
    </span>
  );
}
