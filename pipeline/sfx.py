"""Procedural sound design: every sound is synthesised here, so there are no
licensing questions and renders are fully reproducible.

Writes public/audio/sfx/*.wav and public/audio/music/bed.wav (48 kHz).
"""
import sys
import wave
from pathlib import Path

import numpy as np

SR = 48000
rng = np.random.default_rng(1234)
ROOT = Path(__file__).resolve().parent.parent / "public" / "audio"


def write(path: Path, x: np.ndarray, stereo: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    x = np.asarray(x, dtype=np.float64)
    if not stereo:
        x = np.stack([x, x], axis=1)
    peak = np.max(np.abs(x)) or 1.0
    x = x / peak * 0.89
    data = (x * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())


def t(sec: float) -> np.ndarray:
    return np.arange(int(SR * sec)) / SR


def env(n: int, attack: float, release: float) -> np.ndarray:
    a = int(SR * attack)
    r = int(SR * release)
    e = np.ones(n)
    e[:a] = np.linspace(0, 1, a) ** 2
    e[-r:] *= np.linspace(1, 0, r) ** 2
    return e


def lowpass(x: np.ndarray, cutoff: np.ndarray | float) -> np.ndarray:
    """One-pole low-pass with optional time-varying cutoff (Hz)."""
    if np.isscalar(cutoff):
        from scipy.signal import lfilter

        a = float(np.exp(-2 * np.pi * cutoff / SR))
        return lfilter([1 - a], [1, -a], x)
    cutoff = np.broadcast_to(cutoff, x.shape)
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.zeros_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = (1 - a[i]) * x[i] + a[i] * acc
        y[i] = acc
    return y


def reverb(x: np.ndarray, decay: float = 1.6, mix: float = 0.35) -> np.ndarray:
    n = int(SR * decay)
    ir = rng.standard_normal(n) * np.exp(-np.linspace(0, 6, n))
    from scipy.signal import fftconvolve

    wet = fftconvolve(x, ir)
    wet /= np.max(np.abs(wet)) or 1
    out = np.zeros(len(wet))
    out[: len(x)] += x * (1 - mix)
    out += wet * mix * np.max(np.abs(x))
    return out


def whoosh() -> np.ndarray:
    tt = t(0.9)
    noise = rng.standard_normal(len(tt))
    sweep = 300 + 5200 * np.sin(np.pi * tt / tt[-1]) ** 2
    return reverb(lowpass(noise, sweep) * env(len(tt), 0.35, 0.45), 0.8, 0.25)


def riser() -> np.ndarray:
    tt = t(1.6)
    f = 110 * 2 ** (tt / tt[-1] * 2)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.4 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    noise = lowpass(rng.standard_normal(len(tt)), 400 + 4000 * tt / tt[-1]) * 0.6
    return reverb((tone * 0.5 + noise) * env(len(tt), 1.3, 0.1), 1.2, 0.3)


def impact() -> np.ndarray:
    tt = t(1.4)
    body = np.sin(2 * np.pi * (48 + 60 * np.exp(-tt * 18)) * tt) * np.exp(-tt * 3.2)
    click = lowpass(rng.standard_normal(len(tt)), 3000) * np.exp(-tt * 40)
    return reverb(body + 0.5 * click, 1.8, 0.3)


def tick() -> np.ndarray:
    tt = t(0.5)
    ping = np.sin(2 * np.pi * 1760 * tt) * np.exp(-tt * 22) + 0.3 * np.sin(2 * np.pi * 2640 * tt) * np.exp(-tt * 30)
    return reverb(ping, 0.9, 0.3)


def shimmer() -> np.ndarray:
    tt = t(2.2)
    out = np.zeros(len(tt))
    for k, f in enumerate([880, 1108.7, 1318.5, 1760, 2217.5]):
        out += np.sin(2 * np.pi * f * tt + k) * np.exp(-((tt - 0.25 * k) ** 2) / 0.12) * 0.4
    return reverb(out * env(len(tt), 0.05, 0.8), 2.0, 0.45)


def pulse() -> np.ndarray:
    tt = t(1.8)
    hb = np.zeros(len(tt))
    for start in (0.0, 0.32):
        s = int(start * SR)
        seg = t(0.4)
        hb[s : s + len(seg)] += np.sin(2 * np.pi * 55 * seg) * np.exp(-seg * 14)
    return reverb(hb, 1.2, 0.25)


def pop() -> np.ndarray:
    tt = t(0.45)
    f = 420 + 900 * np.exp(-tt * 30)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 16)
    return reverb(body, 0.6, 0.2)


def cash() -> np.ndarray:
    tt = t(1.1)
    out = np.zeros(len(tt))
    for k, (start, f) in enumerate([(0.0, 2093.0), (0.07, 2637.0), (0.14, 3136.0)]):
        s0 = int(start * SR)
        seg = tt[: len(tt) - s0]
        out[s0:] += np.sin(2 * np.pi * f * seg) * np.exp(-seg * 9) * (0.8 - 0.15 * k)
    click = lowpass(rng.standard_normal(len(tt)), 5000) * np.exp(-tt * 60) * 0.4
    return reverb(out + click, 1.0, 0.3)


def music_bed(seconds: float = 96.0) -> np.ndarray:
    """Slow cinematic pad: A minor - F - C - G, soft sub pulse, filtered air."""
    tt = t(seconds)
    chords = [[220.0, 261.63, 329.63], [174.61, 220.0, 261.63], [196.0, 261.63, 329.63], [196.0, 246.94, 293.66]]
    bar = 6.0
    L = np.zeros(len(tt))
    R = np.zeros(len(tt))
    for i, chord in enumerate(chords * int(np.ceil(seconds / (bar * 4)))):
        s0 = int(i * bar * SR)
        if s0 >= len(tt):
            break
        seg = t(bar + 2.0)
        e = env(len(seg), 2.2, 2.4)
        for j, f in enumerate(chord):
            det = 0.6 + j * 0.25
            v = (np.sin(2 * np.pi * (f - det) * seg) + np.sin(2 * np.pi * (f + det) * seg)) * 0.12 * e
            end = min(len(tt), s0 + len(seg))
            L[s0:end] += v[: end - s0] * (1.0 if j % 2 else 0.7)
            R[s0:end] += v[: end - s0] * (0.7 if j % 2 else 1.0)
        sub = np.sin(2 * np.pi * chord[0] / 4 * seg) * 0.18 * e
        end = min(len(tt), s0 + len(seg))
        L[s0:end] += sub[: end - s0]
        R[s0:end] += sub[: end - s0]
    air = lowpass(rng.standard_normal(len(tt)), 900) * 0.04
    L = lowpass(L, 2400) + air
    R = lowpass(R, 2400) + air
    fade = env(len(tt), 3.0, 3.0)
    return np.stack([L * fade, R * fade], axis=1)


def main() -> None:
    force = "--force" in sys.argv
    sounds = {"whoosh": whoosh, "riser": riser, "impact": impact, "tick": tick, "shimmer": shimmer, "pulse": pulse, "pop": pop, "cash": cash}
    for name, fn in sounds.items():
        p = ROOT / "sfx" / f"{name}.wav"
        if force or not p.exists():
            write(p, fn())
    print(f"sound library ready in {ROOT}")


if __name__ == "__main__":
    main()
