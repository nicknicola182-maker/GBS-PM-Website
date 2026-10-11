// GBS HORIZON email signature compiler.
// Resolves {{company.*}} and {{person.*}} tokens from company.json (same regex as tools/render.mjs) so the
// signatures can be pasted into mail clients without the renderer. Usage (from anywhere):
//   node 09_DIGITAL/email-signature/build-signature.mjs
// Writes, for every entry in company.json people[]:  signature-<first-last>.compiled.html and .txt
//         signature-staff-template.compiled.html / .txt  (placeholders, for staff not yet in company.json)
//         signature-generic.compiled.html                 (shared mailbox, no named person)
//         signature.preview.html                          (first person, logo from this folder, review only)
import fs from "node:fs";
import path from "node:path";

const HERE = path.dirname(new URL(import.meta.url).pathname);
const ROOT = path.resolve(HERE, "..", "..");
const company = JSON.parse(fs.readFileSync(path.join(ROOT, "company.json"), "utf8"));
const LIMIT = 8 * 1024;

function substitute(html, data) {
  return html.replace(/\{\{\s*([\w.\-]+)\s*\}\}/g, (m, key) => {
    const v = key.split(".").reduce((o, k) => (o == null ? undefined : o[k]), data);
    if (v === undefined || v === null) { console.warn(`  ! unresolved token ${m}`); return m; }
    return typeof v === "object" ? JSON.stringify(v) : String(v);
  });
}
const slug = (name) => name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
function write(src, out, data) {
  const compiled = substitute(fs.readFileSync(path.join(HERE, src), "utf8"), data);
  fs.writeFileSync(path.join(HERE, out), compiled);
  const size = Buffer.byteLength(compiled, "utf8");
  console.log(`  ${out}  ${size} bytes${size > LIMIT ? "  !! over 8 KB limit" : ""}`);
}

// Remove compiled files from earlier runs so renamed or removed people do not linger.
for (const f of fs.readdirSync(HERE)) if (/^signature(-.+)?\.compiled\.(html|txt)$/.test(f)) fs.unlinkSync(path.join(HERE, f));

const people = company.people || [];
if (!people.length) console.warn("  ! company.json has no people[]; only the template and generic signatures are built");
for (const person of people) {
  const s = slug(person.name);
  write("signature.html", `signature-${s}.compiled.html`, { company, person });
  write("signature.txt", `signature-${s}.compiled.txt`, { company, person });
}
const template = { name: "FIRST LAST", role: "JOB TITLE", email: "first.last@" + company.domain, mobile: "07xxx xxxxxx", mobileTel: "+447xxxxxxxxx" };
write("signature.html", "signature-staff-template.compiled.html", { company, person: template });
write("signature.txt", "signature-staff-template.compiled.txt", { company, person: template });
write("signature-generic.html", "signature-generic.compiled.html", { company });

// Offline review copy: first person's markup, logo served from this folder instead of the website.
const first = people[0] ? `signature-${slug(people[0].name)}.compiled.html` : "signature-staff-template.compiled.html";
const hosted = `${company.url}/assets/img/logo-email-600.png`;
const preview = fs.readFileSync(path.join(HERE, first), "utf8")
  .split(hosted).join("logo-email-600.png")
  .replace('<body style="margin:0;padding:0;">', '<body style="margin:0;padding:24px;background:#ffffff;">');
fs.writeFileSync(path.join(HERE, "signature.preview.html"), preview);
console.log(`  signature.preview.html  (${first} with the local logo, review only - do not install this file)`);
