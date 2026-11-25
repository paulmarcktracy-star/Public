"""Original emotional score, composed in code and played with real instrument
samples (FluidSynth + FluidR3 General MIDI soundfont: piano, strings, cello).
No third-party music, so no licensing questions.

Usage: python pipeline/music.py [style ...]      styles: reflexion | esperanza | intimo
Writes public/audio/music/<style>.wav (48 kHz stereo, ~85 s, mastered to -20 LUFS).
"""
import random
import subprocess
import sys
from pathlib import Path

import mido

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public" / "audio" / "music"
SF2_CANDIDATES = [Path("/usr/share/sounds/sf2/FluidR3_GM.sf2"), Path("/usr/share/soundfonts/FluidR3_GM.sf2")]
TPB = 480
BAR = TPB * 4

NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}


def chord(name: str, octave: int = 3) -> list[int]:
    """'Am' -> [A3, C4, E4] as MIDI numbers."""
    minor = name.endswith("m")
    root = NOTE[name[:-1] if minor else name] + 12 * (octave + 1)
    return [root, root + (3 if minor else 4), root + 7]


class Track:
    def __init__(self, channel: int, program: int, name: str):
        self.ch, self.events, self.name = channel, [], name
        self.events.append((0, mido.Message("program_change", channel=channel, program=program)))

    def note(self, start: int, dur: int, pitch: int, vel: int) -> None:
        self.events.append((start, mido.Message("note_on", channel=self.ch, note=pitch, velocity=max(1, min(127, vel)))))
        self.events.append((start + dur, mido.Message("note_off", channel=self.ch, note=pitch, velocity=0)))

    def expr(self, start: int, end: int, a: int, b: int, steps: int = 24) -> None:
        for i in range(steps + 1):
            t = start + (end - start) * i // steps
            self.events.append((t, mido.Message("control_change", channel=self.ch, control=11, value=int(a + (b - a) * i / steps))))

    def to_midi(self) -> mido.MidiTrack:
        tr = mido.MidiTrack()
        tr.append(mido.MetaMessage("track_name", name=self.name))
        now = 0
        for t, msg in sorted(self.events, key=lambda e: (e[0], 0 if e[1].type == "note_off" else 1)):
            tr.append(msg.copy(time=t - now))
            now = t
        return tr


def save(path: Path, bpm: int, tracks: list[Track]) -> None:
    mid = mido.MidiFile(ticks_per_beat=TPB)
    meta = mido.MidiTrack()
    meta.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(bpm)))
    mid.tracks.append(meta)
    for t in tracks:
        mid.tracks.append(t.to_midi())
    mid.save(path)


def humanize(rng: random.Random, v: int, spread: int = 6) -> int:
    return v + rng.randint(-spread, spread)


def arpeggio(tr: Track, rng: random.Random, bar: int, notes: list[int], vel: int, bars: int = 2) -> None:
    r, third, fifth = notes
    pattern = [r - 12, fifth - 12, r, third, fifth, third, r, fifth - 12]
    for b in range(bars):
        for i, p in enumerate(pattern):
            start = (bar + b) * BAR + i * TPB // 2 + rng.randint(0, 12)
            tr.note(start, TPB, p, humanize(rng, vel - (6 if i % 2 else 0)))


def reflexion() -> tuple[int, list[Track]]:
    """Piano arpeggios, strings enter, cello and a slow melody in the second half (A minor)."""
    rng = random.Random(3)
    piano, strings, cello, violin = Track(0, 0, "piano"), Track(1, 48, "strings"), Track(2, 42, "cello"), Track(3, 49, "violin")
    prog = ["Am", "F", "C", "G", "Am", "F", "Dm", "E"] * 2
    melody = {8: [76, 74, 72], 9: [72, 69], 10: [67, 72, 76], 11: [74], 12: [76, 79, 77], 13: [76, 72], 14: [74, 72, 71], 15: [69]}
    for i, name in enumerate(prog[:12]):
        bar = i * 2
        notes = chord(name, 3)
        arpeggio(piano, rng, bar, notes, 58 if bar < 16 else 66)
        if bar >= 2:
            for p in chord(name, 4):
                strings.note(bar * BAR, 2 * BAR, p, 52 if bar < 12 else 64)
            strings.expr(bar * BAR, bar * BAR + BAR, 50, 100 if bar >= 12 else 85)
            strings.expr(bar * BAR + BAR, (bar + 2) * BAR, 100 if bar >= 12 else 85, 70)
        if bar >= 8:
            cello.note(bar * BAR, 2 * BAR - 40, notes[0] - 12, 70)
        if bar >= 16 and i in melody:
            seq = melody[i]
            step = 2 * BAR // len(seq)
            for k, p in enumerate(seq):
                violin.note(bar * BAR + k * step, step - 30, p, 62)
    # resolution
    end = 24 * BAR
    for p in chord("Am", 3) + [57 + 12]:
        piano.note(end, 2 * BAR, p, 50)
    for p in chord("Am", 4):
        strings.note(end, 2 * BAR, p, 50)
    cello.note(end, 2 * BAR, 45, 60)
    return 72, [piano, strings, cello, violin]


def esperanza() -> tuple[int, list[Track]]:
    """Tension (D minor, pulsing pizzicato + heartbeat) that lifts to hope (F major) at ~50 s."""
    rng = random.Random(7)
    piano, pizz, strings, cello, drums = Track(0, 0, "piano"), Track(1, 45, "pizz"), Track(2, 48, "strings"), Track(3, 42, "cello"), Track(9, 0, "drums")
    tension = ["Dm", "Bb", "Gm", "A", "Dm", "Bb", "A"]
    lift = ["F", "C", "Dm", "Bb", "F", "C"]
    for i, name in enumerate(tension):
        bar = i * 2
        notes = chord(name, 2)
        for k in range(16):  # 8th-note pulse
            pizz.note(bar * BAR + k * TPB // 2, TPB // 3, notes[0] + (12 if k % 4 == 2 else 0), humanize(rng, 60 + bar * 2, 4))
        for b in range(2):  # heartbeat
            drums.note((bar + b) * BAR, 120, 36, 52 + bar)
            drums.note((bar + b) * BAR + TPB * 3 // 4, 120, 36, 38 + bar)
        motif = [notes[2] + 24, notes[1] + 24, notes[0] + 24]
        for k, p in enumerate(motif):
            piano.note(bar * BAR + BAR + k * TPB, TPB * 2, p, humanize(rng, 48))
        if bar >= 6:
            for p in chord(name, 3):
                strings.note(bar * BAR, 2 * BAR, p, 46 + bar * 2)
            strings.expr(bar * BAR, (bar + 2) * BAR, 40, 90)
    start = len(tension) * 2
    for i, name in enumerate(lift):
        bar = start + i * 2
        notes = chord(name, 3)
        arpeggio(piano, rng, bar, notes, 64)
        for p in chord(name, 4) + [chord(name, 5)[0]]:
            strings.note(bar * BAR, 2 * BAR, p, 72)
        strings.expr(bar * BAR, bar * BAR + BAR, 70, 110)
        strings.expr(bar * BAR + BAR, (bar + 2) * BAR, 110, 85)
        cello.note(bar * BAR, 2 * BAR - 40, notes[0] - 12, 78)
    end = (start + len(lift) * 2) * BAR
    for p in chord("F", 3) + chord("F", 4):
        piano.note(end, 2 * BAR, p, 54)
        strings.note(end, 2 * BAR, p + 12, 56)
    cello.note(end, 2 * BAR, 41, 64)
    return 72, [piano, pizz, strings, cello, drums]


def intimo() -> tuple[int, list[Track]]:
    """Minimal and modern: warm pad, sparse high piano, soft low pulse (E minor)."""
    rng = random.Random(11)
    pad, piano, bass = Track(0, 89, "pad"), Track(1, 0, "piano"), Track(2, 48, "low strings")
    prog = ["Em", "C", "G", "D"] * 3
    for i, name in enumerate(prog):
        bar = i * 2
        for p in chord(name, 3):
            pad.note(bar * BAR, 2 * BAR, p, 58)
        pad.expr(bar * BAR, (bar + 2) * BAR, 60, 95 if i % 2 == 0 else 75)
        bass.note(bar * BAR, 2 * BAR, chord(name, 2)[0], 50 + (10 if bar >= 12 else 0))
        top = chord(name, 5)
        for k in range(rng.choice([3, 4, 5])):
            piano.note(bar * BAR + k * BAR // 2 + rng.randint(0, 60), BAR, rng.choice(top), humanize(rng, 44, 8))
    for p in chord("Em", 3):
        pad.note(24 * BAR, 2 * BAR, p, 50)
    return 66, [pad, piano, bass]


STYLES = {"reflexion": reflexion, "esperanza": esperanza, "intimo": intimo}


def render(style: str) -> Path:
    sf2 = next((p for p in SF2_CANDIDATES if p.exists()), None)
    if not sf2:
        raise SystemExit("FluidR3_GM.sf2 not found: apt-get install fluidsynth fluid-soundfont-gm")
    OUT.mkdir(parents=True, exist_ok=True)
    bpm, tracks = STYLES[style]()
    mid = OUT / f"{style}.mid"
    raw = OUT / f"{style}.raw.wav"
    wav = OUT / f"{style}.wav"
    save(mid, bpm, tracks)
    subprocess.run(
        ["fluidsynth", "-ni", "-q", "-g", "0.5", "-r", "48000", "-o", "synth.reverb.active=1", "-o", "synth.reverb.room-size=0.85",
         "-o", "synth.reverb.damp=0.35", "-o", "synth.reverb.level=0.6", "-o", "synth.reverb.width=1.0", "-F", str(raw), str(sf2), str(mid)],
        check=True,
    )
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-af",
         "highpass=f=35,aecho=0.8:0.6:60|110:0.18|0.12,afade=t=in:d=1.5,loudnorm=I=-20:TP=-3:LRA=11", "-ar", "48000", "-ac", "2", str(wav)],
        check=True,
    )
    raw.unlink()
    return wav


if __name__ == "__main__":
    for s in sys.argv[1:] or list(STYLES):
        print("music:", render(s))
