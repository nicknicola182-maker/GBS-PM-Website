/* GBS Property Maintenance - site script (no dependencies). Navigation, service category filtering and contact form handling. */
(function () {
  "use strict";

  var reducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /**
   * Navigation: the menu is hidden under 860 px and revealed by the toggle button, with
   * aria-expanded kept in sync so screen readers announce the state. Escape closes it, as does
   * choosing a link, so same-page anchors (Sectors, Projects) do not leave the menu open.
   */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  function setMenu(open) {
    nav.classList.toggle("open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
  }
  if (toggle && nav) {
    toggle.addEventListener("click", function () { setMenu(!nav.classList.contains("open")); });
    nav.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) { setMenu(false); toggle.focus(); }
    });
  }

  /**
   * Services page: the three category cards filter the server-rendered service list.
   * Every service is in the HTML, so the full list is indexable and visible without JavaScript.
   * The chosen category is kept in the URL (?category=) and restored on reload and browser Back.
   */
  var grid = document.getElementById("directory-grid");
  if (grid) {
    var CATEGORIES = {
      all: { title: "The full service range", text: "Explore the trades and services available for individual properties, residential buildings and managed portfolios." },
      planned: { title: "Planned maintenance", text: "Scheduled care, recurring work and preventative programmes for your home, building or portfolio." },
      reactive: { title: "Reactive repairs", text: "Practical repair services when something goes wrong, from an individual flat to a wider estate." },
      improve: { title: "Refurbishments & improvements", text: "The trades and coordination needed to improve a home, upgrade shared spaces or deliver a larger project." }
    };
    var cards = Array.prototype.slice.call(grid.querySelectorAll(".trade-card[data-groups]"));
    var buttons = Array.prototype.slice.call(document.querySelectorAll("[data-filter]"));
    var heading = document.getElementById("directory-heading");
    var description = document.getElementById("directory-description");
    var count = document.getElementById("result-count");
    var list = document.getElementById("service-list");

    function fromUrl() {
      var c = new URLSearchParams(window.location.search).get("category");
      if (!CATEGORIES[c] || c === "all") return "all";
      // A link straight to a service that is not in the requested category shows the full list instead of hiding it.
      var target = window.location.hash ? document.getElementById(window.location.hash.slice(1)) : null;
      if (target && target.classList.contains("trade-card") && (" " + target.getAttribute("data-groups") + " ").indexOf(" " + c + " ") === -1) return "all";
      return c;
    }
    function apply(filter) {
      var shown = 0;
      cards.forEach(function (card) {
        var match = filter === "all" || (" " + card.getAttribute("data-groups") + " ").indexOf(" " + filter + " ") !== -1;
        card.hidden = !match; if (match) shown++;
      });
      buttons.forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-filter") === filter ? "true" : "false"); });
      heading.textContent = CATEGORIES[filter].title;
      description.textContent = CATEGORIES[filter].text;
      count.textContent = shown + (shown === 1 ? " service" : " services") + (filter === "all" ? " listed" : " in this category");
    }
    function urlFor(filter) {
      return window.location.pathname + (filter === "all" ? "" : "?category=" + filter) + "#service-list";
    }
    buttons.forEach(function (b) {
      b.addEventListener("click", function () {
        var filter = b.getAttribute("data-filter");
        apply(filter);
        if (window.history && history.pushState) history.pushState({ category: filter }, "", urlFor(filter));
        if (list) list.scrollIntoView({ behavior: reducedMotion ? "auto" : "smooth", block: "start" });
      });
    });
    window.addEventListener("popstate", function () { apply(fromUrl()); });
    apply(fromUrl());
  }

  /** Contact form: posts to the Worker relay, with the visitor's email client as the fallback. */
  var form = document.getElementById("quote-form");
  if (!form) return;
  var status = document.getElementById("form-status");
  var endpoint = form.getAttribute("data-endpoint") || "";
  var mailto = form.getAttribute("data-mailto") || "";
  var setStatus = function (msg, state) { if (status) { status.textContent = msg; status.setAttribute("data-state", state || ""); } };

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
      '<p><button type="button" class="text-link">Send another enquiry</button></p>';
    form.parentNode.insertBefore(box, form);
    form.hidden = true;
    box.querySelector("button").addEventListener("click", function () {
      box.parentNode.removeChild(box);
      form.hidden = false;
      var first = form.querySelector("input, select, textarea"); if (first) first.focus();
    });
    box.focus();
    if (box.scrollIntoView) box.scrollIntoView({ block: "center", behavior: reducedMotion ? "auto" : "smooth" });
  }

  function escapeText(s) {
    return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; });
  }

  /** Builds a mailto: link to the company inbox with the enquiry fields in the body. */
  function mailtoLink(data) {
    var labels = { name: "Name", company: "Company", role: "Enquiring as", email: "Email", phone: "Phone", service: "Type of work", trade: "Specific service", site: "Property address", message: "Details" };
    var lines = [];
    ["name", "company", "role", "email", "phone", "service", "trade", "site", "message"].forEach(function (k) {
      var v = data.get(k); if (v) lines.push(labels[k] + ": " + v);
    });
    var subject = "Enquiry - " + (data.get("service") || "General enquiry") + (data.get("site") ? " - " + data.get("site") : "");
    return "mailto:" + mailto + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(lines.join("\n"));
  }
})();
