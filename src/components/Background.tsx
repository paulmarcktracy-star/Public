import React, { useMemo } from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { COLORS } from "../design/tokens";
import { rng } from "./anim";

/** Cinematic backdrop: deep gradient, slow gold dust, vignette and film grain. */
export const Background: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  const dust = useMemo(() => {
    const r = rng(7);
    return Array.from({ length: 70 }, () => ({
      x: r() * width,
      y: r() * height,
      size: 1 + r() * 3.2,
      speed: 0.15 + r() * 0.5,
      drift: r() * Math.PI * 2,
      alpha: 0.12 + r() * 0.4,
    }));
  }, [width, height]);

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.bg }}>
      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse 80% 55% at 50% 38%, #1a1610 0%, ${COLORS.bg} 70%)`,
        }}
      />
      <svg width={width} height={height} style={{ position: "absolute" }}>
        {dust.map((d, i) => {
          const y = (d.y - frame * d.speed + height * 4) % height;
          const x = d.x + Math.sin(frame / 60 + d.drift) * 14;
          const twinkle = 0.6 + 0.4 * Math.sin(frame / 18 + d.drift * 3);
          return <circle key={i} cx={x} cy={y} r={d.size} fill={COLORS.gold} opacity={d.alpha * twinkle} />;
        })}
      </svg>
      <AbsoluteFill
        style={{
          background: "radial-gradient(ellipse 75% 65% at 50% 45%, transparent 55%, rgba(0,0,0,0.85) 100%)",
        }}
      />
      {/* Film grain: seed changes every 2 frames, deterministic per frame */}
      <svg width={width} height={height} style={{ position: "absolute", opacity: 0.045, mixBlendMode: "screen" }}>
        <filter id="grain">
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={Math.floor(frame / 2) % 50} />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter="url(#grain)" />
      </svg>
    </AbsoluteFill>
  );
};
