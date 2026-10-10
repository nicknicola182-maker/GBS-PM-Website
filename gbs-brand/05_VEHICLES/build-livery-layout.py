#!/usr/bin/env python3
"""Writes 05_VEHICLES/livery-layout.html: A3 landscape livery layout sheet (side elevations 1:15, rear/front 1:10)."""
import sys, os
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "05_VEHICLES", "livery-layout.html")
L = "../01_LOGO_MASTER/svg/"
LOCK = L + "GBS_HORIZON_LOGO_PRIMARY_SAGE-RED_v1.0.svg"
ICON = L + "GBS_HORIZON_ICON_SAGE-RED_v1.0.svg"

def hdim(x1, x2, y, label, above=True, t=45):
    ty = y - t * 0.35 if above else y + t * 1.25
    k = t * 0.3
    return (f'<g class="dim"><line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}"/><line x1="{x1}" y1="{y-k}" x2="{x1}" y2="{y+k}"/><line x1="{x2}" y1="{y-k}" x2="{x2}" y2="{y+k}"/>'
            f'<text x="{(x1+x2)/2}" y="{ty}" text-anchor="middle" font-size="{t}">{label}</text></g>')
def vdim(x, y1, y2, label, left=True, t=45):
    k = t * 0.3; tx = x - t * 0.35 if left else x + t * 1.1
    ty = (y1 + y2) / 2
    return (f'<g class="dim"><line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}"/><line x1="{x-k}" y1="{y1}" x2="{x+k}" y2="{y1}"/><line x1="{x-k}" y1="{y2}" x2="{x+k}" y2="{y2}"/>'
            f'<text x="{tx}" y="{ty}" text-anchor="middle" font-size="{t}" transform="rotate(-90 {tx} {ty})">{label}</text></g>')
def ext(x1, y1, x2, y2): return f'<line class="ext" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'
def lab(x, y, txt, t=42, anchor="start", cls="lab"): return f'<text class="{cls}" x="{x}" y="{y}" font-size="{t}" text-anchor="{anchor}">{txt}</text>'
def art(href, x, y, w, h): return f'<rect class="zone" x="{x}" y="{y}" width="{w}" height="{h}"/><image href="{href}" x="{x}" y="{y}" width="{w}" height="{h}"/>'
def bars(x, y_bottom):
    b = [(15, 170, "sage"), (40, 310, "red"), (40, 460, "sage")]; out = ""; cx = x
    for w, h, c in b: out += f'<rect class="bar-{c}" x="{cx}" y="{y_bottom-h}" width="{w}" height="{h}"/>'; cx += w + 25
    return out
def scalebar(x, y, t=45):
    return (f'<g class="dim"><rect x="{x}" y="{y}" width="500" height="{t*0.5}" fill="#2E3531"/><rect x="{x+500}" y="{y}" width="500" height="{t*0.5}" fill="#fff" stroke="#2E3531" stroke-width="{t*0.08}"/>'
            f'<text x="{x}" y="{y+t*1.4}" text-anchor="middle" font-size="{t*0.8}">0</text><text x="{x+500}" y="{y+t*1.4}" text-anchor="middle" font-size="{t*0.8}">500</text><text x="{x+1000}" y="{y+t*1.4}" text-anchor="middle" font-size="{t*0.8}">1000 mm</text></g>')

# ---------------- side elevation geometry (full-scale mm, y down, ground = 2000) ----------------
BODY = "M80,1580 L40,1450 L40,1150 L100,980 L200,950 L720,890 L1180,120 Q1260,0 1420,0 L5160,0 Q5270,0 5270,110 L5270,1460 L5290,1580 L4720,1580 A430,430 0 0 0 3880,1580 L1420,1580 A430,430 0 0 0 580,1580 Z"
COMMON = (f'<path class="body" d="{BODY}"/>'
          '<circle class="tyre" cx="1000" cy="1660" r="330"/><circle class="rim" cx="1000" cy="1660" r="200"/><circle class="tyre" cx="4300" cy="1660" r="330"/><circle class="rim" cx="4300" cy="1660" r="200"/>'
          '<polygon class="glass" points="760,880 1190,120 1300,120 880,880"/>'
          '<polygon class="glass" points="1080,990 1960,990 1960,200 1560,200"/>'
          '<path class="gap" d="M1000,1560 L1000,1010 L1500,120"/><path class="gap" d="M2000,80 L2000,1560"/><path class="gap" d="M1420,80 L5200,80"/>'
          '<rect class="handle" x="1780" y="1000" width="170" height="45" rx="20"/><rect class="handle" x="1140" y="480" width="90" height="180" rx="15"/>'
          '<rect class="lamp" x="5200" y="900" width="70" height="450" rx="20"/>')
NEARSIDE_EXTRA = ('<path class="gap" d="M3300,80 L3300,1560"/><rect class="handle" x="3100" y="1000" width="170" height="45" rx="20"/>'
                  '<rect class="keep" x="3300" y="80" width="1500" height="100"/>')
OFFSIDE_EXTRA = '<rect class="flap" x="2970" y="900" width="180" height="180" rx="20"/>'  # fuel flap (van x 2150-2330 mirrored)

def side_page(nearside, n):
    title = "Nearside elevation (passenger side, sliding door)" if nearside else "Offside elevation (driver side)"
    if nearside:
        van = f'<g id="van">{COMMON}{NEARSIDE_EXTRA}</g>'
        lx, rx = 3550, 4950   # lockup x range
        cx = 4250
        dims = (ext(lx, 300, lx, 1250) + ext(rx, 300, rx, 1250) + hdim(lx, rx, 1220, "1400 (lockup width)", above=False)
                + ext(3300, 1660, 3300, 1760) + ext(lx, 1660, lx, 1760) + hdim(3300, lx, 1740, "250 from sliding-door edge", above=False)
                + ext(rx, 1660, rx, 1760) + ext(5300, 1660, 5300, 1760) + hdim(rx, 5300, 1740, "350 to rear corner", above=False)
                + vdim(5450, 0, 300, "300", left=False) + ext(5270, 300, 5450, 300) + ext(5270, 0, 5450, 0)
                + vdim(3450, 300, 980, "680 (lockup height)") + vdim(3450, 1040, 1115, "75 contact row")
                + ext(3600, 1040, 3450, 1040) + ext(3600, 1115, 3450, 1115)
                + lab(4050, 155, "sliding-door upper track rail: keep clear 100", 38, "middle", "keeplab")
                + lab(4250, 1340, "all dimensions full-scale mm; placeholder geometry until the vehicle survey", 38, "middle")
                + hdim(0, 5300, -120, "5300 overall length (placeholder)") + vdim(-150, 0, 2000, "2000 overall height")
                + ext(0, -40, 0, -160) + ext(5300, -40, 5300, -160) + ext(-60, 0, -200, 0) + ext(-60, 2000, -200, 2000)
                + hdim(1000, 4300, 1900, "3300 wheelbase (placeholder)", above=False, t=42)
                + vdim(5450, 1120, 1580, "460 bars", left=False) + ext(5145, 1120, 5450, 1120) + ext(5145, 1580, 5450, 1580))
        livery = (art(LOCK, lx, 300, 1400, 680.14)
                  + f'<text class="contact" x="3600" y="1100" font-size="82.5">{{{{company.domain}}}}</text><text class="contact" x="4900" y="1100" font-size="82.5" text-anchor="end">{{{{company.phone}}}}</text>'
                  + f'<rect class="zone" x="3600" y="1040" width="1300" height="75"/>'
                  + bars(5000, 1580))
    else:
        van = f'<g id="van" transform="translate(5300,0) scale(-1,1)">{COMMON}</g>' + OFFSIDE_EXTRA
        lx, rx = 350, 1750
        dims = (ext(lx, 300, lx, 1250) + ext(rx, 300, rx, 1250) + hdim(lx, rx, 1220, "1400 (lockup width)", above=False)
                + ext(0, 1660, 0, 1760) + ext(lx, 1660, lx, 1760) + hdim(0, lx, 1740, "350 to rear corner", above=False)
                + ext(rx, 1660, rx, 1760) + ext(3300, 1660, 3300, 1760) + hdim(rx, 3300, 1740, "1550 to B-pillar", above=False)
                + vdim(-150, 0, 300, "300") + ext(30, 300, -150, 300) + ext(30, 0, -150, 0)
                + vdim(1850, 300, 980, "680 (lockup height)", left=False) + vdim(1850, 1040, 1115, "75 contact row", left=False)
                + ext(1700, 1040, 1850, 1040) + ext(1700, 1115, 1850, 1115)
                + lab(3060, 850, "fuel flap: keep clear 100", 38, "middle", "keeplab")
                + lab(2650, 1340, "all dimensions full-scale mm; placeholder geometry until the vehicle survey", 38, "middle")
                + hdim(0, 5300, -120, "5300 overall length (placeholder)") + vdim(5450, 0, 2000, "2000 overall height", left=False)
                + ext(0, -40, 0, -160) + ext(5300, -40, 5300, -160) + ext(5340, 0, 5450, 0) + ext(5340, 2000, 5450, 2000)
                + vdim(-150, 1120, 1580, "460 bars") + ext(155, 1120, -150, 1120) + ext(155, 1580, -150, 1580))
        livery = (art(LOCK, lx, 300, 1400, 680.14)
                  + f'<text class="contact" x="400" y="1100" font-size="82.5">{{{{company.domain}}}}</text><text class="contact" x="1700" y="1100" font-size="82.5" text-anchor="end">{{{{company.phone}}}}</text>'
                  + f'<rect class="zone" x="400" y="1040" width="1300" height="75"/>'
                  + bars(155, 1580))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-420 -260 6140 2420" class="side">'
           f'<line class="ground" x1="-300" y1="2000" x2="5600" y2="2000"/>{van}{livery}{dims}{scalebar(-300, 2120)}</svg>')
    return f'''
<section class="page" data-trim="420 x 297 mm" aria-label="{title}">
  {head("Vehicle livery layout", title, "V01", n, "Scale 1:15 on A3 (a 5.3 m van does not fit A3 at 1:10); verify on vehicle survey")}
  <div class="drawing side-wrap">{svg}</div>
  <div class="notes-row">
    <div><h3>Elements on this side</h3>
      <ul><li>Side lockup: primary logo with strapline, 1400 x 680 mm, centred on the rear load panel at 4250 mm from the front (250 mm behind the {'sliding-door rear edge' if nearside else 'equivalent line'}, 350 mm from the rear corner), top edge 300 mm below the roof line. File GBS_HORIZON_VAN_SIDE-LOCKUP_1400MM_SAGE-RED_v1.0.svg.</li>
      <li>Contact row: web address left, phone right, Inter SemiBold, 60 mm cap height, 1300 mm between outer edges, 60 mm below the strapline. File GBS_HORIZON_VAN_SIDE-CONTACT_1300MM_SAGE_v1.0.svg (outlined).</li>
      <li>Rear-quarter bars: 145 x 460 mm, bottom edge on the sill line, 155 mm from the rear corner. File GBS_HORIZON_VAN_REAR-QUARTER-BARS_460MM_SAGE-RED_v1.0.svg.</li></ul></div>
    <div><h3>Keep clear</h3>
      <ul><li>Door gaps, handles, the {'sliding-door upper track rail (100 mm band below the gutter)' if nearside else 'fuel flap (100 mm all round)'} and the sliding-door travel: no graphic may bridge a gap or sit on a rail.</li>
      <li>Rear lamp wrap-around, side repeater, side sensors and any camera. 50 mm minimum to any panel edge, swage line or rubbing strip.</li>
      <li>Wheel-arch flare: nothing below the 1230 mm line within 500 mm of the rear axle.</li></ul></div>
    <div><h3>Survey before cutting</h3>
      <ul><li>Measure the real panel between the sliding-door rear edge and the rear corner; recentre the lockup on that panel and scale to 1300-1400 mm so that at least 150 mm remains above and below.</li>
      <li>Record roof-line, sill, arch-top and track-rail heights; note swage lines (the lockup must sit within one flat field, or across a shallow swage only with a physical proof).</li>
      <li>Confirm the fuel-flap side and the number of sliding doors on the actual vehicle.</li></ul></div>
  </div>
  {foot()}
</section>'''

def rear_page(n):
    # rear elevation, 1:10. width 2000, y 0..2000 ground.
    van = ('<path class="body" d="M0,160 Q0,0 160,0 L1840,0 Q2000,0 2000,160 L2000,1480 L2000,1620 L0,1620 Z"/>'
           '<rect class="tyre" x="150" y="1560" width="260" height="440" rx="40"/><rect class="tyre" x="1590" y="1560" width="260" height="440" rx="40"/>'
           '<rect class="bumper" x="0" y="1480" width="2000" height="140"/>'
           '<path class="gap" d="M130,80 L130,1480 M985,80 L985,1480 M1015,80 L1015,1480 M1870,80 L1870,1480 M130,80 L1870,80"/>'
           '<rect class="lamp" x="25" y="700" width="90" height="550" rx="25"/><rect class="lamp" x="1885" y="700" width="90" height="550" rx="25"/>'
           '<rect class="lamp" x="900" y="40" width="200" height="30" rx="10"/>'
           '<rect class="handle" x="935" y="1000" width="40" height="120" rx="12"/><rect class="handle" x="1025" y="1000" width="40" height="120" rx="12"/>'
           '<rect class="plate" x="330" y="1300" width="440" height="110"/><text class="lab" x="550" y="1370" font-size="40" text-anchor="middle">number plate</text>'
           '<circle class="sensor" cx="300" cy="1550" r="14"/><circle class="sensor" cx="800" cy="1550" r="14"/><circle class="sensor" cx="1200" cy="1550" r="14"/><circle class="sensor" cx="1700" cy="1550" r="14"/>'
           '<rect class="sensor" x="985" y="1430" width="30" height="30"/>')
    livery = (art(LOCK, 650, 350, 700, 340.07)
              + f'<text class="contact" x="1000" y="815" font-size="75.6" text-anchor="middle">{{{{company.phone}}}}</text>'
              + f'<text class="contact" x="1000" y="885" font-size="57.7" text-anchor="middle">{{{{company.domain}}}}</text>'
              + '<rect class="zone" x="650" y="760" width="700" height="135.5"/>')
    t = 32
    dims = (hdim(650, 1350, 320, "700 (lockup, split at the door gap)", t=t) + vdim(-120, 0, 350, "350 from roof", t=t) + ext(0, 350, -120, 350) + ext(0, 0, -120, 0)
            + vdim(1480, 350, 690, "340", left=False, t=t) + ext(1350, 690, 1480, 690) + ext(1350, 350, 1480, 350)
            + vdim(1480, 760, 895.5, "136 contact block", left=False, t=t) + ext(1350, 760, 1480, 760) + ext(1350, 895.5, 1480, 895.5)
            + vdim(560, 690, 760, "70", t=t) + ext(650, 690, 560, 690) + ext(650, 760, 560, 760)
            + hdim(0, 2000, -100, "2000 overall width (placeholder)", t=t) + ext(0, -40, 0, -140) + ext(2000, -40, 2000, -140)
            + hdim(130, 985, 1460, "855 door", above=False, t=t) + hdim(1015, 1870, 1460, "855 door", above=False, t=t)
            + lab(1000, 1000, "door gap 20: cut artwork on the gap, wrap 10 mm into the shut line only with a proof", 30, "middle")
            + lab(1000, 1560, "parking sensors and reversing camera: keep clear 60", 30, "middle", "keeplab")
            + lab(1000, 1240, "number plate, lamps and high-level brake lamp: keep clear 50", 30, "middle", "keeplab"))
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-320 -220 2250 2320" class="rear"><line class="ground" x1="-300" y1="2000" x2="2250" y2="2000"/>{van}{livery}{dims}{scalebar(-300, 2120, 32)}</svg>'
    return f'''
<section class="page" data-trim="420 x 297 mm" aria-label="Rear doors">
  {head("Vehicle livery layout", "Rear doors", "V01", n, "Scale 1:10 on A3; verify on vehicle survey")}
  <div class="drawing rear-wrap">{svg}</div>
  <aside class="side-notes">
    <h3>Elements</h3>
    <ul><li>Rear lockup: primary logo with strapline, 700 x 340 mm, centred on the vehicle centre line across both doors, top edge 350 mm below the roof line. File GBS_HORIZON_VAN_REAR-LOCKUP_700MM_SAGE-RED_v1.0.svg.</li>
    <li>Contact block: phone (55 mm cap height) over web address (42 mm cap height), Inter SemiBold, centred, 70 mm below the strapline. File GBS_HORIZON_VAN_REAR-CONTACT_700MM_SAGE_v1.0.svg (outlined).</li>
    <li>No bars graphic and no descriptor repeat on the rear: the lockup already carries them.</li></ul>
    <h3>Door split</h3>
    <p>Cut the artwork at the door gap on a named cut layer. The split falls through the lockup; align both halves with the doors shut and check from 5 m. Where a door has a glazed window, move the block below the glass and re-dimension.</p>
    <h3>Keep clear</h3>
    <p>Number plate and plate lamp, rear lamp clusters, high-level brake lamp, wiper, camera, parking sensors, door handles and lock barrels, rear step. Nothing on the bumper.</p>
    <h3>Survey</h3>
    <p>Confirm door widths, glazing, hinge-side trim, the plate position and whether the doors are 180 or 250 degree opening with external hinges (keep 40 mm clear of hinge plates).</p>
  </aside>
  {foot()}
</section>'''

def front_page(n):
    van = ('<path class="body" d="M0,1200 L100,760 Q130,700 200,700 L200,700 Q250,160 400,120 L1600,120 Q1750,160 1800,700 L1800,700 Q1870,700 1900,760 L2000,1200 L2000,1620 L0,1620 Z"/>'
           '<rect class="tyre" x="150" y="1560" width="260" height="440" rx="40"/><rect class="tyre" x="1590" y="1560" width="260" height="440" rx="40"/>'
           '<polygon class="glass" points="260,700 400,160 1600,160 1740,700"/>'
           '<path class="gap" d="M200,700 L1800,700"/><path class="gap" d="M230,1010 L1770,1010"/>'
           '<rect class="grille" x="400" y="1040" width="1200" height="150" rx="20"/>'
           '<rect class="lamp" x="90" y="900" width="320" height="130" rx="30"/><rect class="lamp" x="1590" y="900" width="320" height="130" rx="30"/>'
           '<rect class="bumper" x="0" y="1200" width="2000" height="420"/>'
           '<rect class="plate" x="780" y="1300" width="440" height="110"/><text class="lab" x="1000" y="1370" font-size="40" text-anchor="middle">number plate</text>'
           '<rect class="grille" x="300" y="1440" width="1400" height="120" rx="20"/>'
           '<circle class="sensor" cx="300" cy="1250" r="14"/><circle class="sensor" cx="800" cy="1250" r="14"/><circle class="sensor" cx="1200" cy="1250" r="14"/><circle class="sensor" cx="1700" cy="1250" r="14"/>'
           '<rect class="sensor" x="960" y="200" width="80" height="60"/>'
           '<rect class="handle" x="1000" y="1080" width="0" height="0"/>')
    livery = art(ICON, 875, 760, 250, 207.03)
    t = 32
    dims = (hdim(875, 1125, 730, "250 icon, centred", t=t) + vdim(1300, 760, 967, "207", left=False, t=t) + ext(1125, 760, 1300, 760) + ext(1125, 967, 1300, 967)
            + vdim(-120, 0, 760, "760 from roof (this elevation)", t=t) + ext(400, 120, -120, 120) + ext(200, 760, -120, 760)
            + hdim(0, 2000, -100, "2000 overall width (placeholder)", t=t) + ext(0, -40, 0, -140) + ext(2000, -40, 2000, -140)
            + lab(1000, 1070, "bonnet shut line and grille: keep clear 50 (nothing on the grille or badge)", 30, "middle", "keeplab")
            + lab(1000, 300, "windscreen, wiper park, sensor pod behind the mirror: keep clear", 30, "middle", "keeplab")
            + lab(1000, 1480, "no graphics on the bumper, lamps or plate", 30, "middle", "keeplab")
            + lab(1000, 560, "bonnet emblem: icon only, never the lockup", 30, "middle"))
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-320 -220 2250 2320" class="rear"><line class="ground" x1="-300" y1="2000" x2="2250" y2="2000"/>{van}{livery}{dims}{scalebar(-300, 2120, 32)}</svg>'
    return f'''
<section class="page" data-trim="420 x 297 mm" aria-label="Front and bonnet">
  {head("Vehicle livery layout", "Front and bonnet", "V01", n, "Scale 1:10 on A3; verify on vehicle survey")}
  <div class="drawing rear-wrap">{svg}</div>
  <aside class="side-notes">
    <h3>Element</h3>
    <ul><li>Bonnet emblem: icon only (sage/red), 250 x 207 mm, centred on the bonnet, 150 mm back from the leading edge measured along the panel; this elevation foreshortens the bonnet, so set out on the panel, not from the drawing. File GBS_HORIZON_VAN_BONNET-ICON_250MM_SAGE-RED_v1.0.svg.</li>
    <li>This is the most that goes on the bonnet. No lockup, descriptor, strapline or contact details on the front.</li></ul>
    <h3>Keep clear</h3>
    <p>Manufacturer badge (100 mm), bonnet shut line, grille, headlamps, washer jets, windscreen and wiper park, the camera and sensor pod behind the mirror, front parking sensors, the number plate and the whole bumper.</p>
    <h3>Note on the hinge line</h3>
    <p>Where the bonnet has a central swage or a raised power bulge, place the icon on the flat field to one side (driver side preferred) and record the offset on the survey sheet; otherwise omit the bonnet emblem rather than bridge a crease.</p>
    <h3>Survey</h3>
    <p>Measure the flat bonnet field and the badge position; photograph with a tape in shot.</p>
  </aside>
  {foot()}
</section>'''

def notes_page(n):
    return f'''
<section class="page" data-trim="420 x 297 mm" aria-label="Fabrication notes">
  {head("Vehicle livery layout", "Fabrication notes and schedule", "V01", n, "Read with the production manual, section 06")}
  <div class="fab">
    <div class="col">
      <h3>Materials</h3>
      <ul><li>Cast polymeric vinyl (not calendered) for every element, with a matching cast laminate over all printed vinyl. Cut-vinyl lettering and bars in cast coloured film; no laminate needed on single-colour cut film unless the installer specifies it.</li>
      <li>Colours: sage and red to the approved physical swatches (manual section 02). Supply draw-downs of the proposed films for sign-off before cutting; the digital values are provisional.</li>
      <li>Finish: gloss or satin to match across all elements on one vehicle. No chrome, metallic, reflective or textured films.</li></ul>
      <h3>Artwork</h3>
      <ul><li>All panels are supplied as SVG at full vehicle scale, one millimetre per user unit, with the logo as outlined paths. Text panels (contact row and contact block) are already outlined from Inter SemiBold; if any text is re-set, outline it to paths before cutting and keep the font files (00_BRAND_CORE/fonts) out of the cut file.</li>
      <li>Keep the logo proportions, colour split and clear space exactly as supplied. Do not add keylines, shadows, gradients, rules or a white backing shape on a white vehicle.</li>
      <li>Place cut contours on named layers: LOGO, CONTACT, BARS, CUT-DOOR-GAP, KEEP-CLEAR. Regmarks on a separate layer. Report nest sizes and the number of pieces with the quote.</li>
      <li>Minimum cut-vinyl stroke 3 mm; the descriptor and strapline cut as one piece per word, with application tape.</li></ul>
    </div>
    <div class="col">
      <h3>Vehicle and survey</h3>
      <ul><li>Vehicle: white medium-wheelbase high-roof panel van (Transit Custom / Vivaro class). Every dimension on these sheets is a placeholder from a generic 5300 x 2000 mm elevation; nothing is cut until the survey sheet has real measurements, photographs with a tape in shot and the panel map.</li>
      <li>Record: panel widths between gaps, swage lines, roof line, sill, wheel-arch tops, sliding-door track rails and travel, fuel-flap side, lamp wrap-around, sensors, cameras, plate position, glazing.</li>
      <li>Keep clear of lamps, number plates, sensors, cameras, wipers, washer jets, badges, handles, locks, rubbing strips and all door gaps. Nothing on bumpers or glass.</li></ul>
      <h3>Proof and installation</h3>
      <ul><li>First vehicle: full-size paper or low-tack proof of the side lockup and the rear doors on the vehicle, photographed from 5 m and 15 m and signed off by the GBS Director before vinyl is cut.</li>
      <li>Apply dry on a clean, degreased, dry panel at the film manufacturer's temperature range. Post-heat edges and any recess as specified. Replicate the nearside layout on the offside as a mirror of position, never of the artwork.</li>
      <li>Hand over a photo set (both sides, rear, front, close-ups), the film batch numbers and the aftercare note (no pressure washing closer than 300 mm, no jet washing of edges for 7 days).</li></ul>
    </div>
    <div class="col">
      <h3>Schedule of elements</h3>
      <table>
        <tr><th>Element</th><th>Size (mm)</th><th>Position</th><th>File</th></tr>
        <tr><td>Side lockup (x2)</td><td class="num">1400 x 680</td><td>Rear load panel, 300 below roof line, 350 from rear corner</td><td>GBS_HORIZON_VAN_SIDE-LOCKUP_1400MM_SAGE-RED_v1.0.svg</td></tr>
        <tr><td>Side contact row (x2)</td><td class="num">1300 x 75</td><td>60 below strapline, aligned to lockup</td><td>GBS_HORIZON_VAN_SIDE-CONTACT_1300MM_SAGE_v1.0.svg</td></tr>
        <tr><td>Rear-quarter bars (x2)</td><td class="num">145 x 460</td><td>Bottom on sill line, 155 from rear corner</td><td>GBS_HORIZON_VAN_REAR-QUARTER-BARS_460MM_SAGE-RED_v1.0.svg</td></tr>
        <tr><td>Rear lockup</td><td class="num">700 x 340</td><td>Centred across both doors, 350 below roof line</td><td>GBS_HORIZON_VAN_REAR-LOCKUP_700MM_SAGE-RED_v1.0.svg</td></tr>
        <tr><td>Rear contact block</td><td class="num">700 x 136</td><td>Centred, 70 below strapline</td><td>GBS_HORIZON_VAN_REAR-CONTACT_700MM_SAGE_v1.0.svg</td></tr>
        <tr><td>Bonnet emblem</td><td class="num">250 x 207</td><td>Centred on bonnet, 150 from leading edge</td><td>GBS_HORIZON_VAN_BONNET-ICON_250MM_SAGE-RED_v1.0.svg</td></tr>
      </table>
      <p class="small">Preview: GBS_HORIZON_VAN_SIDE-LOCKUP-PREVIEW-1-10_140MM_SAGE-RED_v1.0.png (300 dpi, 1:10). Contact details on every element come from company.json; the phone number shown is the one verified line.</p>
    </div>
  </div>
  {foot()}
</section>'''

def head(eyebrow, title, code, n, scale):
    return f'''<header class="head">
    <div class="logo"><img src="{L}GBS_HORIZON_LOGO_PRIMARY-NOSTRAP_SAGE-RED_v1.0.svg" alt="GBS Property Maintenance"></div>
    <div class="title"><span class="eyebrow">{eyebrow}</span><h1>{title}</h1><div class="scale">{scale}</div></div>
    <div class="meta"><span class="num">{code}</span><br>Sheet {n} of 5<br>v1.0</div>
  </header>
  <div class="head-rule"></div>'''
def foot():
    return '<footer class="foot"><span>White van. All vehicle dimensions are placeholders until the actual vehicle is surveyed. Full-scale mm throughout. Primary logo (sage/red) on white; red is an accent only.</span><span>{{company.tradingName}} &middot; {{company.domain}} &middot; {{company.phone}}</span></footer>'

CSS = '''
  :root { --trim-w: 420mm; --trim-h: 297mm; }
  .head { position: absolute; left: 14mm; right: 14mm; top: 10mm; height: 18mm; display: flex; align-items: flex-end; gap: 10mm; }
  .head .logo { width: 40mm; flex: none; } .head .logo img { width: 100%; display: block; }
  .head .title { flex: 1; } .head .title .eyebrow { display: block; margin-bottom: 1mm; }
  .head h1 { font-size: 17pt; font-weight: 700; } .head .scale { font-size: 8pt; color: var(--gbs-ink-soft); margin-top: 1mm; }
  .head .meta { text-align: right; font-size: 8pt; line-height: 1.4; color: var(--gbs-ink-soft); }
  .head-rule { position: absolute; left: 14mm; right: 14mm; top: 31mm; height: 0.5pt; background: var(--gbs-sage); }
  .head-rule::after { content: ""; position: absolute; right: 0; top: -1.5pt; width: 18mm; height: 2pt; background: var(--gbs-red); }
  .drawing { position: absolute; left: 14mm; top: 34mm; }
  .side-wrap svg { width: 409.3mm; height: 161.3mm; display: block; }   /* 6140 x 2420 mm at 1:15 */
  .side-wrap { left: 6mm; }
  .rear-wrap svg { width: 225mm; height: 232mm; display: block; }       /* 2250 x 2320 mm at 1:10 */
  .body { fill: #fff; stroke: var(--gbs-ink); stroke-width: 6; stroke-linejoin: round; }
  .tyre { fill: #3a3f3c; stroke: none; } .rim { fill: #DADADA; stroke: #fff; stroke-width: 6; }
  .glass { fill: #E8ECE9; stroke: var(--gbs-ink); stroke-width: 4; }
  .gap { fill: none; stroke: var(--gbs-ink-soft); stroke-width: 4; }
  .handle { fill: #fff; stroke: var(--gbs-ink-soft); stroke-width: 4; }
  .lamp { fill: #F2F2F0; stroke: var(--gbs-ink-soft); stroke-width: 4; }
  .bumper { fill: #EDEDEB; stroke: var(--gbs-ink); stroke-width: 6; } .grille { fill: #D3DAD5; stroke: var(--gbs-ink-soft); stroke-width: 4; }
  .plate { fill: #F9F9F7; stroke: var(--gbs-ink-soft); stroke-width: 4; } .sensor { fill: #fff; stroke: var(--gbs-red); stroke-width: 4; }
  .flap { fill: #fff; stroke: var(--gbs-ink-soft); stroke-width: 4; stroke-dasharray: 20 14; }
  .keep { fill: none; stroke: var(--gbs-red); stroke-width: 4; stroke-dasharray: 30 18; }
  .ground { stroke: var(--gbs-light); stroke-width: 6; }
  .zone { fill: none; stroke: var(--gbs-red); stroke-width: 3; stroke-dasharray: 24 16; }
  .bar-sage { fill: var(--gbs-sage); } .bar-red { fill: var(--gbs-red); }
  .contact { font-family: var(--font-body); font-weight: 600; fill: var(--gbs-sage); }
  .dim line { stroke: var(--gbs-ink-soft); stroke-width: 4; } .dim text { font-family: var(--font-body); font-weight: 500; fill: var(--gbs-ink); }
  .ext { stroke: var(--gbs-light); stroke-width: 4; }
  .lab { font-family: var(--font-body); font-weight: 500; fill: var(--gbs-ink-soft); } .keeplab { font-family: var(--font-body); font-weight: 500; fill: var(--gbs-red); }
  .notes-row { position: absolute; left: 14mm; right: 14mm; top: 200mm; bottom: 20mm; display: flex; gap: 8mm; font-size: 8pt; line-height: 1.4; }
  .notes-row > div { flex: 1; min-width: 0; }
  .notes-row h3, .side-notes h3, .fab h3 { font-size: 8.5pt; text-transform: uppercase; letter-spacing: 0.08em; margin: 0 0 1.2mm; }
  .notes-row ul, .side-notes ul, .fab ul { margin: 0 0 2.5mm; padding-left: 3.5mm; } li { margin-bottom: 0.8mm; }
  .side-notes { position: absolute; left: 250mm; right: 14mm; top: 36mm; bottom: 20mm; font-size: 8.2pt; line-height: 1.42; }
  .side-notes p { margin: 0 0 2.5mm; }
  .fab { position: absolute; left: 14mm; right: 14mm; top: 36mm; bottom: 20mm; display: flex; gap: 9mm; font-size: 8.2pt; line-height: 1.42; }
  .fab .col { flex: 1; min-width: 0; } .fab .col:last-child { flex: 1.25; }
  .fab table { width: 100%; border-collapse: collapse; font-size: 7.4pt; margin-bottom: 3mm; }
  .fab th { text-align: left; font-family: var(--font-heading); font-weight: 600; color: var(--gbs-sage); border-bottom: 0.5pt solid var(--gbs-sage); padding: 0.8mm 1.5mm 0.8mm 0; }
  .fab td { border-bottom: 0.5pt solid var(--gbs-light); padding: 0.8mm 1.5mm 0.8mm 0; vertical-align: top; word-break: break-all; }
  .fab .small { font-size: 7.4pt; color: var(--gbs-ink-soft); }
  .foot { position: absolute; left: 14mm; right: 14mm; bottom: 10mm; display: flex; justify-content: space-between; gap: 10mm; font-size: 7pt; color: var(--gbs-ink-soft); border-top: 0.5pt solid var(--gbs-light); padding-top: 1.5mm; }
'''
html = f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<title>GBS_HORIZON_VAN_LIVERY-LAYOUT_A3L</title>
<link rel="stylesheet" href="../00_BRAND_CORE/tokens.css">
<link rel="stylesheet" href="../00_BRAND_CORE/fonts.css">
<link rel="stylesheet" href="../03_PRINT/_shared/print-base.css">
<style>{CSS}</style>
</head>
<body>
{side_page(True, 1)}
{side_page(False, 2)}
{rear_page(3)}
{front_page(4)}
{notes_page(5)}
</body>
</html>
'''
open(OUT, "w").write(html); print("wrote", OUT, len(html))
