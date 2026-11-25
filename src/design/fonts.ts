import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";
import { TYPE } from "./tokens";

let loaded: Promise<unknown> | null = null;

// Fonts are bundled locally (no network needed at render time).
export const ensureFonts = () => {
  if (!loaded) {
    loaded = Promise.all([
      loadFont({ family: TYPE.sans, url: staticFile("fonts/inter-latin-400-normal.woff2"), weight: "400" }),
      loadFont({ family: TYPE.sans, url: staticFile("fonts/inter-latin-600-normal.woff2"), weight: "600" }),
      loadFont({ family: TYPE.sans, url: staticFile("fonts/inter-latin-800-normal.woff2"), weight: "800" }),
      loadFont({ family: TYPE.display, url: staticFile("fonts/playfair-display-latin-700-normal.woff2"), weight: "700" }),
      loadFont({ family: TYPE.display, url: staticFile("fonts/playfair-display-latin-600-italic.woff2"), weight: "600", style: "italic" }),
    ]);
  }
  return loaded;
};

ensureFonts();
