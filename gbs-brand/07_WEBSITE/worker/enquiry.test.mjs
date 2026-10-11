// Run with: node --test gbs-brand/07_WEBSITE/worker/
import { test, beforeEach, afterEach } from "node:test";
import assert from "node:assert/strict";
import worker, { handleEnquiry, composeEmail } from "./index.js";

const ORIGIN = "https://gbs-pm.co.uk";
const env = { RESEND_API_KEY: "re_test", ENQUIRY_TO: "info@gbs-pm.co.uk", ENQUIRY_FROM: "GBS <onboarding@resend.dev>" };

const valid = {
  name: "Jane Smith",
  company: "Example Managing Agents",
  role: "A managing agent / property manager",
  email: "jane@example.com",
  phone: "020 7946 0000",
  service: "Planned maintenance",
  trade: "Fire doors and firestopping",
  site: "1 Example Road, London N13 6BX",
  message: "Twelve flat entrance doors need inspection and remedials.",
  consent: "yes",
};

function formRequest(fields, { accept = "application/json", origin = ORIGIN, method = "POST" } = {}) {
  const fd = new FormData();
  for (const [k, v] of Object.entries(fields)) fd.append(k, v);
  const headers = { Accept: accept };
  if (origin) headers.Origin = origin;
  return new Request(`${ORIGIN}/api/enquiry`, { method, body: fd, headers });
}

let calls;
const realFetch = globalThis.fetch;
beforeEach(() => {
  calls = [];
  globalThis.fetch = async (url, init) => {
    calls.push({ url, init, body: JSON.parse(init.body) });
    return new Response(JSON.stringify({ id: "email_123" }), { status: 200 });
  };
});
afterEach(() => {
  globalThis.fetch = realFetch;
});

test("non-API requests are served from the assets binding", async () => {
  const ASSETS = { fetch: async () => new Response("asset", { status: 200 }) };
  const res = await worker.fetch(new Request(`${ORIGIN}/services`), { ...env, ASSETS });
  assert.equal(await res.text(), "asset");
});

test("unknown API paths return 404 without touching assets", async () => {
  const res = await worker.fetch(new Request(`${ORIGIN}/api/other`), { ...env, ASSETS: { fetch: () => { throw new Error("no"); } } });
  assert.equal(res.status, 404);
});

test("GET is rejected with 405", async () => {
  const res = await handleEnquiry(new Request(`${ORIGIN}/api/enquiry`), env);
  assert.equal(res.status, 405);
  assert.equal(res.headers.get("Allow"), "POST");
});

test("cross-origin posts are refused", async () => {
  const res = await handleEnquiry(formRequest(valid, { origin: "https://evil.example" }), env);
  assert.equal(res.status, 403);
  assert.equal(calls.length, 0);
});

test("filled honeypot answers ok but sends nothing", async () => {
  const res = await handleEnquiry(formRequest({ ...valid, website: "http://spam.example" }), env);
  assert.equal(res.status, 200);
  assert.deepEqual(await res.json(), { ok: true });
  assert.equal(calls.length, 0);
});

test("missing fields, bad email and no consent give 400 listing the fields", async () => {
  const res = await handleEnquiry(formRequest({ ...valid, name: "  ", email: "not-an-email", consent: "" }), env);
  assert.equal(res.status, 400);
  const data = await res.json();
  assert.deepEqual(data.fields.sort(), ["consent", "email", "name"]);
  assert.equal(calls.length, 0);
});

test("valid multipart post sends the email and returns JSON for fetch callers", async () => {
  const res = await handleEnquiry(formRequest(valid), env);
  assert.equal(res.status, 200);
  assert.deepEqual(await res.json(), { ok: true });
  assert.equal(calls.length, 1);
  assert.equal(calls[0].url, "https://api.resend.com/emails");
  assert.equal(calls[0].init.headers.Authorization, "Bearer re_test");
  const sent = calls[0].body;
  assert.deepEqual(sent.to, ["info@gbs-pm.co.uk"]);
  assert.equal(sent.from, "GBS <onboarding@resend.dev>");
  assert.equal(sent.reply_to, "jane@example.com");
  assert.equal(sent.subject, "Website enquiry: Planned maintenance (Fire doors and firestopping) - Example Managing Agents");
  assert.match(sent.text, /Enquiring as: A managing agent \/ property manager/);
  assert.match(sent.text, /Specific service: Fire doors and firestopping/);
  assert.match(sent.text, /Property address: 1 Example Road, London N13 6BX/);
  assert.match(sent.html, /<th[^>]*>Details of the works<\/th>/);
});

test("a homeowner can enquire without a company name", async () => {
  const res = await handleEnquiry(formRequest({ ...valid, company: "", role: "A homeowner / individual client", service: "Reactive repairs", trade: "" }), env);
  assert.equal(res.status, 200);
  assert.equal(calls.length, 1);
  const sent = calls[0].body;
  assert.equal(sent.subject, "Website enquiry: Reactive repairs - Jane Smith");
  assert.doesNotMatch(sent.text, /Company or organisation:/);
  assert.doesNotMatch(sent.text, /Specific service:/);
});

test("urlencoded post without a JSON accept header redirects to the thank-you page", async () => {
  const body = new URLSearchParams(valid).toString();
  const req = new Request(`${ORIGIN}/api/enquiry`, {
    method: "POST",
    body,
    headers: { "Content-Type": "application/x-www-form-urlencoded", Accept: "text/html", Origin: ORIGIN },
  });
  const res = await handleEnquiry(req, env);
  assert.equal(res.status, 303);
  assert.equal(res.headers.get("Location"), "/thank-you");
  assert.equal(calls.length, 1);
});

test("JSON body is accepted", async () => {
  const req = new Request(`${ORIGIN}/api/enquiry`, {
    method: "POST",
    body: JSON.stringify(valid),
    headers: { "Content-Type": "application/json", Accept: "application/json", Origin: ORIGIN },
  });
  const res = await handleEnquiry(req, env);
  assert.equal(res.status, 200);
  assert.equal(calls.length, 1);
});

test("unsupported content type gives 415", async () => {
  const req = new Request(`${ORIGIN}/api/enquiry`, { method: "POST", body: "x", headers: { "Content-Type": "text/plain", Origin: ORIGIN } });
  const res = await handleEnquiry(req, env);
  assert.equal(res.status, 415);
});

test("missing API key gives 503 so the site can fall back to email", async () => {
  const res = await handleEnquiry(formRequest(valid), { ...env, RESEND_API_KEY: "" });
  assert.equal(res.status, 503);
  assert.equal(calls.length, 0);
});

test("relay rejection gives 502", async () => {
  globalThis.fetch = async () => new Response("nope", { status: 500 });
  const res = await handleEnquiry(formRequest(valid), env);
  assert.equal(res.status, 502);
});

test("values are trimmed, capped and HTML-escaped", () => {
  const req = new Request(`${ORIGIN}/api/enquiry`, { headers: { "CF-Connecting-IP": "203.0.113.9" } });
  const email = composeEmail({ ...valid, message: "<b>bold</b> & \"quotes\"", role: "" }, req, env);
  assert.match(email.html, /&lt;b&gt;bold&lt;\/b&gt; &amp; &quot;quotes&quot;/);
  assert.doesNotMatch(email.text, /Role:/);
  assert.match(email.text, /IP 203\.0\.113\.9/);
});
