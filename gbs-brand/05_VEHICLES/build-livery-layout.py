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
    b = [(41, 460, "sage", 30), (40, 373, "red", 46), (44, 270, "sage", 0)]; out = ""; cx = x
    for w, h, c, g in b: out += f'<rect class="bar-{c}" x="{cx}" y="{y_bottom-h}" width="{w}" height="{h}"/>'; cx += w + g
    return out
def scalebar(x, y, t=45):
    return (f'<g class="dim"><rect x="{x}" y="{y}" width="500" height="{t*0.5}" fill="#4C5D50"/><rect x="{x+500}" y="{y}" width="500" height="{t*0.5}" fill="#fff" stroke="#4C5D50" stroke-width="{t*0.08}"/>'
            f'<text x="{x}" y="{y+t*1.4}" text-anchor="middle" font-size="{t*0.8}">0</text><text x="{x+500}" y="{y+t*1.4}" text-anchor="middle" font-size="{t*0.8}">500</text><text x="{x+1000}" y="{y+t*1.4}" text-anchor="middle" font-size="{t*0.8}">1000 mm</text></g>')

# ---------------- side elevation geometry (full-scale mm, y down, ground = 2000) ----------------
BODY = ("M160,1820 L60,1700 L0,1450 L0,1260 L60,1180 L240,1130 L1000,1010 L1170,960 L1860,170 Q1960,70 2080,65 L5240,65 Q5320,65 5331,160 "
        "L5331,1560 L5331,1760 L5280,1820 L4629,1820 A440,440 0 0 0 3749,1820 L1354,1820 A440,440 0 0 0 474,1820 L300,1820 Z")
COMMON = (f'<path class="body" d="{BODY}"/>'
          '<circle class="tyre" cx="914" cy="1655" r="345"/><circle class="rim" cx="914" cy="1655" r="200"/><circle class="tyre" cx="4189" cy="1655" r="345"/><circle class="rim" cx="4189" cy="1655" r="200"/>'
          '<polygon class="glass" points="1210,940 1830,215 1955,215 1335,940"/>'
          '<polygon class="glass" points="1370,940 2380,940 2380,350 2050,350"/>'
          '<path class="gap" d="M1180,1820 L1180,1180 L1345,940"/><path class="gap" d="M2400,350 L2400,1820"/><path class="gap" d="M2050,300 L5250,300"/>'
          '<path class="gap" d="M2400,950 L5230,950"/><path class="gap" d="M300,1700 L5280,1700"/>'
          '<rect class="handle" x="2180" y="1040" width="170" height="45" rx="20"/><rect class="handle" x="1250" y="500" width="90" height="180" rx="15"/>'
          '<rect class="lamp" x="5230" y="800" width="80" height="500" rx="20"/>')
NEARSIDE_EXTRA = ('<path class="gap" d="M3650,350 L3650,1820"/><rect class="handle" x="3420" y="1040" width="170" height="45" rx="20"/>'
                  '<rect class="keep" x="3650" y="250" width="1400" height="90"/>')
OFFSIDE_EXTRA = '<rect class="flap" x="2560" y="1050" width="180" height="180" rx="20"/>'  # fuel flap on the offside rear quarter (mirrored coordinates)

def side_page(nearside, n):
    title = "Nearside elevation (passenger side, sliding door)" if nearside else "Offside elevation (driver side)"
    if nearside:
        van = f'<g id="van">{COMMON}{NEARSIDE_EXTRA}</g>'
        lx, rx = 3590, 4990   # lockup x range: centred on the panel between the sliding-door rear edge (3650) and the rear corner (5331)
        cx = 4290
        dims = (ext(lx, 315, lx, 1250) + ext(rx, 315, rx, 1250) + hdim(lx, rx, 1220, "1400 (lockup width)", above=False)
                + ext(3650, 1660, 3650, 1760) + ext(lx, 1660, lx, 1760) + hdim(3650, lx, 1740, "340 from sliding-door edge", above=False)
                + ext(rx, 1660, rx, 1760) + ext(5331, 1660, 5331, 1760) + hdim(rx, 5331, 1740, "341 to rear corner", above=False)
                + vdim(5450, 65, 315, "250", left=False) + ext(5300, 315, 5450, 315) + ext(5300, 65, 5450, 65)
                + vdim(3450, 315, 869, "554 (lockup height)") + vdim(3450, 1010, 1085, "75 contact row")
                + ext(3640, 1010, 3450, 1010) + ext(3640, 1085, 3450, 1085)
                + lab(4350, 300, "sliding-door upper track rail: keep clear 90", 36, "middle", "keeplab")
                + lab(4290, 985, "body crease, about 1050 above ground: nothing crosses it", 34, "middle", "keeplab")
                + lab(2660, 1340, "full-scale mm; Citroën Dispatch XL (2026) published dimensions, panel shapes approximate until the vehicle survey", 36, "middle")
                + hdim(0, 5331, -120, "5331 overall length") + vdim(-150, 65, 2000, "1935 overall height")
                + ext(0, -40, 0, -160) + ext(5331, -40, 5331, -160) + ext(-60, 65, -200, 65) + ext(-60, 2000, -200, 2000)
                + hdim(914, 4189, 1900, "3275 wheelbase", above=False, t=42)
                + vdim(5450, 1320, 1780, "460 bars", left=False) + ext(5190, 1320, 5450, 1320) + ext(5190, 1780, 5450, 1780))
        livery = (art(LOCK, lx, 315, 1400, 554.34)
                  + f'<text class="contact" x="3640" y="1070" font-size="82.5">{{{{company.domain}}}}</text><text class="contact" x="4940" y="1070" font-size="82.5" text-anchor="end">{{{{company.phone}}}}</text>'
                  + f'<rect class="zone" x="3640" y="1010" width="1300" height="75"/>'
                  + bars(4975, 1780))
    else:
        van = f'<g id="van" transform="translate(5331,0) scale(-1,1)">{COMMON}</g>' + OFFSIDE_EXTRA
        lx, rx = 341, 1741
        dims = (ext(lx, 315, lx, 1250) + ext(rx, 315, rx, 1250) + hdim(lx, rx, 1220, "1400 (lockup width)", above=False)
                + ext(0, 1660, 0, 1760) + ext(lx, 1660, lx, 1760) + hdim(0, lx, 1740, "341 to rear corner", above=False)
                + ext(rx, 1660, rx, 1760) + ext(2931, 1660, 2931, 1760) + hdim(rx, 2931, 1740, "1190 to B-pillar", above=False)
                + vdim(-150, 65, 315, "250") + ext(30, 315, -150, 315) + ext(30, 65, -150, 65)
                + vdim(1850, 315, 869, "554 (lockup height)", left=False) + vdim(1850, 1010, 1085, "75 contact row", left=False)
                + ext(1700, 1010, 1850, 1010) + ext(1700, 1085, 1850, 1085)
                + lab(2650, 1000, "fuel flap: keep clear 100", 36, "middle", "keeplab")
                + lab(1041, 985, "body crease, about 1050 above ground: nothing crosses it", 34, "middle", "keeplab")
                + lab(2660, 1340, "full-scale mm; Citroën Dispatch XL (2026) published dimensions, panel shapes approximate until the vehicle survey", 36, "middle")
                + hdim(0, 5331, -120, "5331 overall length") + vdim(5450, 65, 2000, "1935 overall height", left=False)
                + ext(0, -40, 0, -160) + ext(5331, -40, 5331, -160) + ext(5371, 65, 5450, 65) + ext(5371, 2000, 5450, 2000)
                + hdim(1142, 4417, 1900, "3275 wheelbase", above=False, t=42)
                + vdim(-150, 1320, 1780, "460 bars") + ext(155, 1320, -150, 1320) + ext(155, 1780, -150, 1780))
        livery = (art(LOCK, lx, 315, 1400, 554.34)
                  + f'<text class="contact" x="391" y="1070" font-size="82.5">{{{{company.domain}}}}</text><text class="contact" x="1691" y="1070" font-size="82.5" text-anchor="end">{{{{company.phone}}}}</text>'
                  + f'<rect class="zone" x="391" y="1010" width="1300" height="75"/>'
                  + bars(155, 1780))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-420 -260 6140 2420" class="side">'
           f'<line class="ground" x1="-300" y1="2000" x2="5600" y2="2000"/>{van}{livery}{dims}{scalebar(-300, 2120)}</svg>')
    return f'''
<section class="page" data-trim="420 x 297 mm" aria-label="{title}">
  {head("Vehicle livery layout", title, "V01", n, "Scale 1:15 on A3 (a 5.3 m van does not fit A3 at 1:10); verify on vehicle survey")}
  <div class="drawing side-wrap">{svg}</div>
  <div class="notes-row">
    <div><h3>Elements on this side</h3>
      <ul><li>Side lockup: primary logo with strapline, 1400 x 554 mm, centred on the rear load panel at 4290 mm from the front (340 mm behind the {'sliding-door rear edge' if nearside else 'equivalent line'}, 341 mm from the rear corner), top edge 250 mm below the roof line, above the body crease. File GBS_HORIZON_VAN_SIDE-LOCKUP_1400MM_SAGE-RED_v1.0.svg.</li>
      <li>Contact row: web address left, phone right, Inter SemiBold, 60 mm cap height, 1300 mm between outer edges, 60 mm below the body crease, aligned to the lockup. File GBS_HORIZON_VAN_SIDE-CONTACT_1300MM_SAGE_v1.0.svg (outlined).</li>
      <li>Rear-quarter bars: 201 x 460 mm, bottom edge on the sill line, 155 mm from the rear corner. File GBS_HORIZON_VAN_REAR-QUARTER-BARS_460MM_SAGE-RED_v1.0.svg.</li></ul></div>
    <div><h3>Keep clear</h3>
      <ul><li>Door gaps, handles, the {'sliding-door upper track rail (100 mm band below the gutter)' if nearside else 'fuel flap (100 mm all round)'} and the sliding-door travel: no graphic may bridge a gap or sit on a rail.</li>
      <li>Rear lamp wrap-around, side repeater, side sensors and any camera. 50 mm minimum to any panel edge, swage line or rubbing strip.</li>
      <li>Body crease at about 1050 mm above ground: the lockup sits above it and the contact row below it; nothing crosses it. Wheel-arch flare: nothing below the arch-top line (1380 on the drawing) within 500 mm of the rear axle.</li></ul></div>
    <div><h3>Survey before cutting</h3>
      <ul><li>Measure the real panel between the sliding-door rear edge and the rear corner; recentre the lockup on that panel and scale to 1300-1400 mm so that at least 150 mm remains above and below.</li>
      <li>Record roof-line, sill, arch-top and track-rail heights; note swage lines (the lockup must sit within one flat field, or across a shallow swage only with a physical proof).</li>
      <li>Confirm the fuel-flap side and the number of sliding doors on the actual vehicle.</li></ul></div>
  </div>
  {foot()}
</section>'''

def rear_page(n):
    # rear elevation, 1:10. Dispatch XL: 1920 wide, 1935 high (roof at y 65), ground at 2000.
    van = ('<path class="body" d="M0,220 Q0,65 140,65 L1780,65 Q1920,65 1920,220 L1920,1560 L1920,1800 L0,1800 Z"/>'
           '<rect class="tyre" x="150" y="1560" width="250" height="440" rx="40"/><rect class="tyre" x="1520" y="1560" width="250" height="440" rx="40"/>'
           '<rect class="bumper" x="0" y="1600" width="1920" height="200"/>'
           '<path class="gap" d="M100,140 L100,1600 M950,140 L950,1600 M970,140 L970,1600 M1820,140 L1820,1600 M100,140 L1820,140"/>'
           '<rect class="lamp" x="20" y="750" width="80" height="520" rx="25"/><rect class="lamp" x="1820" y="750" width="80" height="520" rx="25"/>'
           '<rect class="lamp" x="860" y="85" width="200" height="30" rx="10"/>'
           '<rect class="handle" x="985" y="1000" width="40" height="120" rx="12"/>'
           '<rect class="plate" x="310" y="1340" width="440" height="110"/><text class="lab" x="530" y="1410" font-size="40" text-anchor="middle">number plate</text>'
           '<circle class="sensor" cx="300" cy="1700" r="14"/><circle class="sensor" cx="760" cy="1700" r="14"/><circle class="sensor" cx="1160" cy="1700" r="14"/><circle class="sensor" cx="1620" cy="1700" r="14"/>'
           '<rect class="sensor" x="945" y="1470" width="30" height="30"/>')
    livery = (art(LOCK, 610, 415, 700, 277.17)
              + f'<text class="contact" x="960" y="817" font-size="75.6" text-anchor="middle">{{{{company.phone}}}}</text>'
              + f'<text class="contact" x="960" y="887" font-size="57.7" text-anchor="middle">{{{{company.domain}}}}</text>'
              + '<rect class="zone" x="610" y="762" width="700" height="135.5"/>')
    t = 32
    dims = (hdim(610, 1310, 385, "700 (lockup, split at the door gap)", t=t) + vdim(-120, 65, 415, "350 from roof", t=t) + ext(0, 415, -120, 415) + ext(0, 65, -120, 65)
            + vdim(1440, 415, 692, "277", left=False, t=t) + ext(1310, 692, 1440, 692) + ext(1310, 415, 1440, 415)
            + vdim(1440, 762, 897.5, "136 contact block", left=False, t=t) + ext(1310, 762, 1440, 762) + ext(1310, 897.5, 1440, 897.5)
            + vdim(520, 692, 762, "70", t=t) + ext(610, 692, 520, 692) + ext(610, 762, 520, 762)
            + hdim(0, 1920, -100, "1920 overall width", t=t) + ext(0, -40, 0, -140) + ext(1920, -40, 1920, -140)
            + hdim(100, 950, 1530, "850 door", above=False, t=t) + hdim(970, 1820, 1530, "850 door", above=False, t=t)
            + lab(960, 1180, "door gap 20: cut artwork on the gap, wrap 10 mm into the shut line only with a proof", 30, "middle")
            + lab(960, 1760, "parking sensors and reversing camera: keep clear 60", 30, "middle", "keeplab")
            + lab(960, 1300, "number plate, lamps and high-level brake lamp: keep clear 50", 30, "middle", "keeplab"))
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-320 -220 2250 2320" class="rear"><line class="ground" x1="-300" y1="2000" x2="2250" y2="2000"/>{van}{livery}{dims}{scalebar(-300, 2120, 32)}</svg>'
    return f'''
<section class="page" data-trim="420 x 297 mm" aria-label="Rear doors">
  {head("Vehicle livery layout", "Rear doors", "V01", n, "Scale 1:10 on A3; verify on vehicle survey")}
  <div class="drawing rear-wrap">{svg}</div>
  <aside class="side-notes">
    <h3>Elements</h3>
    <ul><li>Rear lockup: primary logo with strapline, 700 x 277 mm, centred on the vehicle centre line across both doors, top edge 350 mm below the roof line. File GBS_HORIZON_VAN_REAR-LOCKUP_700MM_SAGE-RED_v1.0.svg.</li>
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
    # front elevation, 1:10. Dispatch XL facelift: 1920 wide, roof at y 65, ground at 2000.
    van = ('<path class="body" d="M0,1250 L90,860 Q120,800 200,800 Q230,250 400,100 Q440,65 500,65 L1420,65 Q1480,65 1520,100 Q1690,250 1720,800 Q1800,800 1830,860 L1920,1250 L1920,1800 L0,1800 Z"/>'
           '<rect class="tyre" x="150" y="1560" width="250" height="440" rx="40"/><rect class="tyre" x="1520" y="1560" width="250" height="440" rx="40"/>'
           '<polygon class="glass" points="250,790 410,180 1510,180 1670,790"/>'
           '<path class="gap" d="M200,800 L1720,800"/><path class="gap" d="M230,1060 L1690,1060"/>'
           '<rect class="grille" x="300" y="1060" width="1320" height="170" rx="30"/>'
           '<rect class="lamp" x="110" y="930" width="310" height="90" rx="30"/><rect class="lamp" x="1500" y="930" width="310" height="90" rx="30"/>'
           '<rect class="bumper" x="0" y="1250" width="1920" height="550"/>'
           '<rect class="plate" x="740" y="1320" width="440" height="110"/><text class="lab" x="960" y="1390" font-size="40" text-anchor="middle">number plate</text>'
           '<rect class="grille" x="330" y="1480" width="1260" height="140" rx="20"/>'
           '<circle class="sensor" cx="300" cy="1270" r="14"/><circle class="sensor" cx="760" cy="1270" r="14"/><circle class="sensor" cx="1160" cy="1270" r="14"/><circle class="sensor" cx="1620" cy="1270" r="14"/>'
           '<rect class="sensor" x="920" y="220" width="80" height="60"/>')
    livery = art(ICON, 835, 835, 250, 187.07)
    t = 32
    dims = (hdim(835, 1085, 790, "250 icon, centred", t=t) + vdim(1260, 835, 1022.07, "187", left=False, t=t) + ext(1085, 835, 1260, 835) + ext(1085, 1022.07, 1260, 1022.07)
            + vdim(-120, 65, 835, "770 from roof (this elevation)", t=t) + ext(500, 65, -120, 65) + ext(200, 835, -120, 835)
            + hdim(0, 1920, -100, "1920 overall width", t=t) + ext(0, -40, 0, -140) + ext(1920, -40, 1920, -140)
            + lab(960, 1045, "bonnet shut line and grille: keep clear 50 (nothing on the grille or badge)", 30, "middle", "keeplab")
            + lab(960, 330, "windscreen, wiper park, sensor pod behind the mirror: keep clear", 30, "middle", "keeplab")
            + lab(960, 1470, "no graphics on the bumper, lamps or plate", 30, "middle", "keeplab")
            + lab(960, 620, "bonnet emblem: icon only, never the lockup", 30, "middle"))
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-320 -220 2250 2320" class="rear"><line class="ground" x1="-300" y1="2000" x2="2250" y2="2000"/>{van}{livery}{dims}{scalebar(-300, 2120, 32)}</svg>'
    return f'''
<section class="page" data-trim="420 x 297 mm" aria-label="Front and bonnet">
  {head("Vehicle livery layout", "Front and bonnet", "V01", n, "Scale 1:10 on A3; verify on vehicle survey")}
  <div class="drawing rear-wrap">{svg}</div>
  <aside class="side-notes">
    <h3>Element</h3>
    <ul><li>Bonnet emblem: icon only (sage/red), 250 x 187 mm, centred on the bonnet, 150 mm back from the leading edge measured along the panel; this elevation foreshortens the bonnet, so set out on the panel, not from the drawing. File GBS_HORIZON_VAN_BONNET-ICON_250MM_SAGE-RED_v1.0.svg.</li>
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
      <ul><li>Vehicle: Citroën Dispatch XL panel van, 2026 model year (third generation, 2024 facelift), white, standard roof. Elevations are drawn to Citroën's published dimensions (5331 x 1920 x 1935 mm, wheelbase 3275 mm); panel shapes, crease and rail positions are approximate. Replace the outline with the manufacturer template (GetOutlines, Citroën Jumpy / Dispatch 3rd generation facelift panel van XL) when purchased, and cut nothing until the survey sheet has real measurements, photographs with a tape in shot and the panel map.</li>
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
        <tr><td>Side lockup (x2)</td><td class="num">1400 x 554</td><td>Rear load panel, 250 below roof line, 341 from rear corner, above the body crease</td><td>GBS_HORIZON_VAN_SIDE-LOCKUP_1400MM_SAGE-RED_v1.0.svg</td></tr>
        <tr><td>Side contact row (x2)</td><td class="num">1300 x 75</td><td>60 below the body crease, aligned to lockup</td><td>GBS_HORIZON_VAN_SIDE-CONTACT_1300MM_SAGE_v1.0.svg</td></tr>
        <tr><td>Rear-quarter bars (x2)</td><td class="num">201 x 460</td><td>Bottom on sill line, 155 from rear corner</td><td>GBS_HORIZON_VAN_REAR-QUARTER-BARS_460MM_SAGE-RED_v1.0.svg</td></tr>
        <tr><td>Rear lockup</td><td class="num">700 x 277</td><td>Centred across both doors, 350 below roof line</td><td>GBS_HORIZON_VAN_REAR-LOCKUP_700MM_SAGE-RED_v1.0.svg</td></tr>
        <tr><td>Rear contact block</td><td class="num">700 x 136</td><td>Centred, 70 below strapline</td><td>GBS_HORIZON_VAN_REAR-CONTACT_700MM_SAGE_v1.0.svg</td></tr>
        <tr><td>Bonnet emblem</td><td class="num">250 x 187</td><td>Centred on bonnet, 150 from leading edge</td><td>GBS_HORIZON_VAN_BONNET-ICON_250MM_SAGE-RED_v1.0.svg</td></tr>
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
    return '<footer class="foot"><span>Citroën Dispatch XL (2026), white. Elevations to published dimensions; panel geometry approximate until the vehicle is surveyed. Full-scale mm throughout. Primary logo (sage/red) on white; red is an accent only.</span><span>{{company.tradingName}} &middot; {{company.domain}} &middot; {{company.phone}}</span></footer>'

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
  .glass { fill: #EEF0EB; stroke: var(--gbs-ink); stroke-width: 4; }
  .gap { fill: none; stroke: var(--gbs-ink-soft); stroke-width: 4; }
  .handle { fill: #fff; stroke: var(--gbs-ink-soft); stroke-width: 4; }
  .lamp { fill: #F2F2F0; stroke: var(--gbs-ink-soft); stroke-width: 4; }
  .bumper { fill: #EDEDEB; stroke: var(--gbs-ink); stroke-width: 6; } .grille { fill: #CDD5CC; stroke: var(--gbs-ink-soft); stroke-width: 4; }
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
