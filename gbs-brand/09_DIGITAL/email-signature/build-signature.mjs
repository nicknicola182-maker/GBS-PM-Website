// GBS HORIZON email signature compiler.
// Resolves {{company.*}} tokens from company.json (same regex as tools/render.mjs) so the signature can be
// pasted into mail clients without the renderer. Usage (from gbs-brand root or anywhere):
//   node 09_DIGITAL/email-signature/build-signature.mjs
// Writes: signature.compiled.html, signature-generic.compiled.html, signature.compiled.txt,
//         signature.preview.html (compiled, but pointing the logo at the local PNG for offline review).
import fs from "node:fs";
import path from "node:path";

const HERE = path.dirname(new URL(import.meta.url).pathname);
const ROOT = path.resolve(HERE, "..", "..");
const company = JSON.parse(fs.readFileSync(path.join(ROOT, "company.json"), "utf8"));

function substitute(html, data) {
  return html.replace(/\{\{\s*([\w.\-]+)\s*\}\}/g, (m, key) => {
    const v = key.split(".").reduce((o, k) => (o == null ? undefined : o[k]), data);
    if (v === undefined || v === null) { console.warn(`  ! unresolved token ${m}`); return m; }
    return typeof v === "object" ? JSON.stringify(v) : String(v);
  });
}

const jobs = [
  ["signature.html", "signature.compiled.html"],
  ["signature-generic.html", "signature-generic.compiled.html"],
  ["signature.txt", "signature.compiled.txt"],
];
const LIMIT = 8 * 1024;
for (const [src, out] of jobs) {
  const compiled = substitute(fs.readFileSync(path.join(HERE, src), "utf8"), { company });
  fs.writeFileSync(path.join(HERE, out), compiled);
  const size = Buffer.byteLength(compiled, "utf8");
  console.log(`  ${out}  ${size} bytes${size > LIMIT ? "  !! over 8 KB limit" : ""}`);
}

// Offline review copy: same markup, logo served from the repo instead of the website.
const hosted = `${company.url}/assets/img/logo-email-600.png`;
const preview = fs.readFileSync(path.join(HERE, "signature.compiled.html"), "utf8")
  .split(hosted).join("logo-email-600.png")
  .replace('<body style="margin:0;padding:0;">', '<body style="margin:0;padding:24px;background:#ffffff;">');
fs.writeFileSync(path.join(HERE, "signature.preview.html"), preview);
console.log("  signature.preview.html  (local logo, review only - do not install this file)");
