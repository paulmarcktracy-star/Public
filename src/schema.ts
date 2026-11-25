import { z } from "zod";

/*
 * STORYBOARD = what Claude writes each day (storyboards/<id>.json).
 * TIMELINE   = storyboard + measured voice durations + word captions.
 *              Produced by the pipeline, consumed by the Remotion composition.
 */

const Emphasis = z.string().describe("A word or short phrase from the line to paint gold");

// ---------- Visual scene types (each maps to a reusable component) ----------

export const KineticTitle = z.object({
  type: z.literal("kineticTitle"),
  lines: z.array(z.string()).min(1).max(4),
  emphasis: z.array(Emphasis).default([]),
  kicker: z.string().optional().describe("Small label above the title"),
});

export const Brain3D = z.object({
  type: z.literal("brain3d"),
  highlight: z.array(z.enum(["prefrontal", "reward", "amygdala", "hippocampus", "none"])).default(["none"]),
  labels: z.array(z.object({ region: z.enum(["prefrontal", "reward", "amygdala", "hippocampus"]), text: z.string() })).default([]),
  camera: z.enum(["orbit", "pushIn", "topDown"]).default("orbit"),
  pulses: z.boolean().default(true).describe("Signals travel between highlighted regions"),
  note: z.string().optional(),
});

export const NeuralNetwork = z.object({
  type: z.literal("neuralNetwork"),
  label: z.string().optional(),
  mode: z.enum(["firing", "strengthening", "organizing"]).default("firing"),
  caption: z.string().optional(),
});

export const TwoForces = z.object({
  type: z.literal("twoForces"),
  left: z.object({ label: z.string(), sublabel: z.string().optional(), kind: z.enum(["task", "reward", "future", "now"]) }),
  right: z.object({ label: z.string(), sublabel: z.string().optional(), kind: z.enum(["task", "reward", "future", "now"]) }),
  winner: z.enum(["left", "right", "none"]).default("right"),
});

export const DiscountCurve = z.object({
  type: z.literal("discountCurve"),
  xLabel: z.string(),
  yLabel: z.string(),
  nowLabel: z.string(),
  laterLabel: z.string(),
  note: z.string().optional(),
});

export const BehaviorLoop = z.object({
  type: z.literal("behaviorLoop"),
  steps: z.array(z.string()).min(3).max(5),
  breakAt: z.number().int().min(-1).default(-1).describe("Index of the step where the loop is cut, -1 for none"),
  center: z.string().optional(),
});

export const EmotionWave = z.object({
  type: z.literal("emotionWave"),
  yLabel: z.string(),
  events: z.array(z.object({ at: z.number().min(0).max(1), label: z.string(), tone: z.enum(["spike", "relief", "neutral"]) })).min(1).max(4),
  title: z.string().optional(),
});

export const ActionSteps = z.object({
  type: z.literal("actionSteps"),
  title: z.string(),
  steps: z.array(z.string()).min(1).max(4),
});

export const Closer = z.object({
  type: z.literal("closer"),
  line: z.string(),
  emphasis: z.array(Emphasis).default([]),
  source: z.string().describe("Short citation shown on screen, e.g. 'Sirois y Pychyl, 2013'"),
});


// ---------- Stage: white figure + animated objects + text/numbers (reference style) ----------

export const Accent = z.enum(["white", "gold", "green", "red"]);
export const PropKind = z.enum([
  "phone", "book", "clock", "coins", "bill", "piggy", "door", "mountain", "brain", "chart",
  "donut", "apple", "dumbbell", "cart", "lock", "calendar", "bubble", "question", "hourglass", "lightbulb",
]);
export const PropState = z.enum(["normal", "glow", "dim", "open", "closed", "locked", "spin", "typing", "down", "up"]);
export const Pose = z.enum(["stand", "reach", "point", "phone", "think", "celebrate", "slump", "walk", "lookUp"]);

export const StageProp = z.object({
  kind: PropKind,
  x: z.number(),
  y: z.number(),
  size: z.number().default(170),
  accent: Accent.default("white"),
  state: PropState.default("normal"),
  label: z.string().optional(),
  sublabel: z.string().optional(),
  enter: z.enum(["pop", "draw", "slideLeft", "slideRight", "drop", "fade", "none"]).default("pop"),
  delay: z.number().min(0).default(0).describe("seconds after shot start"),
  to: z
    .object({ x: z.number().optional(), y: z.number().optional(), size: z.number().optional(), accent: Accent.optional(), state: PropState.optional(), at: z.number().min(0).max(1).default(0.35) })
    .optional()
    .describe("animate to these values; 'at' = fraction of the shot when the change starts"),
  mark: z.enum(["check", "cross", "question"]).optional(),
  markAt: z.number().min(0).max(1).default(0.55),
});

export const StageText = z.object({
  content: z.string(),
  x: z.number().default(540),
  y: z.number(),
  size: z.number().default(72),
  accent: Accent.default("white"),
  emphasis: z.array(z.string()).default([]),
  family: z.enum(["display", "sans"]).default("display"),
  delay: z.number().min(0).default(0),
});

export const StageCounter = z.object({
  from: z.number(),
  to: z.number(),
  prefix: z.string().default(""),
  suffix: z.string().default(""),
  x: z.number(),
  y: z.number(),
  size: z.number().default(120),
  accent: Accent.default("gold"),
  delay: z.number().min(0).default(0),
  seconds: z.number().default(0.9),
});

export const Stage = z.object({
  type: z.literal("stage"),
  figure: z
    .object({
      pose: Pose,
      from: Pose.optional().describe("pose at the start of the shot, blends into 'pose'"),
      x: z.number().default(540),
      y: z.number().default(1120).describe("feet baseline"),
      toX: z.number().optional().describe("walks to this x during the shot"),
      facing: z.union([z.literal(1), z.literal(-1)]).default(1),
      scale: z.number().default(1),
      holding: z.enum(["none", "phone", "coins"]).default("none"),
      path: z
        .enum(["auto", "none", "flat", "rise", "fall", "fork", "fade"])
        .default("auto")
        .describe("signature dashed path under the feet; auto = flat, longer when walking"),
      pathFrom: z.number().optional().describe("x where the dashed path starts"),
      pathTo: z.number().optional().describe("x where the dashed path ends"),
    })
    .optional(),
  props: z.array(StageProp).default([]),
  texts: z.array(StageText).default([]),
  counters: z.array(StageCounter).default([]),
  spotlight: z.object({ x: z.number(), snap: z.boolean().default(false), accent: Accent.default("white") }).optional(),
  camera: z
    .object({ fromZoom: z.number().default(1), toZoom: z.number().default(1.07), x: z.number().default(540), y: z.number().default(760), panX: z.number().default(0) })
    .default({ fromZoom: 1, toZoom: 1.07, x: 540, y: 760, panX: 0 }),
  note: z.string().optional().describe("small on-screen footnote (e.g. a scientific caveat)"),
});

export const Visual = z.discriminatedUnion("type", [
  KineticTitle, Brain3D, NeuralNetwork, TwoForces, DiscountCurve, BehaviorLoop, EmotionWave, ActionSteps, Closer, Stage,
]);
export type Visual = z.infer<typeof Visual>;

export const Sfx = z.enum(["whoosh", "riser", "impact", "tick", "shimmer", "pulse", "pop", "cash", "none"]);

export const Shot = z.object({
  text: z.string().min(1).describe("exact consecutive fragment of the scene narration"),
  visual: Visual,
  sfx: Sfx.default("whoosh"),
  minSeconds: z.number().min(0.5).max(20).optional(),
});
export type Shot = z.infer<typeof Shot>;

export const StoryScene = z.object({
  id: z.string(),
  beat: z.enum(["hook", "question", "mechanism", "demonstration", "retention", "reveal", "action", "closer", "cta"]),
  narration: z.string().min(1).describe("spoken in one take so the voice keeps natural intonation"),
  shots: z.array(Shot).min(1).max(6),
  camera: z.string().optional().describe("Human-readable camera note"),
});
export type StoryScene = z.infer<typeof StoryScene>;

export const Source = z.object({
  citation: z.string(),
  url: z.string().url().optional(),
  doi: z.string().optional(),
  supports: z.string().describe("Which claim in the script this source backs"),
});

export const Storyboard = z.object({
  id: z.string().regex(/^[a-z0-9-]+$/),
  title: z.string(),
  pillar: z.number().int().min(1).max(5),
  format: z.enum(["classicExperiment", "mythVsEvidence", "slowMotionBrain", "behaviorLoop", "secondPerson", "openQuestion"]),
  evidenceLevel: z.enum(["solid", "moderate", "mixed"]),
  sources: z.array(Source).min(1),
  scenes: z.array(StoryScene).min(4).max(14),
  music: z.enum(["reflexion", "esperanza", "intimo", "none"]).default("intimo"),
  social: z.object({
    caption: z.string(),
    hashtags: z.array(z.string()).max(8),
    aiLabel: z.literal(true).default(true),
  }),
});
export type Storyboard = z.infer<typeof Storyboard>;

// ---------- Timeline (render props) ----------

export const CaptionWord = z.object({
  text: z.string(),
  startMs: z.number(),
  endMs: z.number(),
  timestampMs: z.number().nullable(),
  confidence: z.number().nullable(),
  pageBreakAfter: z.boolean().optional(),
});

export const TimelineShot = Shot.extend({
  id: z.string(),
  beat: StoryScene.shape.beat,
  startFrame: z.number().int(),
  durationInFrames: z.number().int(),
});

export const Timeline = z.object({
  id: z.string(),
  title: z.string(),
  fps: z.number(),
  durationInFrames: z.number().int(),
  voiceSrc: z.string().nullable(),
  musicSrc: z.string().nullable(),
  sfxDir: z.string().nullable(),
  shots: z.array(TimelineShot),
  captions: z.array(CaptionWord),
  sourceLine: z.string(),
});
export type Timeline = z.infer<typeof Timeline>;
export type TimelineShot = z.infer<typeof TimelineShot>;
