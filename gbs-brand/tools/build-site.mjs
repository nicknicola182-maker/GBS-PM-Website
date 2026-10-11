// Assembles the static website: 07_WEBSITE/src/pages/*.html (content + META comment) wrapped in src/layout.html,
// with {{company.*}} and {{page.*}} tokens resolved from company.json. Output: 07_WEBSITE/public (deploy this folder).
import fs from "node:fs"; import path from "node:path";
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const SITE = path.join(ROOT, "07_WEBSITE"), SRC = path.join(SITE, "src"), PUB = path.join(SITE, "public");
const company = JSON.parse(fs.readFileSync(path.join(ROOT, "company.json"), "utf8"));
const today = new Date().toISOString().slice(0, 10);
company.formAction = company.formEndpoint || `mailto:${company.email}`;
company.formEnctype = company.formEndpoint ? "multipart/form-data" : "text/plain";
company.servicesJsonLd = company.services.map(s => JSON.stringify(s)).join(", ");
company.serviceOptions = company.services.map(s => `<option>${s}</option>`).join("\n                ");

const sub = (html, data) => html.replace(/\{\{\s*([\w.\-]+)\s*\}\}/g, (m, key) => {
  const v = key.split(".").reduce((o, k) => (o == null ? undefined : o[k]), data);
  if (v === undefined || v === null) { console.warn(`  ! unresolved token ${m}`); return ""; }
  return typeof v === "object" ? JSON.stringify(v) : String(v);
});

// static assets
fs.rmSync(PUB, { recursive: true, force: true });
fs.mkdirSync(path.join(PUB, "assets", "fonts"), { recursive: true });
fs.cpSync(path.join(SRC, "assets"), path.join(PUB, "assets"), { recursive: true });
for (const f of fs.readdirSync(path.join(ROOT, "00_BRAND_CORE", "fonts")).filter(f => f.endsWith(".woff2")))
  fs.copyFileSync(path.join(ROOT, "00_BRAND_CORE", "fonts", f), path.join(PUB, "assets", "fonts", f));
const logos = { "logo-primary.svg": "GBS_HORIZON_LOGO_PRIMARY_SAGE-RED_v1.0.svg", "logo-primary-nostrap.svg": "GBS_HORIZON_LOGO_PRIMARY-NOSTRAP_SAGE-RED_v1.0.svg",
  "logo-reversed.svg": "GBS_HORIZON_LOGO_REVERSED_OFFWHITE-RED_v1.0.svg", "logo-reversed-soft.svg": "GBS_HORIZON_LOGO_REVERSED-SOFT_OFFWHITE_v1.0.svg",
  "logo-strip.svg": "GBS_HORIZON_LOGO_STRIP_SAGE-RED_v1.0.svg", "icon.svg": "GBS_HORIZON_ICON_SAGE-RED_v1.0.svg", "icon-reversed.svg": "GBS_HORIZON_ICON_OFFWHITE-RED_v1.0.svg" };
for (const [dst, src] of Object.entries(logos)) fs.copyFileSync(path.join(ROOT, "01_LOGO_MASTER", "svg", src), path.join(PUB, "assets", "img", dst));
fs.copyFileSync(path.join(ROOT, "01_LOGO_MASTER", "png", "GBS_HORIZON_LOGO_PRIMARY-NOSTRAP_SAGE-RED_600px_v1.0.png"), path.join(PUB, "assets", "img", "logo-email-600.png"));
for (const f of ["favicon.ico", "favicon.svg", "apple-touch-icon.png", "icon-192.png", "icon-512.png"])
  fs.copyFileSync(path.join(ROOT, "01_LOGO_MASTER", "favicon", f), path.join(PUB, f));
const og = path.join(ROOT, "09_DIGITAL", "social", "GBS_HORIZON_SOCIAL_OG-IMAGE_1200x630_v1.0.png");
if (fs.existsSync(og)) fs.copyFileSync(og, path.join(PUB, "assets", "img", "og-image.png"));
for (const f of fs.readdirSync(path.join(SRC, "static"))) fs.cpSync(path.join(SRC, "static", f), path.join(PUB, f), { recursive: true });

// pages
const layout = fs.readFileSync(path.join(SRC, "layout.html"), "utf8");
const urls = [];
for (const f of fs.readdirSync(path.join(SRC, "pages")).filter(f => f.endsWith(".html")).sort()) {
  const raw = fs.readFileSync(path.join(SRC, "pages", f), "utf8");
  const m = raw.match(/<!--META\s*([\s\S]*?)-->/); if (!m) throw new Error(`no META in ${f}`);
  const page = { slug: f.replace(/\.html$/, ""), nav: "", bodyClass: "", noindex: false, ...JSON.parse(m[1]) };
  page.content = raw.replace(m[0], "").trim();
  page.fullTitle = page.fullTitle || `${page.title} | ${company.tradingName}`;
  page.canonical = page.slug === "index" ? `${company.url}/` : `${company.url}/${page.slug}`;
  page.robots = page.noindex ? "noindex, nofollow" : "index, follow";
  page.navClass = {}; for (const k of ["home", "services", "about", "contact"]) page.navClass[k] = page.nav === k ? ' aria-current="page"' : "";
  let html = sub(layout.replace("{{page.content}}", () => page.content), { company, page, today });
  fs.writeFileSync(path.join(PUB, `${page.slug}.html`), html);
  if (!page.noindex) urls.push(page.canonical);
  console.log(`  page ${page.slug}.html`);
}
fs.writeFileSync(path.join(PUB, "sitemap.xml"), `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls.map(u => `  <url><loc>${u}</loc><lastmod>${today}</lastmod></url>`).join("\n")}\n</urlset>\n`);
fs.writeFileSync(path.join(PUB, "robots.txt"), `User-agent: *\nAllow: /\nSitemap: ${company.url}/sitemap.xml\n`);
fs.writeFileSync(path.join(PUB, "site.webmanifest"), JSON.stringify({ name: company.tradingName, short_name: company.shortName, start_url: "/", display: "browser", background_color: "#F9F9F7", theme_color: "#6E7F72",
  icons: [{ src: "/icon-192.png", sizes: "192x192", type: "image/png" }, { src: "/icon-512.png", sizes: "512x512", type: "image/png" }] }, null, 2));
console.log(`site built: ${urls.length} indexable pages -> 07_WEBSITE/public`);
