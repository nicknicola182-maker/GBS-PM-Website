#!/usr/bin/env python3
"""Builds the GBS Horizon logo masters from the supplied artwork.

Source of record: 01_LOGO_MASTER/source/horizon-logo.png and horizon-icon.png (October 2026
handover), traced once into 01_LOGO_MASTER/source/layers.json by tools/trace-logo.py.
This script composes every colourway and lockup from those layers and writes
01_LOGO_MASTER/svg/*.svg plus _manifest.json. It needs only the standard library.

Lockups:
  stacked    letters, bars, horizon line, red descriptor, strapline with separators
  nostrap    the same without the strapline (stationery headers, chest prints)
  wordmark   letters, bars and horizon line only (small spaces)
  strip      wordmark with the descriptor on the same line, for narrow bands
  icon       the bars icon on its own; square avatars add a background
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "01_LOGO_MASTER", "source", "layers.json")
OUT = os.path.join(ROOT, "01_LOGO_MASTER", "svg")
os.makedirs(OUT, exist_ok=True)

SAGE, SAGE_SURFACE, RED, OFFWHITE, WHITE, BLACK = "#6E7F72", "#627365", "#E10600", "#F9F9F7", "#FFFFFF", "#000000"
PAD = 40          # padding around the artwork, in layer units (4 units = 1 source pixel)
UNIT = 0.25       # layer units to CSS px, so the stacked lockup is 970 px wide like the supplied file

PRIMARY = dict(word=SAGE, red=RED)
REVERSED = dict(word=OFFWHITE, red=RED)
REVERSED_SOFT = dict(word=OFFWHITE, red=OFFWHITE)
def mono(c): return dict(word=c, red=c)

LOCKUPS = {
    "stacked": dict(layers=["word", "redbar", "descriptor", "strap", "pipes"]),
    "nostrap": dict(layers=["word", "redbar", "descriptor"]),
    "wordmark": dict(layers=["word", "redbar"]),
    # strip: the wordmark with the descriptor set on the same line to its right, for narrow bands
    # (pens, lanyards, belly bands). Assembled from the supplied artwork without redrawing it.
    "strip": dict(layers=["word", "redbar"], inline_descriptor=True),
}
STRIP_GAP = 150   # units between the short bar and the descriptor in the strip lockup
LAYER_COLOUR = {"word": "word", "strap": "word", "redbar": "red", "descriptor": "red", "pipes": "red"}

VARIANTS = [
    dict(name="LOGO_PRIMARY_SAGE-RED", title="GBS Property Maintenance", lockup="stacked", colours=PRIMARY),
    dict(name="LOGO_PRIMARY-NOSTRAP_SAGE-RED", title="GBS Property Maintenance", lockup="nostrap", colours=PRIMARY),
    dict(name="LOGO_WORDMARK_SAGE-RED", title="GBS", lockup="wordmark", colours=PRIMARY),
    dict(name="LOGO_STRIP_SAGE-RED", title="GBS Property Maintenance", lockup="strip", colours=PRIMARY),
    dict(name="LOGO_REVERSED_OFFWHITE-RED", title="GBS Property Maintenance", lockup="stacked", colours=REVERSED),
    dict(name="LOGO_REVERSED-NOSTRAP_OFFWHITE-RED", title="GBS Property Maintenance", lockup="nostrap", colours=REVERSED),
    dict(name="LOGO_REVERSED-SOFT_OFFWHITE", title="GBS Property Maintenance", lockup="nostrap", colours=REVERSED_SOFT),
    dict(name="LOGO_REVERSED_ON-SAGE-PANEL", title="GBS Property Maintenance", lockup="stacked", colours=REVERSED, background=SAGE_SURFACE),
    dict(name="LOGO_WORDMARK_OFFWHITE-RED", title="GBS", lockup="wordmark", colours=REVERSED),
    dict(name="LOGO_STRIP_OFFWHITE-RED", title="GBS Property Maintenance", lockup="strip", colours=REVERSED),
    dict(name="LOGO_MONO_SAGE", title="GBS Property Maintenance", lockup="stacked", colours=mono(SAGE)),
    dict(name="LOGO_MONO-NOSTRAP_SAGE", title="GBS Property Maintenance", lockup="nostrap", colours=mono(SAGE)),
    dict(name="LOGO_MONO_WHITE", title="GBS Property Maintenance", lockup="stacked", colours=mono(WHITE)),
    dict(name="LOGO_MONO-NOSTRAP_WHITE", title="GBS Property Maintenance", lockup="nostrap", colours=mono(WHITE)),
    dict(name="LOGO_MONO_BLACK", title="GBS Property Maintenance", lockup="stacked", colours=mono(BLACK)),
    dict(name="LOGO_MONO-NOSTRAP_BLACK", title="GBS Property Maintenance", lockup="nostrap", colours=mono(BLACK)),
    dict(name="ICON_SAGE-RED", title="GBS Horizon icon", lockup="icon", colours=mono(SAGE)),
    dict(name="ICON_OFFWHITE-RED", title="GBS Horizon icon", lockup="icon", colours=mono(OFFWHITE)),
    dict(name="ICON_MONO_SAGE", title="GBS Horizon icon", lockup="icon", colours=mono(SAGE)),
    dict(name="ICON_MONO_WHITE", title="GBS Horizon icon", lockup="icon", colours=mono(WHITE)),
    dict(name="ICON_MONO_BLACK", title="GBS Horizon icon", lockup="icon", colours=mono(BLACK)),
    dict(name="ICON_SIMPLIFIED_SAGE-RED", title="GBS Horizon icon (embroidery)", lockup="icon", colours=mono(SAGE)),
    dict(name="ICON_SIMPLIFIED_OFFWHITE-RED", title="GBS Horizon icon (embroidery)", lockup="icon", colours=mono(OFFWHITE)),
    dict(name="AVATAR_SQUARE_ON-SAGE", title="GBS Horizon avatar", lockup="icon", colours=mono(OFFWHITE), background=SAGE_SURFACE, square=True),
    dict(name="AVATAR_SQUARE_ON-OFFWHITE", title="GBS Horizon avatar", lockup="icon", colours=mono(SAGE), background=OFFWHITE, square=True),
]


def fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def group(paths, fill):
    out = [f'<g fill="{fill}">']
    for p in paths:
        tr = f' transform="{p["transform"]}"' if p["transform"] else ""
        out.append(f'<path{tr} d="{p["d"]}"/>')
    out.append("</g>")
    return "\n".join(out)


def build(data, v):
    layers, bboxes = data["layers"], data["bboxes"]
    body, note = [], []
    if v["lockup"] == "icon":
        x0, y0, x1, y1 = bboxes["icon"]
        if v.get("square"):
            side = max(x1 - x0, y1 - y0) * 1.5
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            vb = (cx - side / 2, cy - side / 2, side, side)
        else:
            vb = (x0 - PAD, y0 - PAD, x1 - x0 + 2 * PAD, y1 - y0 + 2 * PAD)
        body.append(group(layers["icon"], v["colours"]["word"]))
        note.append("icon from horizon-icon.png")
    else:
        spec = LOCKUPS[v["lockup"]]
        xs0 = min(bboxes[l][0] for l in spec["layers"]); xs1 = max(bboxes[l][2] for l in spec["layers"])
        ys0 = min(bboxes[l][1] for l in spec["layers"]); ys1 = max(bboxes[l][3] for l in spec["layers"])
        for l in spec["layers"]:
            body.append(group(layers[l], v["colours"][LAYER_COLOUR[l]]))
        if spec.get("inline_descriptor"):
            # Descriptor at its supplied size, vertically centred on the GBS letters, after the short bar.
            dx0, dy0, dx1, dy1 = bboxes["descriptor"]
            wx0, wy0, wx1, wy1 = bboxes["word"]
            letters_mid = (wy0 + wy1) / 2
            tx, ty = (xs1 + STRIP_GAP) - dx0, letters_mid - (dy0 + dy1) / 2
            body.append(f'<g transform="translate({fmt(tx)} {fmt(ty)})">' + group(layers["descriptor"], v["colours"]["red"]) + "</g>")
            xs1 = xs1 + STRIP_GAP + (dx1 - dx0)
        vb = (xs0 - PAD, ys0 - PAD, xs1 - xs0 + 2 * PAD, ys1 - ys0 + 2 * PAD)
        note.append(f"{v['lockup']} lockup from horizon-logo.png")
    w, h = vb[2] * UNIT, vb[3] * UNIT
    bg = f'<rect x="{fmt(vb[0])}" y="{fmt(vb[1])}" width="{fmt(vb[2])}" height="{fmt(vb[3])}" fill="{v["background"]}"/>\n' if v.get("background") else ""
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{fmt(vb[0])} {fmt(vb[1])} {fmt(vb[2])} {fmt(vb[3])}" '
        f'width="{fmt(w)}" height="{fmt(h)}" role="img" aria-label="{v["title"]}">\n'
        f"<title>{v['title']}</title>\n"
        f"<!-- GBS HORIZON {v['name']} v1.0 | {'; '.join(note)} | outlined vector traced from the supplied artwork, no live fonts -->\n"
        f"{bg}" + "\n".join(body) + "\n</svg>\n"
    )
    path = os.path.join(OUT, f"GBS_HORIZON_{v['name']}_v1.0.svg")
    with open(path, "w") as fh:
        fh.write(svg)
    return {"file": os.path.basename(path), "w": round(w, 2), "h": round(h, 2), "lockup": v["lockup"]}


if __name__ == "__main__":
    data = json.load(open(SRC))
    manifest = [build(data, v) for v in VARIANTS]
    with open(os.path.join(OUT, "_manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=1)
    print(f"built {len(manifest)} masters in {OUT}")
