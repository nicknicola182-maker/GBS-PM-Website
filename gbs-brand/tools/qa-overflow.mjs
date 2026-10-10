// Detects content overflowing its .page (text clipped at trim or beyond safe area) in a rendered HTML source.
// usage: node tools/qa-overflow.mjs <html> [safe-mm]
import { chromium } from "playwright"; import fs from "node:fs"; import path from "node:path"; import { pathToFileURL } from "node:url";
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const company = JSON.parse(fs.readFileSync(path.join(ROOT, "company.json"), "utf8"));
const src = path.resolve(process.argv[2]); const safe = Number(process.argv[3] || 0);
const html = fs.readFileSync(src, "utf8").replace(/\{\{\s*([\w.\-]+)\s*\}\}/g, (m, k) => { const v = k.split(".").reduce((o, x) => o?.[x], { company }); return v == null ? m : String(v); });
const tmp = src.replace(/\.html$/, ".__qa.html"); fs.writeFileSync(tmp, html);
const b = await chromium.launch(); const p = await b.newPage();
await p.goto(pathToFileURL(tmp).href, { waitUntil: "networkidle" }); await p.evaluate(() => document.fonts.ready);
const issues = await p.evaluate((safeMM) => {
  const mm = 96 / 25.4, out = [];
  document.querySelectorAll(".page").forEach((pg, i) => {
    const pr = pg.getBoundingClientRect();
    pg.querySelectorAll("*").forEach(el => {
      if (el.closest("[class*='bleed']") || el.matches("[class*='bleed']")) return;
      const r = el.getBoundingClientRect(); if (!r.width || !r.height) return;
      const txt = (el.childNodes.length && [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) ? el.textContent.trim().slice(0, 40) : "";
      const over = r.right > pr.right + 0.5 || r.bottom > pr.bottom + 0.5 || r.left < pr.left - 0.5 || r.top < pr.top - 0.5;
      const unsafe = safeMM && txt && (r.right > pr.right - safeMM * mm || r.bottom > pr.bottom - safeMM * mm || r.left < pr.left + safeMM * mm || r.top < pr.top + safeMM * mm);
      const clipped = txt && el.scrollHeight > el.clientHeight + 2 && getComputedStyle(el).overflow !== "visible";
      if (over || unsafe || clipped) out.push(`page ${i + 1}: <${el.tagName.toLowerCase()}${el.className ? "." + String(el.className).split(" ")[0] : ""}> ${over ? "OUTSIDE TRIM" : unsafe ? "inside safe margin" : "TEXT CLIPPED"} "${txt}"`);
    });
  });
  return out.slice(0, 40);
}, safe);
fs.unlinkSync(tmp); await b.close();
console.log(issues.length ? issues.join("\n") : "OK: no overflow detected in " + path.basename(src));
