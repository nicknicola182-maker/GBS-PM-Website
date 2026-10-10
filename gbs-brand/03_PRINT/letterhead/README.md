# Letterhead

| File | Use |
|---|---|
| `GBS_HORIZON_LETTERHEAD_A4_v1.0_SCREEN.pdf` | Digital letterhead at trim size (2 pages: first sheet and continuation sheet). Use as a PDF background or send as-is. |
| `GBS_HORIZON_LETTERHEAD_A4_v1.0_PRESS.pdf` | Printer artwork with 3 mm bleed and crop marks for pre-printed stationery. |
| `GBS_HORIZON_LETTERHEAD_A4_v1.0.docx` | Word template for day-to-day letters: logo and contact block in the header, strapline and statutory disclosure in the footer, 20 mm margins. Install the Montserrat and Inter fonts from `00_BRAND_CORE/fonts` on each PC (Word falls back to Arial otherwise). |
| `letterhead.html` | Source. Regenerate with `node tools/render.mjs tools/manifests/03_print_stationery.json letterhead`. |

Stock suggestion: 120 gsm uncoated, off-white or bright white; approve a drawdown of the sage and red before the first run. Legal footer wording comes from `company.json`.
