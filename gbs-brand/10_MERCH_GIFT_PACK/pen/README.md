# Pen - barrel or clip print

| | |
|---|---|
| Sources | `pen-mono-sage.html`, `pen-mono-white.html` |
| Artwork | `GBS_HORIZON_MERCH_PEN_60x7_MONO-SAGE_300dpi_v1.0.png`, `GBS_HORIZON_MERCH_PEN_60x7_MONO-WHITE_300dpi_v1.0.png` |
| Print area | 60 x 7 mm. PNG is 709 x 84 px at 300 dpi, transparent background, dpi metadata embedded. |
| Logo | Strip lockup (`GBS_HORIZON_LOGO_STRIP`) at 56 mm wide x 5 mm high, centred, 2 mm clear at each end and 1 mm top and bottom. The geometry is the master strip SVG; every fill is set to the single ink colour, in line with the approved MONO logo set. |
| Variants | MONO-SAGE for white, silver or light barrels. MONO-WHITE for sage, dark or anodised barrels (the file looks blank on a white screen; open it over a dark background). |
| Print method | One-colour pad print or screen print. For laser engraving on metal, supply the MONO-SAGE file and ask the supplier to engrave the shape; colour fill is not required. |
| Colour | Sage #6E7F72. Pad-print inks are mixed to match; ask for the nearest standard ink and a sample. White is the supplier's opaque white. |

Notes

- Do not let the supplier stretch the strip to fill 60 x 7 mm. The lockup must keep its proportions (about 11.2 : 1).
- The descriptor "PROPERTY MAINTENANCE" is about 1 mm high at this size. Ask for a pre-production sample; if the supplier's process cannot hold it, switch to the wordmark (`01_LOGO_MASTER/svg/GBS_HORIZON_LOGO_WORDMARK_*`) at 7 mm high instead and tell the brand owner.
- Rendering the manifest again rebuilds the PNG without the 300 dpi metadata. Restore it with: `python3 -I -c "from PIL import Image; f='10_MERCH_GIFT_PACK/pen/GBS_HORIZON_MERCH_PEN_60x7_MONO-SAGE_300dpi_v1.0.png'; Image.open(f).save(f, dpi=(300,300))"` (and the WHITE file). The pixel size is correct either way.
