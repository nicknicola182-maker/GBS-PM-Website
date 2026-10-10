#!/usr/bin/env python3
"""Generate full-scale (mm) vector livery panels for 05_VEHICLES from the logo masters and company.json.
Text panels are outlined from Inter SemiBold with fontTools so no live fonts remain."""
import json, os, re, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVG = os.path.join(ROOT, "01_LOGO_MASTER", "svg")
OUT = os.path.join(ROOT, "05_VEHICLES")
company = json.load(open(os.path.join(ROOT, "company.json")))
SAGE, RED = "#6E7F72", "#E10600"

def fmt(v): return f"{v:.3f}".rstrip("0").rstrip(".")

def logo_panel(src, out, width_mm, title, note):
    s = open(os.path.join(SVG, src)).read()
    m = re.search(r'viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"', s)
    vx, vy, vw, vh = map(float, m.groups())
    k = width_mm / vw; h = vh * k
    body = s[s.index(">", s.index("<svg")) + 1 : s.rindex("</svg>")]
    body = re.sub(r"<title>.*?</title>\s*", "", body, flags=re.S)
    body = re.sub(r"<!--.*?-->\s*", "", body, flags=re.S)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{fmt(width_mm)}mm" height="{fmt(h)}mm" viewBox="0 0 {fmt(width_mm)} {fmt(h)}" role="img" aria-label="{title}">\n'
           f'<title>{title}</title>\n'
           f'<!-- GBS HORIZON vehicle livery panel v1.0 | user unit = 1 mm at full vehicle scale | source: {src} | {note} -->\n'
           f'<g id="artwork" transform="scale({fmt(k)}) translate({fmt(-vx)} {fmt(-vy)})">\n{body.strip()}\n</g>\n</svg>\n')
    open(os.path.join(OUT, out), "w").write(svg)
    print(out, f"{width_mm} x {h:.2f} mm")

def text_paths(text, size_mm, x, baseline, font="Inter-600.ttf", tracking_em=0.0):
    f = TTFont(os.path.join(ROOT, "00_BRAND_CORE", "fonts", font)); cmap = f.getBestCmap(); gs = f.getGlyphSet(); hm = f["hmtx"]
    sc = size_mm / f["head"].unitsPerEm; cx = x; parts = []; xmin = xmax = None
    for ch in text:
        g = cmap[ord(ch)]
        if ch != " ":
            pen = SVGPathPen(gs); gs[g].draw(TransformPen(pen, (sc, 0, 0, -sc, cx, baseline)))
            bp = BoundsPen(gs); gs[g].draw(bp)
            if bp.bounds:
                a, b = cx + bp.bounds[0] * sc, cx + bp.bounds[2] * sc
                xmin = a if xmin is None else min(xmin, a); xmax = b if xmax is None else max(xmax, b)
            parts.append(pen.getCommands())
        cx += hm[g][0] * sc + tracking_em * size_mm
    return parts, xmin, xmax

CAP = 1490 / 2048  # Inter cap height / em
def text_block(text, cap_mm, x, baseline, align="left", colour=SAGE):
    size = cap_mm / CAP
    parts, xmin, xmax = text_paths(text, size, 0, 0)
    w = xmax - xmin
    dx = x - xmin if align == "left" else (x - xmax if align == "right" else x - xmin - w / 2)
    d = " ".join(parts)
    return f'<path fill="{colour}" transform="translate({fmt(dx)} {fmt(baseline)})" d="{d}"/>', w

# 1. Side lockup 1400 mm, 2. rear lockup 700 mm, 3. bonnet icon 250 mm
logo_panel("GBS_HORIZON_LOGO_PRIMARY_SAGE-RED_v1.0.svg", "GBS_HORIZON_VAN_SIDE-LOCKUP_1400MM_SAGE-RED_v1.0.svg", 1400, "GBS Property Maintenance van side lockup, 1400 mm", "side body panel, primary lockup with strapline")
logo_panel("GBS_HORIZON_LOGO_PRIMARY_SAGE-RED_v1.0.svg", "GBS_HORIZON_VAN_REAR-LOCKUP_700MM_SAGE-RED_v1.0.svg", 700, "GBS Property Maintenance van rear lockup, 700 mm", "rear doors, primary lockup with strapline, split across the door gap")
logo_panel("GBS_HORIZON_ICON_SAGE-RED_v1.0.svg", "GBS_HORIZON_VAN_BONNET-ICON_250MM_SAGE-RED_v1.0.svg", 250, "GBS Horizon icon, bonnet emblem 250 mm", "bonnet emblem")

# 4. Side contact row 1400 mm: domain left, phone right, cap height 60 mm
cap = 60; W = 1300
dom, wd = text_block(company["domain"], cap, 0, cap, "left")
ph, wp = text_block(company["phone"], cap, W, cap, "right")
H = cap + 0.25 * cap  # descender allowance
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{fmt(H)}mm" viewBox="0 0 {W} {fmt(H)}" role="img" aria-label="Van side contact row">\n'
       f'<title>Van side contact row (web address left, phone right), cap height {cap} mm</title>\n'
       f'<!-- GBS HORIZON vehicle livery panel v1.0 | user unit = 1 mm | text outlined from company.json (domain, phone) in Inter SemiBold; regenerate when company.json changes -->\n'
       f'<g id="domain">{dom}</g>\n<g id="phone">{ph}</g>\n</svg>\n')
open(os.path.join(OUT, "GBS_HORIZON_VAN_SIDE-CONTACT_1300MM_SAGE_v1.0.svg"), "w").write(svg)
print("side contact: domain ink", round(wd), "mm, phone ink", round(wp), "mm, gap", round(W - wd - wp), "mm, height", H)

# 5. Rear contact block 700 mm: phone (cap 55) over domain (cap 42), centred
W = 700; c1, c2, gap = 55, 42, 28
ph, wp = text_block(company["phone"], c1, W / 2, c1, "centre")
dom, wd = text_block(company["domain"], c2, W / 2, c1 + gap + c2, "centre")
H = c1 + gap + c2 + 0.25 * c2
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{fmt(H)}mm" viewBox="0 0 {W} {fmt(H)}" role="img" aria-label="Van rear contact block">\n'
       f'<title>Van rear contact block (phone over web address), cap heights {c1} / {c2} mm</title>\n'
       f'<!-- GBS HORIZON vehicle livery panel v1.0 | user unit = 1 mm | text outlined from company.json (phone, domain) in Inter SemiBold; regenerate when company.json changes -->\n'
       f'<g id="phone">{ph}</g>\n<g id="domain">{dom}</g>\n</svg>\n')
open(os.path.join(OUT, "GBS_HORIZON_VAN_REAR-CONTACT_700MM_SAGE_v1.0.svg"), "w").write(svg)
print("rear contact: phone ink", round(wp), "domain ink", round(wd), "height", H)

# 6. Rear-quarter decorative bars (derived from the icon bar geometry, no rule): widths 15/40/40, heights 170/310/460, gap 25
bars = [(15, 170, SAGE), (40, 310, RED), (40, 460, SAGE)]; gapb = 25
W = sum(b[0] for b in bars) + gapb * (len(bars) - 1); H = max(b[1] for b in bars)
x = 0; els = []
for w, h, col in bars:
    els.append(f'<rect fill="{col}" x="{x}" y="{H - h}" width="{w}" height="{h}"/>'); x += w + gapb
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}" role="img" aria-label="Rear-quarter decorative bars">\n'
       f'<title>Rear-quarter decorative bars, {W} x {H} mm (bottom edge sits on the sill line)</title>\n'
       f'<!-- GBS HORIZON vehicle livery panel v1.0 | user unit = 1 mm | decorative motif derived from the icon bar proportions; sage and red cut vinyl, no rule -->\n'
       + "\n".join(els) + "\n</svg>\n")
open(os.path.join(OUT, "GBS_HORIZON_VAN_REAR-QUARTER-BARS_460MM_SAGE-RED_v1.0.svg"), "w").write(svg)
print("bars", W, H)
