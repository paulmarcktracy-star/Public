"""Shared storyboard helpers."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "storyboards"


# videos produced before the cinematic camera (2026-11-25 05:40): keep their look
CLASSIC = {"001-pensar-demasiado", "002-sesgo-confirmacion", "004-efecto-espectador", "012-miedo-rechazo", "019-aversion-perdida"}


def write(*videos):
    for v in videos:
        if v["id"] in CLASSIC:
            v["cameraStyle"] = "classic"
        (OUT / f"{v['id']}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1))
        print("wrote", v["id"])


def stage(**kw):
    kw["type"] = "stage"
    return kw


def fig(pose, x=540, **kw):
    return {"pose": pose, "x": x, **kw}


def crowd(xs, pose="stand", scale=0.78, opacity=0.5, facing=None, **kw):
    return [fig(pose, x, scale=scale, opacity=opacity, facing=(facing[i] if facing else (1 if i % 2 else -1)), **kw) for i, x in enumerate(xs)]


def prop(kind, x, y, **kw):
    return {"kind": kind, "x": x, "y": y, **kw}


def text(content, y=330, size=72, **kw):
    return {"content": content, "y": y, "size": size, **kw}


def cam(fz=1.0, tz=1.07, x=540, y=760, pan=0):
    return {"fromZoom": fz, "toZoom": tz, "x": x, "y": y, "panX": pan}


def shot(t, visual, sfx="none"):
    return {"text": t, "visual": visual, "sfx": sfx}


def scene(id_, beat, shots):
    return {"id": id_, "beat": beat, "narration": " ".join(s["text"] for s in shots), "shots": shots}


def sb(id_, title, pillar, sources, scenes, caption, hashtags):
    return {
        "id": id_, "title": title, "pillar": pillar, "format": "secondPerson", "evidenceLevel": "solid",
        "music": "meaningful", "sources": sources, "scenes": scenes,
        "social": {"caption": caption, "hashtags": hashtags, "aiLabel": True},
    }


