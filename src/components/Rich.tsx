import React from "react";
import { COLORS, TYPE } from "../design/tokens";
import { isEmphasis, prog } from "./anim";

/** Word-staggered line with gold emphasis words. */
export const RichLine: React.FC<{
  text: string;
  emphasis: string[];
  frame: number;
  start: number;
  stagger?: number;
  size: number;
  family?: "display" | "sans";
  weight?: number;
  align?: "center" | "left";
  colorOverride?: string;
}> = ({ text, emphasis, frame, start, stagger = 3, size, family = "display", weight = 700, align = "center", colorOverride }) => {
  const words = text.split(/\s+/).filter(Boolean);
  return (
    <div
      style={{
        fontFamily: family === "display" ? TYPE.display : TYPE.sans,
        fontWeight: weight,
        fontSize: size,
        lineHeight: 1.12,
        color: COLORS.ink,
        textAlign: align,
        letterSpacing: family === "display" ? -1 : -0.5,
      }}
    >
      {words.map((w, i) => {
        const p = prog(frame, start + i * stagger, 14);
        const em = isEmphasis(w, emphasis);
        return (
          <span
            key={i}
            style={{
              display: "inline-block",
              marginRight: size * 0.26,
              opacity: p,
              translate: `0 ${(1 - p) * size * 0.45}px`,
              filter: p < 0.99 ? `blur(${(1 - p) * 8}px)` : undefined,
              color: em ? COLORS.goldBright : colorOverride ?? COLORS.ink,
              fontStyle: em && family === "display" ? "italic" : "normal",
              textShadow: em ? `0 0 ${28 * p}px ${COLORS.goldGlow}` : "0 4px 30px rgba(0,0,0,0.6)",
            }}
          >
            {w}
          </span>
        );
      })}
    </div>
  );
};

export const Kicker: React.FC<{ text: string; frame: number; start?: number }> = ({ text, frame, start = 0 }) => {
  const p = prog(frame, start, 16);
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 18, opacity: p, justifyContent: "center" }}>
      <div style={{ width: 70 * p, height: 2, background: COLORS.gold }} />
      <div
        style={{
          fontFamily: TYPE.sans,
          fontWeight: 600,
          fontSize: TYPE.sizes.small,
          letterSpacing: 6,
          textTransform: "uppercase",
          color: COLORS.gold,
        }}
      >
        {text}
      </div>
      <div style={{ width: 70 * p, height: 2, background: COLORS.gold }} />
    </div>
  );
};
