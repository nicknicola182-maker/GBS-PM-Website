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

If a merge does not deploy, open the Worker's Settings tab and look at the Builds section. A blue banner saying the project is disconnected from your Git account means GitHub can no longer notify Cloudflare: click Manage next to the repository and re-authorise GitHub. Reconnecting does not rebuild by itself; the next push to `main` does.

## Things never to change without checking email first

- Do not delete or proxy (orange cloud) any MX, TXT, DKIM, DMARC or autodiscover record in the Cloudflare DNS zone.
- Do not move the nameservers back to Fasthosts unless the Fasthosts DNS zone has first been updated to match Cloudflare's records.

## Enquiry form (contact page)

The form posts to `/api/enquiry`, handled by `worker/index.js` in the same Worker that serves the site. The Worker checks the fields, drops bot submissions (hidden honeypot field), then emails the enquiry to `ENQUIRY_TO` through Resend with reply-to set to the visitor.

Fields: `name`, `email`, `role` (I am enquiring as: homeowner / individual client, landlord / freeholder, managing agent / property manager, commercial client, other), `phone`, `company` (optional, so individuals can enquire), `service` (type of work: Planned maintenance, Reactive repairs, Refurbishments & improvements, Not sure yet), `trade` (optional specific service from `company.json`), `site` (property address), `message`, `consent`, plus the `website` honeypot. The Worker requires name, email, phone, service, site, message and consent. If the relay is unavailable the page falls back to opening the visitor's email client, so enquiries are never lost.

| Setting | Where | Value |
|---|---|---|
| `ENQUIRY_TO` | `wrangler.jsonc` vars | `info@gbs-pm.co.uk` |
| `ENQUIRY_FROM` | `wrangler.jsonc` vars | `GBS Property Maintenance website <onboarding@resend.dev>` until the domain is verified in Resend, then `enquiries@gbs-pm.co.uk` |
| `RESEND_API_KEY` | Cloudflare, Workers & Pages, gbs-pm-website, Settings, Variables and Secrets (type Secret) | API key from resend.com, API Keys. Never put it in the repository. |

Set-up, once:

1. Create the Resend account with `info@gbs-pm.co.uk` as the login email. While the domain is unverified Resend only delivers to the account's own address, which is exactly the inbox we want.
2. Resend, API Keys, Create API key (sending access is enough). Copy it.
3. Cloudflare, Workers & Pages, gbs-pm-website, Settings, Variables and Secrets, Add: type Secret, name `RESEND_API_KEY`, paste the key, Deploy.
4. Submit the form on https://gbs-pm.co.uk/contact and check the inbox.

Branded sender, optional later: Resend, Domains, Add domain `gbs-pm.co.uk`, add the DNS records it lists in Cloudflare DNS (they are for a sending subdomain and DKIM; they do not touch the existing MX for Fasthosts mail), wait for Verified, then change `ENQUIRY_FROM` in `wrangler.jsonc` and merge.

Tests: `node --test gbs-brand/07_WEBSITE/worker/enquiry.test.mjs`. Failures in production are visible under the Worker's Logs tab (observability is enabled).

## Optional follow-ups

- HSTS (SSL/TLS, Edge Certificates, HTTP Strict Transport Security): can be enabled with max-age 6 months, "include subdomains" off, preload off. Leave subdomains off because the mail hostnames are not served over HTTPS by Cloudflare.
- Add the site to a Google Business Profile and LinkedIn.
- The email signature logo is served at https://gbs-pm.co.uk/assets/img/logo-email-600.png.
