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
    if (!form.checkValidity()) { return; } // browser shows validation messages
    var data = new FormData(form);
    if (endpoint) {
      e.preventDefault();
      setStatus("Sending your enquiry...", "");
      var btn = form.querySelector("button[type='submit']"); if (btn) btn.disabled = true;
      fetch(endpoint, { method: "POST", body: data, headers: { "Accept": "application/json" } })
        .then(function (r) { if (!r.ok) throw new Error("Request failed"); window.location.href = "/thank-you"; })
        .catch(function () {
          setStatus("Sorry, the form could not be sent. Please email us directly or call " + (form.getAttribute("data-phone") || "us") + ".", "error");
          if (btn) btn.disabled = false;
        });
      return;
    }
    // No form endpoint configured: open the visitor's email client with the enquiry pre-filled.
    e.preventDefault();
    var lines = [];
    ["name", "company", "role", "email", "phone", "site", "service", "message"].forEach(function (k) {
      var v = data.get(k); if (v) lines.push(k.charAt(0).toUpperCase() + k.slice(1) + ": " + v);
    });
    var subject = "Quote request - " + (data.get("service") || "General enquiry") + (data.get("site") ? " - " + data.get("site") : "");
    window.location.href = "mailto:" + mailto + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(lines.join("\n"));
    setStatus("Your email client should open with the enquiry pre-filled. If it does not, please email " + mailto + ".", "");
  });
})();
