import type { CalendarStatus, Todo } from "../lib/config";
import { formatShopDateTime, shopDateTimeLocal } from "../lib/time";
import { CalendarConnect } from "./calendar-connect";
import { CopyEventButton } from "./copy-event-button";

type TodoActions = {
  create: (formData: FormData) => Promise<void>;
  toggle: (formData: FormData) => Promise<void>;
  remove: (formData: FormData) => Promise<void>;
};

export function TodoPanel({
  todos,
  calendar,
  actions,
  icsPath,
  audience,
}: {
  todos: Todo[];
  calendar: CalendarStatus | null;
  actions: TodoActions;
  icsPath: (id: string) => string;
  audience: "owner" | "member";
}) {
  const open = todos.filter((todo) => todo.status === "open");
  const done = todos.filter((todo) => todo.status === "done");
  return (
    <section className="todo-panel">
      <h2>{audience === "owner" ? "Your to-dos" : "Your to-dos"}</h2>
      <p className="muted">
        Personal list for this session. Download ICS or copy the event to add a
        due date to Apple or Google Calendar.
      </p>
      {todos.length === 0 ? (
        <div className="banner empty">Nothing on your list. Add one below.</div>
      ) : (
        <div className="card">
          <ul className="todo-list">
            {[...open, ...done].map((todo) => (
              <li key={todo.id} className={`todo-row${todo.status === "done" ? " is-done" : ""}`}>
                <form action={actions.toggle}>
                  <input type="hidden" name="id" value={todo.id} />
                  <input type="hidden" name="status" value={todo.status} />
                  <button className="ghost" type="submit">
                    {todo.status === "done" ? "Reopen" : "Done"}
                  </button>
                </form>
                <div>
                  <strong>{todo.title}</strong>
                  {todo.notes ? <div className="muted">{todo.notes}</div> : null}
                  <div className="muted">
                    {todo.due_at ? `Due ${formatShopDateTime(todo.due_at)}` : "No due date"}
                  </div>
                </div>
                <CopyEventButton todo={todo} icsHref={icsPath(todo.id)} />
                <form action={actions.remove}>
                  <input type="hidden" name="id" value={todo.id} />
                  <button className="ghost" type="submit">
                    Delete
                  </button>
                </form>
              </li>
            ))}
          </ul>
        </div>
      )}

      <form action={actions.create} className="card stack-form todo-create">
        <h3>Add a to-do</h3>
        <label>
          Title
          <input name="title" required maxLength={200} placeholder="Call a member, confirm a bay…" />
        </label>
        <label>
          Notes
          <input name="notes" maxLength={2000} placeholder="Optional" />
        </label>
        <label>
          Due (America/Regina)
          <input name="due_at" type="datetime-local" defaultValue="" min={shopDateTimeLocal()} />
        </label>
        <div className="actions">
          <button type="submit">Add to-do</button>
        </div>
      </form>
      <CalendarConnect calendar={calendar} />
    </section>
  );
}
