"use client";

import { useEffect, useRef, useState, type FormEvent } from "react";

import type { ChatMessage, ChatRoom } from "../lib/config";
import { formatShopDateTime } from "../lib/time";

const POLL_MS = 4000;

export function ChatThread({
  room,
  initialMessages,
  initialCursor,
  pollMessages,
  sendMessage,
}: {
  room: ChatRoom;
  initialMessages: ChatMessage[];
  initialCursor: string | null;
  pollMessages: (roomId: string, afterId?: string) => Promise<{ messages: ChatMessage[]; cursor: string | null }>;
  sendMessage: (roomId: string, body: string) => Promise<ChatMessage>;
}) {
  const [messages, setMessages] = useState(initialMessages);
  const [error, setError] = useState<string | null>(null);
  const [sending, setSending] = useState(false);
  const cursorRef = useRef(initialCursor);
  const scrollerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setMessages(initialMessages);
    cursorRef.current = initialCursor;
  }, [initialCursor, initialMessages, room.id]);

  useEffect(() => {
    const node = scrollerRef.current;
    if (node) {
      node.scrollTop = node.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    let cancelled = false;
    const tick = async () => {
      try {
        const page = await pollMessages(room.id, cursorRef.current ?? undefined);
        if (cancelled || page.messages.length === 0) {
          return;
        }
        setMessages((prev) => {
          const seen = new Set(prev.map((row) => row.id));
          const next = page.messages.filter((row) => !seen.has(row.id));
          return next.length ? [...prev, ...next] : prev;
        });
        if (page.cursor) {
          cursorRef.current = page.cursor;
        }
        setError(null);
      } catch (caught) {
        if (!cancelled) {
          setError(caught instanceof Error ? caught.message : "Could not poll chat.");
        }
      }
    };
    const timer = window.setInterval(() => {
      void tick();
    }, POLL_MS);
    return () => {
      cancelled = true;
      window.clearInterval(timer);
    };
  }, [pollMessages, room.id]);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = event.currentTarget;
    const body = String(new FormData(form).get("body") ?? "").trim();
    if (!body) {
      return;
    }
    setSending(true);
    try {
      const message = await sendMessage(room.id, body);
      setMessages((prev) => (prev.some((row) => row.id === message.id) ? prev : [...prev, message]));
      cursorRef.current = message.id;
      form.reset();
      setError(null);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Could not send the message.");
    } finally {
      setSending(false);
    }
  }

  return (
    <section className="chat-thread card">
      <div className="chat-messages" ref={scrollerRef}>
        {messages.length === 0 ? (
          <p className="muted">No messages yet. Owner started this room — say hello.</p>
        ) : (
          messages.map((message) => (
            <article
              key={message.id}
              className={`chat-bubble ${message.sender_role === "owner" ? "owner" : "member"}`}
            >
              <header>
                <strong>{message.sender_name}</strong>
                <span>{formatShopDateTime(message.created_at)}</span>
              </header>
              <p>{message.body}</p>
            </article>
          ))
        )}
      </div>
      {error ? <div className="banner error">{error}</div> : null}
      <form onSubmit={onSubmit} className="chat-compose">
        <label htmlFor={`chat-body-${room.id}`}>
          Message
          <textarea
            id={`chat-body-${room.id}`}
            name="body"
            rows={3}
            required
            maxLength={4000}
            placeholder="Human message — not Matrix, not Grok"
          />
        </label>
        <div className="actions">
          <button type="submit" disabled={sending}>
            {sending ? "Sending…" : "Send"}
          </button>
        </div>
      </form>
    </section>
  );
}
