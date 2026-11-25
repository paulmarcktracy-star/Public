"""Word-level captions synchronised to the narration.

With real audio, faster-whisper gives a timestamp for every spoken word; those
timestamps are then mapped back onto the SCRIPT's words, so the on-screen
spelling is always the script's (no transcription typos).
With the 'estimate' engine, words are spread across each scene by length.

Usage: python pipeline/captions.py <out_dir>
Reads <out_dir>/scenes.json + voice/<scene>.wav, writes <out_dir>/captions.json
"""
import difflib
import json
import subprocess
import os
import re
import sys
import unicodedata
from pathlib import Path


def norm(w: str) -> str:
    w = unicodedata.normalize("NFD", w.lower())
    w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9ñ]", "", w)


def spread(words: list[str], start: float, dur: float) -> list[tuple[float, float]]:
    weights = [max(2, len(norm(w))) + 1.5 for w in words]
    total = sum(weights)
    out, t = [], start
    for wt in weights:
        d = dur * wt / total
        out.append((t, t + d))
        t += d
    return out


def silences(wav: Path, min_len: float = 0.09) -> list[tuple[float, float]]:
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(wav), "-af", f"silencedetect=noise=-38dB:d={min_len}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    return list(zip(starts, ends))


def pause_aligned(words: list[str], wav: Path, start: float, dur: float) -> list[tuple[float, float]]:
    """No ASR available: split the script at punctuation, snap each phrase break to the
    nearest real pause in the audio, then spread words inside each phrase by length."""
    phrases, cur = [], []
    for w in words:
        cur.append(w)
        if re.search(r"[.,;:?!¿¡…]$", w):
            phrases.append(cur)
            cur = []
    if cur:
        phrases.append(cur)
    gaps = silences(wav)
    weights = [sum(max(2, len(norm(w))) + 1.5 for w in ph) for ph in phrases]
    total = sum(weights)
    bounds, acc, used = [0.0], 0.0, set()
    for wt in weights[:-1]:
        acc += wt / total * dur
        cand = [(abs((a + b) / 2 - acc), i) for i, (a, b) in enumerate(gaps) if i not in used]
        if cand and min(cand)[0] < 0.6:
            i = min(cand)[1]
            used.add(i)
            bounds.append((gaps[i][0] + gaps[i][1]) / 2)
        else:
            bounds.append(acc)
    bounds.append(dur)
    times = []
    for ph, a, b in zip(phrases, bounds[:-1], bounds[1:]):
        times += spread(ph, start + a, max(0.1, b - a - 0.05))
    return times


def align(script: list[str], heard: list[tuple[str, float, float]], start: float, dur: float) -> list[tuple[float, float]]:
    a = [norm(w) for w in script]
    b = [norm(h[0]) for h in heard]
    times: list[tuple[float, float] | None] = [None] * len(script)
    for blk in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            _, s, e = heard[blk.b + k]
            times[blk.a + k] = (start + s, start + e)
    # fill gaps by interpolating between known neighbours
    i = 0
    while i < len(times):
        if times[i] is None:
            j = i
            while j < len(times) and times[j] is None:
                j += 1
            left = times[i - 1][1] if i > 0 and times[i - 1] else start
            right = times[j][0] if j < len(times) and times[j] else start + dur
            filled = spread(script[i:j], left, max(0.05, right - left))
            times[i:j] = filled
            i = j
        else:
            i += 1
    return times  # type: ignore[return-value]


def main() -> None:
    out_dir = Path(sys.argv[1])
    meta = json.loads((out_dir / "scenes.json").read_text())
    model = None
    if meta["engine"] != "estimate":
        try:
            from faster_whisper import WhisperModel

            model = WhisperModel(os.environ.get("WHISPER_MODEL", "small"), device="cpu", compute_type="int8")
        except Exception as e:  # offline or not installed: fall back to pause alignment
            print(f"  whisper unavailable ({type(e).__name__}), using pause-aligned timing")

    captions = []
    for sc in meta["scenes"]:
        words = sc["text"].split()
        if model is None and meta["engine"] == "estimate":
            times = spread(words, sc["start"], sc["duration"])
        elif model is None:
            times = pause_aligned(words, out_dir / "voice" / f"{sc['id']}.wav", sc["start"], sc["duration"])
        else:
            wav = out_dir / "voice" / f"{sc['id']}.wav"
            try:
                import soundfile as sf
                audio, sr = sf.read(str(wav), dtype="float32")
                if audio.ndim > 1:
                    audio = audio.mean(axis=1)
                if sr != 16000:
                    from scipy.signal import resample_poly
                    audio = resample_poly(audio, 16000, sr).astype("float32")
                segs, _ = model.transcribe(audio, language="es", word_timestamps=True, initial_prompt=sc["text"])
                heard = [(w.word.strip(), w.start, w.end) for s in segs for w in (s.words or [])]
                times = align(words, heard, sc["start"], sc["duration"])
            except Exception as e:  # never block production on the aligner
                print(f"  whisper failed on {sc['id']} ({type(e).__name__}: {e}), using pause-aligned timing")
                times = pause_aligned(words, wav, sc["start"], sc["duration"])
        breaks, acc = set(), 0
        for n in sc.get("shots", [len(words)]):
            acc += n
            breaks.add(acc - 1)  # each shot starts a fresh caption page
        for k, (w, (s, e)) in enumerate(zip(words, times)):
            item = {"text": " " + w, "startMs": round(s * 1000), "endMs": round(e * 1000), "timestampMs": round((s + e) * 500), "confidence": None}
            if k in breaks:
                item["pageBreakAfter"] = True
            captions.append(item)
    captions[0]["text"] = captions[0]["text"].lstrip()
    (out_dir / "captions.json").write_text(json.dumps(captions, ensure_ascii=False, indent=1))
    print(f"captions: {len(captions)} words")


if __name__ == "__main__":
    main()
