import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import type { z } from "zod";
import type { Stage as StageS, StageProp, StageCounter, Pose as PoseS } from "../schema";
import { COLORS, SCALE, TYPE } from "../design/tokens";
import { easeEnter, easeStd, lerp, prog } from "../components/anim";
import { RichLine } from "../components/Rich";

type Props = z.infer<typeof StageS> & { durationInFrames: number };
type PoseName = z.infer<typeof PoseS>;
type Accent = "white" | "gold" | "green" | "red" | "reward";

export const accentColor = (a: Accent) =>
  a === "reward" ? COLORS.reward : a === "red" ? COLORS.red : COLORS.ink; // B&W identity

/* ============================== FIGURE ============================== */
// Angles in degrees. 0 = limb pointing down, +90 = pointing forward (facing), 180 = up.
type Pose = { lean: number; head: number; rs: number; re: number; ls: number; le: number; rh: number; rk: number; lh: number; lk: number };
const POSES: Record<PoseName, Pose> = {
  stand: { lean: 0, head: 0, rs: 10, re: 6, ls: -10, le: -6, rh: 5, rk: -3, lh: -5, lk: 2 },
  reach: { lean: 8, head: 8, rs: 82, re: 4, ls: -14, le: -4, rh: 12, rk: -8, lh: -10, lk: 2 },
  point: { lean: 3, head: -4, rs: 128, re: 4, ls: -10, le: -6, rh: 5, rk: -3, lh: -5, lk: 2 },
  phone: { lean: 6, head: 26, rs: 28, re: 118, ls: -10, le: -6, rh: 4, rk: -3, lh: -4, lk: 2 },
  think: { lean: -2, head: -10, rs: 22, re: 142, ls: -6, le: 60, rh: 4, rk: -3, lh: -4, lk: 2 },
  celebrate: { lean: -4, head: -16, rs: 160, re: 12, ls: -160, le: -12, rh: 8, rk: -4, lh: -8, lk: 4 },
  slump: { lean: 16, head: 34, rs: 4, re: 2, ls: -2, le: 0, rh: 10, rk: -14, lh: 2, lk: -10 },
  walk: { lean: 5, head: 0, rs: -18, re: 14, ls: 18, le: 14, rh: 0, rk: 0, lh: 0, lk: 0 },
  lookUp: { lean: -4, head: -30, rs: 14, re: 8, ls: -14, le: -8, rh: 5, rk: -3, lh: -5, lk: 2 },
};
const mixPose = (a: Pose, b: Pose, t: number): Pose =>
  Object.fromEntries(Object.keys(a).map((k) => [k, lerp(a[k as keyof Pose], b[k as keyof Pose], t)])) as Pose;

/* ===================== SIGNATURE DASHED PATH ===================== */
type Fig = NonNullable<Props["figure"]>;
const pathShape = (fig: Fig) => (fig.path === "auto" ? "flat" : fig.path);
const pathSpan = (fig: Fig): [number, number] => {
  const end = fig.toX ?? fig.x;
  const lo = Math.min(fig.x, end), hi = Math.max(fig.x, end);
  const walking = fig.toX !== undefined;
  const back = walking ? 220 : 150, ahead = walking ? 300 : 260;
  const a = fig.pathFrom ?? (fig.facing === 1 ? lo - back : lo - ahead);
  const b = fig.pathTo ?? (fig.facing === 1 ? hi + ahead : hi + back);
  return [a, b];
};
/** Ground height under the feet at x: the figure walks ON the path, never floats. */
const pathY = (fig: Fig, x: number) => {
  const shape = pathShape(fig);
  if (shape !== "rise" && shape !== "fall") return fig.y;
  const [a, b] = pathSpan(fig);
  const u = Math.max(0, Math.min(1, (x - a) / Math.max(1, b - a)));
  const k = fig.facing === 1 ? u : 1 - u; // progress in walking direction
  const start = fig.x, s0 = Math.max(0, Math.min(1, (start - a) / Math.max(1, b - a)));
  const k0 = fig.facing === 1 ? s0 : 1 - s0;
  return fig.y + (shape === "rise" ? -1 : 1) * 170 * (k - k0);
};
const DashedPath: React.FC<{ fig: Fig; frame: number; dur: number }> = ({ fig, frame, dur }) => {
  const shape = pathShape(fig);
  if (shape === "none") return null;
  const [a, b] = pathSpan(fig);
  const DASH = 15, STEP = 31; // short, fine, evenly spaced strokes
  const walking = fig.toX !== undefined;
  const walkT = walking ? prog(frame, 4, Math.max(20, dur * 0.7), easeStd) : 0;
  const cur = walking ? lerp(fig.x, fig.toX!, walkT) : fig.x;
  const reveal = prog(frame, 0, 16, easeStd);
  const lines: { pts: [number, number][]; branch?: number }[] = [];
  const main: [number, number][] = [];
  for (let x = a; x <= b; x += 2) main.push([x, pathY(fig, x)]);
  if (shape === "fork") {
    // stem up to a point ahead of the walker, then two diverging branches
    const split = fig.facing === 1 ? Math.min(b - 80, (fig.toX ?? fig.x) + 90) : Math.max(a + 80, (fig.toX ?? fig.x) - 90);
    const stem = main.filter(([x]) => (fig.facing === 1 ? x <= split : x >= split));
    lines.push({ pts: stem });
    const len = fig.facing === 1 ? b - split + 120 : split - a + 120;
    for (const sgn of [-1, 1]) {
      const br: [number, number][] = [];
      for (let d = 0; d <= len; d += 2) br.push([split + fig.facing * d, fig.y + sgn * 0.42 * d]);
      lines.push({ pts: br, branch: sgn });
    }
  } else lines.push({ pts: main });
  const out: React.ReactNode[] = [];
  lines.forEach((ln, li) => {
    let acc = 0;
    for (let i = 1; i < ln.pts.length; i++) {
      const [x0, y0] = ln.pts[i - 1], [x1, y1] = ln.pts[i];
      const seg = Math.hypot(x1 - x0, y1 - y0);
      const prev = acc;
      acc += seg;
      if (Math.floor(prev / STEP) === Math.floor(acc / STEP)) continue;
      // a dash starts here, oriented along the local tangent
      const tx = (x1 - x0) / seg, ty = (y1 - y0) / seg;
      const ahead = (x1 - cur) * fig.facing; // >0 in front of the walker
      const order = ln.branch ? 1 : Math.max(0, Math.min(1, (x1 - a) / Math.max(1, b - a)));
      const shown = reveal >= (fig.facing === 1 ? order : 1 - order) * 0.85 ? 1 : 0;
      let op = ahead > 0 ? 0.78 : 0.32; // the road ahead is brighter than the road walked
      if (shape === "fade" && ahead > 0) op *= Math.max(0, 1 - ahead / 300);
      op *= Math.max(0.15, 1 - Math.max(0, Math.abs(ahead) - 260) / 260); // ends dissolve softly
      if (ln.branch) op *= 0.85;
      out.push(
        <line key={`${li}-${i}`} x1={x1} y1={y1} x2={x1 + tx * DASH} y2={y1 + ty * DASH} stroke={COLORS.ink} strokeWidth={3.2} strokeLinecap="round" opacity={op * shown} />,
      );
    }
  });
  const gy = pathY(fig, cur);
  return (
    <g>
      {/* faint contact glow: grounds the figure on the black void */}
      <ellipse cx={cur} cy={gy + 4} rx={62 * fig.scale} ry={9 * fig.scale} fill={COLORS.ink} opacity={0.1 * reveal} />
      {out}
    </g>
  );
};

const Figure: React.FC<{ fig: NonNullable<Props["figure"]>; frame: number; dur: number }> = ({ fig, frame, dur }) => {
  const s = fig.scale;
  const f = fig.facing;
  const blend = fig.from ? prog(frame, 0, 14) : 1;
  let p = mixPose(POSES[fig.from ?? fig.pose], POSES[fig.pose], blend);
  const walking = fig.toX !== undefined;
  const walkT = walking ? prog(frame, 4, Math.max(20, dur * 0.7), easeStd) : 0;
  const x = walking ? lerp(fig.x, fig.toX!, walkT) : fig.x;
  if (walking && walkT > 0 && walkT < 1) {
    const ph = Math.sin(frame / 4.2);
    p = { ...p, rh: 24 * ph, lh: -24 * ph, rk: ph < 0 ? 30 * ph : -4, lk: ph > 0 ? -30 * ph : -4, rs: p.rs - 18 * ph, ls: p.ls + 18 * ph };
  }
  const groundY = pathY(fig, x);
  const breathe = Math.sin(frame / 13) * 2.2;
  const dir = (deg: number) => [Math.sin((deg * Math.PI) / 180) * f, Math.cos((deg * Math.PI) / 180)];
  const hip = [x, groundY - 132 * s];
  const tl = dir(180 - p.lean); // torso goes up
  const shoulder = [hip[0] + tl[0] * 108 * s, hip[1] + tl[1] * 108 * s + breathe];
  const hd = dir(180 - p.lean - p.head * 0.5);
  const head = [shoulder[0] + hd[0] * 50 * s, shoulder[1] + hd[1] * 50 * s];
  const limb = (root: number[], a1: number, a2: number, l1: number, l2: number) => {
    const d1 = dir(a1);
    const j = [root[0] + d1[0] * l1 * s, root[1] + d1[1] * l1 * s];
    const d2 = dir(a1 + a2);
    return { j, e: [j[0] + d2[0] * l2 * s, j[1] + d2[1] * l2 * s] };
  };
  const ra = limb(shoulder, p.rs, p.re, 58, 54);
  const la = limb(shoulder, p.ls, p.le, 58, 54);
  const rl = limb(hip, p.rh, p.rk, 68, 66);
  const ll = limb(hip, p.lh, p.lk, 68, 66);
  const seg = (a: number[], b: number[], c: number[], w: number, key: string, op = 1) => (
    <polyline key={key} points={`${a[0]},${a[1]} ${b[0]},${b[1]} ${c[0]},${c[1]}`} fill="none" stroke={COLORS.ink} strokeOpacity={op} strokeWidth={w * s} strokeLinecap="round" strokeLinejoin="round" />
  );
  const appear = prog(frame, 0, 10);
  return (
    <g opacity={appear * (fig.opacity ?? 1)}>
      {/* back limbs slightly dimmer for depth */}
      {seg(hip, ll.j, ll.e, 15, "ll", 0.72)}
      {seg(shoulder, la.j, la.e, 13, "la", 0.72)}
      <line x1={hip[0]} y1={hip[1]} x2={shoulder[0]} y2={shoulder[1]} stroke={COLORS.ink} strokeWidth={30 * s} strokeLinecap="round" />
      {seg(hip, rl.j, rl.e, 15, "rl")}
      <circle cx={head[0]} cy={head[1]} r={31 * s} fill={COLORS.ink} />
      {seg(shoulder, ra.j, ra.e, 13, "ra")}
      {fig.holding === "phone" || fig.pose === "phone" ? (
        <g transform={`translate(${ra.e[0] + 4 * f * s} ${ra.e[1] - 14 * s}) rotate(${-12 * f})`}>
          <rect x={-13 * s} y={-22 * s} width={26 * s} height={44 * s} rx={5 * s} fill={COLORS.bg} stroke={COLORS.ink} strokeWidth={4 * s} />
          <rect x={-9 * s} y={-17 * s} width={18 * s} height={32 * s} rx={2 * s} fill={COLORS.goldBright} opacity={0.75 + 0.25 * Math.sin(frame / 5)} filter="url(#stageGlow)" />
        </g>
      ) : null}
      {fig.holding === "coins" ? <ellipse cx={ra.e[0]} cy={ra.e[1] - 6 * s} rx={18 * s} ry={7 * s} fill={COLORS.goldBright} filter="url(#stageGlow)" /> : null}
    </g>
  );
};

/* ============================== PROPS ============================== */
type DrawCtx = { col: string; d: number; frame: number; state: string; glow: boolean; label?: string; t?: number; from?: string; to?: string };
const stroke = (c: DrawCtx, w = 4) => ({
  fill: "none",
  stroke: c.col,
  strokeWidth: w,
  strokeLinecap: "round" as const,
  strokeLinejoin: "round" as const,
  pathLength: 1,
  strokeDasharray: 1,
  strokeDashoffset: 1 - c.d,
});
const solid = (c: DrawCtx, o = 1) => ({ fill: c.col, opacity: o * c.d });

const PROP: Record<string, (c: DrawCtx) => React.ReactNode> = {
  jar: (c) => (
    <>
      <rect x={-30} y={-52} width={60} height={12} rx={3} {...stroke(c, 4)} />
      <path d="M-34 -40 Q-40 -30 -40 -16 L-40 40 Q-40 52 -28 52 L28 52 Q40 52 40 40 L40 -16 Q40 -30 34 -40 Z" {...stroke(c, 4)} />
      <rect x={-24} y={-6} width={48} height={26} rx={4} fill="none" stroke={c.col} strokeWidth={2.5} opacity={c.d * 0.7} />
    </>
  ),
  tag: (c) => (
    <>
      <path d="M-50 -24 L24 -24 L50 0 L24 24 L-50 24 Z" {...stroke(c, 4)} />
      <circle cx={28} cy={0} r={5} {...stroke(c, 3)} />
      {c.label ? <text x={-14} y={11} textAnchor="middle" fontFamily={TYPE.sans} fontWeight={800} fontSize={30} fill={c.col} opacity={c.d}>{c.label}</text> : null}
    </>
  ),
  dice: (c) => {
    const roll = c.state === "spin" ? Math.max(0, 1 - c.frame / 24) : 0;
    const face = c.state === "spin" && roll > 0 ? 1 + (Math.floor(c.frame / 3) % 6) : c.label ? Number(c.label) || 3 : 3;
    const pips: Record<number, number[][]> = {1: [[0, 0]], 2: [[-14, -14], [14, 14]], 3: [[-16, -16], [0, 0], [16, 16]], 4: [[-15, -15], [15, -15], [-15, 15], [15, 15]], 5: [[-16, -16], [16, -16], [0, 0], [-16, 16], [16, 16]], 6: [[-15, -18], [15, -18], [-15, 0], [15, 0], [-15, 18], [15, 18]], 9: [[-16, -16], [0, -16], [16, -16], [-16, 0], [0, 0], [16, 0], [-16, 16], [0, 16], [16, 16]]};
    const f = pips[face] ? face : 3;
    return (
      <g transform={`rotate(${roll * 260})`}>
        <rect x={-34} y={-34} width={68} height={68} rx={12} {...stroke(c, 4)} />
        {pips[f].map(([x, y], i) => <circle key={i} cx={x} cy={y} r={5.5} fill={c.col} opacity={c.d} />)}
      </g>
    );
  },
  wheel: (c) => {
    const ang = c.state === "spin" ? 720 * (1 - Math.pow(1 - Math.min(1, c.frame / 45), 3)) : 0;
    return (
      <>
        <g transform={`rotate(${ang})`}>
          <circle r={46} {...stroke(c, 4)} />
          {Array.from({ length: 10 }, (_, i) => {
            const a = (i / 10) * Math.PI * 2;
            return <line key={i} x1={0} y1={0} x2={Math.sin(a) * 46} y2={-Math.cos(a) * 46} stroke={c.col} strokeWidth={2} opacity={0.6 * c.d} />;
          })}
          <circle r={6} fill={c.col} opacity={c.d} />
        </g>
        <path d="M0 -60 L-8 -48 L8 -48 Z" fill={c.col} opacity={c.d} />
      </>
    );
  },
  checklist: (c) => {
    const done = c.state === "open" ? 3 : c.state === "closed" ? 0 : 2;
    return (
      <>
        <rect x={-40} y={-50} width={80} height={100} rx={8} {...stroke(c, 4)} />
        {[0, 1, 2].map((i) => (
          <g key={i} transform={`translate(-26 ${-28 + i * 28})`}>
            <rect x={0} y={-8} width={16} height={16} rx={3} fill="none" stroke={c.col} strokeWidth={2.5} opacity={c.d} />
            {i < done ? <path d="M3 0 L7 5 L14 -5" fill="none" stroke={c.col} strokeWidth={3} strokeLinecap="round" opacity={c.d} /> : null}
            <line x1={24} y1={0} x2={i === 2 ? 42 : 52} y2={0} stroke={c.col} strokeWidth={3} strokeLinecap="round" opacity={(i < done ? 0.45 : 1) * c.d} />
          </g>
        ))}
      </>
    );
  },
  gauge: (c) => {
    const valOf = (st?: string) => (st === "down" ? -60 : st === "up" ? 60 : 0);
    const wobble = c.state === "spin" ? Math.sin(c.frame / 3) * 25 : 0;
    const a = lerp(valOf(c.from), valOf(c.to ?? c.from), easeStd(c.t ?? 0)) + wobble;
    return (
      <>
        <path d="M-46 14 A46 46 0 0 1 46 14" {...stroke(c, 4)} />
        {[-60, -30, 0, 30, 60].map((t) => (
          <line key={t} x1={Math.sin((t * Math.PI) / 180) * 38} y1={14 - Math.cos((t * Math.PI) / 180) * 38} x2={Math.sin((t * Math.PI) / 180) * 46} y2={14 - Math.cos((t * Math.PI) / 180) * 46} stroke={c.col} strokeWidth={3} opacity={c.d} />
        ))}
        <line x1={0} y1={14} x2={Math.sin((a * Math.PI) / 180) * 36} y2={14 - Math.cos((a * Math.PI) / 180) * 36} stroke={c.col} strokeWidth={4} strokeLinecap="round" opacity={c.d} />
        <circle cx={0} cy={14} r={5} fill={c.col} opacity={c.d} />
      </>
    );
  },
  balance: (c) => {
    // tilt eases between states: down = left pan sinks, up = right pan sinks
    const tiltOf = (st?: string) => (st === "down" ? -13 : st === "up" ? 13 : 0);
    const tilt = lerp(tiltOf(c.from), tiltOf(c.to ?? c.from), easeStd(c.t ?? 0));
    const r = (tilt * Math.PI) / 180;
    const pan = (sx: number) => {
      const px = Math.cos(r) * sx, py = Math.sin(r) * sx - 34;
      return (
        <g transform={`translate(${px} ${py})`}>
          <line x1={0} y1={0} x2={-14} y2={34} stroke={c.col} strokeWidth={2.5} opacity={c.d} />
          <line x1={0} y1={0} x2={14} y2={34} stroke={c.col} strokeWidth={2.5} opacity={c.d} />
          <path d="M-22 34 Q0 48 22 34 Z" {...stroke(c, 4)} />
        </g>
      );
    };
    return (
      <>
        <path d="M0 -40 L0 50 M-26 50 L26 50" {...stroke(c, 5)} />
        <circle cx={0} cy={-40} r={4} fill={c.col} opacity={c.d} />
        <line x1={-46 * Math.cos(r)} y1={-34 - 46 * Math.sin(r)} x2={46 * Math.cos(r)} y2={-34 + 46 * Math.sin(r)} stroke={c.col} strokeWidth={4} strokeLinecap="round" opacity={c.d} />
        {pan(-46)}
        {pan(46)}
      </>
    );
  },
  cctv: (c) => {
    const sweep = Math.sin(c.frame / 28) * 9;
    const rec = Math.floor(c.frame / 15) % 2 === 0 ? 1 : 0.25;
    return (
      <>
        <path d="M34 -30 L34 -6 L18 -6" {...stroke(c, 4)} />
        <g transform={`rotate(${12 + sweep} 18 -6)`}>
          <rect x={-40} y={-20} width={58} height={28} rx={5} {...stroke(c, 4)} />
          <path d="M-40 -14 L-54 -18 L-54 4 L-40 0" {...stroke(c, 3.5)} />
          <circle cx={8} cy={-6} r={3.5} fill={c.col} opacity={c.d * rec} />
        </g>
      </>
    );
  },
  shirt: (c) => (
    <>
      <path d="M-20 -44 L-46 -30 L-36 -8 L-26 -14 L-26 44 L26 44 L26 -14 L36 -8 L46 -30 L20 -44 Q0 -30 -20 -44 Z" {...stroke(c, 4)} />
      <circle cx={0} cy={6} r={12} {...stroke(c, 3)} />
    </>
  ),
  phone: (c) => (
    <>
      <rect x={-26} y={-46} width={52} height={92} rx={9} {...stroke(c)} />
      <rect x={-19} y={-36} width={38} height={66} rx={3} fill={c.glow ? COLORS.goldBright : "rgba(255,255,255,0.08)"} opacity={c.d * (c.glow ? 0.8 + 0.2 * Math.sin(c.frame / 5) : 1)} />
      {c.glow ? [0, 1, 2].map((i) => <rect key={i} x={-14} y={-28 + i * 14} width={28 - i * 6} height={7} rx={3} fill={COLORS.bg} opacity={0.55 * c.d} />) : null}
      <circle cx={0} cy={38} r={3} fill={c.col} opacity={c.d} />
    </>
  ),
  book: (c) => (
    <>
      <path d="M0 -28 L0 34" {...stroke(c)} />
      <path d="M0 -28 Q-24 -38 -48 -30 L-48 30 Q-24 22 0 34" {...stroke(c)} />
      <path d="M0 -28 Q24 -38 48 -30 L48 30 Q24 22 0 34" {...stroke(c)} />
      {[-12, 0, 12].map((y) => <path key={y} d={`M-38 ${y - 8} L-10 ${y - 4} M10 ${y - 4} L38 ${y - 8}`} {...stroke(c, 2.5)} />)}
    </>
  ),
  clock: (c) => {
    const sp = c.state === "spin" ? 14 : 1.2;
    return (
      <>
        <circle r={44} {...stroke(c)} />
        {Array.from({ length: 12 }, (_, i) => {
          const a = (i / 12) * Math.PI * 2;
          return <line key={i} x1={Math.sin(a) * 36} y1={-Math.cos(a) * 36} x2={Math.sin(a) * 41} y2={-Math.cos(a) * 41} stroke={c.col} strokeWidth={3} opacity={c.d} />;
        })}
        <line x1={0} y1={0} x2={0} y2={-24} stroke={c.col} strokeWidth={5} strokeLinecap="round" transform={`rotate(${c.frame * sp * 0.08})`} opacity={c.d} />
        <line x1={0} y1={0} x2={0} y2={-34} stroke={COLORS.goldBright} strokeWidth={3} strokeLinecap="round" transform={`rotate(${c.frame * sp})`} opacity={c.d} />
        <circle r={4} fill={c.col} opacity={c.d} />
      </>
    );
  },
  coins: (c) => (
    <>
      {[24, 10, -4, -18].map((y, i) => (
        <g key={i} opacity={c.d}>
          <path d={`M-34 ${y} L-34 ${y + 10} A34 10 0 0 0 34 ${y + 10} L34 ${y}`} fill={COLORS.bg} stroke={c.col} strokeWidth={4} />
          <ellipse cx={0} cy={y} rx={34} ry={10} fill={COLORS.bg} stroke={c.col} strokeWidth={4} />
        </g>
      ))}
      <text x={0} y={-12} textAnchor="middle" fontFamily={TYPE.sans} fontWeight={800} fontSize={16} fill={c.col} opacity={c.d}>$</text>
    </>
  ),
  bill: (c) => (
    <>
      <rect x={-48} y={-26} width={96} height={52} rx={5} {...stroke(c)} />
      <rect x={-40} y={-18} width={80} height={36} rx={3} {...stroke(c, 2)} />
      <circle r={13} {...stroke(c, 3)} />
      <text x={0} y={7} textAnchor="middle" fontFamily={TYPE.sans} fontWeight={800} fontSize={20} fill={c.col} opacity={c.d}>$</text>
    </>
  ),
  piggy: (c) => (
    <>
      <ellipse cx={-4} cy={4} rx={40} ry={30} {...stroke(c)} />
      <ellipse cx={38} cy={4} rx={8} ry={10} {...stroke(c, 3.5)} />
      <path d="M-16 -22 L-10 -38 L2 -26" {...stroke(c, 3.5)} />
      <path d="M-26 30 L-26 42 M-6 33 L-6 44 M12 32 L12 43 M24 28 L24 40" {...stroke(c, 4)} />
      <path d="M-12 -14 L8 -14" {...stroke(c, 4)} />
      <path d="M-44 0 q-12 -6 -6 -14" {...stroke(c, 3)} />
      <circle cx={18} cy={-6} r={2.5} fill={c.col} opacity={c.d} />
    </>
  ),
  door: (c) => {
    const open = c.state === "open" ? 1 : 0;
    return (
      <>
        {open ? <polygon points="-30,-56 30,-56 30,56 -30,56" fill={COLORS.goldBright} opacity={0.85 * c.d} filter="url(#stageGlow)" /> : null}
        {open ? <polygon points="-30,56 30,56 70,110 -70,110" fill={COLORS.goldBright} opacity={0.16 * c.d} /> : null}
        <rect x={-30} y={-56} width={60} height={112} {...stroke(c)} />
        {open ? (
          <polygon points="-30,-56 -12,-48 -12,50 -30,56" fill={COLORS.bg} stroke={c.col} strokeWidth={4} opacity={c.d} />
        ) : (
          <>
            <rect x={-24} y={-50} width={48} height={100} {...stroke(c, 2.5)} />
            <circle cx={16} cy={4} r={4} fill={c.col} opacity={c.d} />
          </>
        )}
      </>
    );
  },
  mountain: (c) => (
    <>
      <path d="M-50 40 L-14 -22 L4 4 L20 -12 L50 40 Z" {...stroke(c)} />
      <path d="M-14 -22 L-14 -50" {...stroke(c, 3.5)} />
      <path d="M-14 -50 L12 -43 L-14 -36 Z" fill={COLORS.goldBright} opacity={c.d} />
    </>
  ),
  brain: (c) => (
    <>
      <path d="M-40 10 C-52 -10 -40 -38 -14 -40 C0 -52 26 -46 34 -30 C50 -26 54 -4 44 8 C50 22 36 36 20 32 C8 42 -10 40 -18 30 C-34 34 -46 24 -40 10 Z" {...stroke(c)} />
      <path d="M-18 -22 C-6 -12 -22 0 -8 10 M10 -32 C2 -18 18 -10 8 2 M26 6 C14 12 24 22 12 26 M-30 14 C-20 12 -16 22 -6 18" {...stroke(c, 3)} />
      <path d="M8 34 L12 48" {...stroke(c, 4)} />
    </>
  ),
  chart: (c) => {
    const down = c.state !== "up";
    return (
      <>
        <path d="M-46 -44 L-46 42 L48 42" {...stroke({ ...c, col: COLORS.ink })} />
        <path d={down ? "M-38 -30 L-14 -18 L8 4 L36 22" : "M-38 26 L-14 10 L8 -6 L36 -28"} {...stroke(c, 5)} />
        <path d={down ? "M24 22 L38 23 L32 10" : "M24 -28 L38 -29 L33 -16"} {...stroke(c, 5)} />
      </>
    );
  },
  donut: (c) => (
    <>
      <circle r={42} {...stroke(c)} />
      <circle r={13} {...stroke(c)} />
      <path d="M-36 -10 Q-30 -32 -6 -36 Q20 -40 34 -18 Q30 -8 24 -12 Q14 0 4 -14 Q-6 -2 -16 -12 Q-24 -2 -36 -10 Z" {...stroke(c, 3)} />
      {[[-20, -24, 20], [2, -28, -30], [18, -26, 40], [-6, -20, 60]].map(([x, y, r], i) => (
        <line key={i} x1={x - 4} y1={y} x2={x + 4} y2={y} stroke={COLORS.goldBright} strokeWidth={4} strokeLinecap="round" transform={`rotate(${r} ${x} ${y})`} opacity={c.d} />
      ))}
    </>
  ),
  apple: (c) => (
    <>
      <path d="M0 -24 C-18 -36 -46 -26 -42 4 C-38 30 -18 46 0 36 C18 46 38 30 42 4 C46 -26 18 -36 0 -24 Z" {...stroke(c)} />
      <path d="M0 -24 L4 -42" {...stroke(c, 3.5)} />
      <path d="M6 -36 Q22 -48 30 -34 Q16 -28 6 -36 Z" fill={COLORS.green} opacity={0.8 * c.d} />
    </>
  ),
  dumbbell: (c) => (
    <>
      <path d="M-30 0 L30 0" {...stroke(c, 6)} />
      <rect x={-46} y={-22} width={12} height={44} rx={3} {...stroke(c)} />
      <rect x={34} y={-22} width={12} height={44} rx={3} {...stroke(c)} />
      <rect x={-32} y={-14} width={8} height={28} rx={2} {...stroke(c, 3)} />
      <rect x={24} y={-14} width={8} height={28} rx={2} {...stroke(c, 3)} />
    </>
  ),
  cart: (c) => (
    <>
      <path d="M-50 -34 L-36 -34 L-24 20 L34 20 L44 -18 L-30 -18" {...stroke(c)} />
      <circle cx={-16} cy={34} r={7} {...stroke(c)} />
      <circle cx={26} cy={34} r={7} {...stroke(c)} />
      <path d="M-16 -6 L36 -6 M-12 8 L32 8" {...stroke(c, 2.5)} />
    </>
  ),
  lock: (c) => (
    <>
      <path d="M-22 -6 L-22 -26 A22 22 0 0 1 22 -26 L22 -6" {...stroke(c, 5)} />
      <rect x={-34} y={-8} width={68} height={54} rx={8} {...stroke(c)} />
      <circle cx={0} cy={14} r={6} fill={c.col} opacity={c.d} />
      <path d="M0 18 L0 32" {...stroke(c, 4)} />
    </>
  ),
  calendar: (c) => (
    <>
      <rect x={-44} y={-36} width={88} height={82} rx={8} {...stroke(c)} />
      <path d="M-44 -14 L44 -14 M-24 -46 L-24 -28 M24 -46 L24 -28" {...stroke(c)} />
      {c.label ? (
        <text x={0} y={22} textAnchor="middle" fontFamily={TYPE.sans} fontWeight={800} fontSize={c.label.length > 6 ? 17 : 22} fill={c.col} opacity={c.d}>
          {c.label}
        </text>
      ) : null}
    </>
  ),
  bubble: (c) => (
    <>
      <path d="M-50 -34 Q-50 -44 -40 -44 L40 -44 Q50 -44 50 -34 L50 18 Q50 28 40 28 L-6 28 L-24 46 L-22 28 L-40 28 Q-50 28 -50 18 Z" {...stroke(c)} />
      {[-20, 0, 20].map((x, i) => (
        <circle key={x} cx={x} cy={-8 - (c.state === "typing" ? Math.max(0, Math.sin(c.frame / 4 - i * 0.9)) * 8 : 0)} r={6} fill={c.col} opacity={c.d} />
      ))}
    </>
  ),
  question: (c) => (
    <text x={0} y={34} textAnchor="middle" fontFamily={TYPE.display} fontWeight={700} fontSize={100} fill={c.col} opacity={c.d}>
      ?
    </text>
  ),
  hourglass: (c) => {
    const t = (c.frame % 90) / 90;
    return (
      <>
        <path d="M-30 -46 L30 -46 M-30 46 L30 46 M-24 -46 C-24 -10 24 -10 24 -46 M-24 46 C-24 10 24 10 24 46 M-24 -46 C-24 -14 0 -4 0 0 C0 4 -24 14 -24 46 M24 -46 C24 -14 0 -4 0 0 C0 4 24 14 24 46" {...stroke(c)} />
        <path d={`M${-18 * (1 - t)} ${-34 + 26 * t} L${18 * (1 - t)} ${-34 + 26 * t} L0 -4 Z`} fill={COLORS.goldBright} opacity={c.d} />
        <path d={`M-18 40 L18 40 L${10 * t} ${40 - 22 * t} L${-10 * t} ${40 - 22 * t} Z`} fill={COLORS.goldBright} opacity={c.d} />
      </>
    );
  },
  lightbulb: (c) => (
    <>
      {c.glow ? <circle r={58} fill={COLORS.goldBright} opacity={0.18 * c.d} filter="url(#stageGlow)" /> : null}
      <path d="M-16 22 C-16 8 -32 0 -32 -18 A32 32 0 0 1 32 -18 C32 0 16 8 16 22 Z" {...stroke(c)} />
      <path d="M-14 30 L14 30 M-10 38 L10 38" {...stroke(c)} />
    </>
  ),
};

const Mark: React.FC<{ kind: "check" | "cross" | "question"; p: number }> = ({ kind, p }) => {
  const col = kind === "check" ? COLORS.green : kind === "cross" ? COLORS.red : COLORS.goldBright;
  return (
    <g transform={`scale(${0.4 + 0.6 * p})`} opacity={p}>
      <circle r={22} fill={COLORS.bg} stroke={col} strokeWidth={4} />
      {kind === "check" ? <path d="M-10 0 L-3 8 L11 -8" fill="none" stroke={col} strokeWidth={5} strokeLinecap="round" strokeLinejoin="round" /> : null}
      {kind === "cross" ? <path d="M-8 -8 L8 8 M8 -8 L-8 8" stroke={col} strokeWidth={5} strokeLinecap="round" /> : null}
      {kind === "question" ? <text y={9} textAnchor="middle" fontFamily={TYPE.sans} fontWeight={800} fontSize={26} fill={col}>?</text> : null}
    </g>
  );
};

const PropView: React.FC<{ p: z.infer<typeof StageProp>; frame: number; fps: number; dur: number }> = ({ p, frame, fps, dur }) => {
  const start = Math.round(p.delay * fps);
  const e = prog(frame, start, p.enter === "draw" ? 22 : 14);
  const toStart = p.to ? Math.round(p.to.at * dur) : Infinity;
  const tt = p.to ? prog(frame, toStart, 18, easeStd) : 0;
  const x = lerp(p.x, p.to?.x ?? p.x, tt);
  const y = lerp(p.y, p.to?.y ?? p.y, tt);
  const size = lerp(p.size, p.to?.size ?? p.size, tt);
  const accent = (tt > 0.5 && p.to?.accent) || p.accent;
  const state = (tt > 0.5 && p.to?.state) || p.state;
  const glow = state === "glow" || state === "open";
  const dim = state === "dim";
  let dx = 0, dy = 0, sc = 1, op = 1;
  if (p.enter === "pop") { sc = interpolate(e, [0, 1], [0.3, 1]); op = Math.min(1, e * 2); }
  if (p.enter === "slideLeft") { dx = (1 - e) * -260; op = e; }
  if (p.enter === "slideRight") { dx = (1 - e) * 260; op = e; }
  if (p.enter === "drop") { dy = (1 - e) * -240; op = Math.min(1, e * 2); }
  if (p.enter === "fade") op = e;
  if (p.enter === "none") op = 1;
  const d = p.enter === "draw" ? e : 1;
  if (p.enter === "draw") op = e > 0 ? 1 : 0;
  const pulse = glow ? 1 + 0.035 * Math.sin(frame / 6) : 1;
  const k = (size / 100) * sc * pulse;
  const col = accentColor(accent);
  const markP = p.mark ? prog(frame, Math.round(p.markAt * dur), 12) : 0;
  const labelP = prog(frame, start + 8, 12);
  const opacity = op * (dim ? interpolate(tt > 0 && p.to?.state === "dim" ? tt : 1, [0, 1], [1, 0.3]) : 1);
  const draw = PROP[p.kind];
  return (
    <g transform={`translate(${x + dx} ${y + dy})`} opacity={opacity}>
      <g transform={`scale(${k})`} filter={glow ? "url(#stageGlow)" : undefined}>
        {draw({ col, d, frame, state, glow, label: ["calendar", "tag", "dice"].includes(p.kind) ? p.label : undefined, t: tt, from: p.state, to: p.to?.state })}
      </g>
      {p.mark ? (
        <g transform={`translate(${size * 0.42} ${-size * 0.42})`}>
          <Mark kind={p.mark} p={markP} />
        </g>
      ) : null}
      {p.label && !["calendar", "tag", "dice"].includes(p.kind) ? (
        <text y={size * 0.6 + 44} textAnchor="middle" fontFamily={TYPE.sans} fontWeight={700} fontSize={SCALE.label / SCALE.visual} fill={col} opacity={labelP}
          style={{ paintOrder: "stroke", stroke: "rgba(0,0,0,0.8)", strokeWidth: 8 }}>
          {p.label}
        </text>
      ) : null}
      {p.sublabel ? (
        <text y={size * 0.6 + (p.kind === "calendar" ? 44 : 86)} textAnchor="middle" fontFamily={TYPE.sans} fontWeight={400} fontSize={26 / SCALE.visual} fill={COLORS.inkMuted} opacity={labelP}>
          {p.sublabel}
        </text>
      ) : null}
    </g>
  );
};

const Counter: React.FC<{ c: z.infer<typeof StageCounter>; frame: number; fps: number }> = ({ c, frame, fps }) => {
  const start = Math.round(c.delay * fps);
  const t = prog(frame, start, Math.round(c.seconds * fps), easeStd);
  const appear = prog(frame, start, 8);
  const v = Math.round(lerp(c.from, c.to, t));
  const col = accentColor(c.accent);
  return (
    <text x={c.x} y={c.y} textAnchor="middle" fontFamily={TYPE.sans} fontWeight={800} fontSize={c.size * SCALE.counter} fill={col} opacity={appear}
      letterSpacing={-2} filter="url(#stageGlow)" transform={`translate(0 ${(1 - appear) * 30})`}>
      {c.prefix}
      {v.toLocaleString("es-CL")}
      {c.suffix}
    </text>
  );
};

/* ============================== STAGE ============================== */
export const Stage: React.FC<Props> = ({ figure, extras, props, texts, counters, spotlight, camera, note, durationInFrames }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const t = frame / Math.max(1, durationInFrames);
  const BASE = SCALE.visual; // minimal framing: leave negative space around the action
  const zoom = BASE * lerp(camera.fromZoom, camera.toZoom, easeStd(Math.min(1, t)));
  const pan = camera.panX * easeStd(Math.min(1, t));
  const feetY = figure?.y ?? 1120;
  let spot = 0;
  if (spotlight) {
    spot = spotlight.snap ? (frame < 3 ? 0 : frame < 5 ? 1 : frame < 7 ? 0.35 : 1) : prog(frame, 0, 12);
  }
  const spotCol = spotlight ? accentColor(spotlight.accent) : COLORS.ink;
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ transformOrigin: `${camera.x}px ${camera.y}px`, scale: String(zoom), translate: `${-pan}px 0px` }}>
        <svg width={width} height={height} style={{ position: "absolute" }}>
          <defs>
            <filter id="stageGlow" x="-60%" y="-60%" width="220%" height="220%">
              <feGaussianBlur stdDeviation="9" result="b" />
              <feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge>
            </filter>
            <linearGradient id="beam" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={spotCol} stopOpacity="0.22" />
              <stop offset="100%" stopColor={spotCol} stopOpacity="0.03" />
            </linearGradient>
            <radialGradient id="pool">
              <stop offset="0%" stopColor={spotCol} stopOpacity="0.32" />
              <stop offset="100%" stopColor={spotCol} stopOpacity="0" />
            </radialGradient>
          </defs>
          {spotlight ? (
            <g opacity={spot}>
              <polygon points={`${spotlight.x - 50},-20 ${spotlight.x + 50},-20 ${spotlight.x + 250},${feetY} ${spotlight.x - 250},${feetY}`} fill="url(#beam)" />
              <ellipse cx={spotlight.x} cy={feetY} rx={280} ry={50} fill="url(#pool)" />
            </g>
          ) : null}
          {props.map((p, i) => <PropView key={i} p={p} frame={frame} fps={fps} dur={durationInFrames} />)}
          {(extras ?? []).map((ex, i) =>
            ex.path !== "auto" && ex.path !== "none" ? <DashedPath key={`xp${i}`} fig={ex} frame={frame} dur={durationInFrames} /> : null,
          )}
          {(extras ?? []).map((ex, i) => <Figure key={`x${i}`} fig={ex} frame={frame} dur={durationInFrames} />)}
          {figure ? <DashedPath fig={figure} frame={frame} dur={durationInFrames} /> : null}
          {figure ? <Figure fig={figure} frame={frame} dur={durationInFrames} /> : null}
          {counters.map((c, i) => <Counter key={i} c={c} frame={frame} fps={fps} />)}
        </svg>
      </AbsoluteFill>
      {/* texts stay screen-fixed so camera moves never push them out of the safe area */}
      {texts.map((tx, i) => (
          <div key={i} style={{ position: "absolute", left: tx.x - 470, width: 940, top: tx.y - tx.size * SCALE.text * 0.62 }}>
            <RichLine text={tx.content} emphasis={tx.emphasis} frame={frame} start={Math.round(tx.delay * fps)} stagger={2} size={Math.round(tx.size * SCALE.text)}
              family={tx.family} weight={tx.family === "sans" ? 800 : 700} colorOverride={tx.accent === "white" ? undefined : accentColor(tx.accent)} />
          </div>
        ))}
      {note ? (
        <div style={{ position: "absolute", top: 1440, left: 90, right: 170, textAlign: "center", fontFamily: TYPE.sans, fontSize: 26, color: COLORS.inkMuted, opacity: prog(frame, 20, 14) }}>
          {note}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
