#!/usr/bin/env bash
# Builds the vertical 1080x1920 Reels cut from the 16:9 master:
# soft colour-wash background, rounded and shadowed 16:9 frame, optional meme caption,
# and a large URL lower third over the end card.
#   reel/compose.sh            -> out/coffeespot-ad-9x16.mp4 (with "Did Claude cook?" caption)
#   reel/compose.sh --clean    -> out/coffeespot-ad-9x16-clean.mp4
set -euo pipefail
cd "$(dirname "$0")/.."
SRC=out/coffeespot-ad-16x9.mp4
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$SRC")
VY=650                       # top of the 16:9 frame inside the vertical canvas
LT_AT=34.3                   # lower third fades in once the end card has landed
CAP="[c][3:v]overlay=x=0:y=360[c2]"
OUT=out/coffeespot-ad-9x16.mp4
if [[ "${1:-}" == "--clean" ]]; then CAP="[c]null[c2]"; OUT=out/coffeespot-ad-9x16-clean.mp4; fi
ffmpeg -y -loglevel error -i "$SRC" -loop 1 -i reel/mask.png -loop 1 -i reel/shadow.png -loop 1 -i reel/caption.png -loop 1 -i reel/lowerthird.png -filter_complex "
  [0:v]split=2[a][b];
  [a]scale=-2:1920,crop=1080:1920,scale=8:14:flags=area,scale=1080:1920:flags=bicubic,gblur=sigma=90:steps=2,format=rgba[bl];
  color=c=0xf5efe6@0.4:s=1080x1920:d=$DUR,format=rgba[cr];
  [bl][cr]overlay=shortest=1[bg];
  [b]scale=1056:594:flags=lanczos,format=rgba[v];[1:v]format=gray[m];[v][m]alphamerge[vr];
  [bg][2:v]overlay=x=-78:y=$((VY-90))[bg2];
  [bg2][vr]overlay=x=12:y=$VY[c];
  $CAP;
  [4:v]format=rgba,fade=t=in:st=$LT_AT:d=0.5:alpha=1[lt];
  [c2][lt]overlay=x=0:y=1290[o]" -map "[o]" -t "$DUR" \
  -r 30 -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -movflags +faststart "$OUT"
echo "wrote $OUT"
