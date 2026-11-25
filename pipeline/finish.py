"""Loudness mastering, automated quality control and delivery packaging.

Usage: python pipeline/finish.py <storyboard.json> <rendered.mp4> <build_dir> <deliver_dir>
Exit code 1 if any hard QC check fails (the workflow then marks the run red).
"""
import json
import re
import subprocess
import sys
import urllib.request
from datetime import date
from pathlib import Path

TARGET_LUFS = -14.0


def run(*args: str) -> str:
    p = subprocess.run(args, capture_output=True, text=True)
    if p.returncode:
        raise SystemExit(f"command failed: {' '.join(args[:3])}…\n{p.stderr[-800:]}")
    return p.stdout + p.stderr


def probe(path: Path) -> dict:
    return json.loads(run("ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", "-show_format", str(path)))


def master(src: Path, dst: Path) -> dict:
    """Final encode: broadcast-range yuv420p H.264 + two-pass EBU R128 loudness."""
    first = run("ffmpeg", "-hide_banner", "-i", str(src), "-af", f"loudnorm=I={TARGET_LUFS}:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-")
    m = json.loads(re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", first, re.S)[-1])
    af = (
        f"loudnorm=I={TARGET_LUFS}:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
        f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
    )
    vs = next(x for x in probe(src)["streams"] if x["codec_type"] == "video")
    # Remotion may hand over full-range (yuvj420p / pc) or already limited-range video:
    # convert only what needs converting, or black turns grey (B&W identity rule).
    in_range = "full" if vs.get("pix_fmt", "").startswith("yuvj") or vs.get("color_range") == "pc" else "tv"
    run(
        "ffmpeg", "-y", "-hide_banner", "-i", str(src),
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-maxrate", "16M", "-bufsize", "32M",
        "-vf", f"scale=in_range={in_range}:out_range=tv,format=yuv420p", "-color_range", "tv", "-colorspace", "bt709",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-profile:v", "high", "-level", "4.2",
        "-af", af, "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(dst),
    )
    return m


def measure_lufs(path: Path) -> float:
    out = run("ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128", "-f", "null", "-")
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", out)[-1])


def black_and_frozen(path: Path) -> tuple[float, float]:
    out = run("ffmpeg", "-hide_banner", "-i", str(path), "-vf", "blackdetect=d=0.5:pix_th=0.04,freezedetect=n=0.001:d=3", "-an", "-f", "null", "-")
    black = sum(float(x) for x in re.findall(r"black_duration:([\d.]+)", out))
    frozen = sum(float(x) for x in re.findall(r"freeze_duration: ([\d.]+)", out))
    return black, frozen


def check_doi(doi: str) -> bool:
    try:
        req = urllib.request.Request(f"https://doi.org/api/handles/{doi}", headers={"User-Agent": "mente-studio-qc"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read()).get("responseCode") == 1
    except Exception:
        return False


def main() -> None:
    sb_path, rendered, build, deliver = (Path(a) for a in sys.argv[1:5])
    sb = json.loads(sb_path.read_text())
    deliver.mkdir(parents=True, exist_ok=True)
    final = deliver / f"{sb['id']}.mp4"
    loud = master(rendered, final)

    info = probe(final)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    a = [s for s in info["streams"] if s["codec_type"] == "audio"]
    dur = float(info["format"]["duration"])
    lufs = measure_lufs(final)
    black, frozen = black_and_frozen(final)
    meta = json.loads((build / "scenes.json").read_text())
    captions = json.loads((build / "captions.json").read_text())
    script_words = sum(len(s["narration"].split()) for s in sb["scenes"])

    checks = [
        ("dimensions 1080x1920", v["width"] == 1080 and v["height"] == 1920, f"{v['width']}x{v['height']}", True),
        ("frame rate 30", v["r_frame_rate"] in ("30/1", "30000/1001"), v["r_frame_rate"], True),
        ("codec h264 / yuv420p", v["codec_name"] == "h264" and v.get("pix_fmt") == "yuv420p", f"{v['codec_name']}/{v.get('pix_fmt')}", True),
        ("audio track present", len(a) == 1, f"{len(a)} track(s)", True),
        ("duration 30–90 s", 30 <= dur <= 90, f"{dur:.1f}s", True),
        ("duration ≥ 61 s (TikTok rewards rule)", dur >= 61, f"{dur:.1f}s", False),
        (f"loudness {TARGET_LUFS} ±1.5 LUFS", abs(lufs - TARGET_LUFS) <= 1.5, f"{lufs:.1f} LUFS", meta["engine"] != "estimate"),
        ("no black segments > 0.5 s", black < 0.5, f"{black:.1f}s black", True),
        ("no frozen picture > 3 s", frozen < 3, f"{frozen:.1f}s frozen", False),
        ("every script word captioned", len(captions) == script_words, f"{len(captions)}/{script_words}", True),
        ("file size < 287 MB (TikTok upload)", final.stat().st_size < 287e6, f"{final.stat().st_size / 1e6:.1f} MB", True),
    ]
    # B&W identity: the backdrop must decode as near-black (#050505 grid), never grey
    run("ffmpeg", "-y", "-ss", str(dur / 2), "-i", str(final), "-frames:v", "1", str(build / "qc_mid.png"))
    from PIL import Image
    px = Image.open(build / "qc_mid.png").convert("L").getpixel((12, 12))
    checks.append(("background near-black (≤ 9/255)", px <= 9, f"{px}/255", True))
    # hook legible on frame 0: something bright on screen besides captions
    run("ffmpeg", "-y", "-i", str(final), "-frames:v", "1", str(build / "qc_f0.png"))
    f0 = Image.open(build / "qc_f0.png").convert("L").crop((0, 170, 1080, 1180))
    lit = sum(1 for v_ in f0.getdata() if v_ > 180)
    checks.append(("hook visible on frame 0", lit > 1500, f"{lit} bright px", True))
    for s in sb["sources"]:
        if s.get("doi"):
            ok = check_doi(s["doi"])
            checks.append((f"DOI resolves: {s['doi']}", ok, "ok" if ok else "not found / offline", False))

    # Deliverables: thumbnail, caption text, sources, storyboard, QC report
    run("ffmpeg", "-y", "-ss", "1.8", "-i", str(final), "-frames:v", "1", "-q:v", "2", str(deliver / "thumbnail.jpg"))
    tags = " ".join(sb["social"]["hashtags"])
    (deliver / "caption.txt").write_text(f"{sb['social']['caption']}\n\n{tags}\n")
    (deliver / "sources.md").write_text(
        f"# Fuentes — {sb['title']}\n\n" + "\n".join(f"- {s['citation']}" + (f" https://doi.org/{s['doi']}" if s.get('doi') else f" {s.get('url', '')}") + f"\n  - Respalda: {s['supports']}" for s in sb["sources"]) + "\n"
    )
    (deliver / "storyboard.json").write_text(json.dumps(sb, ensure_ascii=False, indent=2))

    hard_fail = [c for c in checks if c[3] and not c[1]]
    report = {
        "id": sb["id"],
        "date": date.today().isoformat(),
        "voiceEngine": meta["engine"],
        "durationSec": round(dur, 2),
        "lufs": lufs,
        "passed": not hard_fail,
        "checks": [{"check": c[0], "ok": c[1], "value": c[2], "blocking": c[3]} for c in checks],
        "publishChecklist": ["Activar la etiqueta «Contenido generado por IA»", "Pegar caption.txt", "Fijar sources.md como primer comentario"],
    }
    (deliver / "qc.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
    md = [f"## QC — {sb['id']} ({'PASS' if report['passed'] else 'FAIL'})", "", "| Check | Result | Value |", "|---|---|---|"]
    md += [f"| {c[0]} | {'✅' if c[1] else ('❌' if c[3] else '⚠️')} | {c[2]} |" for c in checks]
    (deliver / "qc.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))
    sys.exit(1 if hard_fail else 0)


if __name__ == "__main__":
    main()
