# GBS email signature - installation guide (v1.1)

Files in this folder:

| File | Use |
|---|---|
| `signature-<first>-<last>.compiled.html` | One personal signature per person listed in `company.json` under `people` (currently `signature-nicholas-nicola.compiled.html`). Install your own. |
| `signature-generic.compiled.html` | Shared-mailbox version (info@, no named person). |
| `signature-<first>-<last>.compiled.txt` | Plain-text version of each personal signature for text-only mail and ticketing systems. |
| `signature-staff-template.compiled.html`, `.txt` | Signature with FIRST LAST, JOB TITLE, 07xxx xxxxxx and first.last@ placeholders for staff not yet listed in `company.json`. Edit the placeholders before installing, or add the person to `company.json` and rebuild (preferred). |
| `signature.html`, `signature-generic.html`, `signature.txt` | Token sources. Do not install these; they still contain `{{company.*}}` and `{{person.*}}` placeholders. |
| `build-signature.mjs` | Rebuilds the compiled files from `company.json` (`node 09_DIGITAL/email-signature/build-signature.mjs`). |
| `logo-email-600.png` | The logo the signature loads: the primary lockup with strapline, 600 x 238 px, shown at 200 x 79 px. The website serves it at `https://gbs-pm.co.uk/assets/img/logo-email-600.png`. |
| `signature.preview.html` | Review copy with the logo loaded from this folder instead of the website. Do not install it. |
| `preview.png` / `preview-local.png` | Review renders only. `preview.png` shows the alt text where the hosted logo could not be fetched at render time; `preview-local.png` shows the layout with the logo. |

## Adding a member of staff

1. Open `gbs-brand/company.json` and add the person to the `people` list, copying the existing entry: `name`, `role`, `email`, `mobile` (as it should read) and `mobileTel` (international form, digits only after the +).
2. Run `node gbs-brand/09_DIGITAL/email-signature/build-signature.mjs`. It writes `signature-<first>-<last>.compiled.html` and `.txt` for every person listed.
3. Send the person their two files and this guide. Only the first person listed is used elsewhere in the pack (letterhead, named business cards, quotation and invoice), so adding staff after the Managing Director changes nothing else.

If a signature is needed before the person is added to `company.json`, open `signature-staff-template.compiled.html` in a text editor and replace FIRST LAST, JOB TITLE, the two mobile placeholders (`07xxx xxxxxx` and `+447xxxxxxxxx`) and `first.last@gbs-pm.co.uk`, then install it in the same way.

## Before you start: the hosted logo

The signature does not embed the logo. It loads `https://gbs-pm.co.uk/assets/img/logo-email-600.png` from the website so every message stays small and the image never arrives as an attachment. The website build copies the logo to that path, so it goes live when the change is merged to `main` and Cloudflare redeploys; install signatures after that, otherwise the old logo shows until the deploy completes. If the path changes, rebuild the signature; do not re-insert the logo as a pasted picture.

Some recipients will see a blank box or "download pictures" prompt until they allow images. This is normal for hosted images and is the trade-off for a clean, lightweight signature.

## Copying the rendered HTML

Mail clients want the rendered signature, not the source code.

1. Open your `signature-<first>-<last>.compiled.html` in a web browser (double-click it, or drag it into Chrome or Edge).
2. Press Ctrl+A (Windows) or Cmd+A (Mac) to select everything, then Ctrl+C or Cmd+C to copy.
3. Paste into the signature editor of your mail client as described below.

If a client offers an "insert HTML" or "source" mode, you can instead open your `signature-<first>-<last>.compiled.html` in a text editor, copy the text between `<body ...>` and `</body>`, and paste it there.

## Outlook (classic desktop, Windows)

1. File > Options > Mail > Signatures.
2. Click New, name it `GBS`.
3. Click in the editing box and paste (Ctrl+V) the rendered signature copied from the browser.
4. Under "Choose default signature", set it for New messages. For Replies/forwards you may also set it, or use the plain-text version to keep threads short.
5. OK to save. Send a test message to yourself and to a Gmail address.

If the pasted layout loses the vertical rule or spacing, Outlook has converted it to its own format. Close Outlook, open `%APPDATA%\Microsoft\Signatures\`, and replace the contents of `GBS.htm` with the contents of your `signature-<first>-<last>.compiled.html`.

## New Outlook (Windows), Outlook on the web and Outlook for Mac

1. Settings (gear icon) > Mail > Compose and reply (web and new Outlook), or Outlook > Settings > Signatures (Mac).
2. Create a new signature named `GBS`.
3. Paste the rendered signature from the browser into the editor.
4. Set it as the default for new messages and, if wanted, replies and forwards. Save.

These clients store the signature in the mailbox, so it follows you between devices. The image stays hosted; nothing is uploaded.

## Gmail (web)

1. Settings (gear icon) > See all settings > General > Signature.
2. Create new, name it `GBS`.
3. Paste the rendered signature from the browser into the box.
4. Under "Signature defaults", select it for new emails and for replies/forwards. Tick "Insert signature before quoted text" if you want it above the thread history.
5. Save Changes at the bottom of the page.

Gmail trims signatures over about 10,000 characters. This one is about 3,300, so it fits.

## Apple Mail (Mac)

1. Mail > Settings > Signatures. Select your GBS account in the left column.
2. Click +, name it `GBS`.
3. Untick "Always match my default message font".
4. Paste the rendered signature from the browser into the right-hand box. The logo appears as a linked image.
5. Close the window to save. In the Choose Signature menu, select `GBS` for the account.

If pasting drops the layout, use the file method: create a dummy signature, quit Mail, find it in `~/Library/Mail/V10/MailData/Signatures/` (the version folder varies), open the newest `.mailsignature` file in a text editor, replace everything after the header lines with the contents of your `signature-<first>-<last>.compiled.html`, lock the file (Get Info > Locked), and reopen Mail.

## iPhone and iPad

iOS Mail only supports a basic signature.

1. Send yourself an email from a computer with the full signature installed.
2. Open it on the phone, press and hold the signature, Select All, Copy.
3. Settings > Mail > Signature (or Apps > Mail > Signature on newer iOS). Select the GBS account, paste. If the paste arrives as plain text, shake the device and choose Undo Change Attributes to restore the formatting.

If the formatted paste will not hold, use `signature.compiled.txt` instead. The Outlook app for iOS and Android takes the HTML version from the mailbox automatically once it is set in Outlook on the web.

## Dark mode

Many clients show mail on a dark background. Expect:

- Text colours may be lightened automatically (sage and ink become pale). This is normal.
- Outlook (Windows) can partially invert colours; the red labels stay red.
- The logo is a transparent PNG. On a dark background the sage lettering keeps roughly 3:1 contrast and remains legible. Do not add a white box behind it.
- The `color-scheme: light` meta in the file asks compliant clients to keep the light version where they can.

Send a test to a colleague on a phone in dark mode before rolling out.

## Please do not

- Add quotes, mottoes, banners, promotional images, award badges or a second logo. The signature is a contact block, not an advert.
- Change the colours, fonts or sizes, or move the legal line. It is a statutory disclosure.
- Paste the logo as an attachment or insert it from a local file. It must stay as the hosted image.
- Add social icons unless the company LinkedIn page is live and listed in `company.json`.

## Fonts

The signature asks for Montserrat (name) and Inter (everything else) with Arial and Helvetica fallbacks. Recipients without those fonts installed see Arial, which is intended. Do not add webfont links; most mail clients block them.
