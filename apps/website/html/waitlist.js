(function () {
  var CONTACT_EMAIL = "info@projectcar.ca";
  var DISCORD_URL = "https://discord.gg/projectcar";

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

  function appendLink(el, href, label, extra) {
    var a = document.createElement("a");
    a.href = href;
    a.textContent = label;
    if (extra && extra.external) {
      a.target = "_blank";
      a.rel = "noopener noreferrer";
    }
    el.appendChild(a);
    return a;
  }

  function setStatus(el, kind, text, opts) {
    if (!el) return;
    el.hidden = !text;
    el.dataset.kind = kind || "";
    el.textContent = "";
    if (!text) return;

    el.appendChild(document.createTextNode(text));

    if (opts && opts.discord && opts.mailto) {
      el.appendChild(document.createTextNode(" "));
      appendLink(el, DISCORD_URL, "Discord", { external: true });
      el.appendChild(document.createTextNode(", or email "));
      appendLink(el, opts.mailto, CONTACT_EMAIL);
      el.appendChild(document.createTextNode("."));
      return;
    }

    if (opts && opts.discord) {
      el.appendChild(document.createTextNode(" "));
      appendLink(el, DISCORD_URL, "Discord", { external: true });
      el.appendChild(document.createTextNode("."));
      return;
    }

    if (opts && opts.mailto) {
      el.appendChild(document.createTextNode(" "));
      appendLink(el, opts.mailto, CONTACT_EMAIL);
      el.appendChild(document.createTextNode("."));
    }
  }

  function setShopUnreachable(status, mailto) {
    setStatus(
      status,
      "err",
      "The shop API is briefly unreachable. Join",
      { discord: true, mailto: mailto }
    );
  }

  function headerHaystack(res) {
    var bits = [];
    try {
      if (res && res.headers && typeof res.headers.forEach === "function") {
        res.headers.forEach(function (value, name) {
          bits.push(name + ":" + value);
        });
      }
    } catch (_) { /* ignore */ }
    return bits.join("\n");
  }

  function looksLikeCf1033(hay) {
    if (!hay) return false;
    var s = String(hay);
    if (/error[\s:-]*1033\b/i.test(s)) return true;
    if (/\bcf-error-code\b/i.test(s) && /\b1033\b/.test(s)) return true;
    if (/cloudflare/i.test(s) && /\b1033\b/.test(s)) return true;
    return false;
  }

  function isShopUnreachable(res, rawText) {
    if (!res) return true;
    if (res.status === 502 || res.status === 530) return true;
    if (looksLikeCf1033(rawText)) return true;
    return looksLikeCf1033(headerHaystack(res));
  }

  async function readResponse(res) {
    var rawText = "";
    try { rawText = await res.text(); } catch (_) { /* ignore */ }
    var data = null;
    if (rawText) {
      try { data = JSON.parse(rawText); } catch (_) { /* ignore */ }
    }
    return { rawText: rawText, data: data };
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
      var parsed = await readResponse(res);
      var data = parsed.data;

      if (isShopUnreachable(res, parsed.rawText)) {
        setShopUnreachable(status, mailto);
        return;
      }
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
      setShopUnreachable(status, mailto);
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
