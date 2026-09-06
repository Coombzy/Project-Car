/* Apex chat panel — Project Car Contact page */
(function () {
  const mount = document.querySelector("[data-apex-mount]");
  if (!mount) return;

  // Bump keys when greeting/policy changes so visitors see the new intro.
  const STORAGE_KEY = "pc_apex_session_v2";
  const HISTORY_KEY = "pc_apex_history_v2";
  const INTRO =
    "Hey, I'm Apex, Project Car's Community Assistant. I'm here to help answer as many Project Car related questions as I can and I'm also here to take any feedback you have! How can I help?";

  function newId() {
    return (crypto.randomUUID && crypto.randomUUID()) || String(Date.now()) + Math.random();
  }

  function loadSession() {
    try {
      let id = localStorage.getItem(STORAGE_KEY);
      if (!id) {
        id = newId();
        localStorage.setItem(STORAGE_KEY, id);
      }
      return id;
    } catch (_) {
      return newId();
    }
  }

  function loadHistory() {
    try {
      const raw = localStorage.getItem(HISTORY_KEY);
      const arr = raw ? JSON.parse(raw) : [];
      return Array.isArray(arr) ? arr.slice(-12) : [];
    } catch (_) {
      return [];
    }
  }

  function saveHistory(h) {
    try {
      localStorage.setItem(HISTORY_KEY, JSON.stringify(h.slice(-12)));
    } catch (_) {}
  }

  function clearChatStorage() {
    try {
      localStorage.removeItem(STORAGE_KEY);
      localStorage.removeItem(HISTORY_KEY);
      // Drop legacy keys too
      localStorage.removeItem("pc_apex_session_v1");
      localStorage.removeItem("pc_apex_history_v1");
    } catch (_) {}
  }

  let sessionId = loadSession();
  let history = loadHistory();
  let busy = false;

  mount.innerHTML = "";
  mount.classList.add("apex-live");

  const shell = document.createElement("div");
  shell.className = "apex-chat";
  shell.innerHTML = `
    <div class="apex-chat-toolbar">
      <button type="button" class="apex-new-chat" id="apex-new-chat">New chat</button>
    </div>
    <div class="apex-chat-log" id="apex-log" role="log" aria-live="polite" aria-relevant="additions"></div>
    <form class="apex-chat-form" id="apex-form">
      <label class="visually-hidden" for="apex-input">Message to Apex</label>
      <textarea id="apex-input" name="message" rows="2" maxlength="2000" placeholder="Ask Apex about Project Car…" required></textarea>
      <button type="submit" id="apex-send">Send</button>
    </form>
    <p class="apex-chat-foot">Apex uses Project Car’s public info only. For anything sensitive or official, email <a href="mailto:info@projectcar.ca">info@projectcar.ca</a>.</p>
  `;
  mount.appendChild(shell);

  const logEl = shell.querySelector("#apex-log");
  const form = shell.querySelector("#apex-form");
  const input = shell.querySelector("#apex-input");
  const sendBtn = shell.querySelector("#apex-send");
  const newChatBtn = shell.querySelector("#apex-new-chat");

  function addBubble(role, text) {
    const row = document.createElement("div");
    row.className = "apex-row apex-row-" + role;

    if (role === "assistant") {
      const av = document.createElement("img");
      av.className = "apex-avatar";
      av.src = "assets/apex.jpg?v=11";
      av.width = 40;
      av.height = 40;
      av.alt = "";
      av.decoding = "async";
      row.appendChild(av);
    }

    const div = document.createElement("div");
    div.className = "apex-bubble apex-bubble-" + role;
    const who = document.createElement("div");
    who.className = "apex-who";
    who.textContent = role === "user" ? "You" : "Apex";
    const body = document.createElement("div");
    body.className = "apex-bubble-text";
    body.textContent = text;
    div.appendChild(who);
    div.appendChild(body);
    row.appendChild(div);
    logEl.appendChild(row);
    logEl.scrollTop = logEl.scrollHeight;
  }

  function showIntro() {
    logEl.innerHTML = "";
    addBubble("assistant", INTRO);
  }

  function resetChat() {
    if (busy) return;
    clearChatStorage();
    sessionId = loadSession();
    history = [];
    saveHistory(history);
    showIntro();
    input.focus();
  }

  if (history.length) {
    history.forEach((m) => addBubble(m.role === "assistant" ? "assistant" : "user", m.content));
  } else {
    showIntro();
  }

  newChatBtn.addEventListener("click", resetChat);

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (busy) return;
    const message = (input.value || "").trim();
    if (!message) return;

    busy = true;
    sendBtn.disabled = true;
    newChatBtn.disabled = true;
    input.value = "";
    addBubble("user", message);
    history.push({ role: "user", content: message });
    saveHistory(history);

    const thinking = document.createElement("div");
    thinking.className = "apex-row apex-row-assistant";
    thinking.innerHTML =
      '<img class="apex-avatar" src="assets/apex.jpg?v=11" width="40" height="40" alt="">' +
      '<div class="apex-bubble apex-bubble-assistant apex-thinking">Apex is thinking…</div>';
    logEl.appendChild(thinking);
    logEl.scrollTop = logEl.scrollHeight;

    try {
      const res = await fetch("/api/apex/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          message,
          history: history.slice(0, -1),
        }),
      });
      const data = await res.json().catch(() => ({}));
      thinking.remove();
      const reply =
        (data && data.reply) ||
        "I couldn’t respond just now. Please email info@projectcar.ca.";
      addBubble("assistant", reply);
      history.push({ role: "assistant", content: reply });
      saveHistory(history);
    } catch (_) {
      thinking.remove();
      const reply =
        "Connection problem. Please try again, or email info@projectcar.ca.";
      addBubble("assistant", reply);
      history.push({ role: "assistant", content: reply });
      saveHistory(history);
    } finally {
      busy = false;
      sendBtn.disabled = false;
      newChatBtn.disabled = false;
      input.focus();
    }
  });

  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      form.requestSubmit();
    }
  });
})();
