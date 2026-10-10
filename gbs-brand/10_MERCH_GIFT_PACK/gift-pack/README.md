# Client gift pack artwork

All items are A-series or custom print PDFs with 3 mm bleed, rendered from the HTML sources here by `tools/manifests/10_merch.json`. Contact details come from `company.json` tokens.

| Item | Source | Artwork (PRESS = bleed + crop marks, SCREEN = trim) | Size | Print |
|---|---|---|---|---|
| Box lid / sleeve | `box-sleeve.html` | `GBS_HORIZON_GIFT_BOX-SLEEVE_300x200_v1.0_*.pdf` | 300 x 200 mm, 3 mm bleed. Sage ground, reversed logo 112 mm wide, "With our thanks" Montserrat 600 20 pt off-white, web address at the foot. | Printed wrap for a rigid lid, or a printed card sleeve. 4-colour or 2 spot (sage + red) plus off-white as paper. Matt laminate or uncoated. |
| Belly band | `belly-band.html` | `GBS_HORIZON_GIFT_BELLY-BAND_400x100_v1.0_*.pdf` | 400 x 100 mm (400 long, 100 high), 3 mm bleed, fold marks at 100 and 300 mm shown as hairlines (ask the printer to drop them or keep as scores). Off-white, strip logo 120 mm wide centred on the 200 mm top panel, "With our thanks", web address; sage rules with a red tip along the top and bottom of the panel. | 170-200 gsm uncoated, 1 side, scored twice, glued or tucked under the box. If the box is deeper than about 60 mm, lengthen the band in the HTML (`--trim-w`) and the manifest. |
| Thank-you card | `thank-you-card.html` | `GBS_HORIZON_GIFT_THANK-YOU-CARD_A6_105x148_v1.0_*.pdf` (2 pages) | A6 105 x 148 mm portrait, 3 mm bleed. Front: "Thank you" Montserrat 700 30 pt sage, "for working with GBS", horizon bars motif on a baseline rule. Back: strip logo, copy, name and role, mobile, phone, email, web. | 350 gsm uncoated or silk, duplex, 4-colour or 2 spot. |
| Contents card | `contents-card.html` | `GBS_HORIZON_GIFT_CONTENTS-CARD_A6_105x148_v1.0_*.pdf` | A6 105 x 148 mm portrait, 3 mm bleed, single sided. Lists the pack contents with an optional line for tea/biscuits, a sourcing note in [brackets] to confirm, and contact details. | 300-350 gsm uncoated, 1 side. |
| Welcome letter | `welcome-letter.md` | Printed by the office on the A4 letterhead (`03_PRINT/letterhead`) | A4 | Office print on letterhead; two pages maximum. |

Before printing

- Replace or delete the bracketed items on the contents card (optional tea/biscuits line and the sourcing note).
- Confirm the box's outer dimensions with the box supplier first; the sleeve and band are drawn for a 300 x 200 mm footprint and a lid depth of up to 60 mm.
- Ask the box, notebook and mug suppliers for physical sage samples and compare them side by side. The pack should read as one colour.
