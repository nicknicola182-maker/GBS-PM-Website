#!/usr/bin/env python3
"""Writes 04_WORKWEAR/placement-sheet.html: A4 landscape placement sheet, one page per garment + embroidery brief."""
import sys, os
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "04_WORKWEAR", "placement-sheet.html")
L = "../01_LOGO_MASTER/svg/"

# ---------- SVG helpers (garment coordinates = full-scale mm, canvas 660 x 840) ----------
CW, CH = 840, 840
def hdim(x1, x2, y, label, above=True):
    ty = y - 8 if above else y + 26
    return (f'<g class="dim"><line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}"/>'
            f'<line x1="{x1}" y1="{y-7}" x2="{x1}" y2="{y+7}"/><line x1="{x2}" y1="{y-7}" x2="{x2}" y2="{y+7}"/>'
            f'<text x="{(x1+x2)/2}" y="{ty}" text-anchor="middle">{label}</text></g>')
def vdim(x, y1, y2, label, left=True):
    tx = x - 10 if left else x + 10
    anchor = "end" if left else "start"
    return (f'<g class="dim"><line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}"/>'
            f'<line x1="{x-7}" y1="{y1}" x2="{x+7}" y2="{y1}"/><line x1="{x-7}" y1="{y2}" x2="{x+7}" y2="{y2}"/>'
            f'<text x="{tx}" y="{(y1+y2)/2+7}" text-anchor="{anchor}">{label}</text></g>')
def guide(x1, y1, x2, y2):
    return f'<line class="guide" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'
def logo(file, x, y, w, h):
    return f'<rect class="zone" x="{x}" y="{y}" width="{w}" height="{h}"/><image href="{L}{file}" x="{x}" y="{y}" width="{w}" height="{h}"/>'
def note(x, y, txt, anchor="start"):
    return f'<text class="lab" x="{x}" y="{y}" text-anchor="{anchor}">{txt}</text>'

# garment bodies. HPS (neck point) at y=60, centre front x=320, shoulder seam point at (90,100)/(550,100)
TEE_FRONT = "M250,60 L90,100 L-20,165 L-50,290 L30,350 L70,290 L70,780 L570,780 L570,290 L610,350 L690,290 L660,165 L550,100 L390,60 Q320,150 250,60 Z"
TEE_BACK  = "M250,60 L90,100 L-20,165 L-50,290 L30,350 L70,290 L70,780 L570,780 L570,290 L610,350 L690,290 L660,165 L550,100 L390,60 Q320,88 250,60 Z"
TEE_DETAIL_F = '<path class="seam" d="M258,70 Q320,138 382,70"/><path class="seam" d="M70,290 L30,350 M570,290 L610,350"/>'
TEE_DETAIL_B = '<path class="seam" d="M258,68 Q320,84 382,68"/><path class="seam" d="M70,290 L30,350 M570,290 L610,350"/>'
POLO_DETAIL_F = ('<path class="seam" d="M250,60 L208,150 L302,118 L320,128 L338,118 L432,150 L390,60"/>'
                 '<path class="seam" d="M302,118 L302,255 L338,255 L338,118"/><circle class="seam" cx="320" cy="170" r="5"/><circle class="seam" cx="320" cy="215" r="5"/>'
                 '<path class="seam" d="M70,290 L30,350 M570,290 L610,350"/>')
POLO_DETAIL_B = '<path class="seam" d="M244,56 L252,30 L388,30 L396,56"/><path class="seam" d="M258,68 Q320,84 382,68"/><path class="seam" d="M70,290 L30,350 M570,290 L610,350"/>'
JKT_FRONT = "M245,40 L80,100 L-30,160 L-80,560 L0,590 L85,290 L85,800 L555,800 L555,290 L640,590 L720,560 L670,160 L560,100 L395,40 L400,90 L320,95 L240,90 Z"
JKT_BACK  = "M245,40 L80,100 L-30,160 L-80,560 L0,590 L85,290 L85,800 L555,800 L555,290 L640,590 L720,560 L670,160 L560,100 L395,40 Q320,70 245,40 Z"
JKT_DETAIL_F = ('<path class="seam" d="M320,95 L320,800"/><path class="seam" d="M240,90 L400,90"/><path class="seam" d="M85,290 L0,590 M555,290 L640,590"/>'
                '<path class="seam" d="M120,590 L150,720 M520,590 L490,720"/>')
JKT_DETAIL_B = '<path class="seam" d="M85,290 L0,590 M555,290 L640,590"/>'
VEST_FRONT = "M250,60 L130,90 Q60,200 70,330 L70,760 L570,760 L570,330 Q580,200 510,90 L390,60 Q320,160 250,60 Z"
VEST_BACK  = "M250,60 L130,90 Q60,200 70,330 L70,760 L570,760 L570,330 Q580,200 510,90 L390,60 Q320,90 250,60 Z"
def vest_bands(front):
    b = ('<rect class="tape" x="70" y="320" width="500" height="50"/><rect class="tape" x="70" y="520" width="500" height="50"/>'
         '<rect class="tape" x="150" y="60" width="50" height="260"/><rect class="tape" x="440" y="60" width="50" height="260"/>')
    if front: b += '<path class="seam" d="M320,160 L320,760"/>'
    return b

def drawing(title, body_path, detail, art, scale_note=""):
    return (f'<figure class="draw"><figcaption>{title}</figcaption>'
            f'<svg viewBox="-100 0 {CW} {CH}" xmlns="http://www.w3.org/2000/svg">'
            f'<path class="garment" d="{body_path}"/>{detail}{art}</svg></figure>')

CHEST_X, CHEST_Y, CHEST_W, CHEST_H = 377.5, 150, 95, 38.24   # wearer's left = viewer's right
BACK_X, BACK_Y, BACK_W, BACK_H = 190, 170, 260, 126.31
BNS_X, BNS_Y, BNS_W, BNS_H = 205, 175, 230, 92.57            # no-strap back 230 (polo optional)
SLV_X, SLV_Y, SLV_W, SLV_H = 590, 200, 48.3, 40

def chest_art(file, w=CHEST_W, h=CHEST_H, x=CHEST_X, y=CHEST_Y, hps=60):
    cx = x + w/2
    return (guide(320, 60, 320, 800) + guide(cx, 100, cx, y-5) + logo(file, x, y, w, h)
            + hdim(320, cx, 120, f"{cx-320:.0f}") + vdim(cx+w/2+22, hps, y, f"{y-hps:.0f}", left=False)
            + hdim(x, x+w, y+h+16, f"{w:g} wide", above=False) + note(320, 820, "centre front", "middle"))
def back_art(file, w=BACK_W, h=BACK_H, x=BACK_X, y=BACK_Y, hps=60):
    return (guide(320, 60, 320, 800) + logo(file, x, y, w, h)
            + vdim(x+w+22, hps, y, f"{y-hps:.0f} below back neck seam", left=False)
            + hdim(x, x+w, y+h+16, f"{w:g} wide, centred", above=False) + note(320, 820, "centre back", "middle"))
def sleeve_art(file, x=SLV_X, y=SLV_Y, w=SLV_W, h=SLV_H):
    return (logo(file, x, y, w, h) + vdim(x+w+20, 100, y, f"{y-100:.0f}", left=False) + hdim(x, x+w, y+h+16, f"{h:g} high", above=False))

GARMENTS = [
 dict(name="White T-shirt", placement="Chest mark: wearer's left, centre 105 mm from centre front, top edge 90 mm below the shoulder seam at the neck point, 95 mm wide. Sleeve emblem: wearer's left sleeve, centred on the outer sleeve, top edge 100 mm below the shoulder seam, 40 mm high. Back: centred on centre back, top edge 110 mm below the back neck seam, 260 mm wide.", code="W01-A", colour="White or off-white garment", technique="Screen print (2 spot colours, sage + red) for runs of 25 or more; DTF transfer for small runs and re-orders. Soft-hand ink, no underbase on white.",
      front=TEE_FRONT, back=TEE_BACK, fdet=TEE_DETAIL_F, bdet=TEE_DETAIL_B,
      chest="GBS_HORIZON_LOGO_PRIMARY-NOSTRAP_SAGE-RED_v1.0.svg", backlogo="GBS_HORIZON_LOGO_PRIMARY_SAGE-RED_v1.0.svg", sleeve="GBS_HORIZON_ICON_SAGE-RED_v1.0.svg",
      files=["GBS_HORIZON_WORKWEAR_CHEST_95MM_SAGE-RED_v1.0.png", "GBS_HORIZON_WORKWEAR_BACK_260MM_SAGE-RED_v1.0.png", "GBS_HORIZON_WORKWEAR_SLEEVE_40MM_SAGE-RED_v1.0.png"],
      extra="Garment white should read as clean white or off-white; avoid optic-bright blue-whites next to the sage."),
 dict(name="Sage T-shirt", placement="Chest mark: wearer's left, centre 105 mm from centre front, top edge 90 mm below the shoulder seam at the neck point, 95 mm wide. Sleeve emblem: wearer's left sleeve, centred on the outer sleeve, top edge 100 mm below the shoulder seam, 40 mm high. Back: centred on centre back, top edge 110 mm below the back neck seam, 260 mm wide.", code="W01-B", colour="Sage garment (dye matched to the brand sage, supplier swatch to be approved)", technique="Screen print (off-white + red, with a white underbase under the red only if the supplier needs it for opacity) or DTF transfer.",
      front=TEE_FRONT, back=TEE_BACK, fdet=TEE_DETAIL_F, bdet=TEE_DETAIL_B,
      chest="GBS_HORIZON_LOGO_REVERSED-NOSTRAP_OFFWHITE-RED_v1.0.svg", backlogo="GBS_HORIZON_LOGO_REVERSED_OFFWHITE-RED_v1.0.svg", sleeve="GBS_HORIZON_ICON_OFFWHITE-RED_v1.0.svg",
      files=["GBS_HORIZON_WORKWEAR_CHEST_95MM_OFFWHITE-RED_v1.0.png", "GBS_HORIZON_WORKWEAR_BACK_260MM_OFFWHITE-RED_v1.0.png", "GBS_HORIZON_WORKWEAR_SLEEVE_40MM_OFFWHITE-RED_v1.0.png"],
      extra="The reversed lockup is the only approved use of red on sage. Do not add a keyline or drop shadow."),
 dict(name="White polo", placement="Chest mark: wearer's left, centre 105 mm from centre front, top edge 90 mm below the shoulder seam at the neck point, 95 mm wide, clear of the placket. Sleeve emblem: wearer's left sleeve, centred, top edge 100 mm below the shoulder seam, 40 mm high (simplified icon). Back (optional): centred, top edge 115 mm below the back neck seam, 230 mm wide no-strap lockup.", code="W02-A", colour="White garment", technique="Embroidery. Chest: no-strap lockup 95 mm wide. Sleeve: simplified icon 40 mm high. Back (optional, only if ordered): no-strap lockup 230 mm wide. Stitch sample (sew-out on the actual garment) required before production.",
      front=TEE_FRONT, back=TEE_BACK, fdet=POLO_DETAIL_F, bdet=POLO_DETAIL_B, polo=True,
      chest="GBS_HORIZON_LOGO_PRIMARY-NOSTRAP_SAGE-RED_v1.0.svg", backlogo="GBS_HORIZON_LOGO_PRIMARY-NOSTRAP_SAGE-RED_v1.0.svg", sleeve="GBS_HORIZON_ICON_SIMPLIFIED_SAGE-RED_v1.0.svg",
      files=["01_LOGO_MASTER/svg/GBS_HORIZON_LOGO_PRIMARY-NOSTRAP_SAGE-RED_v1.0.svg (digitise from vector)", "01_LOGO_MASTER/svg/GBS_HORIZON_ICON_SIMPLIFIED_SAGE-RED_v1.0.svg", "See page 7, embroidery brief"],
      extra="Descriptor cap height at 95 mm is 3.9 mm: below the 5 mm letter test. See the embroidery brief for the sew-out decision and wordmark fallback."),
 dict(name="Sage polo", placement="Chest mark: wearer's left, centre 105 mm from centre front, top edge 90 mm below the shoulder seam at the neck point, 95 mm wide, clear of the placket. Sleeve emblem: wearer's left sleeve, centred, top edge 100 mm below the shoulder seam, 40 mm high (simplified icon). Back (optional): centred, top edge 115 mm below the back neck seam, 230 mm wide no-strap lockup.", code="W02-B", colour="Sage garment (dye matched to the brand sage)", technique="Embroidery, as the white polo. Off-white and red threads on sage. Stitch sample required.",
      front=TEE_FRONT, back=TEE_BACK, fdet=POLO_DETAIL_F, bdet=POLO_DETAIL_B, polo=True,
      chest="GBS_HORIZON_LOGO_REVERSED-NOSTRAP_OFFWHITE-RED_v1.0.svg", backlogo="GBS_HORIZON_LOGO_REVERSED-NOSTRAP_OFFWHITE-RED_v1.0.svg", sleeve="GBS_HORIZON_ICON_SIMPLIFIED_OFFWHITE-RED_v1.0.svg",
      files=["01_LOGO_MASTER/svg/GBS_HORIZON_LOGO_REVERSED-NOSTRAP_OFFWHITE-RED_v1.0.svg (digitise from vector)", "01_LOGO_MASTER/svg/GBS_HORIZON_ICON_SIMPLIFIED_OFFWHITE-RED_v1.0.svg", "See page 7, embroidery brief"],
      extra="Sew the second (hollow) bar of the icon as a solid bar, as in the simplified icon: the 1 mm outline will not sew at this size."),
 dict(name="Softshell jacket", placement="Chest mark: wearer's left, centre 105 mm from centre front, top edge 90 mm below the shoulder seam at the neck point, 95 mm wide. Sleeve emblem: wearer's left sleeve, centred on the outer sleeve, top edge 90 mm below the shoulder seam, 40 mm high. Back: centred on centre back, top edge 110 mm below the back neck seam, 260 mm wide.", code="W03-A", colour="Sage garment (reversed artwork). If a white or off-white shell is ever ordered, use the primary files from the T-shirt page.", technique="Heat transfer (DTF or cut flex) applied at the temperature and dwell the shell membrane allows: supplier to confirm. Keep transfers clear of seams, zips and pockets.",
      front=JKT_FRONT, back=JKT_BACK, fdet=JKT_DETAIL_F, bdet=JKT_DETAIL_B, jacket=True,
      chest="GBS_HORIZON_LOGO_REVERSED-NOSTRAP_OFFWHITE-RED_v1.0.svg", backlogo="GBS_HORIZON_LOGO_REVERSED_OFFWHITE-RED_v1.0.svg", sleeve="GBS_HORIZON_ICON_OFFWHITE-RED_v1.0.svg",
      files=["GBS_HORIZON_WORKWEAR_CHEST_95MM_OFFWHITE-RED_v1.0.png", "GBS_HORIZON_WORKWEAR_BACK_260MM_OFFWHITE-RED_v1.0.png", "GBS_HORIZON_WORKWEAR_SLEEVE_40MM_OFFWHITE-RED_v1.0.png"],
      extra="Chest mark sits on the wearer's left, clear of the zip by at least 40 mm. If the jacket has a left chest pocket, move the mark 20 mm above the pocket zip or agree an alternative position."),
 dict(name="Hi-vis vest (yellow, EN ISO 20471)", placement="Chest mark: wearer's left, centred between the front opening and the shoulder band (60 mm from centre front on this drawing), top edge 170 mm below the shoulder seam at the neck point, 95 mm wide. Back: centred on centre back, centred in the clear zone between the two horizontal bands (150 mm deep on this drawing), 260 mm wide. Final positions to be agreed with the manufacturer.", code="W03-B", colour="Fluorescent yellow garment, mono black artwork", technique="Screen print or transfer in black. Position to be agreed with the manufacturer so that no print touches the retroreflective tape and the certified fluorescent area is kept. Supplier to confirm the garment stays within its EN ISO 20471 class after printing.",
      front=VEST_FRONT, back=VEST_BACK, fdet=vest_bands(True), bdet=vest_bands(False), vest=True,
      chest="GBS_HORIZON_LOGO_MONO-NOSTRAP_BLACK_v1.0.svg", backlogo="GBS_HORIZON_LOGO_MONO_BLACK_v1.0.svg", sleeve=None,
      files=["GBS_HORIZON_WORKWEAR_HIVIS-BACK_260MM_BLACK_v1.0.png (zones 150 mm or deeper)", "GBS_HORIZON_WORKWEAR_HIVIS-BACK-NOSTRAP_260MM_BLACK_v1.0.png (shallower zones)", "GBS_HORIZON_WORKWEAR_HIVIS-CHEST_95MM_BLACK_v1.0.png"],
      extra="Back print centred between the two horizontal bands; if the clear zone between bands is under 150 mm deep, use the no-strap file (105 mm deep) or reduce to 230 mm wide. Chest mark between the shoulder band and the front opening, above the upper band; reduce to 85 mm if the zone is narrower than 110 mm."),
]

def page(g, n, total):
    if g.get("vest"):
        # chest zone between brace band (inner edge x=430) and front opening (x=320): centre 375
        cx = 380; w = 95; h = 38.24; x = cx - w/2; y = 230
        front_art = (guide(320, 60, 320, 760) + logo(g["chest"], x, y, w, h) + hdim(320, cx, 200, f"{cx-320:.0f}") + vdim(x+w+18, 60, y, f"{y-60:.0f}", left=False)
                     + hdim(x, x+w, y+h+16, f"{w:g} wide", above=False) + note(320, 800, "centre front", "middle")
                     + note(320, 345, "retroreflective tape: keep clear", "middle") + note(320, 545, "retroreflective tape: keep clear", "middle"))
        by = 370 + (150 - 126.31)/2
        back_art_ = (guide(320, 60, 320, 760) + logo(g["backlogo"], 190, by, 260, 126.31) + vdim(190+260+22, 370, 520, "150 clear zone between bands", left=False)
                     + hdim(190, 450, 525+16, "260 wide, centred", above=False) + note(320, 800, "centre back", "middle")
                     + note(320, 345, "retroreflective tape: keep clear", "middle") + note(320, 545, "retroreflective tape: keep clear", "middle"))
    elif g.get("polo"):
        front_art = chest_art(g["chest"]) + sleeve_art(g["sleeve"])
        back_art_ = back_art(g["backlogo"], BNS_W, BNS_H, BNS_X, BNS_Y) + note(320, 300, "optional back embroidery", "middle")
    elif g.get("jacket"):
        # jacket: chest centre 105 from CF at 150 below HPS (HPS y=40): y=130
        front_art = chest_art(g["chest"], y=130, hps=40) + sleeve_art(g["sleeve"], x=596, y=190)
        back_art_ = back_art(g["backlogo"], y=150, hps=40)
    else:
        front_art = chest_art(g["chest"]) + sleeve_art(g["sleeve"])
        back_art_ = back_art(g["backlogo"])
    files = "".join(f"<li>{f}</li>" for f in g["files"])
    return f'''
<section class="page" data-trim="297 x 210 mm" aria-label="{g['name']} placement">
  <header class="head">
    <div class="logo"><img src="{L}GBS_HORIZON_LOGO_PRIMARY-NOSTRAP_SAGE-RED_v1.0.svg" alt="GBS Property Maintenance"></div>
    <div class="title"><span class="eyebrow">Workwear placement sheet</span><h1>{g['name']}</h1></div>
    <div class="meta"><span class="num">{g['code']}</span><br>Sheet {n} of {total}<br>v1.0</div>
  </header>
  <div class="head-rule"></div>
  <div class="drawings">
    {drawing("Front (as worn: wearer's left is on the right of the drawing)", g['front'], g['fdet'], front_art)}
    {drawing("Back", g['back'], g['bdet'], back_art_)}
  </div>
  <aside class="notes">
    <h3>Garment</h3><p>{g['colour']}</p>
    <h3>Technique</h3><p>{g['technique']}</p>
    <h3>Placement</h3>
    <p>{g['placement']}</p>
    <h3>Files</h3><ul>{files}</ul>
    <p class="small">{g['extra']}</p>
  </aside>
  <footer class="foot"><span>Dimensions in mm at full size, measured flat; drawings not to scale. Sizes shown for a size L; scale positions by +/- 10 mm per size step and confirm on a sample.</span><span>{{{{company.tradingName}}}} &middot; {{{{company.domain}}}}</span></footer>
</section>'''

BRIEF = '''
<section class="page" data-trim="297 x 210 mm" aria-label="Embroidery brief">
  <header class="head">
    <div class="logo"><img src="../01_LOGO_MASTER/svg/GBS_HORIZON_LOGO_PRIMARY-NOSTRAP_SAGE-RED_v1.0.svg" alt="GBS Property Maintenance"></div>
    <div class="title"><span class="eyebrow">Workwear placement sheet</span><h1>Embroidery brief</h1></div>
    <div class="meta"><span class="num">W02</span><br>Sheet 7 of 7<br>v1.0</div>
  </header>
  <div class="head-rule"></div>
  <div class="brief">
    <div class="col">
      <h3>Scope</h3>
      <p>Polo shirts (white and sage): left chest lockup and left sleeve emblem; optional back lockup only when ordered. Softshell jackets are heat transfer by default; embroider only if agreed in writing, using the same files.</p>
      <h3>Artwork supplied (vector, outlined, no live fonts)</h3>
      <ul>
        <li>01_LOGO_MASTER/svg/GBS_HORIZON_LOGO_PRIMARY-NOSTRAP_SAGE-RED_v1.0.svg (white polo chest, 95 mm wide; optional back 230 mm)</li>
        <li>01_LOGO_MASTER/svg/GBS_HORIZON_LOGO_REVERSED-NOSTRAP_OFFWHITE-RED_v1.0.svg (sage polo chest, 95 mm wide; optional back 230 mm)</li>
        <li>01_LOGO_MASTER/svg/GBS_HORIZON_ICON_SIMPLIFIED_SAGE-RED_v1.0.svg and _OFFWHITE-RED (sleeve emblem, 40 mm high)</li>
        <li>04_WORKWEAR/GBS_HORIZON_WORKWEAR_CHEST_95MM_*.png and SLEEVE_40MM_*.png (300 dpi size references only; digitise from the SVG)</li>
      </ul>
      <p>Digitise from the vector files without redrawing. Keep the proportions, the clear space (one GBS cap height on every side) and the colour split exactly as supplied. In the lockup, sew the second (hollow) bar of the icon as a solid bar, matching the simplified icon: its 1 mm outline will not sew at chest size.</p>
      <h3>Sizes and letter heights</h3>
      <table>
        <tr><th>Mark</th><th>Width</th><th>Height</th><th>GBS cap</th><th>Descriptor cap</th></tr>
        <tr><td>Chest lockup</td><td class="num">95 mm</td><td class="num">38 mm</td><td class="num">21.4 mm</td><td class="num">3.9 mm</td></tr>
        <tr><td>Chest lockup (maximum)</td><td class="num">105 mm</td><td class="num">42 mm</td><td class="num">23.6 mm</td><td class="num">4.3 mm</td></tr>
        <tr><td>Sleeve emblem (simplified icon)</td><td class="num">48 mm</td><td class="num">40 mm</td><td colspan="2">no lettering</td></tr>
        <tr><td>Back lockup (optional)</td><td class="num">230 mm</td><td class="num">93 mm</td><td class="num">51.8 mm</td><td class="num">9.5 mm</td></tr>
      </table>
    </div>
    <div class="col">
      <h3>Thread colour targets</h3>
      <table>
        <tr><th>Colour</th><th>Target (RGB / hex)</th><th>Use</th></tr>
        <tr><td>Sage</td><td class="num">110 / 127 / 114 &nbsp; #6E7F72</td><td>GBS letters, bars, rule, descriptor on reversed marks is off-white</td></tr>
        <tr><td>Red</td><td class="num">225 / 6 / 0 &nbsp; #E10600</td><td>Third bar and descriptor (primary); third bar only on reversed marks where supplied</td></tr>
        <tr><td>Off-white</td><td class="num">249 / 249 / 247 &nbsp; #F9F9F7</td><td>Letters, bars and rule on sage garments</td></tr>
      </table>
      <p>Propose the two nearest 40 wt polyester shades for each colour and submit thread cards. Final shades are approved against the physical samples held by GBS, not against screen values. No metallic or high-sheen threads.</p>
      <h3>Minimum letter height test</h3>
      <p>Before production, sew out the descriptor PROPERTY MAINTENANCE at 5 mm and 6 mm cap height and at the actual chest size (3.9 mm at 95 mm wide; 4.3 mm at 105 mm) on the production fabric with the proposed stabiliser. If the 3.9 mm descriptor does not resolve cleanly, GBS will approve one of: (a) chest mark at 105 mm wide; (b) the wordmark without descriptor (01_LOGO_MASTER/svg/GBS_HORIZON_LOGO_WORDMARK_*) at 95 mm for embroidered chest marks. The descriptor must not be re-set in a larger size or a different font.</p>
      <h3>Sign-off</h3>
      <p>Supply a sew-out of every mark on the actual garment colour for approval by the GBS Director before the production run (asset W02 in the production register). Keep the stitch files and report stitch counts with the quote.</p>
    </div>
  </div>
  <footer class="foot"><span>Dimensions in mm at full size.</span><span>{{company.tradingName}} &middot; {{company.domain}}</span></footer>
</section>'''

CSS = '''
  :root { --trim-w: 297mm; --trim-h: 210mm; }
  .page { padding: 0; }
  .head { position: absolute; left: 12mm; right: 12mm; top: 9mm; height: 16mm; display: flex; align-items: flex-end; gap: 8mm; }
  .head .logo { width: 34mm; flex: none; } .head .logo img { width: 100%; display: block; }
  .head .title { flex: 1; } .head .title .eyebrow { display: block; margin-bottom: 1mm; }
  .head h1 { font-size: 15pt; font-weight: 700; }
  .head .meta { text-align: right; font-size: 7.5pt; line-height: 1.4; color: var(--gbs-ink-soft); }
  .head-rule { position: absolute; left: 12mm; right: 12mm; top: 27.5mm; height: 0.5pt; background: var(--gbs-sage); }
  .head-rule::after { content: ""; position: absolute; right: 0; top: -1.5pt; width: 14mm; height: 2pt; background: var(--gbs-red); }
  .drawings { position: absolute; left: 12mm; top: 31mm; width: 205mm; height: 160mm; display: flex; gap: 5mm; }
  .draw { margin: 0; width: 100mm; }
  .draw figcaption { font-family: var(--font-heading); font-weight: 600; font-size: 7pt; color: var(--gbs-sage); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 1.5mm; }
  .draw svg { width: 100mm; height: 100mm; display: block; }
  .garment { fill: #fff; stroke: var(--gbs-ink); stroke-width: 3; stroke-linejoin: round; }
  .seam { fill: none; stroke: var(--gbs-ink-soft); stroke-width: 1.5; }
  .tape { fill: #DADADA; stroke: none; }
  .zone { fill: none; stroke: var(--gbs-red); stroke-width: 1; stroke-dasharray: 6 4; }
  .guide { stroke: var(--gbs-light); stroke-width: 1.5; stroke-dasharray: 8 6; }
  .dim line { stroke: var(--gbs-ink-soft); stroke-width: 1.5; }
  .dim text, .lab { font-family: var(--font-body); font-weight: 500; font-size: 19px; fill: var(--gbs-ink); }
  .lab { fill: var(--gbs-ink-soft); font-size: 17px; }
  .notes { position: absolute; left: 222mm; right: 12mm; top: 31mm; bottom: 18mm; font-size: 7.6pt; line-height: 1.4; }
  .notes h3 { font-size: 8pt; margin: 0 0 1mm; text-transform: uppercase; letter-spacing: 0.08em; color: var(--gbs-sage); }
  .notes p { margin: 0 0 2.2mm; } .notes ul { margin: 0 0 2.2mm; padding-left: 3.5mm; } .notes li { margin-bottom: 0.6mm; word-break: break-all; }
  .notes .small { font-size: 7pt; color: var(--gbs-ink-soft); }
  .foot { position: absolute; left: 12mm; right: 12mm; bottom: 9mm; display: flex; justify-content: space-between; gap: 8mm; font-size: 6.8pt; color: var(--gbs-ink-soft); border-top: 0.5pt solid var(--gbs-light); padding-top: 1.5mm; }
  .brief { position: absolute; left: 12mm; right: 12mm; top: 32mm; bottom: 18mm; display: flex; gap: 10mm; font-size: 8.2pt; line-height: 1.42; }
  .brief .col { flex: 1; min-width: 0; }
  .brief h3 { font-size: 8.5pt; text-transform: uppercase; letter-spacing: 0.08em; margin: 0 0 1.2mm; }
  .brief p { margin: 0 0 2.8mm; } .brief ul { margin: 0 0 2.8mm; padding-left: 3.5mm; } .brief li { margin-bottom: 0.7mm; }
  .brief table { width: 100%; border-collapse: collapse; margin: 0 0 3mm; font-size: 7.6pt; }
  .brief th { text-align: left; font-family: var(--font-heading); font-weight: 600; color: var(--gbs-sage); border-bottom: 0.5pt solid var(--gbs-sage); padding: 0.8mm 1.5mm 0.8mm 0; }
  .brief td { border-bottom: 0.5pt solid var(--gbs-light); padding: 0.8mm 1.5mm 0.8mm 0; vertical-align: top; }
'''

html = f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<title>GBS_HORIZON_WORKWEAR_PLACEMENT-SHEET_A4L</title>
<link rel="stylesheet" href="../00_BRAND_CORE/tokens.css">
<link rel="stylesheet" href="../00_BRAND_CORE/fonts.css">
<link rel="stylesheet" href="../03_PRINT/_shared/print-base.css">
<style>{CSS}</style>
</head>
<body>
{"".join(page(g, i + 1, 7) for i, g in enumerate(GARMENTS))}
{BRIEF}
</body>
</html>
'''
open(OUT, "w").write(html)
print("wrote", OUT, len(html), "bytes")
