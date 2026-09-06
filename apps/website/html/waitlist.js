(function () {
  function baseUrl() {
    return (window.PC_SHOP_API_BASE || "https://api.projectcar.ca").replace(/\/$/, "");
  }

  function setStatus(el, kind, text) {
    if (!el) return;
    el.hidden = !text;
    el.textContent = text || "";
    el.dataset.kind = kind || "";
  }

  async function submitWaitlist(form) {
    var status = form.querySelector("[data-waitlist-status]");
    var btn = form.querySelector("[type=submit]");
    var name = (form.elements.namedItem("name") || {}).value || "";
    var email = (form.elements.namedItem("email") || {}).value || "";
    var phone = (form.elements.namedItem("phone") || {}).value || "";
    var notes = (form.elements.namedItem("notes") || {}).value || "";

    setStatus(status, "pending", "Sending…");
    if (btn) btn.disabled = true;

    var body = {
      name: String(name).trim(),
      email: String(email).trim(),
      phone: String(phone).trim() || null,
      notes: String(notes).trim() || null
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
        setStatus(status, "ok", "You're on the waitlist. We'll be in touch.");
        form.reset();
        return;
      }
      if (res.status === 409) {
        setStatus(status, "err", "That email is already on the waitlist.");
        return;
      }
      if (res.status === 404 && data && data.detail && data.detail.code === "waitlist_disabled") {
        setStatus(status, "err", "Waitlist is not open yet. Email info@projectcar.ca instead.");
        return;
      }
      var msg = (data && data.detail && (data.detail.message || data.detail)) || ("Request failed (" + res.status + "). Try again or email info@projectcar.ca.");
      if (typeof msg !== "string") msg = "Request failed. Try again or email info@projectcar.ca.";
      setStatus(status, "err", msg);
    } catch (err) {
      setStatus(
        status,
        "err",
        "Could not reach the waitlist API (" + baseUrl() + "). Email info@projectcar.ca for now."
      );
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
