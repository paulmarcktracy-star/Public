import React from "react";
import { AbsoluteFill, Sequence, interpolate, staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import "./design/fonts";
import type { Timeline, TimelineShot } from "./schema";
import { Background } from "./components/Background";
import { SceneFrame } from "./components/SceneFrame";
import { Captions } from "./components/Captions";
import { Brain3D } from "./scenes/Brain3D";
import { ActionSteps, Closer, KineticTitle } from "./scenes/TextScenes";
import { BehaviorLoop, DiscountCurve, EmotionWave, NeuralNetwork, TwoForces } from "./scenes/DiagramScenes";
import { Stage } from "./scenes/Stage";
import { SCALE, VIDEO } from "./design/tokens";

const renderVisual = (s: TimelineShot) => {
  const d = { durationInFrames: s.durationInFrames };
  const v = s.visual;
  switch (v.type) {
    case "kineticTitle": return <KineticTitle {...v} {...d} />;
    case "brain3d": return <Brain3D {...v} {...d} />;
    case "neuralNetwork": return <NeuralNetwork {...v} {...d} />;
    case "twoForces": return <TwoForces {...v} {...d} />;
    case "discountCurve": return <DiscountCurve {...v} {...d} />;
    case "behaviorLoop": return <BehaviorLoop {...v} {...d} />;
    case "emotionWave": return <EmotionWave {...v} {...d} />;
    case "actionSteps": return <ActionSteps {...v} {...d} />;
    case "closer": return <Closer {...v} {...d} />;
    case "stage": return <Stage {...v} {...d} />;
  }
};

export const Video: React.FC<{ timeline: Timeline }> = ({ timeline }) => {
  const { fps, durationInFrames } = useVideoConfig();
  const overlap = VIDEO.sceneOverlapFrames;
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <Background />
      {timeline.shots.map((s, i) => {
        const isLast = i === timeline.shots.length - 1;
        const lead = i === 0 ? VIDEO.hookLeadFrames : 0; // hook: already on screen at frame 0
        const dur = s.durationInFrames + (isLast ? 0 : overlap) + lead;
        return (
          <Sequence key={s.id} name={`${s.beat}:${s.visual.type}`} from={s.startFrame - lead} durationInFrames={dur}>
            <SceneFrame durationInFrames={dur} first={i === 0}>
              {s.visual.type === "stage" ? (
                renderVisual({ ...s, durationInFrames: dur })
              ) : (
                // minimal framing for diagram / 3D / text scenes
                <AbsoluteFill style={{ scale: String(SCALE.visual), transformOrigin: "540px 760px" }}>{renderVisual({ ...s, durationInFrames: dur })}</AbsoluteFill>
              )}
            </SceneFrame>
          </Sequence>
        );
      })}
      <Captions captions={timeline.captions} />

      {timeline.voiceSrc ? <Audio src={staticFile(timeline.voiceSrc)} /> : null}
      {timeline.musicSrc ? (
        <Audio
          src={staticFile(timeline.musicSrc)}
          loop
          volume={(f) =>
            (timeline.musicGain ?? 0.24) *
            interpolate(f, [0, fps, durationInFrames - fps * 1.5, durationInFrames], [0, 1, 1, 0], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            })
          }
        />
      ) : null}
      {timeline.fxSrc ? <Audio src={staticFile(timeline.fxSrc)} /> : null}
      {timeline.sfxDir && !timeline.fxSrc
        ? timeline.shots.map((s, i) =>
            s.sfx === "none" ? null : (
              <Sequence key={`sfx-${s.id}`} from={Math.max(0, s.startFrame - (i ? 4 : 0))} durationInFrames={fps * 3}>
                <Audio src={staticFile(`${timeline.sfxDir}/${s.sfx}.wav`)} volume={0.42} />
              </Sequence>
            ),
          )
        : null}
    </AbsoluteFill>
  );
};
