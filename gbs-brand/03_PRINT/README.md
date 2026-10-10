# 03_PRINT - Stationery and document templates

Print artwork for GBS Property Maintenance, produced to the conventions in `BRAND_RULES.md` (section 6). Every item is an HTML source that links `00_BRAND_CORE/tokens.css`, `00_BRAND_CORE/fonts.css` and `_shared/print-base.css`; company particulars are `{{company.*}}` tokens filled from `company.json` at render time, never typed into the artwork. Rendered PDFs sit next to their source: `*_SCREEN.pdf` is the trim size for on-screen use and office printing, `*_PRESS.pdf` is trim + bleed + crop marks + slug for the printer.

## Specification

| Item | Source | Output (v1.0) | Trim (mm) | Bleed | Pages | Stock recommendation | Print method |
|---|---|---|---|---|---|---|---|
| Letterhead | `letterhead/letterhead.html` | `GBS_HORIZON_LETTERHEAD_A4_v1.0` | 210 x 297 | 3 mm (nothing runs to the edge) | 2: sheet 1, continuation | 120 gsm uncoated white, laser-guaranteed | Litho (sage + red as CMYK or 2 spot colours) or digital; short runs digital |
| Business cards, colourway A | `business-cards/business-card-A-named.html`, `business-card-A-template.html` | `GBS_HORIZON_BUSINESS-CARD_A-NAMED_85x55_v1.0`, `..._A-TEMPLATE_85x55_v1.0` | 85 x 55 | 3 mm (solid sage back bleeds) | 2: front (white, details), back (sage, reversed logo and strapline) | 400 gsm uncoated white board | Digital or litho, double-sided, 5 mm live-text safety |
| Business cards, colourway B | `business-cards/business-card-B-named.html`, `business-card-B-template.html` | `GBS_HORIZON_BUSINESS-CARD_B-NAMED_85x55_v1.0`, `..._B-TEMPLATE_85x55_v1.0` | 85 x 55 | 3 mm (solid sage front bleeds) | 2: front (sage, reversed logo and strapline), back (white, details centred) | 400 gsm uncoated white board | As colourway A |
| Compliment slip | `compliment-slip/compliment-slip.html` | `GBS_HORIZON_COMPLIMENT-SLIP_DL_v1.0` | 210 x 99 (DL) | 3 mm (side bars run off the bottom edge) | 1 | 120 gsm uncoated white, matching the letterhead | Litho or digital, single-sided |
| Envelope DL | `envelope/envelope-DL.html` | `GBS_HORIZON_ENVELOPE_DL_220x110_v1.0` | 220 x 110 | None | 2: front, back (flap) | 100-120 gsm white wove, wallet (long-edge flap), peel and seal | Overprint on made-up envelopes; front keeps the right 60 % and bottom 20 mm clear for the address and postal indicia |
| Envelope C4 | `envelope/envelope-C4.html` | `GBS_HORIZON_ENVELOPE_C4_324x229_v1.0` | 324 x 229 | None | 2: front, back (flap) | 100-120 gsm white wove, wallet (long-edge flap), peel and seal | As DL |
| Quotation | `documents/quotation.html` | `GBS_HORIZON_DOCUMENT_QUOTATION_A4_v1.0` | 210 x 297 | None needed (press file carries 3 mm white bleed) | 1 | Issued as PDF, or office laser on 90-100 gsm white or on pre-printed letterhead stock | Digital / office print |
| Invoice | `documents/invoice.html` | `GBS_HORIZON_DOCUMENT_INVOICE_A4_v1.0` | 210 x 297 | As quotation | 1 | As quotation | Digital / office print |
| Job report | `documents/job-report.html` | `GBS_HORIZON_DOCUMENT_JOB-REPORT_A4_v1.0` | 210 x 297 | As quotation | 2: report and sign-off, photographic record | As quotation | Digital / office print |

Shared styles: `business-cards/cards.css` (all four card sources) and `documents/documents.css` (all three document sources). Type sizes: cards 7-7.5 pt with the name in Montserrat 600 at 10 pt; slip and envelopes 7.5-8 pt; A4 documents 9-9.5 pt body, 8.5 pt panels, 7.5 pt legal line. Logos: primary no-strap lockup on white (40 mm on cards, 45 mm on the slip and DL envelope, 48 mm on documents, 60 mm on C4), reversed no-strap lockup on solid sage, Horizon icon at 8 mm beside the envelope return address. Red appears only as the tick on the header rule, the pipes in the strapline and the web address.

Colour values are the provisional digital values from `00_BRAND_CORE/tokens.css` (sage #6E7F72, red #E10600). The printer converts to their PDF/X profile; a physical proof is signed off before manufacture (see `08_APPROVALS`).

## Regenerating

Run from the `gbs-brand` root. `tools/node_modules` already resolves Playwright.

```
node tools/render.mjs tools/manifests/03_print_stationery.json            # everything in this folder
node tools/render.mjs tools/manifests/03_print_stationery.json business-cards
node tools/render.mjs tools/manifests/03_print_stationery.json compliment-slip
node tools/render.mjs tools/manifests/03_print_stationery.json envelope
node tools/render.mjs tools/manifests/03_print_stationery.json documents
node tools/render.mjs tools/manifests/03_print_stationery.json letterhead
```

The filter matches any part of the source or output path. Each manifest entry gives the source, output base name and trim; the envelope entries set `"bleed": 0, "marks": 6`, so their press sheets are trim + 12 mm. `render.mjs` positions crop marks and writes its slug for a 3 mm bleed, so the envelope sources carry a short CSS block that pulls the marks in by 3 mm and replaces the slug with one reading "bleed 0 mm" (see the comment in `envelope/envelope-DL.html`).

To change a name, role or number, edit `company.json` and re-render; to add a person, copy `business-card-A-named.html` and change the `people.0` index. Named and template cards share `cards.css`, so layout changes apply to all four.

## QA tools

```
node tools/qa-overflow.mjs 03_PRINT/business-cards/business-card-A-named.html 5    # cards, slip, envelopes: 5 mm safety
node tools/qa-overflow.mjs 03_PRINT/documents/quotation.html 10                    # A4: 10 mm safety
python3 -I tools/qa-ascii.py 100 03_PRINT/documents/GBS_HORIZON_DOCUMENT_QUOTATION_A4_v1.0_SCREEN.pdf 1
pdftotext 03_PRINT/documents/GBS_HORIZON_DOCUMENT_INVOICE_A4_v1.0_SCREEN.pdf - | grep '{{'   # must print nothing
pdffonts 03_PRINT/documents/GBS_HORIZON_DOCUMENT_INVOICE_A4_v1.0_SCREEN.pdf                   # Montserrat and Inter embedded
```

Page size and count can be checked with pypdf: `PdfReader(f).pages[n].mediabox` in points; divide by 72 and multiply by 25.4 for mm. Expected: screen PDF = trim; press PDF = trim + 2 x (bleed + 6 mm marks), i.e. 103 x 73 for cards, 228 x 117 for the slip, 232 x 122 (DL) and 336 x 241 (C4) for envelopes, 228 x 315 for A4.

## Preflight checklist

1. `company.json` is current and the `_CONFIRM` fields (registered office, place of registration, service area) have been checked before anything is released externally.
2. The source has been re-rendered after the last edit and no `{{` token survives in the PDF text.
3. `qa-overflow` is clean at 5 mm (cards, slip, envelopes) or 10 mm (A4).
4. Page count and page size match the table above for both the screen and press files.
5. Montserrat and Inter are embedded (`pdffonts`); no substitute fonts.
6. Solid sage sides and the side-bar motif run 3 mm into the bleed; crop marks sit on the trim line (6 mm from the sheet edge on envelope press files, 9 mm on all others).
7. Logo minimum sizes and clear space are respected: primary lockup never below 35 mm, icon never below 8 mm, no strapline inside a lockup under 60 mm wide.
8. The standard legal line is present and verbatim on the letterhead, compliment slip, quotation, invoice and job report; the VAT number is on the invoice.
9. Red is confined to the header-rule tick, strapline pipes and web address; nothing else prints red.
10. Envelopes: confirm wallet (long-edge flap) or pocket (short-edge flap) with the supplier before print; the return address on the back is positioned for a long-edge flap. Keep the front's right 60 % and bottom 20 mm free of print for the address and postal indicia.
11. Business cards: named versions checked against `company.json`; template versions still show `[Name]`, `[Role]` and `[Mobile]`.
12. Supply the `_PRESS.pdf` to the printer, the `_SCREEN.pdf` for office use; the printer converts to PDF/X with their profile and returns a proof for sign-off in `08_APPROVALS`.

## Known limitations

- `render.mjs` hard-codes a 3 mm bleed in its crop-mark script and slug. Only the envelopes need a different bleed, and they compensate in their own CSS; any future zero-bleed item should copy that block.
- `letterhead.html` places its foot-rule at 27 mm from the trim, which runs through the cap height of the footer strapline (visible at high zoom). The document templates place theirs at 30 mm; the letterhead has not been altered.
- The renderer's slug line is wider than a business-card press sheet, so `cards.css` forces it onto one line at 4.5 pt to keep it out of the bleed.
