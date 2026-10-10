# GBS HORIZON - release checklist and sign-off

Mirrors section 11 of the production manual. Nothing goes to external manufacture or public launch until the relevant line is initialled.

## Status of this pack (v1.0)

| Item | Status in this pack | Still required before release |
|---|---|---|
| Final vector logo and outlined descriptor | Done: outlined SVG masters built from Montserrat glyph outlines (`01_LOGO_MASTER/svg`) | Director review of the master on screen and in print; optional designer refinement of optical spacing |
| Positive / reversed / mono / icon artwork | Done: 25 variants plus PNG exports and favicons | Reconcile against physical proofs |
| Colour match | Digital values only | Printer ICC conversion and drawdown signed under D50 light for paper, garment and vinyl |
| Typography licence | Montserrat and Inter under SIL OFL 1.1, files bundled | None (keep licence text with supplier files) |
| Legal name, company number, office, disclosures | Done from `company.json` (16560774, registered office Woodgate House, 2-8 Games Road, Cockfosters EN4 9HN; trading address 5-6 Tile Kiln Lane N13 6BX; VAT GB 500 0054 76) | Registered office confirmed 10 Oct 2026, differs from the trading address; confirm "England and Wales" |
| Dummy contact information replaced | Done: all templates driven by `company.json` | Independent check of every rendered PDF before print |
| Business stationery PDF/X proof | Press PDFs with bleed and crop marks supplied | Printer to impose and convert to PDF/X-4; approve one hard proof |
| Embroidered stitch-out and wash test | Artwork and placement sheets supplied; chest descriptor is 3.9 mm cap height at 95 mm, below the 5 mm test | Digitise, sew-out at 5 mm, 6 mm and actual size; fall back to the 105 mm mark or wordmark-only if the descriptor does not hold; 5-cycle wash test |
| Van dimensional survey and first-vehicle proof | Layout sheets on a generic medium panel van (sides 1:15, rear and front 1:10) | Survey the actual vehicle, re-scale, physical positioning proof |
| Signage consent, safety method and fabrication drawing | Artwork supplied | Site-specific sizes, landlord consent, fixing specification, RAMS |
| Website mobile/desktop, WCAG, performance and legal pages | Built and QA'd in Chromium at 1440 px and 390 px; no cookies; privacy notice included | Deploy, test on real devices, review privacy notice, configure form endpoint |
| Archive and release register | `Asset_Production_Register.csv` updated | Keep a version log as suppliers return proofs |

## Sign-off

GBS director: ______________________________ Date: ____________

Design lead: _______________________________ Version: __________

Print / garment / wrap supplier: __________________________________
