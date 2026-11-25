/**
 * Editorial + schema gate (enforces the production rules in CLAUDE.md).
 * Runs before any audio is generated.
 * Usage: tsx pipeline/validate.ts storyboards/<id>.json [...]
 */
import { readFileSync } from "node:fs";
import { Storyboard } from "../src/schema";

const WPS = 2.55; // narration pace (words per second)
const GAP = 0.3; // pause between scenes
const norm = (s: string) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9ñ ]/g, " ").replace(/\s+/g, " ").trim();
let failed = false;

for (const file of process.argv.slice(2)) {
  const problems: string[] = [];
  const warnings: string[] = [];
  let sb;
  try {
    sb = Storyboard.parse(JSON.parse(readFileSync(file, "utf8")));
  } catch (e) {
    console.error(`✗ ${file}\n${e}`);
    failed = true;
    continue;
  }
  const words = sb.scenes.reduce((n, s) => n + s.narration.split(/\s+/).length, 0);
  const est = words / WPS + (sb.scenes.length - 1) * GAP + 1.6;
  const shots = sb.scenes.flatMap((s) => s.shots);

  // Structure: hook -> retention/development -> CTA (rules 5, 6, 8)
  if (sb.scenes[0].beat !== "hook") problems.push("first scene must be the hook");
  if (sb.scenes.at(-1)!.beat !== "cta") problems.push("last scene must be the CTA (rule 8)");
  if (!sb.scenes.some((s) => s.beat === "action")) problems.push("needs a practical takeaway (action beat)");
  if (!sb.scenes.some((s) => s.beat === "retention" || s.beat === "question")) warnings.push("no explicit retention/question beat");
  const hookWords = sb.scenes[0].narration.split(/\s+/).length;
  if (hookWords > 22) warnings.push(`hook is long (${hookWords} words)`);
  if (!/[?¿]/.test(sb.scenes.at(-1)!.narration)) warnings.push("CTA has no question to answer in comments");

  // Duration target
  if (est < 61) warnings.push(`estimated ${est.toFixed(0)}s < 61s target`);
  if (est > 75) warnings.push(`estimated ${est.toFixed(0)}s > 75s target`);
  if (est > 90) problems.push(`too long: ~${est.toFixed(0)}s`);

  // Shots: every phrase has a visual, no long static shots (rules 1, 2)
  for (const sc of sb.scenes) {
    const joined = norm(sc.shots.map((s) => s.text).join(" "));
    if (joined !== norm(sc.narration)) problems.push(`scene ${sc.id}: shot texts do not add up to the narration`);
    sc.shots.forEach((sh, i) => {
      const secs = sh.text.split(/\s+/).length / WPS;
      if (secs > 6.5) problems.push(`scene ${sc.id} shot ${i + 1}: ~${secs.toFixed(1)}s of narration on one visual (max ~6s)`);
      else if (secs > 5) warnings.push(`scene ${sc.id} shot ${i + 1}: ~${secs.toFixed(1)}s, make sure the visual keeps changing`);
    });
  }
  let run = 1;
  for (let i = 1; i < shots.length; i++) {
    run = shots[i].visual.type === shots[i - 1].visual.type && shots[i].visual.type !== "stage" ? run + 1 : 1;
    if (run > 2) problems.push(`three ${shots[i].visual.type} shots in a row`);
  }
  const avg = est / shots.length;
  if (avg > 4.5) warnings.push(`average shot length ${avg.toFixed(1)}s: consider more cuts`);

  // Evidence (rule 9)
  if (!sb.sources.some((s) => s.doi || s.url)) problems.push("at least one source needs a DOI or URL");
  if (/\d+\s?%/.test(sb.scenes.map((s) => s.narration).join(" "))) warnings.push("percentage in narration: confirm it is in a cited source");
  if (sb.social.hashtags.length > 6) warnings.push("more than 6 hashtags");

  const mark = problems.length ? "✗" : "✓";
  console.log(`${mark} ${sb.id}: ${words} words, ~${est.toFixed(0)}s, ${sb.scenes.length} scenes, ${shots.length} shots (avg ${avg.toFixed(1)}s)`);
  warnings.forEach((w) => console.log(`   ! ${w}`));
  problems.forEach((p) => console.log(`   ✗ ${p}`));
  if (problems.length) failed = true;
}
process.exit(failed ? 1 : 0);
