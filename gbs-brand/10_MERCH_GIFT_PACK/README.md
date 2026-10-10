# 10_MERCH_GIFT_PACK - branded merchandise and client gift pack (v1.0)

Every artwork file here is rendered from an HTML source by `node tools/render.mjs tools/manifests/10_merch.json` (run from the `gbs-brand` root). Sources link `00_BRAND_CORE/tokens.css`, `00_BRAND_CORE/fonts.css` and `03_PRINT/_shared/print-base.css`; contact details are `{{company.*}}` tokens from `company.json` and are resolved at render time. Do not edit the PDFs; edit the HTML and re-render. Each folder has a README with the supplier specification.

PDFs come in two forms: `_SCREEN.pdf` is the trim size for approval; `_PRESS.pdf` is trim + bleed + crop marks + slug for the printer. Suppliers that work from their own templates should take the PRESS file and ignore the marks.

## Artwork files

| Folder | Source | Artwork | Size (trim) | Bleed | Pages | Print method |
|---|---|---|---|---|---|---|
| `mug/` | `mug-wrap.html` | `GBS_HORIZON_MERCH_MUG-WRAP_200x90_v1.0_SCREEN.pdf`, `_PRESS.pdf` (218 x 108 mm) | 200 x 90 mm | 3 mm | 2 (off-white; sage alternative) | Dye-sublimation full wrap, 11 oz white mug |
| `pen/` | `pen-mono-sage.html` | `GBS_HORIZON_MERCH_PEN_60x7_MONO-SAGE_300dpi_v1.0.png` | 60 x 7 mm (709 x 84 px) | none | 1 | 1-colour pad or screen print, or laser engrave |
| `pen/` | `pen-mono-white.html` | `GBS_HORIZON_MERCH_PEN_60x7_MONO-WHITE_300dpi_v1.0.png` | 60 x 7 mm (709 x 84 px) | none | 1 | 1-colour white pad or screen print on sage or dark barrels |
| `lanyard/` | `lanyard.html` | `GBS_HORIZON_MERCH_LANYARD_900x20_v1.0_SCREEN.pdf`, `_PRESS.pdf` (918 x 38 mm) | 900 x 20 mm | 3 mm | 2 (single direction; second half flipped) | Dye-sublimation polyester, both sides |
| `hard-hat/` | `hard-hat-decal.html` | `GBS_HORIZON_MERCH_HARD-HAT-DECAL_60x40_v1.0_SCREEN.pdf`, `_PRESS.pdf` (78 x 58 mm) | 60 x 40 mm | 2 mm | 1 | Printed and laminated self-adhesive vinyl, kiss-cut |
| `notebook/` | `notebook-cover.html` | `GBS_HORIZON_MERCH_NOTEBOOK-A5_148x210_v1.0_SCREEN.pdf`, `_PRESS.pdf` (166 x 228 mm) | 148 x 210 mm | 3 mm | 3 (front, back, inside front page) | Digital or litho cover, matt laminate; ruled FSC pages; perfect, PUR or case bound |
| `key-fob/` | `key-fob.html` | `GBS_HORIZON_MERCH_KEY-FOB_50x30_v1.0_SCREEN.pdf`, `_PRESS.pdf` (68 x 48 mm) | 50 x 30 mm | 3 mm | 2 (icon; strip logo) | Printed insert under acrylic or direct UV print |
| `gift-pack/` | `box-sleeve.html` | `GBS_HORIZON_GIFT_BOX-SLEEVE_300x200_v1.0_SCREEN.pdf`, `_PRESS.pdf` (318 x 218 mm) | 300 x 200 mm | 3 mm | 1 | Printed lid wrap or card sleeve, 4-colour or 2 spot |
| `gift-pack/` | `belly-band.html` | `GBS_HORIZON_GIFT_BELLY-BAND_400x100_v1.0_SCREEN.pdf`, `_PRESS.pdf` (418 x 118 mm) | 400 x 100 mm | 3 mm | 1 | 170-200 gsm uncoated, scored |
| `gift-pack/` | `thank-you-card.html` | `GBS_HORIZON_GIFT_THANK-YOU-CARD_A6_105x148_v1.0_SCREEN.pdf`, `_PRESS.pdf` (123 x 166 mm) | 105 x 148 mm | 3 mm | 2 (front, back) | 350 gsm uncoated, duplex |
| `gift-pack/` | `contents-card.html` | `GBS_HORIZON_GIFT_CONTENTS-CARD_A6_105x148_v1.0_SCREEN.pdf`, `_PRESS.pdf` (123 x 166 mm) | 105 x 148 mm | 3 mm | 1 | 300-350 gsm uncoated, single side |
| `gift-pack/` | `welcome-letter.md` | printed on the A4 letterhead by the office | A4 | - | 2 | Office print |

Related documents: `GIFT_PACK_SPEC.md` (pack specification, indicative cost plan at 25 / 50 / 100 units, assembly and handover notes).

## Logo use

| Item | Logo file |
|---|---|
| Mug page 1, OG and print grounds | `GBS_HORIZON_LOGO_PRIMARY_SAGE-RED` (with strapline) |
| Mug page 2, notebook front, box sleeve | `GBS_HORIZON_LOGO_REVERSED_OFFWHITE-RED` on sage |
| Pen, key fob side B, belly band, notebook back, cards | `GBS_HORIZON_LOGO_STRIP_SAGE-RED` (single-line lockup; pen uses it as a mono single-ink derivative) |
| Hard hat decal, notebook inside page | `GBS_HORIZON_LOGO_WORDMARK_SAGE-RED` |
| Key fob side A | `GBS_HORIZON_ICON_SAGE-RED` |

The lanyard carries typeset text only, no logo, because a 20 mm strap is below the strip lockup's legible size.

## Checks run on this release

- `node tools/qa-overflow.mjs <source> 4` on every HTML: no text outside trim or inside the 4 mm safe margin.
- PDF page sizes and page counts checked with pypdf; PNG pixel size, transparency and single-ink fill checked with Pillow.
- Hard hat 2 mm bleed: crop marks measured on the press raster at 9 / 49 / 69 mm, matching the trim box.
- Lanyard: text repeat measured at exactly 150 mm pitch, 121.6 mm per repeat, red pipes present; page 2 confirmed rotated on cells 4-6.
- Known renderer trait: Chromium rounds page sizes up to whole points, so PDF boxes read 0.1-0.4 mm over nominal (same as the letterhead). The PRESS files place trim and marks correctly; the extra sliver falls outside the marks.

## Re-rendering

```
cd gbs-brand
node tools/render.mjs tools/manifests/10_merch.json            # everything
node tools/render.mjs tools/manifests/10_merch.json NOTEBOOK   # one job (filter on src/out path)
node tools/qa-overflow.mjs 10_MERCH_GIFT_PACK/notebook/notebook-cover.html 4
python3 -I tools/qa-ascii.py 100 10_MERCH_GIFT_PACK/notebook/GBS_HORIZON_MERCH_NOTEBOOK-A5_148x210_v1.0_SCREEN.pdf 1
```

After re-rendering the pen PNGs, restore the 300 dpi metadata as described in `pen/README.md`.
