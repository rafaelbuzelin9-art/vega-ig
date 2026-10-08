#!/bin/bash
# uso: ./render.sh [n...]  — exporta slides 1080x1350 (2x + reduz) para render/
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LISTA=${*:-1 2 3 4 5 6 7 8 9 10}; for n in $LISTA; do
  out="$PWD/render/slide-$n@2x.png"; rm -f "$out"; prof=$(mktemp -d)
  "$CH" --headless=old --disable-gpu --hide-scrollbars --force-device-scale-factor=2 --user-data-dir="$prof" \
    --window-size=1080,1350 --virtual-time-budget=4000 --screenshot="$out" "http://localhost:8791/?s=$n" >/dev/null 2>&1 &
  pid=$!; for i in $(seq 60); do [ -s "$out" ] && break; sleep 0.5; done; sleep 0.5; kill $pid 2>/dev/null; rm -rf "$prof"
  sips -z 1350 1080 "$out" --out "$PWD/render/slide-$n.png" >/dev/null && echo "ok $n" || echo "FALHOU $n"
done
