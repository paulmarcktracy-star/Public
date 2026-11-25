#!/usr/bin/env bash
# One storyboard -> one finished, QC'd, packaged video.
# Usage: pipeline/produce.sh storyboards/<id>.json [engine]   (engine: kokoro | piper | elevenlabs | estimate)
set -euo pipefail
SB="$1"
ENGINE="${2:-${VOICE_ENGINE:-kokoro}}"
ID="$(basename "$SB" .json)"
BUILD_REL="build/$ID"
BUILD="public/$BUILD_REL"
DELIVER="output/$ID"
T0=$(date +%s)
step() { echo; echo "▶ $1  (+$(( $(date +%s) - T0 ))s)"; }

step "validate"
npx tsx pipeline/validate.ts "$SB"

step "sound library + score"
python3 pipeline/sfx.py
[ -f "public/audio/music/$(python3 -c "import json;print(json.load(open('$SB')).get('music','esperanza'))").wav" ] || python3 pipeline/music.py

step "voice ($ENGINE)"
python3 pipeline/voice.py "$SB" "$ENGINE" "$BUILD"

step "captions"
python3 pipeline/captions.py "$BUILD"

step "timeline"
npx tsx pipeline/timeline.ts "$SB" "$BUILD_REL"

step "render"
mkdir -p out
npx remotion render src/index.ts PsychVideo "out/$ID.mp4" --props="$BUILD/props.json" \
  --concurrency="${RENDER_CONCURRENCY:-$(nproc)}" --log=error

step "master + QC + package"
python3 pipeline/finish.py "$SB" "out/$ID.mp4" "$BUILD" "$DELIVER"

echo "✔ $ID done in $(( $(date +%s) - T0 ))s → $DELIVER"
