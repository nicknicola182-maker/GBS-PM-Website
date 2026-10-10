# gbs-pm.co.uk: how the site is hosted (as built, 10 October 2026)

The site is live at https://gbs-pm.co.uk and https://www.gbs-pm.co.uk. This page records the configuration that is actually in place so anyone can maintain it. The earlier runbook (Cloudflare Pages plus a CNAME at Fasthosts) was not used; the live setup is below.

## Summary

| Item | Where | Setting |
|---|---|---|
| Domain registration | Fasthosts | gbs-pm.co.uk, nameservers changed to `adelaide.ns.cloudflare.com` and `kyrie.ns.cloudflare.com` |
| DNS | Cloudflare (free plan), zone gbs-pm.co.uk | Records imported from Fasthosts at set-up; mail records kept, parking A records removed |
| Hosting | Cloudflare Worker `gbs-pm-website` (static assets) | Built from this GitHub repository on every push to `main` |
| Custom domains | Worker, Settings, Domains and Routes | `gbs-pm.co.uk` and `www.gbs-pm.co.uk` (Production) |
| HTTPS | Cloudflare | Certificate issued automatically; "Always Use HTTPS" on (SSL/TLS, Edge Certificates) |
| Email | Fasthosts LiveMail, unchanged | MX `mailserver.livemail.co.uk`, SPF, DKIM, DMARC and autodiscover records served by Cloudflare as DNS only (grey cloud). Tested send and receive after the move. |

## Worker build settings

| Setting | Value |
|---|---|
| Repository | `nicknicola182-maker/GBS-PM-Website` |
| Production branch | `main` |
| Root directory | `gbs-brand/07_WEBSITE` |
| Build command | none |
| Deploy command | `npx wrangler deploy` |
| Config | `gbs-brand/07_WEBSITE/wrangler.jsonc` (assets directory `./public`, 404 page handling, auto trailing slash) |

`public/_headers` supplies the security headers (CSP, nosniff, frame, referrer, permissions policy). `public/_redirects` is present for the Pages format but the Worker uses `wrangler.jsonc` for routing.

## Publishing a change

1. Edit the source under `gbs-brand/07_WEBSITE/src` or `gbs-brand/company.json`.
2. Rebuild: `node gbs-brand/tools/build-site.mjs` (or `bash gbs-brand/tools/build-all.sh` for the whole pack).
3. QA: `node gbs-brand/tools/qa-site.mjs`.
4. Commit the source and the rebuilt `public` folder, open a pull request, merge to `main`. The Worker redeploys within about a minute.

## Things never to change without checking email first

- Do not delete or proxy (orange cloud) any MX, TXT, DKIM, DMARC or autodiscover record in the Cloudflare DNS zone.
- Do not move the nameservers back to Fasthosts unless the Fasthosts DNS zone has first been updated to match Cloudflare's records.

## Optional follow-ups

- HSTS (SSL/TLS, Edge Certificates, HTTP Strict Transport Security): can be enabled with max-age 6 months, "include subdomains" off, preload off. Leave subdomains off because the mail hostnames are not served over HTTPS by Cloudflare.
- `formEndpoint` in `gbs-brand/company.json`: set to a form-handling service URL if server-side enquiry delivery is wanted; until then the contact form opens the visitor's email client addressed to info@gbs-pm.co.uk.
- Add the site to a Google Business Profile and LinkedIn.
- The email signature logo is served at https://gbs-pm.co.uk/assets/img/logo-email-600.png.
