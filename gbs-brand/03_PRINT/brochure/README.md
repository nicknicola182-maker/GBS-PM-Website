# GBS HORIZON - Company profile brochure (A4, 8 pp)

Source: `brochure.html` (one `<section class="page">` per page, tokens from `company.json`).
Outputs: `GBS_HORIZON_BROCHURE_A4-8PP_v1.0_SCREEN.pdf` (trim size, for email and approval) and
`GBS_HORIZON_BROCHURE_A4-8PP_v1.0_PRESS.pdf` (trim + 3 mm bleed + crop marks + slug, for the printer).

## Pagination

| Page | Content | Sheet (saddle-stitched) |
|---|---|---|
| 1 | Cover: company profile, reversed logo on sage, horizon bars | Outer (cover) |
| 2 | Who we are, at a glance, Build / Maintain / Improve | Outer (cover) |
| 3 | Services overview (six service cards) | Inner (text) |
| 4 | Planned maintenance and reactive repairs, how jobs are reported | Inner (text) |
| 5 | Fire door services, five-step process | Inner (text) |
| 6 | Refurbishment and insurance reinstatement | Inner (text) |
| 7 | How we work: values, commercial clarity, sectors | Outer (cover) |
| 8 | Back cover: request a quote, contact block, legal line | Outer (cover) |

## Print specification

- Format: A4 portrait, 210 x 297 mm trim, 8 pages, saddle-stitched (two A3 sheets folded and stapled on the spine).
- Bleed: 3 mm on all edges. Crop marks and a slug line are included in the PRESS file. Safe area: live text is at least 10 mm inside trim (12 mm margins).
- Stock (suggested): 300 gsm silk for the outer sheet (pages 1, 2, 7, 8) and 170 gsm silk for the inner sheet (pages 3 to 6). A self-cover on 170 gsm silk throughout is acceptable for short runs. Matt lamination to the outer sheet optional.
- Colour: 4-colour process. Brand colours are supplied as RGB working values (sage #6E7F72, red #E10600, light grey #DADADA, off-white #F9F9F7); the printer converts to their CMYK / PDF-X profile and supplies a proof before manufacture. The cover and back cover carry large solid sage areas and should be proofed for evenness. The off-white on the upper third of the cover is a very light tint and may be substituted with paper white at the printer's discretion.
- Fonts: Montserrat and Inter are embedded by the renderer (self-hosted OFL webfonts in `00_BRAND_CORE/fonts/`).
- Imposition: files are supplied as single pages in reading order; the printer imposes for saddle-stitching.
- Approval: proof-quality production artwork. Physical proofs are signed off before manufacture (see `08_APPROVALS`).

## Regenerate

From the `gbs-brand` root:

```
node tools/render.mjs tools/manifests/03_print_brochure.json
```

Quality checks:

```
node tools/qa-overflow.mjs 03_PRINT/brochure/brochure.html 10
python3 -I tools/qa-ascii.py 100 03_PRINT/brochure/GBS_HORIZON_BROCHURE_A4-8PP_v1.0_SCREEN.pdf <page>
```

Edit copy in `brochure.html` only. Contact details, people, hours, service area and the legal line come from `company.json` via `{{company.*}}` tokens and must not be typed into the page.
