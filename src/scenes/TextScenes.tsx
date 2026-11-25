import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import type { z } from "zod";
import type { ActionSteps as ActionStepsS, Closer as CloserS, KineticTitle as KineticTitleS } from "../schema";
import { COLORS, TYPE, VIDEO } from "../design/tokens";
import { Kicker, RichLine } from "../components/Rich";
import { prog } from "../components/anim";

type D = { durationInFrames: number };

const Stage: React.FC<{ children: React.ReactNode; top?: number }> = ({ children, top = VIDEO.safe.top }) => (
  <AbsoluteFill
    style={{
      paddingTop: top,
      paddingLeft: VIDEO.safe.left,
      paddingRight: VIDEO.safe.right - 40,
      height: VIDEO.captionY - 40,
      justifyContent: "center",
      alignItems: "center",
      gap: 40,
    }}
  >
    {children}
  </AbsoluteFill>
);

export const KineticTitle: React.FC<z.infer<typeof KineticTitleS> & D> = ({ lines, emphasis, kicker }) => {
  const frame = useCurrentFrame();
  let offset = 0; // the hook must be readable from frame 0
  const size = lines.join(" ").length > 70 ? TYPE.sizes.title : TYPE.sizes.hero;
  return (
    <Stage>
      {kicker ? <Kicker text={kicker} frame={frame} /> : null}
      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {lines.map((l, i) => {
          const start = offset;
          offset += l.split(/\s+/).length * 2 + 3;
          return <RichLine key={i} text={l} emphasis={emphasis} frame={frame} start={start - 6} stagger={2} size={size} />;
        })}
      </div>
    </Stage>
  );
};

export const ActionSteps: React.FC<z.infer<typeof ActionStepsS> & D> = ({ title, steps, durationInFrames }) => {
  const frame = useCurrentFrame();
  const gap = Math.min(28, Math.max(12, (durationInFrames - 30) / (steps.length + 1)));
  return (
    <Stage>
      <Kicker text={title} frame={frame} />
      <div style={{ display: "flex", flexDirection: "column", gap: 26, width: "100%" }}>
        {steps.map((s, i) => {
          const p = prog(frame, 12 + i * gap, 16);
          const check = prog(frame, 12 + i * gap + 12, 12);
          return (
            <div
              key={i}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 30,
                padding: "30px 34px",
                borderRadius: 22,
                background: "rgba(20,18,14,0.78)",
                border: `1.5px solid ${check > 0.5 ? COLORS.gold : COLORS.line}`,
                opacity: p,
                translate: `${(1 - p) * 80}px 0`,
                boxShadow: check > 0.5 ? `0 0 40px ${COLORS.goldGlow}` : "none",
              }}
            >
              <div
                style={{
                  fontFamily: TYPE.display,
                  fontWeight: 700,
                  fontSize: 54,
                  color: COLORS.goldBright,
                  width: 64,
                  textAlign: "center",
                }}
              >
                {i + 1}
              </div>
              <div style={{ fontFamily: TYPE.sans, fontWeight: 600, fontSize: 34, color: COLORS.ink, lineHeight: 1.25, flex: 1 }}>
                {s}
              </div>
            </div>
          );
        })}
      </div>
    </Stage>
  );
};

export const Closer: React.FC<z.infer<typeof CloserS> & D> = ({ line, emphasis, source }) => {
  const frame = useCurrentFrame();
  const words = line.split(/\s+/).length;
  const rule = prog(frame, words * 3 + 6, 22);
  const src = prog(frame, words * 3 + 16, 18);
  const mark = prog(frame, words * 3 + 26, 20);
  return (
    <Stage>
      <RichLine text={line} emphasis={emphasis} frame={frame} start={4} size={TYPE.sizes.title} />
      <div style={{ width: 360 * rule, height: 2, background: `linear-gradient(90deg, transparent, ${COLORS.gold}, transparent)` }} />
      <div
        style={{
          opacity: src,
          fontFamily: TYPE.sans,
          fontSize: TYPE.sizes.small,
          letterSpacing: 2,
          color: COLORS.inkMuted,
          textAlign: "center",
        }}
      >
        Fuente: {source}
      </div>
      <svg width={120} height={120} style={{ opacity: mark, marginTop: 20 }}>
        {[0, 1, 2, 3, 4, 5].map((k) => {
          const a = (k / 6) * Math.PI * 2 + frame / 90;
          return (
            <line key={k} x1={60} y1={60} x2={60 + Math.cos(a) * 44 * mark} y2={60 + Math.sin(a) * 44 * mark} stroke={COLORS.gold} strokeWidth={2} />
          );
        })}
        <circle cx={60} cy={60} r={14} fill={COLORS.goldBright} />
      </svg>
    </Stage>
  );
};
