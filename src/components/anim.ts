import { Easing, interpolate } from "remotion";
import { MOTION } from "../design/tokens";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

export const easeEnter = Easing.bezier(...MOTION.enter);
export const easeExit = Easing.bezier(...MOTION.exit);
export const easeStd = Easing.bezier(...MOTION.standard);

/** 0→1 progress between two frames with the studio's enter curve. */
export const prog = (frame: number, start: number, dur: number, ease = easeEnter) =>
  interpolate(frame, [start, start + Math.max(1, dur)], [0, 1], { ...clamp, easing: ease });

export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

/** Deterministic PRNG (mulberry32) so every render is identical. */
export const rng = (seed: number) => {
  let s = seed >>> 0;
  return () => {
    s = (s + 0x6d2b79f5) >>> 0;
    let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};

/** Normalise a word for matching emphasis (strip accents/punctuation, lower). */
export const norm = (w: string) =>
  w.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9ñ]/g, "");

export const isEmphasis = (word: string, emphasis: string[]) => {
  const n = norm(word);
  if (!n) return false;
  return emphasis.some((e) => e.split(/\s+/).map(norm).includes(n));
};
