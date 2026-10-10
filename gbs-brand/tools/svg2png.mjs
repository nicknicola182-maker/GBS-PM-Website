// Render SVG files to transparent PNG at given pixel widths using Playwright/Chromium.
// usage: node tools/svg2png.mjs <out-dir> <width[,width...]> <svg...>
import { chromium } from "playwright";
import fs from "node:fs"; import path from "node:path";
const [outDir, widthsArg, ...files] = process.argv.slice(2);
const widths = widthsArg.split(",").map(Number);
fs.mkdirSync(outDir, { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage();
for (const f of files) {
  const svg = fs.readFileSync(f, "utf8");
  const m = svg.match(/viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"/);
  const vw = +m[3], vh = +m[4];
  for (const w of widths) {
    const h = Math.round(w * vh / vw);
    await page.setViewportSize({ width: w, height: h });
    await page.setContent(`<html><body style="margin:0;background:transparent"><img src="data:image/svg+xml;base64,${Buffer.from(svg).toString("base64")}" style="display:block;width:${w}px;height:${h}px"></body></html>`);
    const base = path.basename(f, ".svg").replace(/_v1\.0$/, "");
    const out = path.join(outDir, `${base}_${w}px_v1.0.png`);
    await page.screenshot({ path: out, omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } });
    console.log(out, `${w}x${h}`);
  }
}
await browser.close();
