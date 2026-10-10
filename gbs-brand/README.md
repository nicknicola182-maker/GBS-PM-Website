# GBS Property Maintenance - Horizon brand production pack v1.0

Everything needed to launch the GBS Property Maintenance identity: a publish-ready static website, outlined logo masters, print stationery, an 8-page company brochure, workwear artwork, white van livery layouts, signage, an email signature, social assets, merchandise artwork and a client gift pack. All of it is generated from one set of sources so that a change to the company details or the logo flows through every file.

The folder numbering follows section 10 of `GBS_Horizon_Brand_Production_Manual_v1`.

## Folder map

| Folder | Contents |
|---|---|
| `company.json` | **Single source of truth** for trading name, legal name, phone, email, address, company number, VAT number and people. Edit here, then run `tools/build-all.sh`. |
| `BRAND_RULES.md` | Condensed working rules: colour, type, logo usage, copy tone, print conventions. |
| `00_BRAND_CORE` | Design tokens (`tokens.css`), self-hosted fonts (Montserrat, Inter; OFL licence). |
| `01_LOGO_MASTER` | 25 outlined SVG logo variants, PNG exports (400-4000 px, transparent), favicon set. Generator: `tools/build-logos.py`. |
| `02_COLOUR_TYPE` | Brand quick guide PDF (colour, type, logo variants, clear space, misuse), palette files. |
| `03_PRINT` | Letterhead, business cards, compliment slip, envelopes, quotation / invoice / job report templates, 8 pp brochure. HTML sources plus `_SCREEN` (trim) and `_PRESS` (bleed + crop marks) PDFs. |
| `04_WORKWEAR` | 300 dpi transfer artwork (chest, back, sleeve, hi-vis), placement sheets, embroidery brief. |
| `05_VEHICLES` | Van livery layout sheets (sides at 1:15, rear and bonnet at 1:10, all dimensions in full-scale mm), full-scale vector panels, fabrication notes. |
| `06_SIGNAGE` | Site board, hoarding panel, entrance sign, resident works notice. |
| `07_WEBSITE` | Website, live at https://gbs-pm.co.uk on a Cloudflare Worker (static `public/` plus the enquiry form relay in `worker/`). See `07_WEBSITE/README.md` and `07_WEBSITE/GO-LIVE.md`. |
| `08_APPROVALS` | Production register (status per asset), release checklist and sign-off sheet, the supplied v1 register. |
| `09_DIGITAL` | Email signature (HTML, plain text, install guide), social avatars, banners, post templates, Open Graph image. |
| `10_MERCH_GIFT_PACK` | Mug, pen, lanyard, hard hat decal, notebook, key fob, gift box, thank-you card, contents card, welcome letter, gift pack spec and indicative cost plan. |
| `tools` | Build scripts: `build-logos.py`, `export-logos.sh`, `build-site.mjs`, `render.mjs` (HTML to PDF/PNG), QA helpers, `build-all.sh`. |

## Regenerating

```bash
cd gbs-brand/tools && npm install          # once: installs Playwright (Chromium) for rendering
pip install fonttools pillow pypdf         # once: logo outlining and QA helpers
cd .. && bash tools/build-all.sh           # rebuild everything from sources
```

Individual steps: `python3 tools/build-logos.py` (SVG masters), `bash tools/export-logos.sh` (PNG + favicons), `node tools/build-site.mjs` (website), `node tools/render.mjs tools/manifests/<area>.json` (any print or artwork set).

## Before anything is manufactured or published

1. Confirm the particulars in `company.json` (registered office, VAT number, service area) and re-run the build.
2. Review `08_APPROVALS/Release_Checklist.md` and work through the sign-off gates with each supplier: colour drawdowns, hard proofs, stitch-outs, van survey, signage consents.
3. Website is live; add the `RESEND_API_KEY` secret in Cloudflare so the contact form delivers to the inbox (`07_WEBSITE/GO-LIVE.md`).
4. Add accreditations to `company.json` and the website only once the certificates are held.

## Notes on this issue

- The logo masters were rebuilt as clean geometry from the brand manual's description and the approved mood board, because the supplied PNG logos are AI-rendered rasters that the manual itself says must not be released. Geometry is documented in the brand quick guide so a designer can refine optical spacing in Illustrator or Affinity if required.
- No photography was supplied, so the website and brochure are typographic by design, with a "horizon" bar motif derived from the icon. Slots for audited project photography are described in `07_WEBSITE/README.md`.
- Colour values remain provisional working digital values until physical proofs are approved.
