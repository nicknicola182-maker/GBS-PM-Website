# GBS Property Maintenance - website

Static HTML, CSS and a few lines of JavaScript. No framework, no database, no build dependencies on the host. Deploy the `public/` folder as-is.

## Pages

| URL | Source | Purpose |
|---|---|---|
| `/` | `src/pages/index.html` | Home: positioning, services, fire door specialism, process, values, sectors |
| `/services` | `src/pages/services.html` | All six services with anchors (`#planned`, `#reactive`, `#fire-doors`, `#refurbishment`, `#insurance`, `#reporting`) |
| `/about` | `src/pages/about.html` | Company, approach, values, leadership, H&S, registered particulars |
| `/contact` | `src/pages/contact.html` | Contact details and quote request form (`#quote`) |
| `/privacy` | `src/pages/privacy.html` | UK GDPR privacy notice (site sets no cookies) |
| `/thank-you`, `/404` | | Form confirmation and not-found pages (noindex) |

Also generated: `sitemap.xml`, `robots.txt`, `site.webmanifest`, favicons, Open Graph image, LocalBusiness JSON-LD on every page, `_headers` (security headers and caching) and `_redirects` (clean URLs).

## Editing

1. Company particulars live in `../company.json` (phone, email, address, company number, VAT number, people). Change them there, never in the pages.
2. Page copy lives in `src/pages/*.html`. Each file starts with a `<!--META {...}-->` block for title, description and nav highlight. The shared header, footer and `<head>` are in `src/layout.html`.
3. Rebuild: `node ../tools/build-site.mjs` (Node 18+). Output goes to `public/`.

## Contact form

The form works in two modes:

- **No endpoint configured (default):** the visitor's email client opens with the enquiry pre-filled, addressed to `company.email`. Works without any third-party service.
- **Form endpoint configured:** set `"formEndpoint"` in `company.json` to a form-handling URL (for example a Formspree, Basin or Web3Forms endpoint, or your own serverless function), rebuild, and submissions are posted there and the visitor is sent to `/thank-you`. The form includes a honeypot field (`website`) that the handler should treat as spam when filled.

Update the privacy notice's "Cookies and website analytics" paragraph if you add analytics or a form provider that sets cookies.

## Deploying

- **Cloudflare Pages:** create a project, upload or connect the repo, set the build output directory to `07_WEBSITE/public` (no build command needed). `_headers` and `_redirects` are picked up automatically.
- **Cloudflare Workers (static assets):** from this folder run `npx wrangler deploy` (uses `wrangler.jsonc`).
- **Netlify:** publish directory `07_WEBSITE/public`.
- **Any other host (cPanel, Plesk, S3, nginx):** upload the contents of `public/`. Configure clean URLs (serve `services.html` for `/services`) or keep the `.html` links; both work because every internal link is root-relative.

Point `gbs-pm.co.uk` and `www.gbs-pm.co.uk` at the host and enable HTTPS (automatic on Cloudflare and Netlify).

## Adding photographs

The site is designed to work without photography. When audited project photography is available, the natural slots are: the hero (replace the SVG illustration in `index.html` with an `<img>` at 1200 x 900 or wider, WebP or AVIF, with meaningful alt text), the service cards and the About page. Keep file sizes under 200 KB each and use `loading="lazy"` below the fold.

## Pre-launch checklist

- [ ] `company.json` particulars confirmed (registered office, VAT number, service area)
- [ ] Form endpoint configured and tested, or mailto mode accepted
- [ ] Accreditations added to `company.json` only once certificates are held
- [ ] Domain, HTTPS, `www` redirect and 404 handling verified
- [ ] Privacy notice reviewed by whoever is responsible for data protection
- [ ] Google Business Profile and LinkedIn page link to the site
