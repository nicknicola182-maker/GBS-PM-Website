// Loads every page of 07_WEBSITE/public in Chromium (served from disk with clean-URL mapping) and reports:
// missing resources, console errors, horizontal overflow at mobile width, unresolved tokens, broken internal links, nav toggle.
// Also writes full-page screenshots to the folder given as argv[2]. usage: node tools/qa-site.mjs [shot-dir]
import { chromium } from "playwright"; import fs from "node:fs"; import path from "node:path";
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), ".."); const PUB = path.join(ROOT, "07_WEBSITE", "public");
const shotDir = process.argv[2]; if (shotDir) fs.mkdirSync(shotDir, { recursive: true });
const MIME = { html: "text/html", css: "text/css", js: "text/javascript", svg: "image/svg+xml", png: "image/png", ico: "image/x-icon", woff2: "font/woff2", xml: "application/xml", txt: "text/plain", webmanifest: "application/manifest+json" };
const resolve = (p) => { p = decodeURIComponent(p.split("?")[0]); if (p === "/") return "index.html"; let f = p.replace(/^\//, ""); if (!path.extname(f)) f += ".html"; return f; };
const pages = fs.readdirSync(PUB).filter(f => f.endsWith(".html")).map(f => "/" + f.replace(/\.html$/, "")).map(p => p === "/index" ? "/" : p);
const browser = await chromium.launch(); let problems = 0;
for (const vp of [{ w: 1920, h: 1080, name: "xl" }, { w: 1440, h: 900, name: "desktop" }, { w: 1024, h: 768, name: "laptop" }, { w: 768, h: 1024, name: "tablet" }, { w: 390, h: 844, name: "mobile" }, { w: 320, h: 640, name: "narrow" }]) {
  const ctx = await browser.newContext({ viewport: { width: vp.w, height: vp.h }, deviceScaleFactor: 1 });
  await ctx.route("**/*", async route => {
    const u = new URL(route.request().url()); if (u.hostname !== "gbs-pm.local") return route.continue();
    const f = path.join(PUB, resolve(u.pathname)); if (!fs.existsSync(f)) return route.fulfill({ status: 404, body: "not found" });
    route.fulfill({ status: 200, body: fs.readFileSync(f), contentType: MIME[path.extname(f).slice(1)] || "application/octet-stream" });
  });
  for (const p of pages) {
    const page = await ctx.newPage(); const missing = [], errors = [];
    page.on("response", r => { if (r.status() >= 400) missing.push(r.url().replace("http://gbs-pm.local", "")); });
    page.on("console", m => { if (m.type() === "error") errors.push(m.text()); }); page.on("pageerror", e => errors.push(e.message));
    await page.goto("http://gbs-pm.local" + p, { waitUntil: "networkidle" }); await page.evaluate(() => document.fonts.ready);
    const info = await page.evaluate(() => {
      const links = [...document.querySelectorAll("a[href]")].map(a => a.getAttribute("href")).filter(h => h.startsWith("/"));
      const anchors = [...document.querySelectorAll("a[href^='#'], a[href*='#']")].map(a => a.getAttribute("href"));
      return { title: document.title, overflow: document.documentElement.scrollWidth - window.innerWidth, tokens: (document.documentElement.outerHTML.match(/\{\{[^}]*\}\}/g) || []).slice(0, 5),
        links: [...new Set(links)], anchors, h1: document.querySelectorAll("h1").length, fonts: [...document.fonts].filter(f => f.status === "loaded").map(f => f.family + " " + f.weight) };
    });
    // internal link targets
    const broken = info.links.filter(h => { const [pth, hash] = h.split("#"); if (pth && !fs.existsSync(path.join(PUB, resolve(pth)))) return true; return false; });
    const badAnchors = [];
    for (const h of info.anchors) { const [pth, hash] = h.split("#"); if (!hash) continue; const f = path.join(PUB, resolve(pth || p)); if (fs.existsSync(f) && !fs.readFileSync(f, "utf8").includes(`id="${hash}"`)) badAnchors.push(h); }
    let navOk = "n/a";
    if (vp.w <= 860) { await page.click(".nav-toggle"); navOk = await page.evaluate(() => document.getElementById("site-nav").classList.contains("open") && document.querySelector(".nav-toggle").getAttribute("aria-expanded") === "true"); await page.click(".nav-toggle"); }
    const flag = missing.length || errors.length || info.overflow > 0 || info.tokens.length || broken.length || badAnchors.length || info.h1 !== 1 || navOk === false;
    if (flag) problems++;
    console.log(`${flag ? "FAIL" : "ok  "} ${vp.name.padEnd(7)} ${p.padEnd(12)} h1=${info.h1} overflow=${info.overflow}px fonts=${info.fonts.length} nav=${navOk}` +
      (missing.length ? `\n      missing: ${missing.join(", ")}` : "") + (errors.length ? `\n      errors: ${errors.join(" | ")}` : "") +
      (info.tokens.length ? `\n      tokens: ${info.tokens.join(" ")}` : "") + (broken.length ? `\n      broken links: ${broken.join(", ")}` : "") + (badAnchors.length ? `\n      bad anchors: ${badAnchors.join(", ")}` : ""));
    if (shotDir) await page.screenshot({ path: path.join(shotDir, `${vp.name}-${p === "/" ? "home" : p.slice(1)}.png`), fullPage: true });
    await page.close();
  }
  await ctx.close();
}
await browser.close(); console.log(problems ? `${problems} page/viewport combinations need attention` : "ALL PAGES OK");
