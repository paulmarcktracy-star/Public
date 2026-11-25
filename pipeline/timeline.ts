/**
 * storyboard + measured voice timing + word captions  ->  render props
 *
 * Each scene is voiced in one take (natural intonation). Its shots are then
 * placed on the timeline at the exact moment their first word is spoken,
 * using the word-level caption timestamps.
 *
 * Usage: tsx pipeline/timeline.ts <storyboard.json> <build_dir_relative_to_public>
 */
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { Storyboard, Timeline } from "../src/schema";
import { VIDEO } from "../src/design/tokens";

const [sbPath, buildRel] = process.argv.slice(2);
if (!sbPath || !buildRel) throw new Error("usage: timeline.ts <storyboard.json> <public-relative build dir>");

const sb = Storyboard.parse(JSON.parse(readFileSync(sbPath, "utf8")));
const buildDir = path.join("public", buildRel);
const voice = JSON.parse(readFileSync(path.join(buildDir, "scenes.json"), "utf8")) as {
  engine: string;
  scenes: { id: string; start: number; duration: number }[];
};
const captions = JSON.parse(readFileSync(path.join(buildDir, "captions.json"), "utf8")) as { startMs: number; endMs: number }[];

const fps = VIDEO.fps;
const LEAD = 0.18; // a shot appears just before its first word
const TAIL = 1.6; // hold after the last word

// Flatten shots with the global index of their first word.
type Flat = { sceneId: string; beat: string; shot: (typeof sb.scenes)[number]["shots"][number]; firstWord: number; idx: number };
const flat: Flat[] = [];
let wordCursor = 0;
for (const sc of sb.scenes) {
  sc.shots.forEach((shot, idx) => {
    flat.push({ sceneId: sc.id, beat: sc.beat, shot, firstWord: wordCursor, idx });
    wordCursor += shot.text.split(/\s+/).filter(Boolean).length;
  });
}
if (wordCursor !== captions.length) throw new Error(`caption count ${captions.length} != script words ${wordCursor}`);

const lastVoiceEnd = voice.scenes.at(-1)!.start + voice.scenes.at(-1)!.duration;
const startSec = flat.map((f, i) => (i === 0 ? 0 : Math.max(0, captions[f.firstWord].startMs / 1000 - LEAD)));

const shots = flat.map((f, i) => {
  let endSec = i + 1 < flat.length ? startSec[i + 1] : lastVoiceEnd + TAIL;
  const min = f.shot.minSeconds;
  if (i === flat.length - 1 && min && endSec - startSec[i] < min) endSec = startSec[i] + min;
  return {
    ...f.shot,
    id: `${f.sceneId}-${f.idx + 1}`,
    beat: f.beat,
    startFrame: Math.round(startSec[i] * fps),
    durationInFrames: Math.max(1, Math.round((endSec - startSec[i]) * fps)),
  };
});
// make frames contiguous (no rounding gaps)
for (let i = 0; i + 1 < shots.length; i++) shots[i].durationInFrames = shots[i + 1].startFrame - shots[i].startFrame;

const last = shots[shots.length - 1];
const timeline: Timeline = Timeline.parse({
  id: sb.id,
  title: sb.title,
  fps,
  durationInFrames: last.startFrame + last.durationInFrames,
  voiceSrc: voice.engine === "estimate" ? null : `${buildRel}/voice.wav`,
  musicSrc: sb.music === "none" ? null : `audio/music/${sb.music}.wav`,
  sfxDir: "audio/sfx",
  shots,
  captions,
  sourceLine: sb.sources.map((s) => s.citation).join(" | "),
});

writeFileSync(path.join(buildDir, "props.json"), JSON.stringify({ timeline }, null, 1));
const lens = shots.map((s) => s.durationInFrames / fps);
console.log(
  `timeline: ${shots.length} shots, ${(timeline.durationInFrames / fps).toFixed(1)}s, shot length ${Math.min(...lens).toFixed(1)}–${Math.max(...lens).toFixed(1)}s`,
);
