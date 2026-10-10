# GBS HORIZON - Working brand rules (v1.0)

Condensed from `GBS_Horizon_Brand_Production_Manual_v1` so every file in this pack is produced the same way. Read this before creating or editing any asset.

## 1. Identity

- Trading identity: **GBS Property Maintenance**. The visible logo never shows "LTD".
- Legal entity for disclosures: **GBS Property Maintenance Ltd**, registered in England and Wales, company number 16560774, registered office 5-6 Tile Kiln Lane, London N13 6BX, VAT GB 500 0054 76. These must appear on letters, order forms, invoices, quotations, email footers and the website footer.
- Strapline: **BUILD | MAINTAIN | IMPROVE** (pipes in red). Drop it where it would be illegible (anything under about 60 mm wide in print or 300 px on screen).
- Positioning: specialist maintenance, repair, refurbishment and fire door services for residential blocks and managed property portfolios. Tone: concise, technical, dependable. No generic builder imagery, no unsupported claims, no accreditations unless they are listed in `company.json`.

## 2. Colour

| Token | Hex | RGB | Use |
|---|---|---|---|
| `--gbs-sage` | #6E7F72 | 110 127 114 | Logo, headings, panels, uniforms |
| `--gbs-red` | #E10600 | 225 6 0 | Descriptor, icon highlight, CTAs, accents (small areas only) |
| `--gbs-light` | #DADADA | 218 218 218 | Dividers, supporting graphics |
| `--gbs-offwhite` | #F9F9F7 | 249 249 247 | Paper, page background |

No charcoal. Body text uses `--gbs-ink` (#2E3531, a dark sage-neutral) defined in `00_BRAND_CORE/tokens.css`. Red is an accent, never a background for body text and never used on sage except in the approved reversed logo. Values are provisional digital values; printers convert via ICC profile and proof.

## 3. Typography

- Headings and descriptor: **Montserrat** 600/700 (800 for display only). Descriptor and labels in uppercase with 0.12 em tracking.
- Body and UI: **Inter** 400/500/600. Sentence case. Tabular numerals for prices, dates and references.
- Print scale: A4 brochure H1 26-32 pt, H2 14-18 pt, body 9.5-11 pt, footnotes 7.5 pt min. Stationery body 10-11 pt, legal footer 7.5-9 pt. Website display 48-64 px desktop / 32-40 px mobile, body 16-18 px.
- Fonts are self-hosted in `00_BRAND_CORE/fonts/` (OFL licence). Link `00_BRAND_CORE/tokens.css` and `00_BRAND_CORE/fonts.css` from every HTML source.

## 4. Logo files (`01_LOGO_MASTER/svg`)

All SVGs are outlined vectors (no live fonts). Unit X = GBS cap height. Keep clear space of at least 1X on every side. Never stretch, recolour outside the approved set, rotate, add effects, or redraw the bars.

| File | Use |
|---|---|
| `GBS_HORIZON_LOGO_PRIMARY_SAGE-RED` | Default on white/off-white, with strapline |
| `GBS_HORIZON_LOGO_PRIMARY-NOSTRAP_SAGE-RED` | Default where strapline would be too small (stationery headers, chest prints) |
| `GBS_HORIZON_LOGO_REVERSED_OFFWHITE-RED` / `-NOSTRAP` | On solid sage (manual-approved reversed version) |
| `GBS_HORIZON_LOGO_REVERSED-SOFT_OFFWHITE` | On sage at small sizes where red descriptor would not read |
| `GBS_HORIZON_LOGO_MONO_SAGE` / `_WHITE` / `_BLACK` | Single-ink print, etching, stamps, tonal garments |
| `GBS_HORIZON_LOGO_WORDMARK_*` | GBS + icon only (lockup without descriptor) for very small spaces |
| `GBS_HORIZON_LOGO_STRIP_*` | Single-line lockup for narrow strips (lanyards, pens, van rear, web header) |
| `GBS_HORIZON_ICON_*` | Horizon bars only (avatars, sleeve, hard hat, favicon) |
| `GBS_HORIZON_ICON_SIMPLIFIED_*` | Solid-bar version for embroidery and sizes under 20 mm |
| `GBS_HORIZON_AVATAR_SQUARE_*` | Square social avatars and app icons |

Minimum sizes to proof from: 35 mm wide print, 100 mm embroidery, 140 px screen (primary lockup). Icon: 8 mm print, 20 mm embroidery (simplified).

PNG exports live in `01_LOGO_MASTER/png` (transparent, 400/1200/2400/4000 px). Favicons in `01_LOGO_MASTER/favicon`.

## 5. Company particulars - one source

Never type contact details into an asset. Use tokens that `tools/render.mjs` and `tools/build-site.mjs` replace from `company.json`:

`{{company.tradingName}}` `{{company.legalName}}` `{{company.phone}}` `{{company.phoneTel}}` `{{company.email}}` `{{company.domain}}` `{{company.url}}` `{{company.addressOneLine}}` `{{company.address.line1}}` `{{company.address.town}}` `{{company.address.postcode}}` `{{company.registeredOffice}}` `{{company.placeOfRegistration}}` `{{company.companyNumber}}` `{{company.vatNumber}}` `{{company.people.0.name}}` `{{company.people.0.role}}` `{{company.people.0.email}}` `{{company.people.0.mobile}}` `{{company.people.0.mobileTel}}` `{{company.serviceArea}}` `{{company.hours}}` `{{company.year}}`

Standard legal line (use verbatim):
`{{company.legalName}} · Registered in {{company.placeOfRegistration}}, company number {{company.companyNumber}} · Registered office: {{company.registeredOffice}} · VAT registration number {{company.vatNumber}}`

## 6. Print production conventions

- Every print source is an HTML file linking `tokens.css`, `fonts.css` and `03_PRINT/_shared/print-base.css`, with `--trim-w`/`--trim-h` on `:root` and one `<section class="page" data-trim="W x H mm">` per page. Backgrounds that run to the edge use `.bleed` (or `.bleed-top` etc.). Keep live text at least 5 mm inside trim on cards and 10 mm on A4.
- Register each source in a manifest under `tools/manifests/*.json`; `tools/render.mjs <manifest>` produces `*_SCREEN.pdf` (trim size) and `*_PRESS.pdf` (trim + 3 mm bleed + crop marks + slug), or 300 dpi PNG artwork for transfer/garment/vinyl suppliers.
- File naming: `GBS_HORIZON_[ASSET]_[VARIANT]_[SIZE]_[COLOUR]_vMAJOR.MINOR.ext`.
- Outputs here are proof-quality production artwork. The printer still converts to their PDF/X profile, and physical proofs are signed off before manufacture (see `08_APPROVALS`).

## 7. Copy rules

UK English. Short paragraphs. Construction terminology: Scope of Works, Remedial Works, Make Good, Supply & Install, Planned Preventative Maintenance, Reactive Repairs, Variation, Job Report, RAMS. No emojis, no marketing superlatives, no invented case studies, client names, statistics or accreditations.
