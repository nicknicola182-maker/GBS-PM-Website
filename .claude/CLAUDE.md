# GBS-PM-Website (formerly workers-ai-streaming)

This repository is the **GBS Property Maintenance website and Horizon brand production pack** (`gbs-brand/`): static website plus logo masters and print, workwear, vehicle, signage, digital and merchandise artwork. Plain HTML/CSS/JS, no framework, no database, no authentication. The former Workers AI streaming endpoint at the repository root was removed (see git history).

## gbs-brand conventions
- `gbs-brand/company.json` is the single source of truth for company particulars; every output uses `{{company.*}}` tokens.
- Rebuild everything with `bash gbs-brand/tools/build-all.sh` (needs Node 18+ with Playwright, python3 with fonttools/Pillow/pypdf, poppler-utils).
- Website source is `gbs-brand/07_WEBSITE/src`, output `gbs-brand/07_WEBSITE/public` (deploy as-is). QA: `node gbs-brand/tools/qa-site.mjs`.
- Print sources are HTML with `.page` sections rendered by `gbs-brand/tools/render.mjs` from manifests in `gbs-brand/tools/manifests/`.
- Brand rules: `gbs-brand/BRAND_RULES.md`. Colours sage #6E7F72, red #E10600, light #DADADA, off-white #F9F9F7; fonts Montserrat (headings) and Inter (body).
