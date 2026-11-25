"""Event-driven sound design + mix bus (owner rule: premium, subtle, frame-synced SFX).

Reads the timeline (props.json) and derives every sound from the SAME timing rules the
animations use (src/scenes/Stage.tsx), so each footstep lands on a foot contact, each pop on
an appearance, each pencil stroke on a line being drawn.

Writes, next to props.json:
  fx.wav     every micro-SFX layer (+ a very low room-tone texture), ducked lightly under the voice
  music.wav  the score, looped to length, faded, ducked under the voice (sidechain)
and points the timeline at them (fxSrc, musicSrc, musicGain=1).

Usage: python3 pipeline/mix.py public/build/<id>
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import butter, fftconvolve, resample_poly, sosfilt

SR = 48000
ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
FPS = 30
OVERLAP = 10  # VIDEO.sceneOverlapFrames
HOOK_LEAD = 12  # VIDEO.hookLeadFrames: the first shot is pre-rolled
WALK_PERIOD = 4.2  # Stage.tsx: ph = sin(frame / 4.2)


def db(x: float) -> float:
    return 10 ** (x / 20)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], btype="band", fs=SR, output="sos"), x)


def lp(x, f, order=2):
    return sosfilt(butter(order, f, btype="low", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, btype="high", fs=SR, output="sos"), x)


def tt(sec):
    return np.arange(int(sec * SR)) / SR


_ir_cache: dict[float, np.ndarray] = {}


def room(x, size=0.6, mix=0.18, seed=3):
    """Small, dark room: glues the micro sounds together without washing them out."""
    if size not in _ir_cache:
        r = np.random.default_rng(seed)
        n = int(SR * size)
        _ir_cache[size] = lp(r.standard_normal(n) * np.exp(-np.linspace(0, 7, n)), 5000) * 0.08
    wet = fftconvolve(x, _ir_cache[size])[: len(x) + int(SR * size)]
    out = np.zeros(len(wet))
    out[: len(x)] += x
    return out * (1 - mix) + wet * mix


def norm(x, peak_db):
    m = np.max(np.abs(x)) or 1.0
    return x / m * db(peak_db)


# ---------------------------------------------------------------- sound palette
def footstep(r):
    """Soft heel-toe on a hard floor: low thump + short scuff, a little different every step."""
    k = 1 + r.uniform(-0.06, 0.06)
    t = tt(0.22)
    thump = np.sin(2 * np.pi * 95 * k * t) * np.exp(-t * 55)
    scuff = bp(r.standard_normal(len(t)), 900 * k, 4200 * k) * np.exp(-t * 70)
    toe = np.zeros(len(t))
    d = int(SR * r.uniform(0.045, 0.06))
    toe[d:] = bp(r.standard_normal(len(t) - d), 1500, 5000) * np.exp(-t[: len(t) - d] * 90) * 0.5
    return norm(lp(thump * 0.9 + scuff * 0.35 + toe * 0.3, 6000), -30 + r.uniform(-1.5, 1.5))


def pop_soft(r):
    t = tt(0.16)
    f = 520 * (1 + r.uniform(-0.05, 0.05)) + 380 * np.exp(-t * 60)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 34)
    air = hp(r.standard_normal(len(t)), 4000) * np.exp(-t * 160) * 0.15
    return norm(body + air, -27)


def click_soft(r):
    """Micro text tick: a damped, high, very short click."""
    t = tt(0.06)
    x = bp(r.standard_normal(len(t)), 2500, 7000) * np.exp(-t * 220)
    x += np.sin(2 * np.pi * 3100 * t) * np.exp(-t * 120) * 0.3
    return norm(x, -33)


def pencil(r, seconds):
    """A white line being drawn: grainy, airy scratch that follows the stroke."""
    t = tt(max(0.15, seconds))
    grain = r.standard_normal(len(t)) * (0.6 + 0.4 * np.abs(np.sin(2 * np.pi * r.uniform(9, 14) * t)))
    x = bp(grain, 2200, 7500)
    e = np.minimum(1, t / 0.05) * np.minimum(1, (t[-1] - t) / 0.12 + 0.05)
    return norm(x * e, -36)


def swish(r, seconds=0.45):
    """Object moving: soft airy pass, no tonal content."""
    t = tt(seconds)
    sweep = 500 + 3500 * np.sin(np.pi * t / t[-1]) ** 2
    n = r.standard_normal(len(t))
    out = np.zeros(len(t))
    blk = 512
    for i in range(0, len(t), blk):  # time-varying band
        f = float(sweep[min(i, len(t) - 1)])
        out[i : i + blk] = bp(n[i : i + blk], max(200, f * 0.5), min(16000, f * 1.6), 1)
    return norm(out * np.sin(np.pi * t / t[-1]) ** 1.5, -31)


def whoosh_soft(r):
    """Scene transition: cinematic but gentle."""
    t = tt(0.75)
    n = r.standard_normal(len(t))
    e = np.sin(np.pi * np.clip(t / 0.75, 0, 1)) ** 2
    low = lp(n, 700) * e
    high = bp(n, 1500, 6000) * e ** 2 * 0.4
    sub = np.sin(2 * np.pi * 55 * t) * e * 0.25
    return norm(room(low + high + sub, 0.8, 0.2), -25)


def thud_soft(r):
    t = tt(0.35)
    x = np.sin(2 * np.pi * (70 + 40 * np.exp(-t * 30)) * t) * np.exp(-t * 18)
    return norm(lp(x, 900), -27)


def check_ding(r):
    t = tt(0.5)
    x = (np.sin(2 * np.pi * 1318.5 * t) + 0.5 * np.sin(2 * np.pi * 1975.5 * t)) * np.exp(-t * 11)
    return norm(room(x, 0.6, 0.2), -30)


def cross_thock(r):
    t = tt(0.25)
    x = np.sin(2 * np.pi * 180 * t) * np.exp(-t * 30) + lp(r.standard_normal(len(t)), 1200) * np.exp(-t * 60) * 0.3
    return norm(x, -29)


def light_on(r):
    """Spotlight: relay clack + faint electric hum swell."""
    t = tt(0.6)
    clack = bp(r.standard_normal(len(t)), 300, 2500) * np.exp(-t * 120)
    hum = np.sin(2 * np.pi * 100 * t) * 0.15 * np.minimum(1, t / 0.1) * np.exp(-t * 3)
    return norm(clack + hum, -27)


def count_tick(r, i):
    t = tt(0.04)
    x = np.sin(2 * np.pi * (1800 + 25 * i) * t) * np.exp(-t * 200)
    return norm(x, -37)


def dice_clack(r):
    t = tt(0.09)
    x = bp(r.standard_normal(len(t)), 1200, 6000) * np.exp(-t * 90) + np.sin(2 * np.pi * r.uniform(900, 1400) * t) * np.exp(-t * 70) * 0.4
    return norm(x, -29)


def wheel_tick(r):
    t = tt(0.03)
    return norm(bp(r.standard_normal(len(t)), 2500, 8000) * np.exp(-t * 300), -35)


def hook_hit(r):
    """Frame 0: a soft, deep hit that says 'listen' without startling."""
    t = tt(1.2)
    body = np.sin(2 * np.pi * (44 + 30 * np.exp(-t * 14)) * t) * np.exp(-t * 3.5)
    air = lp(r.standard_normal(len(t)), 1500) * np.exp(-t * 25) * 0.15
    return norm(room(body + air, 1.0, 0.25), -21)


def reveal_rise(r, seconds=1.2):
    """Reverse swell that resolves exactly on the reveal."""
    t = tt(seconds)
    n = r.standard_normal(len(t))
    e = (t / t[-1]) ** 2.2
    tone = np.sin(2 * np.pi * np.cumsum(110 * 2 ** (t / t[-1])) / SR) * 0.3
    return norm((bp(n, 300, 5000) * 0.7 + tone) * e, -26)


def reveal_hit(r):
    t = tt(2.0)
    sub = np.sin(2 * np.pi * (38 + 25 * np.exp(-t * 10)) * t) * np.exp(-t * 2.2)
    tone = sum(np.sin(2 * np.pi * f * t) * a for f, a in ((164.8, 0.3), (246.9, 0.18), (329.6, 0.1))) * np.exp(-t * 1.6)
    return norm(room(sub + tone, 1.6, 0.35), -18)


def reward_chime(r):
    """The 'satisfying' moment: warm, rising major arpeggio with a soft bloom."""
    t = tt(2.4)
    out = np.zeros(len(t))
    for k, f in enumerate((659.3, 830.6, 987.8, 1318.5)):
        s = int(SR * 0.085 * k)
        seg = t[: len(t) - s]
        out[s:] += (np.sin(2 * np.pi * f * seg) + 0.25 * np.sin(4 * np.pi * f * seg)) * np.exp(-seg * 2.6) * 0.5
    return norm(room(out, 1.8, 0.35), -22)


def room_tone(seconds, r):
    """Barely-there texture layer so silence never feels digital."""
    n = r.standard_normal(int(seconds * SR))
    return lp(n, 400) * db(-54) / (np.std(lp(n[: SR * 2], 400)) or 1)


# ---------------------------------------------------------------- event extraction (mirrors Stage.tsx)
def prog_end(start, length):
    return start + length


def walk_steps(fig, eff_dur, kind):
    """Foot contacts at the extremes of sin(frame / 4.2), inside the walk window (Stage.tsx)."""
    out = []
    if fig.get("toX") is None:
        return out
    end = max(20, eff_dur * 0.7)
    k = 0
    while True:
        f = WALK_PERIOD * (math.pi / 2 + k * math.pi)
        k += 1
        if f > end:
            return out
        if f >= 4:
            out.append((f, kind, {"x": fig.get("x", 540)}))


def events_for_shot(shot, eff_dur, scene_first: bool, is_first: bool, reveal_start: bool):
    """Return [(local_frame, kind, params)]."""
    ev: list[tuple[float, str, dict]] = []
    v = shot["visual"]
    if is_first:
        ev.append((0, "hook", {}))
    elif scene_first:
        ev.append((-6, "whoosh", {}))
    if reveal_start:
        ev.append((-36, "reveal_rise", {"sec": 1.2}))
        ev.append((0, "reveal_hit", {}))
    if v["type"] != "stage":
        if v["type"] in ("discountCurve", "behaviorLoop", "neuralNetwork", "emotionWave", "twoForces"):
            ev.append((6, "pencil", {"sec": 0.9}))
        if v["type"] in ("kineticTitle", "closer", "actionSteps"):
            ev.append((2, "click", {}))
        return ev
    fig = v.get("figure")
    if fig:
        if fig.get("path", "auto") != "none":
            ev.append((0, "pencil", {"sec": 0.5}))
        ev += walk_steps(fig, eff_dur, "step")
    for ex in v.get("extras", []):
        ev += walk_steps(ex, eff_dur, "step_far")
    sp = v.get("spotlight")
    if sp:
        ev.append((3 if sp.get("snap") else 0, "light", {}))
    for p in v.get("props", []):
        start = round(p.get("delay", 0) * FPS)
        enter = p.get("enter", "pop")
        reward = p.get("accent") == "reward"
        if enter == "pop":
            ev.append((start, "pop", {}))
        elif enter == "drop":
            ev.append((start + 10, "thud", {}))
        elif enter == "draw":
            ev.append((start, "pencil", {"sec": 22 / FPS}))
        elif enter in ("slideLeft", "slideRight"):
            ev.append((start, "swish", {"sec": 0.45}))
        if reward:
            ev.append((start + 4, "reward", {}))
        if p["kind"] == "dice" and p.get("state") == "spin":
            for f in (0, 5, 11, 16, 21, 24):
                ev.append((start + f, "dice", {}))
        if p["kind"] == "wheel" and p.get("state") == "spin":
            f = 0.0
            while f < 45:  # decelerating clicks, same easing as the wheel (cubic out)
                ev.append((start + f, "wheel", {}))
                f += 1.2 + (f / 45) ** 2 * 7
        to = p.get("to")
        if to:
            at = round(to.get("at", 0.35) * eff_dur)
            ev.append((at, "swish", {"sec": 0.6}))
            if to.get("accent") == "reward":
                ev.append((at + 9, "reward", {}))
        if p.get("mark"):
            at = round(p.get("markAt", 0.55) * eff_dur)
            ev.append((at, "check" if p["mark"] == "check" else "cross" if p["mark"] == "cross" else "pop", {}))
    for tx in v.get("texts", []):
        ev.append((round(tx.get("delay", 0) * FPS), "click", {}))
        if tx.get("accent") == "reward":
            ev.append((round(tx.get("delay", 0) * FPS) + 3, "reward", {}))
    for c in v.get("counters", []):
        start = round(c.get("delay", 0) * FPS)
        frames = max(1, round(c.get("seconds", 0.9) * FPS))
        steps = min(8, abs(int(c["to"]) - int(c["from"])) or 1)
        for i in range(steps):
            ev.append((start + frames * (1 - (1 - i / steps) ** 2), "tick", {"i": i}))  # eased like the number
        ev.append((start + frames, "pop", {}))
        if c.get("accent") == "reward":
            ev.append((start + frames, "reward", {}))
    return ev


# ---------------------------------------------------------------- mix
def place(bus, x, frame, gain=1.0, pan=0.0):
    s = int(round(frame / FPS * SR))
    if s < 0:
        x, s = x[-s:], 0
    e = min(len(bus), s + len(x))
    if e <= s:
        return
    l, rr = math.cos((pan + 1) * math.pi / 4), math.sin((pan + 1) * math.pi / 4)
    bus[s:e, 0] += x[: e - s] * gain * l * math.sqrt(2)
    bus[s:e, 1] += x[: e - s] * gain * rr * math.sqrt(2)


def load(path: Path):
    x, sr = sf.read(str(path), dtype="float32", always_2d=True)
    if sr != SR:
        x = resample_poly(x, SR, sr, axis=0)
    if x.shape[1] == 1:
        x = np.repeat(x, 2, axis=1)
    return x.astype(np.float64)


def envelope(voice_mono, attack=0.06, release=0.45):
    """Smoothed voice activity 0..1 used as the sidechain key."""
    blk = int(SR * 0.02)
    n = max(1, (len(voice_mono) + blk - 1) // blk)
    rms = np.array([np.sqrt(np.mean(voice_mono[i * blk : (i + 1) * blk] ** 2) + 1e-12) for i in range(n)])
    act = np.clip((20 * np.log10(rms + 1e-9) + 50) / 25, 0, 1)  # -50 dBFS → 0, -25 dBFS → 1
    out = np.zeros(n)
    a, r_ = math.exp(-0.02 / attack), math.exp(-0.02 / release)
    for i in range(n):
        c = a if act[i] > (out[i - 1] if i else 0) else r_
        out[i] = act[i] + c * ((out[i - 1] if i else 0) - act[i])
    return np.repeat(out, blk)[: len(voice_mono)]


def main() -> None:
    build = Path(sys.argv[1]).resolve()
    props_p = build / "props.json"
    props = json.loads(props_p.read_text())
    tl = props["timeline"]
    total = tl["durationInFrames"] / FPS
    N = int(total * SR) + SR
    r = np.random.default_rng(1234)  # fixed seed: same storyboard → same sound

    fx = np.zeros((N, 2))
    shots = tl["shots"]
    counts: dict[str, int] = {}
    step_side = 1
    prev_scene = None
    seen_reveal = False
    for i, s in enumerate(shots):
        scene = s["id"].split("-")[0]
        lead = HOOK_LEAD if i == 0 else 0
        eff = s["durationInFrames"] + (0 if i == len(shots) - 1 else OVERLAP) + lead
        reveal_start = s.get("beat") == "reveal" and not seen_reveal
        seen_reveal = seen_reveal or reveal_start
        evs = events_for_shot(s, eff, scene != prev_scene, i == 0, reveal_start)
        prev_scene = scene
        fig = s["visual"].get("figure") or {}
        fx_x = (fig.get("x", 540) - 540) / 540
        for f, kind, par in evs:
            g = s["startFrame"] + (f if kind == "hook" else f - lead)
            if g < 0:
                continue  # happened during the pre-roll, before the video starts
            counts[kind] = counts.get(kind, 0) + 1
            if kind == "step":
                step_side = -step_side
                fx_x = (par["x"] - 540) / 540
                place(fx, footstep(r), g, pan=float(np.clip(fx_x * 0.5 + step_side * 0.08, -0.6, 0.6)))
            elif kind == "step_far":
                step_side = -step_side
                place(fx, footstep(r), g, gain=db(-7), pan=float(np.clip((par["x"] - 540) / 700, -0.6, 0.6)))
            elif kind == "pop":
                place(fx, pop_soft(r), g, pan=r.uniform(-0.2, 0.2))
            elif kind == "click":
                place(fx, click_soft(r), g)
            elif kind == "pencil":
                place(fx, pencil(r, par["sec"]), g, pan=r.uniform(-0.15, 0.15))
            elif kind == "swish":
                place(fx, swish(r, par["sec"]), g, pan=r.uniform(-0.3, 0.3))
            elif kind == "whoosh":
                place(fx, whoosh_soft(r), g)
            elif kind == "thud":
                place(fx, thud_soft(r), g)
            elif kind == "check":
                place(fx, check_ding(r), g)
            elif kind == "cross":
                place(fx, cross_thock(r), g)
            elif kind == "light":
                place(fx, light_on(r), g)
            elif kind == "tick":
                place(fx, count_tick(r, par["i"]), g)
            elif kind == "dice":
                place(fx, dice_clack(r), g, pan=r.uniform(-0.2, 0.2))
            elif kind == "wheel":
                place(fx, wheel_tick(r), g)
            elif kind == "hook":
                place(fx, hook_hit(r), g)
            elif kind == "reveal_rise":
                place(fx, reveal_rise(r, par["sec"]), g)
            elif kind == "reveal_hit":
                place(fx, reveal_hit(r), g)
            elif kind == "reward":
                place(fx, reward_chime(r), g)

    # texture layer
    rt = room_tone(total + 1, r)
    fx[: len(rt), 0] += rt[: N]
    fx[: len(rt), 1] += np.roll(rt, 4800)[: N]

    # sidechain: voice is king
    voice = load(PUBLIC / tl["voiceSrc"]) if tl.get("voiceSrc") else np.zeros((N, 2))
    vm = np.zeros(N)
    vm[: min(N, len(voice))] = voice[:N, 0]
    key = envelope(vm)
    fx *= (1 - 0.35 * key)[:, None]  # ≈ -3.7 dB under speech: present but never on top

    music_out = None
    if tl.get("musicSrc"):
        m = load(PUBLIC / tl["musicSrc"])
        reps = int(np.ceil(N / len(m)))
        m = np.tile(m, (reps, 1))[:N]
        t = np.arange(N) / SR
        fade = np.clip(t / 1.0, 0, 1) * np.clip((total - t) / 1.5, 0, 1)
        duck = 1 - 0.5 * key  # ≈ -6 dB while she speaks, swells back in the pauses
        music_out = m * (0.24 * fade * duck)[:, None]

    peak = np.max(np.abs(fx))
    if peak > db(-3):
        fx *= db(-3) / peak
    sf.write(str(build / "fx.wav"), fx.astype(np.float32), SR, subtype="PCM_16")
    rel = build.relative_to(PUBLIC).as_posix()
    tl["fxSrc"] = f"{rel}/fx.wav"
    if music_out is not None:
        sf.write(str(build / "music.wav"), music_out.astype(np.float32), SR, subtype="PCM_16")
        tl["musicSrc"] = f"{rel}/music.wav"
        tl["musicGain"] = 1.0
    tl["sfxEvents"] = counts
    props_p.write_text(json.dumps(props, ensure_ascii=False))
    print("sound design: " + ", ".join(f"{k}×{v}" for k, v in sorted(counts.items())))


if __name__ == "__main__":
    main()
