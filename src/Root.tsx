import React from "react";
import { Composition, type CalculateMetadataFunction } from "remotion";
import { Video } from "./Video";
import { Timeline } from "./schema";
import { VIDEO } from "./design/tokens";
import demo from "./demo-timeline.json";

type Props = { timeline: Timeline };

const calculateMetadata: CalculateMetadataFunction<Props> = ({ props }) => {
  const timeline = Timeline.parse(props.timeline);
  return {
    durationInFrames: timeline.durationInFrames,
    fps: timeline.fps,
    props: { timeline },
    defaultOutName: timeline.id,
  };
};

export const RemotionRoot: React.FC = () => (
  <Composition
    id="PsychVideo"
    component={Video}
    width={VIDEO.width}
    height={VIDEO.height}
    fps={VIDEO.fps}
    durationInFrames={300}
    defaultProps={{ timeline: demo as unknown as Timeline }}
    calculateMetadata={calculateMetadata}
  />
);
