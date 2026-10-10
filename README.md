# GBS-PM-Website

Repository for **GBS Property Maintenance** (Go Building Solutions): the public website for gbs-pm.co.uk and the Horizon brand production pack.

| Folder | What it is |
|---|---|
| `gbs-brand/07_WEBSITE/public` | The static website, deployed to Cloudflare Pages. Pages settings: production branch `main`, no build command, build output directory `gbs-brand/07_WEBSITE/public`. |
| `gbs-brand/07_WEBSITE/src` | Page sources and layout; rebuild with `node gbs-brand/tools/build-site.mjs`. |
| `gbs-brand/` | Logo masters, brand guide, stationery, brochure, workwear, van livery, signage, email signature, social and merchandise artwork. See `gbs-brand/README.md` and `gbs-brand/INDEX.md`. |
| `gbs-brand/company.json` | Single source of truth for company particulars (phone, email, address, company and VAT numbers, services, approved-contractor list). Change it here, then run `bash gbs-brand/tools/build-all.sh`. |

Go-live steps for the domain: `gbs-brand/07_WEBSITE/GO-LIVE.md`.

The repository previously held a Cloudflare Workers AI streaming endpoint (`ai-inference.nicknicola182.workers.dev`). That code was removed when the repository became the GBS website; it remains in the git history before the "Remove legacy Workers AI endpoint" commit if it is ever needed again.
