import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { easeEnter, easeExit } from "./anim";
import { VIDEO } from "../design/tokens";

/** Wraps every scene: soft focus-pull in, fade + drift out. */
export const SceneFrame: React.FC<{ children: React.ReactNode; durationInFrames: number; first?: boolean }> = ({
  children,
  durationInFrames,
  first = false,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const inDur = first ? 1 : Math.round(0.45 * fps);
  const outDur = VIDEO.sceneOverlapFrames;
  const opts = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

  const opacity =
    (first ? 1 : interpolate(frame, [0, inDur], [0, 1], { ...opts, easing: easeEnter })) *
    interpolate(frame, [durationInFrames - outDur, durationInFrames], [1, 0], { ...opts, easing: easeExit });
  const blur =
    (first ? 0 : interpolate(frame, [0, inDur], [14, 0], { ...opts, easing: easeEnter })) +
    interpolate(frame, [durationInFrames - outDur, durationInFrames], [0, 10], opts);

  return (
    <AbsoluteFill
      style={{
        opacity,
        filter: blur > 0.05 ? `blur(${blur}px)` : undefined,
        scale: interpolate(frame, [0, inDur, durationInFrames], [first ? 1 : 1.05, 1, 0.985], { ...opts, easing: easeEnter }),
      }}
    >
      {children}
    </AbsoluteFill>
  );
};
