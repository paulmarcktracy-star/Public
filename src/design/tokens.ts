// Design system: premium black / white / gold.
// Every scene component reads from here so the brand stays consistent.

export const COLORS = {
  bg: "#000000",
  bgRaised: "#0E0E0F",
  ink: "#F5F2EA", // warm white for text
  inkMuted: "rgba(245, 242, 234, 0.62)",
  inkFaint: "rgba(245, 242, 234, 0.18)",
  gold: "#D4AF62",
  goldBright: "#F3D48A",
  goldDeep: "#8C6A2E",
  goldGlow: "rgba(212, 175, 98, 0.45)",
  line: "rgba(245, 242, 234, 0.14)",
  danger: "#E5534B", // red: cost, loss, wrong choice (use sparingly)
  red: "#E5534B",
  green: "#5FD38D", // green: gain, right choice, improvement (use sparingly)
};

export const VIDEO = {
  width: 1080,
  height: 1920,
  fps: 30,
  // TikTok / Reels UI covers the bottom ~320px and the right ~140px.
  safe: { top: 170, bottom: 360, left: 72, right: 150 },
  captionY: 1270,
  sceneOverlapFrames: 10,
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
