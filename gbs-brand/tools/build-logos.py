#!/usr/bin/env python3
"""GBS HORIZON logo master generator.
Builds clean outlined SVG masters (no live fonts) for every mandatory variant in manual section 03,
using the real Montserrat glyph outlines. Run: python3 tools/build-logos.py
Outputs: 01_LOGO_MASTER/svg/*.svg
"""
import json, os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "00_BRAND_CORE", "fonts")
OUT = os.path.join(ROOT, "01_LOGO_MASTER", "svg")
os.makedirs(OUT, exist_ok=True)

SAGE, RED, LIGHT, OFFWHITE, WHITE, BLACK = "#6E7F72", "#E10600", "#DADADA", "#F9F9F7", "#FFFFFF", "#000000"

# ---- geometry (unit: X = GBS cap height = 100) ---------------------------------------------
X = 100.0
TRACK_GBS = 0.08          # em
RULE_T = 3.5              # rule thickness
RULE_GAP = 25.0           # letters baseline -> rule top
ICON_GAP = 24.0           # S right edge -> icon left
BAR_GAP = 10.0
BARS = [  # (width, height above rule top, style)
    (6.0, 42.0, "solid"),
    (20.0, 95.0, "hollow"),
    (20.0, 125.0, "red"),
    (20.0, 62.0, "solid"),
]
HOLLOW_STROKE = 5.0
DESC_WIDTH_RATIO = 0.96   # descriptor width vs lockup width
DESC_TRACK = 0.12
DESC_GAP = 28.0           # rule bottom -> descriptor cap top
STRAP_TRACK = 0.15
STRAP_CAP_RATIO = 0.60    # strapline cap height / descriptor cap height
STRAP_GAP = 26.0          # descriptor baseline -> strapline cap top
STRAP_RULE_T = 2.0
STRAP_RULE_PAD = 14.0

fonts = {}
def font(weight):
    if weight not in fonts:
        fonts[weight] = TTFont(os.path.join(FONTS, f"Montserrat-{weight}.ttf"))
    return fonts[weight]

def text_paths(text, weight, size, x, y, tracking_em=0.0):
    """Return list of (char, path_d, advance_x) with glyphs placed at baseline y, starting x. size = px per em."""
    f = font(weight); cmap = f.getBestCmap(); gs = f.getGlyphSet(); hmtx = f["hmtx"]
    out = []; cx = x; scale = size / f["head"].unitsPerEm
    for i, ch in enumerate(text):
        if ch == " ":
            cx += hmtx[cmap[ord(" ")]][0] * scale + tracking_em * size
            continue
        gname = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        tpen = TransformPen(pen, (scale, 0, 0, -scale, cx, y))
        gs[gname].draw(tpen)
        d = pen.getCommands()
        adv = hmtx[gname][0] * scale
        out.append((ch, d, cx, adv))
        cx += adv + tracking_em * size
    width = cx - x - tracking_em * size
    return out, width

def glyph_bounds(text, weight, size, tracking_em=0.0):
    """Ink bounds (xmin, xmax) relative to start x for a text run."""
    from fontTools.pens.boundsPen import BoundsPen
    f = font(weight); cmap = f.getBestCmap(); gs = f.getGlyphSet(); hmtx = f["hmtx"]
    scale = size / f["head"].unitsPerEm; cx = 0; xmin = None; xmax = None
    for ch in text:
        gname = cmap[ord(ch)]
        if ch != " ":
            bp = BoundsPen(gs); gs[gname].draw(bp)
            if bp.bounds:
                gx0, _, gx1, _ = bp.bounds
                a, b = cx + gx0 * scale, cx + gx1 * scale
                xmin = a if xmin is None else min(xmin, a); xmax = b if xmax is None else max(xmax, b)
        cx += hmtx[gname][0] * scale + tracking_em * size
    return xmin, xmax

def fmt(v): return f"{v:.2f}".rstrip("0").rstrip(".")

def build(variant):
    """variant dict: name, colours, include_descriptor, include_strapline, layout ('stacked'|'strip'|'icon'|'wordmark')"""
    c = variant["colours"]
    els = []  # svg elements as strings
    size_gbs = X / 0.70  # cap height 700/1000
    yb = X                # baseline of GBS at y=100 (cap top at 0)
    gbs_bounds = glyph_bounds("GBS", 600, size_gbs, TRACK_GBS)
    x0 = -gbs_bounds[0]   # shift so ink starts at x=0
    layout = variant["layout"]
    rule_top = yb + RULE_GAP
    rule_bot = rule_top + RULE_T

    parts = []
    if layout in ("stacked", "strip", "wordmark"):
        glyphs, adv_w = text_paths("GBS", 600, size_gbs, x0, yb, TRACK_GBS)
        for ch, d, gx, adv in glyphs:
            parts.append(f'<path fill="{c["word"]}" d="{d}"/>')
        ink_right = x0 + gbs_bounds[1]
        icon_x = ink_right + ICON_GAP
    else:
        icon_x = 0.0

    # icon bars
    bx = icon_x
    icon_w = sum(b[0] for b in BARS) + BAR_GAP * (len(BARS) - 1)
    bars_svg = []
    for w, h, style in BARS:
        if variant.get("simplified") and style == "hollow":
            style = "solid"
        top = rule_top - h
        col = c["red"] if style == "red" else c["bars"]
        if style == "hollow":
            s = HOLLOW_STROKE
            bars_svg.append(f'<path fill="{col}" fill-rule="evenodd" d="M{fmt(bx)} {fmt(top)}h{fmt(w)}v{fmt(h)}h-{fmt(w)}z M{fmt(bx+s)} {fmt(top+s)}v{fmt(h-s)}h{fmt(w-2*s)}v-{fmt(h-s)}z"/>')
        else:
            bars_svg.append(f'<rect fill="{col}" x="{fmt(bx)}" y="{fmt(top)}" width="{fmt(w)}" height="{fmt(h)}"/>')
        bx += w + BAR_GAP
    icon_right = icon_x + icon_w

    if layout == "icon":
        pad = 30.0
        rule_x0, rule_x1 = -pad, icon_right + pad
    else:
        rule_x0, rule_x1 = 0.0, icon_right
    parts.extend(bars_svg)
    parts.append(f'<rect fill="{c["rule"]}" x="{fmt(rule_x0)}" y="{fmt(rule_top)}" width="{fmt(rule_x1-rule_x0)}" height="{fmt(RULE_T)}"/>')

    lock_w = rule_x1 - rule_x0
    top_y = rule_top - 125.0  # red bar top == cap top == 0
    bottom_y = rule_bot
    left_x, right_x = rule_x0, rule_x1

    if layout == "stacked" and variant.get("descriptor", True):
        # descriptor
        dsize1 = 1.0
        _, nat_w = text_paths("PROPERTY MAINTENANCE", 700, dsize1, 0, 0, DESC_TRACK)
        b0, b1 = glyph_bounds("PROPERTY MAINTENANCE", 700, dsize1, DESC_TRACK)
        ink_w1 = b1 - b0
        dsize = lock_w * DESC_WIDTH_RATIO / ink_w1
        dcap = 0.70 * dsize
        dy = rule_bot + DESC_GAP + dcap  # baseline
        dx = rule_x0 + (lock_w - ink_w1 * dsize) / 2 - b0 * dsize
        glyphs, _ = text_paths("PROPERTY MAINTENANCE", 700, dsize, dx, dy, DESC_TRACK)
        for ch, d, gx, adv in glyphs:
            parts.append(f'<path fill="{c["desc"]}" d="{d}"/>')
        bottom_y = dy
        if variant.get("strapline", True):
            ssize = dsize * STRAP_CAP_RATIO
            scap = 0.70 * ssize
            sy = dy + STRAP_GAP + scap
            t = "BUILD | MAINTAIN | IMPROVE"
            sb0, sb1 = glyph_bounds(t, 500, ssize, STRAP_TRACK)
            sw = sb1 - sb0
            sx = rule_x0 + (lock_w - sw) / 2 - sb0
            glyphs, _ = text_paths(t, 500, ssize, sx, sy, STRAP_TRACK)
            for ch, d, gx, adv in glyphs:
                col = c["pipe"] if ch == "|" else c["strap"]
                parts.append(f'<path fill="{col}" d="{d}"/>')
            ry = sy - scap / 2 - STRAP_RULE_T / 2
            lx0, lx1 = rule_x0, sx + sb0 - STRAP_RULE_PAD
            rx0, rx1 = sx + sb1 + STRAP_RULE_PAD, rule_x1
            parts.append(f'<rect fill="{c["straprule"]}" x="{fmt(lx0)}" y="{fmt(ry)}" width="{fmt(lx1-lx0)}" height="{fmt(STRAP_RULE_T)}"/>')
            parts.append(f'<rect fill="{c["straprule"]}" x="{fmt(rx0)}" y="{fmt(ry)}" width="{fmt(rx1-rx0)}" height="{fmt(STRAP_RULE_T)}"/>')
            bottom_y = sy

    if layout == "strip":
        # single-line: lockup | PROPERTY MAINTENANCE
        div_x = icon_right + 40.0
        div_h = 100.0
        parts.append(f'<rect fill="{c["rule"]}" x="{fmt(div_x)}" y="{fmt(yb-div_h)}" width="{fmt(RULE_T)}" height="{fmt(div_h + RULE_GAP + RULE_T)}"/>')
        dsize = 0.42 * X / 0.70
        dcap = 0.42 * X
        t = "PROPERTY MAINTENANCE"
        b0, b1 = glyph_bounds(t, 700, dsize, DESC_TRACK)
        tx = div_x + RULE_T + 36.0 - b0
        # vertically centre descriptor on the cap-height band of GBS
        ty = yb - (X - dcap) / 2
        glyphs, _ = text_paths(t, 700, dsize, tx, ty, DESC_TRACK)
        for ch, d, gx, adv in glyphs:
            parts.append(f'<path fill="{c["desc"]}" d="{d}"/>')
        right_x = tx + b1

    pad = 2.0
    vb_x, vb_y = left_x - pad, top_y - pad
    vb_w, vb_h = (right_x - left_x) + 2 * pad, (bottom_y - top_y) + 2 * pad
    bg = ""
    if variant.get("background"):
        if layout == "icon" and variant.get("square"):
            side = max(vb_w, vb_h) * 1.6
            vb_x, vb_y = left_x + (right_x - left_x) / 2 - side / 2, top_y + (bottom_y - top_y) / 2 - side / 2 + 6
            vb_w = vb_h = side
        bg = f'<rect fill="{variant["background"]}" x="{fmt(vb_x)}" y="{fmt(vb_y)}" width="{fmt(vb_w)}" height="{fmt(vb_h)}"/>'
    title = variant["title"]
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{fmt(vb_x)} {fmt(vb_y)} {fmt(vb_w)} {fmt(vb_h)}" '
           f'width="{fmt(vb_w)}" height="{fmt(vb_h)}" role="img" aria-label="{title}">\n<title>{title}</title>\n'
           f'<!-- GBS HORIZON {variant["name"]} v1.0 | outlined vector, no live fonts | unit X (GBS cap height) = 100 | clear space = 1X all sides -->\n'
           f'{bg}\n' + "\n".join(parts) + "\n</svg>\n")
    path = os.path.join(OUT, f'GBS_HORIZON_{variant["name"]}_v1.0.svg')
    with open(path, "w") as fh: fh.write(svg)
    return {"file": os.path.basename(path), "w": round(vb_w, 2), "h": round(vb_h, 2)}

def colours(word, bars, red, rule, desc, strap, pipe, straprule):
    return dict(word=word, bars=bars, red=red, rule=rule, desc=desc, strap=strap, pipe=pipe, straprule=straprule)

PRIMARY = colours(SAGE, SAGE, RED, SAGE, RED, SAGE, RED, SAGE)
REVERSED = colours(OFFWHITE, OFFWHITE, RED, OFFWHITE, RED, OFFWHITE, RED, OFFWHITE)
REVERSED_SOFT = colours(OFFWHITE, OFFWHITE, RED, OFFWHITE, OFFWHITE, OFFWHITE, RED, OFFWHITE)  # small-size legibility option
def mono(col): return colours(col, col, col, col, col, col, col, col)

VARIANTS = [
    dict(name="LOGO_PRIMARY_SAGE-RED", title="GBS Property Maintenance", layout="stacked", colours=PRIMARY),
    dict(name="LOGO_PRIMARY-NOSTRAP_SAGE-RED", title="GBS Property Maintenance", layout="stacked", colours=PRIMARY, strapline=False),
    dict(name="LOGO_WORDMARK_SAGE-RED", title="GBS", layout="wordmark", colours=PRIMARY),
    dict(name="LOGO_STRIP_SAGE-RED", title="GBS Property Maintenance", layout="strip", colours=PRIMARY),
    dict(name="LOGO_REVERSED_OFFWHITE-RED", title="GBS Property Maintenance", layout="stacked", colours=REVERSED),
    dict(name="LOGO_REVERSED-NOSTRAP_OFFWHITE-RED", title="GBS Property Maintenance", layout="stacked", colours=REVERSED, strapline=False),
    dict(name="LOGO_REVERSED-SOFT_OFFWHITE", title="GBS Property Maintenance", layout="stacked", colours=REVERSED_SOFT, strapline=False),
    dict(name="LOGO_REVERSED_ON-SAGE-PANEL", title="GBS Property Maintenance", layout="stacked", colours=REVERSED, background=SAGE),
    dict(name="LOGO_WORDMARK_OFFWHITE-RED", title="GBS", layout="wordmark", colours=REVERSED),
    dict(name="LOGO_STRIP_OFFWHITE-RED", title="GBS Property Maintenance", layout="strip", colours=REVERSED),
    dict(name="LOGO_MONO_SAGE", title="GBS Property Maintenance", layout="stacked", colours=mono(SAGE)),
    dict(name="LOGO_MONO-NOSTRAP_SAGE", title="GBS Property Maintenance", layout="stacked", colours=mono(SAGE), strapline=False),
    dict(name="LOGO_MONO_WHITE", title="GBS Property Maintenance", layout="stacked", colours=mono(WHITE)),
    dict(name="LOGO_MONO-NOSTRAP_WHITE", title="GBS Property Maintenance", layout="stacked", colours=mono(WHITE), strapline=False),
    dict(name="LOGO_MONO_BLACK", title="GBS Property Maintenance", layout="stacked", colours=mono(BLACK)),
    dict(name="LOGO_MONO-NOSTRAP_BLACK", title="GBS Property Maintenance", layout="stacked", colours=mono(BLACK), strapline=False),
    dict(name="ICON_SAGE-RED", title="GBS Horizon icon", layout="icon", colours=PRIMARY),
    dict(name="ICON_OFFWHITE-RED", title="GBS Horizon icon", layout="icon", colours=REVERSED),
    dict(name="ICON_MONO_SAGE", title="GBS Horizon icon", layout="icon", colours=mono(SAGE)),
    dict(name="ICON_MONO_WHITE", title="GBS Horizon icon", layout="icon", colours=mono(WHITE)),
    dict(name="ICON_MONO_BLACK", title="GBS Horizon icon", layout="icon", colours=mono(BLACK)),
    dict(name="ICON_SIMPLIFIED_SAGE-RED", title="GBS Horizon icon (simplified, embroidery)", layout="icon", colours=PRIMARY, simplified=True),
    dict(name="ICON_SIMPLIFIED_OFFWHITE-RED", title="GBS Horizon icon (simplified, embroidery)", layout="icon", colours=REVERSED, simplified=True),
    dict(name="AVATAR_SQUARE_ON-SAGE", title="GBS Horizon avatar", layout="icon", colours=REVERSED, background=SAGE, square=True),
    dict(name="AVATAR_SQUARE_ON-OFFWHITE", title="GBS Horizon avatar", layout="icon", colours=PRIMARY, background=OFFWHITE, square=True),
]

if __name__ == "__main__":
    manifest = [build(v) for v in VARIANTS]
    with open(os.path.join(OUT, "_manifest.json"), "w") as fh: json.dump(manifest, fh, indent=1)
    for m in manifest: print(f'{m["file"]:55s} {m["w"]:8.2f} x {m["h"]:8.2f}')
