/**
 * Cinematic intelligent camera (owner rule, 2026-11-25).
 *
 * One camera for the whole film, applied to the scene layer only: the static dot grid
 * and the captions are never moved. Keyframes are planned from the timeline itself:
 * which element is the most important in each shot, when it appears, and the beat
 * (hook, reveal, closer...). Each movement is a reusable CameraMove
 * { fromZoom, toZoom, start, duration, focus{x,y}, type, easing }.
 *
 * Framing safety: zoom is about the content centre (540, 760); the focus pull is
 * partial and clamped so screen-fixed titles (y≈330) stay below the 170 px safe line,
 * and edges never show (|translate| ≤ (zoom−1)·half-size).
 */
import React from "react";
import { AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import type { Timeline, TimelineShot } from "../schema";
import { SCALE, VIDEO } from "../design/tokens";

export type MoveType = "hold" | "pushIn" | "pullOut" | "track" | "pan" | "focus";
export type CameraMove = {
  start: number; // global frame
  duration: number;
  fromZoom: number;
  toZoom: number;
  from: { x: number; y: number };
  to: { x: number; y: number };
  type: MoveType;
  easing: "cinematic" | "gentle" | "spring";
};

const ORIGIN = { x: 540, y: 760 };
const PULL = 0.45; // how much of the way the focus point travels toward the centre
const MAX_T = { x: 70, y: 46 };

const EASE = {
  cinematic: Easing.bezier(0.45, 0, 0.15, 1), // slow start, long soft landing
  gentle: Easing.bezier(0.33, 0, 0.25, 1),
};

/* ------------------------------------------------------------ hierarchy: what matters in a shot */
type Focus = { x: number; y: number; at: number; weight: number; kind: string };

const stageToScreen = (v: Extract<TimelineShot["visual"], { type: "stage" }>, x: number, y: number) => {
  const cam = v.camera ?? { fromZoom: 1, toZoom: 1.07, x: 540, y: 760, panX: 0 };
  const z = SCALE.visual * ((cam.fromZoom + cam.toZoom) / 2);
  return { x: cam.x + (x - cam.x) * z - (cam.panX ?? 0) / 2, y: cam.y + (y - cam.y) * z };
};

export const focusOf = (s: TimelineShot, fps: number): Focus => {
  const v = s.visual;
  if (v.type !== "stage") {
    return { x: 540, y: 760, at: 0, weight: v.type === "closer" ? 3 : v.type === "kineticTitle" ? 2 : 1, kind: v.type };
  }
  const cands: Focus[] = [];
  for (const c of v.counters ?? []) {
    const p = stageToScreen(v, c.x, c.y);
    cands.push({ ...p, at: Math.round((c.delay ?? 0) * fps), weight: c.accent === "reward" ? 6 : 5, kind: "number" });
  }
  for (const p of v.props ?? []) {
    const sp = stageToScreen(v, p.x, p.y);
    const reward = p.accent === "reward" || p.to?.accent === "reward";
    const w = reward ? 5.5 : p.mark ? 3.5 : p.to ? 3 : p.state === "glow" ? 2.5 : 1.5 + (p.size ?? 100) / 200;
    const at = p.mark ? Math.round((p.markAt ?? 0.55) * s.durationInFrames) - 8 : p.to ? Math.round((p.to.at ?? 0.35) * s.durationInFrames) - 6 : Math.round((p.delay ?? 0) * fps);
    cands.push({ ...sp, at: Math.max(0, at), weight: w, kind: "object" });
  }
  if (v.figure) {
    const f = v.figure;
    const mid = f.toX !== undefined ? (f.x + f.toX) / 2 : f.x;
    const p = stageToScreen(v, mid, (f.y ?? 1120) - 150 * (f.scale ?? 1));
    cands.push({ ...p, at: 0, weight: f.toX !== undefined ? 3 : 2, kind: f.toX !== undefined ? "walker" : "character" });
  }
  for (const t of v.texts ?? []) {
    if ((t.emphasis ?? []).length) cands.push({ x: t.x ?? 540, y: t.y, at: Math.round((t.delay ?? 0) * fps), weight: t.accent === "reward" ? 5 : 2.2, kind: "text" });
  }
  if (!cands.length) return { x: 540, y: 760, at: 0, weight: 1, kind: "empty" };
  return cands.sort((a, b) => b.weight - a.weight)[0];
};

/* ------------------------------------------------------------ direction: one decision per shot */
export const planCamera = (tl: Timeline, fps: number): CameraMove[] => {
  const moves: CameraMove[] = [];
  const shots = tl.shots;
  const firstScene = shots[0]?.id.split("-")[0];
  const hookShots = shots.filter((s) => s.id.split("-")[0] === firstScene);
  const hookEnd = hookShots.length ? hookShots[hookShots.length - 1].startFrame + hookShots[hookShots.length - 1].durationInFrames : 0;
  const hf = focusOf(shots[0], fps);
  // 1. Opening: already in close-up (110 %), barely breathing while the hook is spoken…
  moves.push({ start: 0, duration: Math.max(1, hookEnd - 8), fromZoom: 1.1, toZoom: 1.115, from: hf, to: hf, type: "hold", easing: "gentle" });
  // …then the camera slowly pulls away to the normal composition.
  const centre = { x: 540, y: 760 };
  moves.push({ start: hookEnd - 8, duration: 40, fromZoom: 1.115, toZoom: 1.0, from: hf, to: centre, type: "pullOut", easing: "cinematic" });

  let last: MoveType = "pullOut";
  let z = 1.0;
  let pos = centre;
  for (let i = hookShots.length; i < shots.length; i++) {
    const s = shots[i];
    const v = s.visual;
    const f = focusOf(s, fps);
    const innerPush = v.type === "stage" ? (v.camera?.toZoom ?? 1.07) : 1;
    const room = innerPush > 1.12 ? 0.35 : innerPush > 1.08 ? 0.7 : 1; // respect the shot's own camera: never stack zooms into a crop
    const reveal = s.beat === "reveal";
    const start = s.startFrame;
    const D = s.durationInFrames;
    // settle into the shot (transition): ease from where we were toward a calm framing
    const settle = s.beat === "cta" ? 1.0 : Math.min(z, 1.03);
    if (i === hookShots.length) {
      // the opening pull-back is still landing: let it finish before the next idea
      const free = hookEnd - 8 + 40;
      const f2 = focusOf(s, fps);
      const at2 = Math.max(free, start + Math.min(f2.at, D - 20));
      if (f2.kind === "number" || (f2.kind === "object" && f2.weight >= 3)) {
        moves.push({ start: at2, duration: Math.max(12, Math.min(30, start + D - at2)), fromZoom: 1, toZoom: 1.05, from: centre, to: f2, type: "focus", easing: "cinematic" });
        z = 1.05; pos = f2; last = "focus";
      } else {
        moves.push({ start: free, duration: Math.max(12, start + D - free), fromZoom: 1, toZoom: 1.03, from: centre, to: { x: 560, y: 760 }, type: "pan", easing: "gentle" });
        z = 1.03; pos = { x: 560, y: 760 }; last = "pan";
      }
      continue;
    }
    moves.push({ start: start - 4, duration: 20, fromZoom: z, toZoom: settle, from: pos, to: { x: (pos.x + 540) / 2, y: (pos.y + 760) / 2 }, type: "hold", easing: "gentle" });
    z = settle;
    pos = { x: (pos.x + 540) / 2, y: (pos.y + 760) / 2 };

    let type: MoveType;
    let target = 1.0;
    let to = pos;
    let at = start + Math.max(6, Math.min(f.at, D - 24));
    let dur = Math.min(36, Math.max(18, D - (at - start) - 6));
    let easing: CameraMove["easing"] = "cinematic";
    if (s.beat === "closer") {
      type = "pushIn"; target = 1.08; to = { x: 540, y: 740 }; at = start + 4; dur = D - 8; easing = "gentle"; // deliberate, slow
    } else if (s.beat === "cta") {
      type = "pullOut"; target = 1.0; to = centre; at = start + 2; dur = Math.min(40, D - 4);
    } else if (f.kind === "number") {
      type = "focus"; target = reveal ? 1.11 : 1.07; to = f; easing = "spring";
    } else if (f.kind === "object" && f.weight >= 3) {
      type = "focus"; target = reveal ? 1.1 : 1.06; to = f;
    } else if (f.kind === "walker") {
      const w = (v.type === "stage" && v.figure) || null;
      const from = w ? stageToScreen(v as never, w.x, (w.y ?? 1120) - 150) : f;
      const dest = w && w.toX !== undefined ? stageToScreen(v as never, w.toX, (w.y ?? 1120) - 150) : f;
      type = "track"; target = 1.045; to = { x: (from.x + dest.x * 2) / 3, y: dest.y }; at = start + 4; dur = Math.round(Math.max(20, (D + VIDEO.sceneOverlapFrames) * 0.7)); easing = "gentle";
    } else if (v.type === "kineticTitle") {
      type = "pushIn"; target = 1.06; to = centre; at = start + 2; dur = D - 4; easing = "gentle";
    } else if (f.kind === "text") {
      type = "focus"; target = 1.04; to = { x: f.x, y: (f.y + 760) / 2 };
    } else {
      // explanation shots: vary — slow pan or a soft pull-out, never the previous move twice
      type = last === "pan" ? "pullOut" : "pan";
      if (type === "pan") { target = 1.035; to = { x: pos.x + (i % 2 ? 36 : -36), y: pos.y }; at = start + 4; dur = D - 6; easing = "gentle"; }
      else { target = 1.0; to = centre; at = start + 4; dur = Math.min(40, D - 6); }
    }
    target = 1 + (target - 1) * room;
    moves.push({ start: at, duration: Math.max(8, dur), fromZoom: z, toZoom: target, from: pos, to, type, easing });
    z = target; pos = to; last = type;
  }
  return resolve(moves, fps);
};

/** Chain the moves: each one begins from the state the previous ones actually reached. */
const resolve = (moves: CameraMove[], fps: number): CameraMove[] => {
  const out: CameraMove[] = [];
  let minStart = 0;
  for (const m0 of moves) {
    const m = { ...m0, start: Math.max(m0.start, minStart) };
    if (out.length) {
      const st = rawAt(out, m.start, fps);
      m.fromZoom = st.zoom;
      m.from = { x: st.fx, y: st.fy };
    }
    out.push(m);
    minStart = m.start;
  }
  return out;
};

/* ------------------------------------------------------------ evaluation */
const clamp = (v: number, m: number) => Math.max(-m, Math.min(m, v));

const rawAt = (moves: CameraMove[], frame: number, fps: number) => {
  let zoom = moves[0]?.fromZoom ?? 1;
  let fx = moves[0]?.from.x ?? 540;
  let fy = moves[0]?.from.y ?? 760;
  for (const m of moves) {
    if (frame < m.start) break;
    const t =
      m.easing === "spring"
        ? Math.min(1, spring({ frame: frame - m.start, fps, config: { damping: 200, stiffness: 60, mass: 1 }, durationInFrames: m.duration }))
        : interpolate(frame, [m.start, m.start + m.duration], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: EASE[m.easing] });
    zoom = m.fromZoom + (m.toZoom - m.fromZoom) * t;
    fx = m.from.x + (m.to.x - m.from.x) * t;
    fy = m.from.y + (m.to.y - m.from.y) * t;
  }
  return { zoom, fx, fy };
};

export const cameraAt = (moves: CameraMove[], frame: number, fps: number) => {
  const { zoom, fx, fy } = rawAt(moves, frame, fps);
  // partial pull of the focus toward the centre, clamped so nothing important leaves the frame
  const k = (zoom - 1) / 0.12; // stronger zoom → stronger re-centring
  const tx = clamp(-(fx - ORIGIN.x) * zoom * PULL * Math.min(1, k), Math.min(MAX_T.x, (zoom - 1) * 540));
  const ty = clamp(-(fy - ORIGIN.y) * zoom * PULL * Math.min(1, k), Math.min(MAX_T.y, (zoom - 1) * 760));
  return { zoom, tx, ty };
};

export const CameraRig: React.FC<{ timeline: Timeline; children: React.ReactNode }> = ({ timeline, children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const moves = React.useMemo(() => planCamera(timeline, fps), [timeline, fps]);
  const { zoom, tx, ty } = cameraAt(moves, frame, fps);
  return (
    <AbsoluteFill style={{ transformOrigin: `${ORIGIN.x}px ${ORIGIN.y}px`, transform: `translate(${tx}px, ${ty}px) scale(${zoom})` }}>
      {children}
    </AbsoluteFill>
  );
};
