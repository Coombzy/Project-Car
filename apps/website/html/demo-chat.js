(function () {
  var form = document.querySelector("[data-demo-chat]");
  if (!form) return;
  var input = form.querySelector("[data-demo-chat-input]");
  var status = form.querySelector("[data-demo-chat-status]");
  var log = form.querySelector("[data-demo-chat-log]");
  var button = form.querySelector("button[type=submit]");

  function say(text) {
    status.hidden = false;
    status.textContent = text;
  }

  function line(who, text) {
    var p = document.createElement("p");
    p.className = "demo-chat-line";
    var label = document.createElement("span");
    label.className = "demo-chat-who";
    label.textContent = who;
    p.appendChild(label);
    p.appendChild(document.createTextNode(text));
    log.appendChild(p);
  }

  var errors = {
    not_connected: "Demo chat is not connected yet. Email or Discord still work.",
    busy: "Demo chat is busy. Try again in a few minutes, or use email.",
    no_reply: "The demo assistant did not answer in time. Email or Discord still work.",
    not_sent: "Demo chat could not send that. Email or Discord still work.",
    bad_message: "Keep it to one short message, under 400 characters.",
  };

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var message = (input.value || "").replace(/\s+/g, " ").trim();
    if (!message || message.length > 400) {
      say(errors.bad_message);
      return;
    }
    button.disabled = true;
    say("Sending…");
    fetch("/api/demo-chat", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ message: message }),
    })
      .then(function (response) {
        return response.json().then(function (body) {
          return { ok: response.ok, body: body || {} };
        });
      })
      .then(function (result) {
        if (result.ok && result.body.reply) {
          line("You", message);
          line("Demo", result.body.reply);
          input.value = "";
          say("Demo only. The shop is not open.");
          return;
        }
        say(errors[result.body.error] || errors.not_sent);
      })
      .catch(function () {
        say(errors.not_sent);
      })
      .then(function () {
        button.disabled = false;
      });
  });
})();
