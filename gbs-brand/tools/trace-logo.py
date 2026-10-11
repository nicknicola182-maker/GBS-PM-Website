#!/usr/bin/env python3
"""Traces the supplied Horizon artwork into layered vector paths.

Inputs (01_LOGO_MASTER/source):
  horizon-logo.png   the lockup supplied in the October 2026 handover: off-white letters and
                     tall second bar, light sage first and fourth bars and horizon line, red third
                     bar and descriptor, off-white strapline with red separators (970 x 391, transparent)
  horizon-icon.png   the two-colour, five-bar icon from the same handover (1199 x 1076). Kept for the
                     record only: on the owner's instruction (11 Oct 2026) the icon is the four bars
                     and horizon line of the lockup in their three colours, so it is cut from
                     horizon-logo.png below rather than traced from this file.

Output:
  01_LOGO_MASTER/source/layers.json   path data per layer, in 4x (logo) and 2x (icon) units

The layers are: tint (first and fourth bars, horizon line), word (letters, second bar), redbar,
descriptor, strap, pipes, and icon_tint / icon_word / icon_red for the icon.
tools/build-logos.py composes every master variant from this file, so tracing only has to
run again if the supplied artwork changes. Needs Pillow, numpy and vtracer (pip install vtracer).
"""
import json, os, re, sys, tempfile
import numpy as np
from PIL import Image
import vtracer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "01_LOGO_MASTER", "source")
LOGO, ICON = os.path.join(SRC, "horizon-logo.png"), os.path.join(SRC, "horizon-icon.png")
K_LOGO, K_ICON = 4, 16  # upscale factors before tracing, for smooth curves (the icon is a small crop)

# Row boundaries in the supplied logo (source pixels): the descriptor sits between 280 and 340,
# the strapline below 340. Everything above 280 is the GBS lockup with its bars and horizon line.
DESCRIPTOR_TOP, STRAP_TOP = 280, 340

# Icon crop of the supplied logo (source pixels): the four bars stand between x=704 and x=859.
# The horizon line is kept to the proportions of the supplied icon file (longer tail on the left).
ICON_CROP = (620, 0, 930, 275)       # x0, y0, x1, y1 of the crop that becomes the icon canvas
ICON_BARS = (690, 875)               # columns that hold the bars (the letters end at x=669)
ICON_LINE = (636, 913)               # columns kept of the horizon line
TINT_MAX = 205                       # red channel below this (and not red) is the light sage tint (172); antialiased
                                     # edges of the off-white shapes sit above it


def trace_mask(mask, k, name):
    """Upscales a 0..1 mask, thresholds it and traces the dark shapes. Returns path dicts."""
    big = Image.fromarray((mask * 255).astype(np.uint8)).resize((mask.shape[1] * k, mask.shape[0] * k), Image.LANCZOS)
    bw = np.array(big) >= 128
    rgb = np.repeat(np.where(bw[..., None], 0, 255).astype(np.uint8), 3, axis=2)
    with tempfile.TemporaryDirectory() as tmp:
        png, svg = os.path.join(tmp, name + ".png"), os.path.join(tmp, name + ".svg")
        Image.fromarray(rgb).save(png)
        vtracer.convert_image_to_svg_py(png, svg, colormode="binary", hierarchical="stacked", mode="spline",
                                        filter_speckle=8, corner_threshold=60, length_threshold=3.5,
                                        max_iterations=10, splice_threshold=45, path_precision=2)
        text = open(svg).read()
    paths = []
    for attrs in re.findall(r"<path([^>]*)/?>", text):
        d = re.search(r'\sd="([^"]+)"', attrs)
        fill = re.search(r'fill="([^"]+)"', attrs)
        tr = re.search(r'transform="([^"]+)"', attrs)
        if not d or (fill and fill.group(1).upper() in ("#FFFFFF", "WHITE")):
            continue
        paths.append({"d": d.group(1), "transform": tr.group(1) if tr else ""})
    ys, xs = np.where(bw)
    bbox = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())] if len(xs) else None
    return paths, bbox


def region(mask, y0, y1):
    out = np.zeros_like(mask)
    out[y0:y1] = mask[y0:y1]
    return out


def main():
    im = np.array(Image.open(LOGO).convert("RGBA")).astype(float)
    alpha = im[..., 3] / 255.0
    is_red = (im[..., 0] - im[..., 1]) > 80
    is_tint = (~is_red) & (im[..., 0] < TINT_MAX)
    h = alpha.shape[0]
    # The tint split applies above the descriptor only: the thin strapline is antialiased below
    # TINT_MAX in places and must stay whole in the strap layer.
    tint = region(alpha * is_tint, 0, DESCRIPTOR_TOP)
    white, red = alpha * (~is_red) - tint, alpha * is_red
    masks = {
        "tint": tint,
        "word": region(white, 0, STRAP_TOP),
        "strap": region(white, STRAP_TOP, h),
        "redbar": region(red, 0, DESCRIPTOR_TOP),
        "descriptor": region(red, DESCRIPTOR_TOP, STRAP_TOP),
        "pipes": region(red, STRAP_TOP, h),
    }
    layers, bboxes = {}, {}
    for name, m in masks.items():
        layers[name], bboxes[name] = trace_mask(m, K_LOGO, name)
        print(f"{name:10s} {len(layers[name]):3d} paths  bbox {bboxes[name]}")
    # Icon: the bars and a length of the horizon line, cut from the same artwork.
    x0, y0, x1, y1 = ICON_CROP
    def crop(m, cols):
        out = np.zeros_like(m)
        out[:, cols[0]:cols[1]] = m[:, cols[0]:cols[1]]
        return out[y0:y1, x0:x1]
    icon_masks = {"icon_tint": crop(tint, ICON_LINE), "icon_word": crop(white, ICON_BARS), "icon_red": crop(red, ICON_BARS)}
    for name, m in icon_masks.items():
        layers[name], bboxes[name] = trace_mask(m, K_ICON, name)
        print(f"{name:10s} {len(layers[name]):3d} paths  bbox {bboxes[name]}")
    data = {
        "source": {"logo": os.path.basename(LOGO), "icon": "horizon-logo.png (bars and horizon line, see ICON_CROP)",
                   "logo_scale": K_LOGO, "icon_scale": K_ICON},
        "logo_size": [int(alpha.shape[1] * K_LOGO), int(alpha.shape[0] * K_LOGO)],
        "icon_size": [int((x1 - x0) * K_ICON), int((y1 - y0) * K_ICON)],
        "bboxes": bboxes,
        "layers": layers,
    }
    with open(os.path.join(SRC, "layers.json"), "w") as fh:
        json.dump(data, fh)
    print("wrote", os.path.join(SRC, "layers.json"))


if __name__ == "__main__":
    main()
