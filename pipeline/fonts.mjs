// Copies the brand fonts from npm packages into public/fonts (run on install).
import { copyFileSync, mkdirSync } from "node:fs";
const files = [
  ["@fontsource/inter/files/inter-latin-400-normal.woff2"],
  ["@fontsource/inter/files/inter-latin-600-normal.woff2"],
  ["@fontsource/inter/files/inter-latin-800-normal.woff2"],
  ["@fontsource/playfair-display/files/playfair-display-latin-700-normal.woff2"],
  ["@fontsource/playfair-display/files/playfair-display-latin-600-italic.woff2"],
];
mkdirSync("public/fonts", { recursive: true });
for (const [f] of files) copyFileSync(`node_modules/${f}`, `public/fonts/${f.split("/").pop()}`);
console.log(`fonts ready (${files.length})`);
