import React from "react";
import { AbsoluteFill } from "remotion";
import { COLORS } from "../design/tokens";

/**
 * Static dot grid (owner rule): near-black backdrop with tiny evenly spaced grey dots,
 * drawn with a CSS radial-gradient. It never moves, pulses or fades, and it is rendered
 * once under every scene, so camera moves and scene transitions never touch it.
 */
export const GRID = { spacing: 36, dot: 1.3, opacity: 0.2 };

export const Background: React.FC = () => (
  <AbsoluteFill
    style={{
      backgroundColor: COLORS.bgGrid,
      backgroundImage: `radial-gradient(circle, rgba(255,255,255,${GRID.opacity}) ${GRID.dot}px, transparent ${GRID.dot + 0.4}px)`,
      backgroundSize: `${GRID.spacing}px ${GRID.spacing}px`,
      backgroundPosition: `${GRID.spacing / 2}px ${GRID.spacing / 2}px`,
    }}
  />
);
