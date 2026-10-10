// GBS HORIZON production renderer.
// Renders HTML sources to PDF (screen = trim size, press = trim + bleed + crop marks) and PNG artwork,
// substituting {{company.*}} tokens from company.json. Usage: node tools/render.mjs [manifest.json] [filter]
import { chromium } from "playwright";
import fs from "node:fs"; import path from "node:path"; import { pathToFileURL } from "node:url"; import { spawnSync } from "node:child_process";

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const manifestPath = process.argv[2] ? path.resolve(process.argv[2]) : path.join(ROOT, "tools", "render-manifest.json");
const filter = process.argv[3] || "";
const company = JSON.parse(fs.readFileSync(path.join(ROOT, "company.json"), "utf8"));
const jobs = JSON.parse(fs.readFileSync(manifestPath, "utf8")).filter(j => !filter || (j.src + j.out).includes(filter));

export function substitute(html, data) {
  return html.replace(/\{\{\s*([\w.\-]+)\s*\}\}/g, (m, key) => {
    const v = key.split(".").reduce((o, k) => (o == null ? undefined : o[k]), data);
    if (v === undefined || v === null) { console.warn(`  ! unresolved token ${m}`); return m; }
    return typeof v === "object" ? JSON.stringify(v) : String(v);
  });
}

const CROP = (bleed, marks) => `
(function(){
  const marks = ${marks}, bleed = ${bleed}, len = 4, gap = 1; // mm
  document.querySelectorAll('.page').forEach(pg => {
    const wrap = document.createElement('div'); wrap.className = 'page-wrap';
    pg.parentNode.insertBefore(wrap, pg); wrap.appendChild(pg);
    const corners = [['left','top'],['right','top'],['left','bottom'],['right','bottom']];
    for (const [h, v] of corners) {
      for (const dir of ['h','v']) {
        const m = document.createElement('div');
        m.style.cssText = 'position:absolute;background:#000;print-color-adjust:exact;-webkit-print-color-adjust:exact;';
        const off = (marks + bleed) + 'mm';
        if (dir === 'h') { m.style.width = len + 'mm'; m.style.height = '0.25pt'; m.style[v] = off; m.style[h] = (marks - len - gap) + 'mm'; }
        else { m.style.height = len + 'mm'; m.style.width = '0.25pt'; m.style[h] = off; m.style[v] = (marks - len - gap) + 'mm'; }
        wrap.appendChild(m);
      }
    }
    const slug = document.createElement('div');
    slug.style.cssText = 'position:absolute;left:' + (marks + bleed) + 'mm;right:' + (marks + bleed) + 'mm;bottom:1.2mm;font:5pt Inter,Arial,sans-serif;color:#000;letter-spacing:0.03em;white-space:nowrap;overflow:hidden;';
    slug.textContent = (document.title || '') + ' | trim ' + (pg.dataset.trim || '') + ' | bleed ' + bleed + ' mm | v1.0 | ' + new Date().toISOString().slice(0,10);
    wrap.appendChild(slug);
  });
  document.documentElement.classList.add('press');
})();`;

const browser = await chromium.launch();
const ctx = await browser.newContext({ deviceScaleFactor: 1 });
let n = 0;
for (const job of jobs) {
  const src = path.join(ROOT, job.src);
  const html = substitute(fs.readFileSync(src, "utf8"), { company, job });
  const tmp = src.replace(/\.html$/, ".__render.html");
  fs.writeFileSync(tmp, html);
  const outBase = path.join(ROOT, job.out);
  fs.mkdirSync(path.dirname(outBase), { recursive: true });
  const page = await ctx.newPage();
  try {
    await page.goto(pathToFileURL(tmp).href, { waitUntil: "networkidle" });
    await page.evaluate(() => document.fonts.ready);
    const type = job.type || "pdf";
    if (type === "pdf") {
      const [tw, th] = job.trim; // mm
      const bleed = job.bleed ?? 3, marks = job.marks ?? 6;
      if (job.screen !== false) {
        await page.pdf({ path: `${outBase}_SCREEN.pdf`, width: `${tw}mm`, height: `${th}mm`, printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 }, preferCSSPageSize: false });
        console.log(`  pdf  ${job.out}_SCREEN.pdf (${tw}x${th}mm)`);
      }
      if (job.press !== false) {
        await page.evaluate(CROP(bleed, marks));
        const W = tw + 2 * (bleed + marks), H = th + 2 * (bleed + marks);
        await page.pdf({ path: `${outBase}_PRESS.pdf`, width: `${W}mm`, height: `${H}mm`, printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 }, preferCSSPageSize: false });
        console.log(`  pdf  ${job.out}_PRESS.pdf (${W}x${H}mm incl. ${bleed}mm bleed + marks)`);
      }
    } else if (type === "png") {
      const dpi = job.dpi || 300, scale = dpi / 96;
      const pxW = Math.round((job.widthMM / 25.4) * 96), pxH = Math.round((job.heightMM / 25.4) * 96);
      await page.setViewportSize({ width: pxW, height: pxH });
      const p2 = await (await browser.newContext({ deviceScaleFactor: scale, viewport: { width: pxW, height: pxH } })).newPage();
      await p2.goto(pathToFileURL(tmp).href, { waitUntil: "networkidle" });
      await p2.evaluate(() => document.fonts.ready);
      const el = job.selector ? await p2.$(job.selector) : null;
      const opts = { path: `${outBase}.png`, omitBackground: !!job.transparent };
      if (el) await el.screenshot(opts); else await p2.screenshot({ ...opts, fullPage: false });
      await p2.context().close();
      // write physical resolution metadata so suppliers see the intended print size
      spawnSync("python3", ["-I", "-c", "import sys;from PIL import Image;p=sys.argv[1];d=int(sys.argv[2]);im=Image.open(p);im.save(p,dpi=(d,d))", `${outBase}.png`, String(dpi)]);
      console.log(`  png  ${job.out}.png (${job.widthMM}x${job.heightMM}mm @ ${dpi}dpi)`);
    } else if (type === "screenshot") {
      await page.setViewportSize({ width: job.width || 1440, height: job.height || 900 });
      await page.screenshot({ path: `${outBase}.png`, fullPage: !!job.fullPage });
      console.log(`  shot ${job.out}.png`);
    }
    n++;
  } catch (e) { console.error(`  ERROR ${job.src}: ${e.message}`); }
  finally { await page.close(); fs.unlinkSync(tmp); }
}
await browser.close();
console.log(`rendered ${n}/${jobs.length} jobs`);
