/* GBS Property Maintenance - site script (no dependencies). Mobile navigation and contact form handling. */
(function () {
  "use strict";
  /**
   * Mobile navigation: the menu is hidden under 860 px and revealed by the toggle button,
   * with aria-expanded kept in sync so screen readers announce the state. Escape closes it.
   */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) { nav.classList.remove("open"); toggle.setAttribute("aria-expanded", "false"); toggle.focus(); }
    });
  }

  var form = document.getElementById("quote-form");
  if (!form) return;
  var status = document.getElementById("form-status");
  var endpoint = form.getAttribute("data-endpoint") || "";
  var mailto = form.getAttribute("data-mailto") || "";
  /** Writes feedback into the live region under the form so the visitor knows what happened. */
  var setStatus = function (msg, state) { if (status) { status.textContent = msg; status.setAttribute("data-state", state || ""); } };

  /**
   * Submission has two modes so the site works without any third-party service:
   * posts to a configured form endpoint when one is set in company.json, otherwise
   * opens the visitor's email client with the enquiry pre-filled (mailto).
   */
  form.addEventListener("submit", function (e) {
    if (form.querySelector("[name='website']").value) { e.preventDefault(); return; } // honeypot
    if (!form.checkValidity()) {
      // The form carries novalidate so the browser does not block the mailto fallback;
      // ask it to show its own messages here and stop the submission.
      e.preventDefault();
      form.reportValidity();
      setStatus("Please complete the highlighted fields.", "error");
      return;
    }
    var data = new FormData(form);
    if (endpoint) {
      e.preventDefault();
      setStatus("Sending your enquiry...", "");
      var btn = form.querySelector("button[type='submit']"); if (btn) btn.disabled = true;
      fetch(endpoint, { method: "POST", body: data, headers: { "Accept": "application/json" } })
        .then(function (r) {
          if (r.ok) { showSent(); return; }
          if (r.status === 400) {
            // The relay found a problem with the details: say so and let the visitor correct it.
            return r.json().then(function (j) { throw { handled: true, message: (j && j.error) || "Please check the details and try again." }; });
          }
          throw new Error("Request failed");
        })
        .catch(function (err) {
          if (btn) btn.disabled = false;
          if (err && err.handled) { setStatus(err.message, "error"); return; }
          // Relay unavailable: never lose the enquiry, hand it to the visitor's email client instead.
          setStatus("Sorry, the form could not be sent automatically. Your email client should open with the enquiry pre-filled; otherwise email " + mailto + " or call " + (form.getAttribute("data-phone") || "us") + ".", "error");
          window.location.href = mailtoLink(data);
        });
      return;
    }
    // No form endpoint configured: open the visitor's email client with the enquiry pre-filled.
    e.preventDefault();
    window.location.href = mailtoLink(data);
    setStatus("Your email client should open with the enquiry pre-filled. If it does not, please email " + mailto + ".", "");
  });

  /** Clears the form and replaces it with a confirmation so the visitor knows the enquiry has gone. */
  function showSent() {
    form.reset();
    setStatus("", "");
    var submit = form.querySelector("button[type='submit']"); if (submit) submit.disabled = false;
    var phone = form.getAttribute("data-phone") || "";
    var tel = form.getAttribute("data-phone-tel") || "";
    var hours = form.getAttribute("data-hours") || "working hours";
    var box = document.createElement("div");
    box.className = "form-sent";
    box.setAttribute("role", "status");
    box.tabIndex = -1;
    box.innerHTML =
      '<h3>Enquiry sent</h3>' +
      '<p>Thank you. Your enquiry has been received and we will come back to you during working hours (' + escapeText(hours) + ').' +
      (phone ? ' If the matter is urgent, call <a href="tel:' + escapeText(tel) + '" class="num">' + escapeText(phone) + '</a>.' : '') + '</p>' +
      '<p><button type="button" class="btn btn-outline">Send another enquiry</button></p>';
    form.parentNode.insertBefore(box, form);
    form.hidden = true;
    box.querySelector("button").addEventListener("click", function () {
      box.parentNode.removeChild(box);
      form.hidden = false;
      var first = form.querySelector("input, select, textarea"); if (first) first.focus();
    });
    box.focus();
    if (box.scrollIntoView) box.scrollIntoView({ block: "center", behavior: "smooth" });
  }

  function escapeText(s) {
    return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; });
  }

  /** Builds a mailto: link to the company inbox with the enquiry fields in the body. */
  function mailtoLink(data) {
    var lines = [];
    ["name", "company", "role", "email", "phone", "site", "service", "message"].forEach(function (k) {
      var v = data.get(k); if (v) lines.push(k.charAt(0).toUpperCase() + k.slice(1) + ": " + v);
    });
    var subject = "Quote request - " + (data.get("service") || "General enquiry") + (data.get("site") ? " - " + data.get("site") : "");
    return "mailto:" + mailto + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(lines.join("\n"));
  }
})();
