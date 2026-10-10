# Putting the site on gbs-pm.co.uk

Domain: registered at Fasthosts (nameservers ns1/ns2/ns3.livedns.co.uk), no hosting package, email already live on the domain.
Hosting: Cloudflare Pages (free, automatic HTTPS, redeploys on every merge to `main`). Nothing needs to be purchased from Fasthosts; do not buy the Fasthosts SSL certificate.

## Stage 1: review link (about 10 minutes, no DNS changes)

1. Create a free account at cloudflare.com (or sign in).
2. Workers & Pages, Create, Pages, Connect to Git. Authorise GitHub and choose `workers-ai-streaming`.
3. Settings: production branch `main`; framework preset None; build command left blank; build output directory `gbs-brand/07_WEBSITE/public`.
4. Save and Deploy. Cloudflare gives a link like `https://gbs-pm.pages.dev` within a minute. Share that with colleagues for review. Every later merge to `main` republishes it automatically.

## Stage 2: live on gbs-pm.co.uk (email unaffected)

In Cloudflare, open the Pages project, Custom domains, Set up a custom domain, enter `www.gbs-pm.co.uk`. Cloudflare shows a CNAME target (the project's `pages.dev` address).

In Fasthosts, Domain Names, gbs-pm.co.uk:

| Where | Action |
|---|---|
| Advanced DNS | Add a CNAME record: host `www`, points to `<project>.pages.dev` (the value Cloudflare shows), TTL default. Do not change any MX, TXT, SPF, DKIM or autodiscover records. |
| Web forwarding | Forward `gbs-pm.co.uk` (the bare domain) to `https://www.gbs-pm.co.uk`, permanent (301), with "forward path" on if offered. |
| Domain name | Disable the parking page. |

Back in Cloudflare the custom domain shows Active once the CNAME is seen (minutes to a few hours). HTTPS is issued automatically, and the Fasthosts "missing SSL certificate" warning can be ignored.

## Alternative for the bare domain

If you would rather `gbs-pm.co.uk` itself serve the site (no forwarding), move the nameservers to Cloudflare: add the site in Cloudflare (free plan), let it import the existing DNS records, check that the MX and TXT records for email are all present, then change the nameservers in Fasthosts (Manage nameservers) to the two Cloudflare gives you. Only do this once the email records are confirmed, otherwise mail stops.

## After go-live

- In `gbs-brand/company.json` set `formEndpoint` if you want server-side form delivery, rebuild and merge; until then the form opens the visitor's email client.
- The email signature logo at `https://gbs-pm.co.uk/assets/img/logo-email-600.png` resolves once the site is live.
- Add the site to a Google Business Profile and LinkedIn.
