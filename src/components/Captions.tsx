import React, { useMemo } from "react";
import { AbsoluteFill, Sequence, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { createTikTokStyleCaptions, type Caption, type TikTokPage } from "@remotion/captions";
import { COLORS, SCALE, TYPE, VIDEO } from "../design/tokens";
import { easeEnter } from "./anim";

const SWITCH_EVERY_MS = 1100;

const Page: React.FC<{ page: TikTokPage }> = ({ page }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const nowMs = page.startMs + (frame / fps) * 1000;
  const pop = interpolate(frame, [0, 5], [0.92, 1], { extrapolateRight: "clamp", easing: easeEnter });

  return (
    <AbsoluteFill
      style={{ top: VIDEO.captionY, height: 220, paddingLeft: VIDEO.safe.left, paddingRight: VIDEO.safe.right }}
    >
      <div
        style={{
          width: "100%",
          textAlign: "center",
          fontFamily: TYPE.sans,
          fontWeight: 800,
          fontSize: SCALE.caption,
          lineHeight: 1.15,
          letterSpacing: -0.5,
          whiteSpace: "pre-wrap",
          scale: String(pop),
          textShadow: "0 4px 24px rgba(0,0,0,0.9), 0 0 2px rgba(0,0,0,1)",
        }}
      >
        {page.tokens.map((t, i) => {
          const active = t.fromMs <= nowMs && t.toMs > nowMs;
          return (
            <span key={i} style={{ color: active ? COLORS.goldBright : COLORS.ink, opacity: t.fromMs <= nowMs ? 1 : 0.55 }}>
              {t.text}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

export const Captions: React.FC<{ captions: Caption[] }> = ({ captions }) => {
  const { fps } = useVideoConfig();
  const { pages } = useMemo(
    () => createTikTokStyleCaptions({ captions, combineTokensWithinMilliseconds: SWITCH_EVERY_MS }),
    [captions],
  );
  return (
    <AbsoluteFill>
      {pages.map((page, i) => {
        const next = pages[i + 1];
        const start = Math.round((page.startMs / 1000) * fps);
        const endMs = Math.min(next ? next.startMs : Infinity, page.startMs + page.durationMs + 400);
        const dur = Math.max(1, Math.round(((endMs - page.startMs) / 1000) * fps));
        return (
          <Sequence key={i} from={start} durationInFrames={dur} layout="none">
            <Page page={page} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
