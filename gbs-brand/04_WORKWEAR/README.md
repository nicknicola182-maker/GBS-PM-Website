# 04_WORKWEAR - garment artwork and placement

Transfer and print artwork for GBS Property Maintenance workwear, plus the placement sheet and embroidery brief that go to the garment supplier. Everything here is generated from the logo masters in `01_LOGO_MASTER/svg` by `tools/render.mjs tools/manifests/04_workwear.json`; edit the HTML sources, never the PNGs.

Rules applied (production manual, workwear section): chest marks 85-105 mm wide, back marks 230-280 mm wide, sleeve emblem 35-50 mm high. White garments carry the primary sage/red logo; sage garments carry the reversed off-white/red logo. The strapline is never forced into chest marks (the no-strap lockup is used). Embroidery uses the no-strap lockup and the simplified icon. Hi-vis branding never covers retroreflective tape.

## Files

| File | What it is | Size |
|---|---|---|
| `GBS_HORIZON_WORKWEAR_CHEST_95MM_SAGE-RED_v1.0.png` | Chest mark, primary no-strap lockup, white garments | 95 x 38.24 mm, 300 dpi (1125 x 453 px), transparent |
| `GBS_HORIZON_WORKWEAR_CHEST_95MM_OFFWHITE-RED_v1.0.png` | Chest mark, reversed no-strap lockup, sage garments | 95 x 38.24 mm, 300 dpi, transparent |
| `GBS_HORIZON_WORKWEAR_BACK_260MM_SAGE-RED_v1.0.png` | Back print, primary lockup with strapline, white garments | 260 x 126.31 mm, 300 dpi (3072 x 1494 px), transparent |
| `GBS_HORIZON_WORKWEAR_BACK_260MM_OFFWHITE-RED_v1.0.png` | Back print, reversed lockup with strapline, sage garments | 260 x 126.31 mm, 300 dpi, transparent |
| `GBS_HORIZON_WORKWEAR_SLEEVE_40MM_SAGE-RED_v1.0.png` | Sleeve emblem, icon sage/red, white garments | 48.3 x 40 mm, 300 dpi (572 x 475 px), transparent |
| `GBS_HORIZON_WORKWEAR_SLEEVE_40MM_OFFWHITE-RED_v1.0.png` | Sleeve emblem, icon off-white/red, sage garments | 48.3 x 40 mm, 300 dpi, transparent |
| `GBS_HORIZON_WORKWEAR_HIVIS-BACK_260MM_BLACK_v1.0.png` | Hi-vis back print, mono black lockup with strapline (print zones 150 mm or deeper) | 260 x 126.31 mm, 300 dpi, transparent |
| `GBS_HORIZON_WORKWEAR_HIVIS-BACK-NOSTRAP_260MM_BLACK_v1.0.png` | Hi-vis back print, mono black no-strap lockup (shallower zones between the bands) | 260 x 104.64 mm, 300 dpi, transparent |
| `GBS_HORIZON_WORKWEAR_HIVIS-CHEST_95MM_BLACK_v1.0.png` | Hi-vis chest mark, mono black no-strap lockup | 95 x 38.24 mm, 300 dpi, transparent |
| `GBS_HORIZON_WORKWEAR_PLACEMENT-SHEET_A4L_v1.0_SCREEN.pdf` | Placement sheet, A4 landscape, 7 pages: white T-shirt, sage T-shirt, white polo, sage polo, softshell jacket, hi-vis vest, embroidery brief | 297 x 210 mm, no bleed |
| `workwear-*.html` | Sources for the PNG artwork (one `.page` sized exactly to the artwork, containing the logo SVG) | - |
| `placement-sheet.html` | Source for the placement sheet, written by `build-placement-sheet.py` (edit the script, not the HTML) | - |

Embroidery is digitised from the vector masters, not from these PNGs: `01_LOGO_MASTER/svg/GBS_HORIZON_LOGO_PRIMARY-NOSTRAP_SAGE-RED_v1.0.svg`, `..._REVERSED-NOSTRAP_OFFWHITE-RED_v1.0.svg`, `GBS_HORIZON_ICON_SIMPLIFIED_SAGE-RED_v1.0.svg` and `..._SIMPLIFIED_OFFWHITE-RED_v1.0.svg`.

## Supplier instructions

Print and transfer (T-shirts, softshell, hi-vis)

1. Use the PNG files at 100 %. They are 300 dpi with the physical size written into the file; do not resample, rotate, add a keyline, a backing shape or a drop shadow. The ground is transparent.
2. Colour targets: sage RGB 110/127/114 (#6E7F72), red RGB 225/6/0 (#E10600), off-white RGB 249/249/247 (#F9F9F7). Match to the physical swatches held by GBS; the digital values are provisional. For screen print, two spot colours (sage and red) on white; off-white and red on sage, with a white underbase under the red only if needed for opacity.
3. Positions are on the placement sheet, measured flat on a size L: chest mark on the wearer's left, centre 105 mm from centre front, top edge 90 mm below the shoulder seam at the neck point; back print centred, top edge 110 mm below the back neck seam; sleeve emblem on the wearer's left sleeve, top edge 100 mm below the shoulder seam. Scale positions by about 10 mm per size step and confirm on the sample.
4. Softshell: heat transfer at the temperature and dwell the shell membrane allows (supplier to confirm); keep clear of seams, zips and pockets.
5. Hi-vis: mono black only. Agree the exact position with the garment manufacturer so that no print touches the retroreflective tape and the garment keeps its EN ISO 20471 class after printing. Chest mark centred between the front opening and the shoulder band (about 60 mm from centre front on the drawing), above the upper band; reduce to 85 mm if that zone is narrower than 110 mm. If the clear zone between the back bands is under 150 mm deep, use the no-strap file or reduce the width to 230 mm.
6. Supply one physical sample of each garment and colourway for approval by the GBS Director before the production run (production register items W01 and W03).

Embroidery (polos; softshell only if agreed in writing)

1. Follow page 7 of the placement sheet. Digitise from the SVG masters without redrawing; keep proportions, colour split and clear space (one GBS cap height on every side).
2. Chest lockup 95 mm wide (38 mm high), sleeve emblem 40 mm high using the simplified icon, optional back lockup 230 mm wide. In the lockup, sew the second (hollow) bar as a solid bar: its 1 mm outline will not sew at chest size.
3. Letter height: at 95 mm wide the descriptor PROPERTY MAINTENANCE has a cap height of 3.9 mm (4.3 mm at 105 mm), below the 5-6 mm letter test. Sew out the descriptor at 5 mm, 6 mm and the actual size on the production fabric. If it does not resolve, GBS will approve either a 105 mm chest mark or the wordmark (`GBS_HORIZON_LOGO_WORDMARK_*`) for embroidered chest marks. The descriptor is never re-set in a larger size or another font.
4. Thread: propose the two nearest 40 wt polyester shades to each colour target and submit thread cards; final shades are approved against physical samples. No metallic or high-sheen threads.
5. Supply a sew-out of every mark on the actual garment colour for Director approval before production (register item W02); keep the stitch files and report stitch counts with the quote.

## Regenerate

```
python3 -I 04_WORKWEAR/build-placement-sheet.py      # rewrites placement-sheet.html (garment outlines, positions, notes)
node tools/render.mjs tools/manifests/04_workwear.json
node tools/qa-overflow.mjs 04_WORKWEAR/placement-sheet.html 8
```

Sizes to check after a render: a 95 mm wide PNG at 300 dpi is about 1122 px wide (the renderer rounds the element box up by a pixel or two); a 260 mm wide PNG is about 3071 px.
