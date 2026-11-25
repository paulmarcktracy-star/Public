import React, { useMemo } from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import type { z } from "zod";
import type {
  BehaviorLoop as BehaviorLoopS,
  DiscountCurve as DiscountCurveS,
  EmotionWave as EmotionWaveS,
  NeuralNetwork as NeuralNetworkS,
  TwoForces as TwoForcesS,
} from "../schema";
import { COLORS, TYPE } from "../design/tokens";
import { easeStd, lerp, prog, rng } from "../components/anim";

type D = { durationInFrames: number };
const W = 1080;
const H = 1920;

const Label: React.FC<{ x: number; y: number; text: string; size?: number; color?: string; anchor?: "middle" | "start" | "end"; weight?: number; opacity?: number; family?: string }> = ({
  x, y, text, size = 38, color = COLORS.ink, anchor = "middle", weight = 600, opacity = 1, family = TYPE.sans,
}) => (
  <text x={x} y={y} fontFamily={family} fontWeight={weight} fontSize={size} fill={color} textAnchor={anchor} opacity={opacity}
    style={{ paintOrder: "stroke", stroke: "rgba(0,0,0,0.75)", strokeWidth: 8, strokeLinejoin: "round" }}>
    {text}
  </text>
);

const Glow = () => (
  <defs>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="10" result="b" />
      <feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge>
    </filter>
    <radialGradient id="orb" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stopColor="#FFF4D6" />
      <stop offset="45%" stopColor={COLORS.goldBright} />
      <stop offset="100%" stopColor={COLORS.goldDeep} stopOpacity="0" />
    </radialGradient>
  </defs>
);

/* ---------------- Neural network ---------------- */
export const NeuralNetwork: React.FC<z.infer<typeof NeuralNetworkS> & D> = ({ label, mode, caption, durationInFrames }) => {
  const frame = useCurrentFrame();
  const net = useMemo(() => {
    const r = rng(11);
    const nodes = Array.from({ length: 46 }, (_, i) => {
      const cluster = i % 3;
      return {
        x: 140 + r() * 800,
        y: 300 + r() * 760,
        cx: [300, 540, 780][cluster],
        cy: [520, 820, 520][cluster],
        r: 6 + r() * 7,
        phase: r() * 60,
      };
    });
    const edges: [number, number][] = [];
    nodes.forEach((a, i) =>
      nodes.forEach((b, j) => {
        if (j > i && Math.hypot(a.x - b.x, a.y - b.y) < 210) edges.push([i, j]);
      }),
    );
    // a strong path through the network
    const path = [0, 7, 15, 22, 31, 40].filter((k) => k < nodes.length);
    return { nodes, edges, path };
  }, []);
  const appear = prog(frame, 0, 30);
  const org = mode === "organizing" ? prog(frame, 20, durationInFrames * 0.5, easeStd) : 0;
  const pos = (i: number) => {
    const n = net.nodes[i];
    return { x: lerp(n.x, n.cx + (n.x - 540) * 0.18, org), y: lerp(n.y, n.cy + (n.y - 680) * 0.18, org) };
  };
  const strong = mode === "strengthening" ? prog(frame, 20, durationInFrames * 0.6) : 0;

  return (
    <AbsoluteFill>
      <svg width={W} height={H}>
        <Glow />
        {net.edges.map(([a, b], k) => {
          const A = pos(a), B = pos(b);
          const onPath = net.path.includes(a) && net.path.includes(b) && Math.abs(net.path.indexOf(a) - net.path.indexOf(b)) === 1;
          return (
            <line key={k} x1={A.x} y1={A.y} x2={B.x} y2={B.y}
              stroke={onPath && strong > 0 ? COLORS.gold : COLORS.ink}
              strokeOpacity={(onPath ? 0.18 + 0.8 * strong : 0.14) * appear}
              strokeWidth={onPath ? 1.5 + 7 * strong : 1.5} />
          );
        })}
        {/* firing signals travelling along edges */}
        {net.edges.filter((_, k) => k % 3 === 0).map(([a, b], k) => {
          const p = ((frame + k * 9) % 45) / 45;
          const A = pos(a), B = pos(b);
          return <circle key={`s${k}`} cx={lerp(A.x, B.x, p)} cy={lerp(A.y, B.y, p)} r={4} fill={COLORS.goldBright} opacity={Math.sin(p * Math.PI) * appear * 0.9} filter="url(#glow)" />;
        })}
        {net.nodes.map((n, i) => {
          const P = pos(i);
          const fire = Math.max(0, Math.sin((frame + n.phase) / 9)) ** 6;
          return (
            <g key={i} opacity={appear}>
              <circle cx={P.x} cy={P.y} r={n.r + fire * 10} fill={COLORS.gold} opacity={0.15 + fire * 0.35} filter="url(#glow)" />
              <circle cx={P.x} cy={P.y} r={n.r * 0.6} fill={fire > 0.3 ? COLORS.goldBright : COLORS.ink} />
            </g>
          );
        })}
        {label ? <Label x={540} y={230} text={label} size={50} color={COLORS.goldBright} opacity={prog(frame, 10, 16)} /> : null}
        {caption ? <Label x={540} y={1170} text={caption} size={36} color={COLORS.inkMuted} weight={400} opacity={prog(frame, 24, 16)} /> : null}
      </svg>
    </AbsoluteFill>
  );
};

/* ---------------- Two forces (choice between task and reward) ---------------- */
const ForceIcon: React.FC<{ kind: "task" | "reward" | "future" | "now"; x: number; y: number; glow: number; frame: number }> = ({ kind, x, y, glow, frame }) => {
  if (kind === "reward" || kind === "now") {
    const pulse = 1 + 0.06 * Math.sin(frame / 6);
    return (
      <g>
        {[0, 1, 2, 3, 4, 5, 6, 7].map((k) => {
          const a = (k / 8) * Math.PI * 2 + frame / 60;
          return <line key={k} x1={x + Math.cos(a) * 95} y1={y + Math.sin(a) * 95} x2={x + Math.cos(a) * (120 + 30 * glow)} y2={y + Math.sin(a) * (120 + 30 * glow)} stroke={COLORS.gold} strokeWidth={3} opacity={0.3 + 0.6 * glow} strokeLinecap="round" />;
        })}
        <circle cx={x} cy={y} r={88 * pulse} fill="url(#orb)" opacity={0.55 + 0.45 * glow} filter="url(#glow)" />
      </g>
    );
  }
  if (kind === "future") {
    return (
      <g opacity={0.5 + 0.5 * glow}>
        <path d={`M${x - 110} ${y + 70} L${x - 20} ${y - 60} L${x + 20} ${y} L${x + 50} ${y - 30} L${x + 120} ${y + 70} Z`} fill="none" stroke={COLORS.ink} strokeWidth={3} strokeLinejoin="round" />
        <line x1={x - 20} y1={y - 60} x2={x - 20} y2={y - 120} stroke={COLORS.gold} strokeWidth={3} />
        <path d={`M${x - 20} ${y - 120} L${x + 30} ${y - 106} L${x - 20} ${y - 92} Z`} fill={COLORS.gold} />
      </g>
    );
  }
  // task: a document with unchecked lines and a stalled progress bar
  return (
    <g opacity={0.55 + 0.45 * glow}>
      <rect x={x - 85} y={y - 110} width={170} height={220} rx={14} fill="rgba(245,242,234,0.06)" stroke={COLORS.ink} strokeWidth={3} />
      {[0, 1, 2, 3].map((k) => (
        <g key={k}>
          <rect x={x - 60} y={y - 78 + k * 40} width={22} height={22} rx={4} fill="none" stroke={COLORS.inkMuted} strokeWidth={2.5} />
          <line x1={x - 26} y1={y - 67 + k * 40} x2={x + 58} y2={y - 67 + k * 40} stroke={COLORS.inkMuted} strokeWidth={3} strokeLinecap="round" />
        </g>
      ))}
      <rect x={x - 60} y={y + 84} width={120} height={8} rx={4} fill={COLORS.inkFaint} />
      <rect x={x - 60} y={y + 84} width={30} height={8} rx={4} fill={COLORS.danger} />
    </g>
  );
};

export const TwoForces: React.FC<z.infer<typeof TwoForcesS> & D> = ({ left, right, winner, durationInFrames }) => {
  const frame = useCurrentFrame();
  const appear = prog(frame, 0, 24);
  const pull = prog(frame, 20, Math.max(20, durationInFrames * 0.55), easeStd);
  const dir = winner === "right" ? 1 : winner === "left" ? -1 : 0;
  const fx = 540 + dir * 110 * pull;
  const lean = dir * 12 * pull;
  const glowL = winner === "left" ? 0.4 + 0.6 * pull : winner === "right" ? 0.6 - 0.4 * pull : 0.6;
  const glowR = winner === "right" ? 0.4 + 0.6 * pull : winner === "left" ? 0.6 - 0.4 * pull : 0.6;
  const L = { x: 220, y: 470 }, R = { x: 860, y: 470 };
  const headY = 930;
  const tether = (tx: number, strength: number, k: string) => (
    <path key={k} d={`M${fx} ${headY - 56} Q ${(fx + tx) / 2} ${headY - 200 - 60 * strength} ${tx} ${L.y + 262}`} fill="none" stroke={COLORS.gold}
      strokeWidth={1.5 + 5 * strength} strokeOpacity={0.2 + 0.7 * strength} strokeDasharray="14 12" strokeDashoffset={-frame * (1 + 3 * strength)} />
  );
  return (
    <AbsoluteFill style={{ opacity: appear }}>
      <svg width={W} height={H}>
        <Glow />
        {tether(L.x, glowL, "l")}
        {tether(R.x, glowR, "r")}
        <ForceIcon kind={left.kind} x={L.x} y={L.y} glow={glowL} frame={frame} />
        <ForceIcon kind={right.kind} x={R.x} y={R.y} glow={glowR} frame={frame} />
        {/* abstract person */}
        <g transform={`rotate(${lean} ${fx} ${headY + 250})`}>
          <circle cx={fx} cy={headY} r={52} fill="none" stroke={COLORS.ink} strokeWidth={4} />
          <path d={`M${fx - 90} ${headY + 220} Q ${fx - 90} ${headY + 90} ${fx} ${headY + 85} Q ${fx + 90} ${headY + 90} ${fx + 90} ${headY + 220}`} fill="none" stroke={COLORS.ink} strokeWidth={4} strokeLinecap="round" />
          <circle cx={fx} cy={headY} r={14} fill={COLORS.gold} opacity={0.4 + 0.5 * Math.abs(Math.sin(frame / 10))} filter="url(#glow)" />
        </g>
        <Label x={L.x} y={L.y + 190} text={left.label} size={44} opacity={prog(frame, 10, 14)} color={winner === "left" ? COLORS.goldBright : COLORS.ink} />
        {left.sublabel ? <Label x={L.x} y={L.y + 240} text={left.sublabel} size={30} weight={400} color={COLORS.inkMuted} opacity={prog(frame, 16, 14)} /> : null}
        <Label x={R.x} y={R.y + 190} text={right.label} size={44} opacity={prog(frame, 14, 14)} color={winner === "right" ? COLORS.goldBright : COLORS.ink} />
        {right.sublabel ? <Label x={R.x} y={R.y + 240} text={right.sublabel} size={30} weight={400} color={COLORS.inkMuted} opacity={prog(frame, 20, 14)} /> : null}
      </svg>
    </AbsoluteFill>
  );
};

/* ---------------- Hyperbolic discounting: preference reversal ---------------- */
export const DiscountCurve: React.FC<z.infer<typeof DiscountCurveS> & D> = ({ xLabel, yLabel, nowLabel, laterLabel, note, durationInFrames }) => {
  const frame = useCurrentFrame();
  const x0 = 140, x1 = 960, y0 = 1080, y1 = 330;
  const X = (t: number) => lerp(x0, x1, t);
  const Y = (v: number) => lerp(y0, y1, v);
  const small = { t: 0.42, v: 0.55 };
  const large = { t: 0.9, v: 0.95 };
  const k = 9;
  const curve = (rw: { t: number; v: number }) =>
    Array.from({ length: 80 }, (_, i) => {
      const t = (i / 79) * rw.t;
      const delay = rw.t - t;
      return `${i ? "L" : "M"}${X(t)} ${Y(rw.v / (1 + k * delay))}`;
    }).join(" ");
  const axes = prog(frame, 0, 18);
  const bars = prog(frame, 12, 18);
  const draw = prog(frame, 26, Math.max(24, durationInFrames * 0.4), easeStd);
  const today = prog(frame, 26 + durationInFrames * 0.4, 18);
  const todayX = X(0.12);
  const vSmallToday = small.v / (1 + k * (small.t - 0.12));
  const vLargeToday = large.v / (1 + k * (large.t - 0.12));
  return (
    <AbsoluteFill>
      <svg width={W} height={H}>
        <Glow />
        <g opacity={axes}>
          <line x1={x0} y1={y0} x2={x1 + 20} y2={y0} stroke={COLORS.inkMuted} strokeWidth={3} />
          <line x1={x0} y1={y0} x2={x0} y2={y1 - 40} stroke={COLORS.inkMuted} strokeWidth={3} />
          <Label x={x1} y={y0 + 60} text={xLabel} size={32} anchor="end" weight={400} color={COLORS.inkMuted} />
          <Label x={x0} y={y1 - 70} text={yLabel} size={32} anchor="start" weight={400} color={COLORS.inkMuted} />
        </g>
        {[small, large].map((rw, i) => (
          <g key={i} opacity={bars}>
            <rect x={X(rw.t) - 26} y={Y(rw.v * bars)} width={52} height={y0 - Y(rw.v * bars)} rx={8} fill={i === 0 ? COLORS.gold : COLORS.ink} opacity={0.9} />
            <Label x={X(rw.t)} y={Y(rw.v) - 30} text={i === 0 ? nowLabel : laterLabel} size={34} color={i === 0 ? COLORS.goldBright : COLORS.ink} />
          </g>
        ))}
        {[small, large].map((rw, i) => (
          <path key={`c${i}`} d={curve(rw)} fill="none" stroke={i === 0 ? COLORS.goldBright : COLORS.ink} strokeWidth={5}
            strokeDasharray={2000} strokeDashoffset={2000 * (1 - draw)} opacity={0.9} filter={i === 0 ? "url(#glow)" : undefined} />
        ))}
        <g opacity={today}>
          <line x1={todayX} y1={y0} x2={todayX} y2={y1} stroke={COLORS.gold} strokeWidth={2} strokeDasharray="10 10" />
          <Label x={todayX + 14} y={y1 + 10} text="hoy" size={34} anchor="start" color={COLORS.gold} />
          <circle cx={todayX} cy={Y(vSmallToday)} r={14} fill={COLORS.goldBright} filter="url(#glow)" />
          <circle cx={todayX} cy={Y(vLargeToday)} r={11} fill={COLORS.ink} />
        </g>
        {note ? <Label x={540} y={1180} text={note} size={36} weight={400} color={COLORS.inkMuted} opacity={today} /> : null}
      </svg>
    </AbsoluteFill>
  );
};

/* ---------------- Behaviour loop ---------------- */
export const BehaviorLoop: React.FC<z.infer<typeof BehaviorLoopS> & D> = ({ steps, breakAt, center, durationInFrames }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const cx = 500, cy = 680, R = 260;
  const n = steps.length;
  const ang = (i: number) => -Math.PI / 2 + (i / n) * Math.PI * 2;
  const appear = prog(frame, 0, 20);
  const lap = Math.max(fps * 2.2, (durationInFrames - (breakAt >= 0 ? fps * 1.6 : 0)) / 2);
  const cut = breakAt >= 0 ? prog(frame, durationInFrames - fps * 1.6, 14) : 0;
  const cometT = cut > 0 ? (breakAt + 0.5) / n : ((frame / lap) % 1);
  const cometA = -Math.PI / 2 + cometT * Math.PI * 2;
  return (
    <AbsoluteFill>
      <svg width={W} height={H}>
        <Glow />
        <circle cx={cx} cy={cy} r={R} fill="none" stroke={COLORS.line} strokeWidth={3} opacity={appear} />
        <circle cx={cx} cy={cy} r={R} fill="none" stroke={COLORS.gold} strokeWidth={5}
          strokeDasharray={`${2 * Math.PI * R * (cut > 0 ? (breakAt + 0.5) / n : cometT)} 99999`}
          transform={`rotate(-90 ${cx} ${cy})`} opacity={0.75} />
        {steps.map((s, i) => {
          const a = ang(i);
          const x = cx + Math.cos(a) * R, y = cy + Math.sin(a) * R;
          const passed = (((cometT * n - i) % n) + n) % n < 1.2;
          const lit = prog(frame, 8 + i * 6, 12);
          const below = Math.sin(a) > -0.5; // side and bottom nodes: label under the node
          const lx = x;
          const ly = below ? y + 78 : y - 50;
          const anchor = "middle" as const;
          return (
            <g key={i} opacity={lit}>
              <circle cx={x} cy={y} r={passed ? 30 : 22} fill={passed ? COLORS.goldBright : COLORS.bgRaised} stroke={COLORS.gold} strokeWidth={3} filter={passed ? "url(#glow)" : undefined} />
              <Label x={lx} y={ly} text={s} size={38} anchor={anchor} color={passed ? COLORS.goldBright : COLORS.ink} />
            </g>
          );
        })}
        <circle cx={cx + Math.cos(cometA) * R} cy={cy + Math.sin(cometA) * R} r={16} fill="#FFF4D6" filter="url(#glow)" opacity={appear} />
        {cut > 0 ? (
          <g opacity={cut} transform={`translate(${cx + Math.cos(ang(breakAt) + Math.PI / n) * R} ${cy + Math.sin(ang(breakAt) + Math.PI / n) * R}) scale(${0.6 + 0.4 * cut})`}>
            <circle r={54} fill={COLORS.bg} stroke={COLORS.goldBright} strokeWidth={4} />
            <line x1={-22} y1={-22} x2={22} y2={22} stroke={COLORS.goldBright} strokeWidth={6} strokeLinecap="round" />
            <line x1={22} y1={-22} x2={-22} y2={22} stroke={COLORS.goldBright} strokeWidth={6} strokeLinecap="round" />
          </g>
        ) : null}
        {center ? <Label x={cx} y={cy + 16} text={center} size={46} family={TYPE.display} weight={700} color={COLORS.ink} opacity={prog(frame, 14, 16)} /> : null}
      </svg>
    </AbsoluteFill>
  );
};

/* ---------------- Emotion wave (e.g. negative reinforcement) ---------------- */
export const EmotionWave: React.FC<z.infer<typeof EmotionWaveS> & D> = ({ yLabel, events, title, durationInFrames }) => {
  const frame = useCurrentFrame();
  const x0 = 120, x1 = 970, base = 1000, top = 380;
  // Build an intensity function: spikes raise it, relief drops it.
  const level = (t: number) => {
    let v = 0.25 + 0.03 * Math.sin(t * 30);
    events.forEach((e, i) => {
      const w = 0.07;
      const d = (t - e.at) / w;
      if (e.tone === "spike") v += (0.45 + 0.12 * i) * Math.exp(-d * d);
      if (e.tone === "relief" && t > e.at) v -= 0.22 * (1 - Math.exp(-(t - e.at) / 0.04));
    });
    return Math.max(0.04, Math.min(1, v));
  };
  const draw = prog(frame, 10, Math.max(30, durationInFrames * 0.75), easeStd);
  const N = 160;
  const pts = Array.from({ length: N }, (_, i) => {
    const t = i / (N - 1);
    return { x: lerp(x0, x1, t), y: lerp(base, top, level(t)), t };
  });
  const d = pts.filter((p) => p.t <= draw).map((p, i) => `${i ? "L" : "M"}${p.x} ${p.y}`).join(" ");
  const head = pts[Math.min(N - 1, Math.floor(draw * (N - 1)))];
  return (
    <AbsoluteFill>
      <svg width={W} height={H}>
        <Glow />
        {title ? <Label x={540} y={250} text={title} size={50} family={TYPE.display} weight={700} opacity={prog(frame, 0, 16)} /> : null}
        <line x1={x0} y1={base + 20} x2={x1} y2={base + 20} stroke={COLORS.line} strokeWidth={3} />
        <Label x={x0} y={top - 40} text={yLabel} size={32} anchor="start" weight={400} color={COLORS.inkMuted} opacity={prog(frame, 4, 14)} />
        <path d={d} fill="none" stroke={COLORS.goldBright} strokeWidth={6} strokeLinejoin="round" filter="url(#glow)" />
        <circle cx={head.x} cy={head.y} r={14} fill="#FFF4D6" filter="url(#glow)" />
        {events.map((e, i) => {
          const p = pts[Math.round(e.at * (N - 1))];
          const show = prog(frame, 10 + e.at * Math.max(30, durationInFrames * 0.75), 14);
          const above = e.tone !== "relief";
          return (
            <g key={i} opacity={show}>
              <line x1={p.x} y1={p.y} x2={p.x} y2={above ? p.y - 70 : p.y + 70} stroke={COLORS.gold} strokeWidth={2} strokeDasharray="6 6" />
              <Label x={Math.min(Math.max(p.x, 200), 880)} y={above ? p.y - 88 : p.y + 112} text={e.label} size={34}
                color={e.tone === "spike" ? COLORS.goldBright : COLORS.ink} />
            </g>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};
