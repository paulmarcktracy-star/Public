"""Narration: one audio file per scene, then concatenated.

Engines:
  kokoro      open-source (Apache-2.0), runs on CPU, free
  piper       open-source, very fast on CPU, free (es_MX voices)
  elevenlabs  paid API, needs ELEVENLABS_API_KEY (never logged)
  estimate    silent placeholder with estimated timing (for offline tests)

Usage: python pipeline/voice.py <storyboard.json> <engine> <out_dir>
Writes <out_dir>/voice.wav and <out_dir>/scenes.json
"""
import json
import os
import subprocess
import sys
import urllib.request
import wave
from pathlib import Path

GAP = 0.3  # seconds of air between scenes
SR = 48000
MODELS = Path(os.environ.get("MODELS_DIR", Path.home() / ".cache" / "mente-studio"))


def sh(*args: str) -> None:
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def duration(path: Path) -> float:
    with wave.open(str(path)) as w:
        return w.getnframes() / w.getframerate()


def to_standard(src: Path, dst: Path) -> None:
    """48 kHz mono, trim leading/trailing silence, gentle voice EQ."""
    af = (
        "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,"
        "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse,"
        "highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120"
    )
    sh("ffmpeg", "-y", "-i", str(src), "-af", af, "-ar", str(SR), "-ac", "1", str(dst))


# ---------------------------------------------------------------- engines
def tts_estimate(text: str, out: Path, speed: float) -> None:
    secs = max(1.2, len(text.split()) / (2.55 * speed))
    sh("ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono", "-t", f"{secs:.2f}", str(out))


_kokoro = None


KOKORO_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"


def tts_kokoro(text: str, out: Path, speed: float) -> None:
    """Kokoro-82M (Apache-2.0) via ONNX: CPU only, weights from GitHub releases."""
    global _kokoro
    import soundfile as sf
    from kokoro_onnx import Kokoro

    if _kokoro is None:
        MODELS.mkdir(parents=True, exist_ok=True)
        for f in ("kokoro-v1.0.onnx", "voices-v1.0.bin"):
            if not (MODELS / f).exists():
                urllib.request.urlretrieve(KOKORO_URL + f, MODELS / f)
        _kokoro = Kokoro(str(MODELS / "kokoro-v1.0.onnx"), str(MODELS / "voices-v1.0.bin"))
    name = os.environ.get("KOKORO_VOICE", "ef_dora+af_heart")
    # "a+b" blends two voices 50/50 (catalogue of tested voices in VOICES.md)
    voice = name if "+" not in name else sum(_kokoro.get_voice_style(v) for v in name.split("+")) / len(name.split("+"))
    audio, sr = _kokoro.create(text, voice=voice, speed=speed, lang="es")
    sf.write(str(out), audio, sr)


def tts_piper(text: str, out: Path, speed: float) -> None:
    from piper import PiperVoice, SynthesisConfig

    name = os.environ.get("PIPER_VOICE", "es_MX-claude-high")
    lang, region = name.split("-")[0].split("_")[0], name.split("-")[0]
    spk, quality = name.split("-")[1], name.split("-")[2]
    base = f"https://huggingface.co/rhasspy/piper-voices/resolve/main/{lang}/{region}/{spk}/{quality}/{name}"
    MODELS.mkdir(parents=True, exist_ok=True)
    model = MODELS / f"{name}.onnx"
    for suffix in ("", ".json"):
        p = Path(str(model) + suffix)
        if not p.exists():
            urllib.request.urlretrieve(base + ".onnx" + suffix, p)
    voice = PiperVoice.load(str(model))
    with wave.open(str(out), "wb") as w:
        voice.synthesize_wav(text, w, syn_config=SynthesisConfig(length_scale=1 / speed))


def tts_elevenlabs(text: str, out: Path, speed: float, prev: str, nxt: str) -> None:
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise SystemExit("ELEVENLABS_API_KEY is not set (add it as a GitHub secret)")
    voice_id = os.environ.get("ELEVENLABS_VOICE_ID", "")
    if not voice_id:
        raise SystemExit("ELEVENLABS_VOICE_ID is not set")
    body = json.dumps(
        {
            "text": text,
            "model_id": os.environ.get("ELEVENLABS_MODEL", "eleven_multilingual_v2"),
            "previous_text": prev,
            "next_text": nxt,
            "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.15, "speed": speed},
        }
    ).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128",
        data=body,
        headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
    )
    mp3 = out.with_suffix(".mp3")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            mp3.write_bytes(r.read())
    except urllib.error.HTTPError as e:  # never echo the key
        raise SystemExit(f"ElevenLabs request failed: HTTP {e.code}") from None
    sh("ffmpeg", "-y", "-i", str(mp3), str(out))


# ---------------------------------------------------------------- main
def main() -> None:
    sb_path, engine, out_dir = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
    speed = float(os.environ.get("VOICE_SPEED", "0.9"))
    sb = json.loads(sb_path.read_text())
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = out_dir / "voice"
    raw_dir.mkdir(exist_ok=True)

    scenes = sb["scenes"]
    parts: list[Path] = []
    timing = []
    cursor = 0.0
    for i, sc in enumerate(scenes):
        raw = raw_dir / f"{sc['id']}_raw.wav"
        clean = raw_dir / f"{sc['id']}.wav"
        text = sc["narration"]
        if engine == "estimate":
            tts_estimate(text, raw, speed)
            sh("ffmpeg", "-y", "-i", str(raw), "-ar", str(SR), "-ac", "1", str(clean))
        else:
            if engine == "kokoro":
                tts_kokoro(text, raw, speed)
            elif engine == "piper":
                tts_piper(text, raw, speed)
            elif engine == "elevenlabs":
                prev = scenes[i - 1]["narration"] if i else ""
                nxt = scenes[i + 1]["narration"] if i + 1 < len(scenes) else ""
                tts_elevenlabs(text, raw, speed, prev, nxt)
            else:
                raise SystemExit(f"unknown engine {engine}")
            to_standard(raw, clean)
        d = duration(clean)
        shots = [len(sh["text"].split()) for sh in sc.get("shots", [])] or [len(text.split())]
        timing.append({"id": sc["id"], "start": round(cursor, 3), "duration": round(d, 3), "text": text, "shots": shots})
        parts.append(clean)
        cursor += d + GAP
        print(f"  {sc['id']}: {d:.2f}s")

    # Concatenate with gaps
    gap = raw_dir / "gap.wav"
    sh("ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono", "-t", str(GAP), str(gap))
    listing = raw_dir / "concat.txt"
    lines = []
    for i, p in enumerate(parts):
        lines.append(f"file '{p.resolve()}'")
        if i < len(parts) - 1:
            lines.append(f"file '{gap.resolve()}'")
    listing.write_text("\n".join(lines))
    sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy", str(out_dir / "voice.wav"))

    (out_dir / "scenes.json").write_text(json.dumps({"engine": engine, "gap": GAP, "scenes": timing}, ensure_ascii=False, indent=2))
    print(f"voice: {cursor - GAP:.2f}s total with engine={engine}")


if __name__ == "__main__":
    main()
