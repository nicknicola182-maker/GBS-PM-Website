/**
 * Cloudflare Worker for gbs-pm.co.uk.
 *
 * Serves the static site from the assets binding and handles one API route,
 * POST /api/enquiry, which validates the quote request form and emails it to
 * the company inbox through Resend (https://resend.com).
 *
 * Configuration (wrangler.jsonc vars and a dashboard secret):
 *   ENQUIRY_TO      recipient mailbox, e.g. info@gbs-pm.co.uk
 *   ENQUIRY_FROM    sender shown on the email; must be a Resend-verified sender
 *   RESEND_API_KEY  secret, set in Cloudflare (Workers, gbs-pm-website, Settings,
 *                   Variables and Secrets). Never commit it.
 */

const RESEND_URL = "https://api.resend.com/emails";
const DEFAULT_TO = "info@gbs-pm.co.uk";
const DEFAULT_FROM = "GBS Property Maintenance website <onboarding@resend.dev>";
const THANK_YOU = "/thank-you";

/** Form fields, their labels in the email and maximum accepted length. */
const FIELDS = [
  ["name", "Name", 120],
  ["role", "Enquiring as", 120],
  ["company", "Company or organisation", 160],
  ["email", "Email", 254],
  ["phone", "Telephone", 40],
  ["service", "Type of work", 160],
  ["trade", "Specific service", 160],
  ["site", "Property address", 300],
  ["message", "Details of the works", 5000],
];
// Company is optional so homeowners and individual clients can enquire; role and trade are optional too.
const REQUIRED = ["name", "email", "phone", "service", "site", "message"];
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/enquiry") return handleEnquiry(request, env);
    if (url.pathname.startsWith("/api/")) return json({ error: "Not found" }, 404);
    return env.ASSETS.fetch(request);
  },
};

/** Validates and relays one quote request. Exported for the unit tests. */
export async function handleEnquiry(request, env) {
  if (request.method !== "POST") {
    return json({ error: "Method not allowed" }, 405, { Allow: "POST" });
  }
  const url = new URL(request.url);
  const origin = request.headers.get("Origin");
  if (origin && origin !== url.origin) return json({ error: "Forbidden" }, 403);

  const body = await readBody(request);
  if (!body) return json({ error: "Unsupported content type" }, 415);

  const fields = {};
  for (const [key, , max] of FIELDS) fields[key] = clean(body[key], max);
  const consent = clean(body.consent, 10).toLowerCase();
  const honeypot = clean(body.website, 200);

  // Bots fill the hidden "website" field; answer as if sent so they move on.
  if (honeypot) return success(request);

  const missing = REQUIRED.filter((k) => !fields[k]);
  if (!EMAIL_RE.test(fields.email)) missing.push("email");
  if (!["yes", "on", "true", "1"].includes(consent)) missing.push("consent");
  if (missing.length) {
    return json({ error: "Please complete the highlighted fields", fields: [...new Set(missing)] }, 400);
  }

  if (!env.RESEND_API_KEY) {
    console.error("enquiry: RESEND_API_KEY is not set");
    return json({ error: "The enquiry relay is not configured" }, 503);
  }

  const email = composeEmail(fields, request, env);
  let res;
  try {
    res = await fetch(RESEND_URL, {
      method: "POST",
      headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
      body: JSON.stringify(email),
    });
  } catch (err) {
    console.error("enquiry: relay request failed", String(err));
    return json({ error: "The enquiry could not be sent" }, 502);
  }
  if (!res.ok) {
    console.error("enquiry: relay rejected the email", res.status, await res.text().catch(() => ""));
    return json({ error: "The enquiry could not be sent" }, 502);
  }
  return success(request);
}

/** Builds the Resend payload: plain text plus a simple HTML table, reply-to the visitor. */
export function composeEmail(fields, request, env) {
  const to = env.ENQUIRY_TO || DEFAULT_TO;
  const from = env.ENQUIRY_FROM || DEFAULT_FROM;
  const when = new Date().toISOString().replace("T", " ").slice(0, 16) + " UTC";
  const ip = request.headers.get("CF-Connecting-IP") || "";
  const country = (request.cf && request.cf.country) || "";
  const meta = `Sent from the website form at ${when}` + (ip ? `, IP ${ip}` : "") + (country ? ` (${country})` : "") + ".";

  const rows = FIELDS.filter(([k]) => fields[k]).map(([k, label]) => [label, fields[k]]);
  const text = rows.map(([label, value]) => `${label}: ${value}`).join("\n") + `\n\n${meta}\n`;
  const html =
    `<table cellpadding="6" style="border-collapse:collapse;font:14px/1.4 Arial,sans-serif">` +
    rows
      .map(
        ([label, value]) =>
          `<tr><th align="left" valign="top" style="background:#f2f2f0;border:1px solid #dadada">${escapeHtml(label)}</th>` +
          `<td valign="top" style="border:1px solid #dadada;white-space:pre-wrap">${escapeHtml(value)}</td></tr>`
      )
      .join("") +
    `</table><p style="font:12px Arial,sans-serif;color:#555">${escapeHtml(meta)}</p>`;

  return {
    from,
    to: [to],
    reply_to: fields.email,
    subject: `Website enquiry: ${fields.service}${fields.trade ? ` (${fields.trade})` : ""} - ${fields.company || fields.name}`,
    text,
    html,
  };
}

/** Reads multipart, urlencoded or JSON bodies into a plain object of strings. */
async function readBody(request) {
  const type = (request.headers.get("Content-Type") || "").toLowerCase();
  try {
    if (type.includes("application/json")) {
      const data = await request.json();
      return data && typeof data === "object" ? data : null;
    }
    if (type.includes("multipart/form-data") || type.includes("application/x-www-form-urlencoded")) {
      const out = {};
      for (const [k, v] of await request.formData()) if (typeof v === "string") out[k] = v;
      return out;
    }
  } catch {
    return null;
  }
  return null;
}

function clean(value, max) {
  if (typeof value !== "string") return "";
  return value.replace(/\r\n?/g, "\n").trim().slice(0, max);
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
}

/** JSON for fetch callers, otherwise a redirect to the thank-you page for plain form posts. */
function success(request) {
  const accept = request.headers.get("Accept") || "";
  if (accept.includes("application/json")) return json({ ok: true }, 200);
  return new Response(null, { status: 303, headers: { Location: THANK_YOU } });
}

function json(data, status = 200, extra = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", ...extra },
  });
}
