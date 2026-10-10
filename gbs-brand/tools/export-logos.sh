#!/usr/bin/env bash
# Export PNG logo set + favicons from the SVG masters. Requires: node + playwright, python3 + Pillow.
set -euo pipefail
cd "$(dirname "$0")/.."
SVG=01_LOGO_MASTER/svg; PNG=01_LOGO_MASTER/png; FAV=01_LOGO_MASTER/favicon
rm -rf "$PNG" "$FAV"; mkdir -p "$PNG" "$FAV"
node tools/svg2png.mjs "$PNG" 400,600,1200,2400,4000 \
  $SVG/GBS_HORIZON_LOGO_PRIMARY_SAGE-RED_v1.0.svg $SVG/GBS_HORIZON_LOGO_PRIMARY-NOSTRAP_SAGE-RED_v1.0.svg \
  $SVG/GBS_HORIZON_LOGO_REVERSED_OFFWHITE-RED_v1.0.svg $SVG/GBS_HORIZON_LOGO_REVERSED-NOSTRAP_OFFWHITE-RED_v1.0.svg \
  $SVG/GBS_HORIZON_LOGO_MONO_SAGE_v1.0.svg $SVG/GBS_HORIZON_LOGO_MONO_WHITE_v1.0.svg $SVG/GBS_HORIZON_LOGO_MONO_BLACK_v1.0.svg \
  $SVG/GBS_HORIZON_LOGO_WORDMARK_SAGE-RED_v1.0.svg $SVG/GBS_HORIZON_LOGO_STRIP_SAGE-RED_v1.0.svg $SVG/GBS_HORIZON_LOGO_STRIP_OFFWHITE-RED_v1.0.svg >/dev/null
node tools/svg2png.mjs "$PNG" 256,512,1024,2048 \
  $SVG/GBS_HORIZON_ICON_SAGE-RED_v1.0.svg $SVG/GBS_HORIZON_ICON_OFFWHITE-RED_v1.0.svg $SVG/GBS_HORIZON_ICON_MONO_SAGE_v1.0.svg \
  $SVG/GBS_HORIZON_ICON_MONO_WHITE_v1.0.svg $SVG/GBS_HORIZON_ICON_SIMPLIFIED_SAGE-RED_v1.0.svg \
  $SVG/GBS_HORIZON_AVATAR_SQUARE_ON-SAGE_v1.0.svg $SVG/GBS_HORIZON_AVATAR_SQUARE_ON-OFFWHITE_v1.0.svg >/dev/null
# favicons from the sage avatar
node tools/svg2png.mjs "$FAV" 16,32,48,180,192,512 $SVG/GBS_HORIZON_AVATAR_SQUARE_ON-SAGE_v1.0.svg >/dev/null
( cd "$FAV" && for s in 16 32 48 180 192 512; do mv "GBS_HORIZON_AVATAR_SQUARE_ON-SAGE_${s}px_v1.0.png" "favicon-${s}.png"; done
  mv favicon-180.png apple-touch-icon.png; mv favicon-192.png icon-192.png; mv favicon-512.png icon-512.png
  python3 -I -c "from PIL import Image; im=Image.open('favicon-48.png'); im.save('favicon.ico', sizes=[(16,16),(32,32),(48,48)])"
  cp ../svg/GBS_HORIZON_AVATAR_SQUARE_ON-SAGE_v1.0.svg favicon.svg )
echo "PNG exports: $(ls $PNG | wc -l) files; favicons: $(ls $FAV | wc -l) files"
