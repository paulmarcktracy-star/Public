// Design system: STRICT BLACK & WHITE (owner rule, 2026-11-25).
// Legacy names (gold, green, red) are kept so scenes compile, but they now resolve
// to white / grey. The only colour left is `reward`, reserved for a rare narrative
// moment (victory, reward, key emotion) via accent "reward".

export const COLORS = {
  bg: "#000000",
  bgGrid: "#050505", // static dot-grid backdrop
  bgRaised: "#0B0B0B",
  ink: "#FFFFFF",
  inkMuted: "rgba(255, 255, 255, 0.62)",
  inkFaint: "rgba(255, 255, 255, 0.18)",
  gold: "#FFFFFF",
  goldBright: "#FFFFFF",
  goldDeep: "#8C8C8C",
  goldGlow: "rgba(255, 255, 255, 0.35)",
  line: "rgba(255, 255, 255, 0.14)",
  danger: "#6E6E6E", // loss / wrong choice = dimmed grey, not red
  red: "#6E6E6E",
  green: "#FFFFFF",
  reward: "#E8C872", // RARE: only with a real narrative function (max 2 shots per video)
};

export const VIDEO = {
  width: 1080,
  height: 1920,
  fps: 30,
  // TikTok / Reels UI covers the bottom ~320px and the right ~140px.
  safe: { top: 170, bottom: 360, left: 72, right: 150 },
  captionY: 1270,
  sceneOverlapFrames: 10,
  hookLeadFrames: 12, // first shot starts pre-rolled so frame 0 is already legible (owner hook rule)
};

export const TYPE = {
  display: "Playfair Display",
  sans: "Inter",
  sizes: { hero: 84, title: 66, heading: 52, body: 38, label: 30, small: 24 },
};

// MINIMALISM: nothing should fill the screen. Visuals are framed with generous
// negative space for 9:16 feeds (TikTok / Reels / Shorts UI overlays the edges).
export const SCALE = {
  visual: 0.84, // every scene is drawn at 84 % around the centre of the content zone
  text: 0.74, // on-stage titles
  counter: 0.78,
  caption: 48, // px
  label: 32, // px, object labels
};

// Motion curves. Keep all easing here so motion feels like one studio.
export const MOTION = {
  enter: [0.16, 1, 0.3, 1] as const, // fast out, soft settle
  exit: [0.7, 0, 0.84, 0] as const,
  standard: [0.45, 0, 0.55, 1] as const,
};
