"use client";

import { useEffect, useState } from "react";

import type { Todo } from "../lib/config";
import { safeIcsHref } from "../lib/ics-href";
import { googleTemplateUrl } from "../lib/todo-calendar";

export function CopyEventButton({
  todo,
  icsHref,
}: {
  todo: Todo;
  icsHref: string;
}) {
  const [copied, setCopied] = useState(false);
  const [origin, setOrigin] = useState("https://shop.invalid");
  const google = googleTemplateUrl(todo);
  const safeHref = safeIcsHref(icsHref, origin);

  useEffect(() => {
    setOrigin(window.location.origin);
  }, []);

  async function copyEvent() {
    const href = safeIcsHref(icsHref, window.location.origin);
    if (!href) {
      return;
    }
    try {
      const response = await fetch(href, { cache: "no-store" });
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
      {safeHref ? (
        <a className="button ghost" href={safeHref}>
          ICS
        </a>
      ) : null}
      <button className="ghost" type="button" onClick={copyEvent}>
        {copied ? "Copied" : "Copy event"}
      </button>
      {google ? (
        <a className="button ghost" href={google} target="_blank" rel="noopener noreferrer">
          Google
        </a>
      ) : null}
    </span>
  );
}
