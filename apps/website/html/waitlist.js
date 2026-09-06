(function () {
  var CONTACT_EMAIL = "info@projectcar.ca";

  function baseUrl() {
    return (window.PC_SHOP_API_BASE || "https://api.projectcar.ca").replace(/\/$/, "");
  }

  function mailtoHref(fields) {
    var subject = encodeURIComponent("Waitlist interest");
    var lines = [];
    if (fields) {
      if (fields.name) lines.push("Name: " + fields.name);
      if (fields.email) lines.push("Email: " + fields.email);
      if (fields.phone) lines.push("Phone: " + fields.phone);
      if (fields.notes) lines.push("Notes: " + fields.notes);
    }
    var body = lines.length ? "&body=" + encodeURIComponent(lines.join("\n")) : "";
    return "mailto:" + CONTACT_EMAIL + "?subject=" + subject + body;
  }

  function setStatus(el, kind, text, opts) {
    if (!el) return;
    el.hidden = !text;
    el.dataset.kind = kind || "";
    el.textContent = "";
    if (!text) return;

    el.appendChild(document.createTextNode(text));

    if (opts && opts.mailto) {
      el.appendChild(document.createTextNode(" "));
      var a = document.createElement("a");
      a.href = opts.mailto;
      a.textContent = CONTACT_EMAIL;
      el.appendChild(a);
      el.appendChild(document.createTextNode("."));
    }
  }

  async function submitWaitlist(form) {
    var status = form.querySelector("[data-waitlist-status]");
    var btn = form.querySelector("[type=submit]");
    var name = String((form.elements.namedItem("name") || {}).value || "").trim();
    var email = String((form.elements.namedItem("email") || {}).value || "").trim();
    var phone = String((form.elements.namedItem("phone") || {}).value || "").trim();
    var notes = String((form.elements.namedItem("notes") || {}).value || "").trim();
    var mailto = mailtoHref({
      name: name,
      email: email,
      phone: phone,
      notes: notes
    });

    setStatus(status, "pending", "Sending…");
    if (btn) btn.disabled = true;

    var body = {
      name: name,
      email: email,
      phone: phone || null,
      notes: notes || null
    };

    try {
      var res = await fetch(baseUrl() + "/waitlist", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(body)
      });
      var data = null;
      try { data = await res.json(); } catch (_) { /* ignore */ }

      if (res.status === 201) {
        setStatus(status, "ok", "You're on the list. We'll email you when membership access is ready.");
        form.reset();
        return;
      }
      if (res.status === 409) {
        setStatus(status, "err", "That email is already on the list.");
        return;
      }
      if (res.status === 404 && data && data.detail && data.detail.code === "waitlist_disabled") {
        setStatus(status, "err", "Waitlist isn't taking submissions right now. Email", { mailto: mailto });
        return;
      }
      setStatus(status, "err", "Could not join the waitlist. Try again, or email", { mailto: mailto });
    } catch (err) {
      setStatus(status, "err", "Could not reach the waitlist. Email", { mailto: mailto });
    } finally {
      if (btn) btn.disabled = false;
    }
  }

  function enhance(form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      submitWaitlist(form);
    });
  }

  document.querySelectorAll("form[data-waitlist-form]").forEach(enhance);
})();
