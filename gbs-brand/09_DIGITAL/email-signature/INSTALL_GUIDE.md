# GBS email signature - installation guide (v1.0)

Files in this folder:

| File | Use |
|---|---|
| `signature.compiled.html` | Personal signature with the details from `company.json` resolved. Install this one. |
| `signature-generic.compiled.html` | Shared-mailbox version (info@, no named person). |
| `signature.compiled.txt` | Plain-text version for text-only mail and ticketing systems. |
| `signature.html`, `signature-generic.html`, `signature.txt` | Token sources. Do not install these; they still contain `{{company.*}}` placeholders. |
| `build-signature.mjs` | Rebuilds the compiled files from `company.json` (`node 09_DIGITAL/email-signature/build-signature.mjs`). |
| `logo-email-600.png` | The logo the signature loads. The website serves it at `https://gbs-pm.co.uk/assets/img/logo-email-600.png`. |
| `preview.png` / `preview-local.png` | Review renders only. |

For a second person, copy `signature.html` details or add them to `company.json` under `people` and rebuild.

## Before you start: the hosted logo

The signature does not embed the logo. It loads `https://gbs-pm.co.uk/assets/img/logo-email-600.png` from the website so every message stays small and the image never arrives as an attachment. Upload `logo-email-600.png` to that exact path on the web server before anyone installs the signature. If the path changes, rebuild the signature; do not re-insert the logo as a pasted picture.

Some recipients will see a blank box or "download pictures" prompt until they allow images. This is normal for hosted images and is the trade-off for a clean, lightweight signature.

## Copying the rendered HTML

Mail clients want the rendered signature, not the source code.

1. Open `signature.compiled.html` in a web browser (double-click it, or drag it into Chrome or Edge).
2. Press Ctrl+A (Windows) or Cmd+A (Mac) to select everything, then Ctrl+C or Cmd+C to copy.
3. Paste into the signature editor of your mail client as described below.

If a client offers an "insert HTML" or "source" mode, you can instead open `signature.compiled.html` in a text editor, copy the text between `<body ...>` and `</body>`, and paste it there.

## Outlook (classic desktop, Windows)

1. File > Options > Mail > Signatures.
2. Click New, name it `GBS`.
3. Click in the editing box and paste (Ctrl+V) the rendered signature copied from the browser.
4. Under "Choose default signature", set it for New messages. For Replies/forwards you may also set it, or use the plain-text version to keep threads short.
5. OK to save. Send a test message to yourself and to a Gmail address.

If the pasted layout loses the vertical rule or spacing, Outlook has converted it to its own format. Close Outlook, open `%APPDATA%\Microsoft\Signatures\`, and replace the contents of `GBS.htm` with the contents of `signature.compiled.html`.

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

If pasting drops the layout, use the file method: create a dummy signature, quit Mail, find it in `~/Library/Mail/V10/MailData/Signatures/` (the version folder varies), open the newest `.mailsignature` file in a text editor, replace everything after the header lines with the contents of `signature.compiled.html`, lock the file (Get Info > Locked), and reopen Mail.

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
