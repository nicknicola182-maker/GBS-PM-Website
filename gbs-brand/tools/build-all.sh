#!/usr/bin/env bash
# Regenerates every output in the pack from company.json + sources. Run from anywhere.
# Requires: node 18+ with playwright (npm i inside tools/), python3 with fonttools + Pillow + pypdf, poppler-utils (pdftoppm) for QA previews.
set -euo pipefail
cd "$(dirname "$0")/.."
echo "== 1. Logo masters (SVG) and exports (PNG, favicon)"; python3 -I tools/build-logos.py >/dev/null && bash tools/export-logos.sh
echo "== 2. Website"; node tools/build-site.mjs
echo "== 3. Email signature (compiled)"; [ -f 09_DIGITAL/email-signature/build-signature.mjs ] && node 09_DIGITAL/email-signature/build-signature.mjs || true
echo "== 4. Print, workwear, vehicle, signage, merch and digital renders"
for m in tools/manifests/*.json; do echo "-- $m"; node tools/render.mjs "$m"; done
echo "== 5. Website rebuild (picks up the Open Graph image from 09_DIGITAL/social)"; node tools/build-site.mjs >/dev/null
echo "== Done. Outputs are committed alongside sources; see README.md."
