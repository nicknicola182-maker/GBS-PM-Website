# GBS-PM-Website (formerly workers-ai-streaming)

This repository is the **GBS Property Maintenance website and Horizon brand production pack** (`gbs-brand/`): static website plus logo masters and print, workwear, vehicle, signage, digital and merchandise artwork. Plain HTML/CSS/JS, no framework, no database, no authentication. The former Workers AI streaming endpoint at the repository root was removed (see git history).

## gbs-brand conventions
- `gbs-brand/company.json` is the single source of truth for company particulars; every output uses `{{company.*}}` tokens.
- Rebuild everything with `bash gbs-brand/tools/build-all.sh` (needs Node 18+ with Playwright, python3 with fonttools/Pillow/pypdf, poppler-utils).
- Website source is `gbs-brand/07_WEBSITE/src`, output `gbs-brand/07_WEBSITE/public` (deploy as-is). QA: `node gbs-brand/tools/qa-site.mjs`.
- Print sources are HTML with `.page` sections rendered by `gbs-brand/tools/render.mjs` from manifests in `gbs-brand/tools/manifests/`.
- Website copy (owner instruction 11 Oct 2026): no filler lines or caption bars; never advertise detailed cost breakdowns, labour and materials separated, unit rates shown or materials mark-up. Say "clear scope and quotation" instead.
- Logo masters (Oct 2026): traced from the handover artwork in `gbs-brand/01_LOGO_MASTER/source` by `tools/trace-logo.py` (needs `pip install vtracer`), composed by `tools/build-logos.py`; never redraw. Four bars in three colours (owner, 11 Oct 2026): first and fourth bars and horizon line light sage #ACBCAC (`--gbs-sage-light`), second bar letter colour, third bar red; the icon is those bars cut from the lockup, not `horizon-icon.png`. Pack body text is deep sage #4C5D50, solid sage surfaces #627365.
- Brand rules: `gbs-brand/BRAND_RULES.md`. Colours sage #6E7F72, red #E10600, light #DADADA, off-white #F9F9F7; fonts Montserrat (headings) and Inter (body). Website (Oct 2026 redesign): sage header/footer with the white Horizon logo PNG, deep sage #4C5D50 text, three work categories (planned / reactive / improve) on Home and Services; fire doors are an ordinary service; display name GBS Property Maintenance only, never expanded.

## Hosting (live since 10 Oct 2026)
- Site is live at https://gbs-pm.co.uk on Cloudflare Worker `gbs-pm-website`, built from `main` (root `gbs-brand/07_WEBSITE`, `npx wrangler deploy`). DNS is on Cloudflare; email stays on Fasthosts LiveMail with mail records DNS-only. Details: `gbs-brand/07_WEBSITE/GO-LIVE.md`.
- Contact form posts to `/api/enquiry` (Worker `gbs-brand/07_WEBSITE/worker/index.js`), which emails info@ via Resend; the API key is the Cloudflare secret `RESEND_API_KEY`, never in the repo. Tests: `node --test gbs-brand/07_WEBSITE/worker/enquiry.test.mjs`. Verified end to end 11 Oct 2026.
