#!/usr/bin/env bash
# Builds the vertical 1080x1920 Reels cut from the 16:9 master:
# blurred fill background + rounded, shadowed 16:9 frame + optional meme caption.
#   reel/compose.sh            -> out/coffeespot-ad-9x16.mp4 (with caption)
#   reel/compose.sh --clean    -> out/coffeespot-ad-9x16-clean.mp4
set -euo pipefail
cd "$(dirname "$0")/.."
SRC=out/coffeespot-ad-16x9.mp4
VY=660                      # top of the 16:9 frame inside the vertical canvas
CAP="[3:v]overlay=x=0:y=372"
OUT=out/coffeespot-ad-9x16.mp4
if [[ "${1:-}" == "--clean" ]]; then CAP="null"; OUT=out/coffeespot-ad-9x16-clean.mp4; fi
ffmpeg -y -loglevel error -i "$SRC" -loop 1 -i reel/mask.png -loop 1 -i reel/shadow.png -loop 1 -i reel/caption.png -filter_complex "
  [0:v]split=2[a][b];
  [a]scale=-2:1920,crop=1080:1920,gblur=sigma=42,eq=brightness=-0.035:saturation=1.08[bg];
  [b]scale=1040:585:flags=lanczos,format=rgba[v];[1:v]format=gray[m];[v][m]alphamerge[vr];
  [bg][2:v]overlay=x=-70:y=$((VY-90))[bg2];
  [bg2][vr]overlay=x=20:y=$VY[c];
  [c]${CAP}[o]" -map "[o]" -t "$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$SRC")" \
  -r 30 -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -movflags +faststart "$OUT"
echo "wrote $OUT"
