import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import fs from "fs";
const tl = JSON.parse(fs.readFileSync("src/timeline.json"));
const frames = process.argv[2] ? process.argv[2].split(",").map(Number) :
  tl.scenes.map((s) => s.from_ + Math.round(s.frames / 2));
const dir = process.argv[3] || "out/tmp/stills";
fs.mkdirSync(dir, { recursive: true });
const serveUrl = await bundle({ entryPoint: "src/index.ts" });
const BX = "/opt/pw-browsers/chromium_headless_shell";
const composition = await selectComposition({ serveUrl, id: "Reel", browserExecutable: BX });
for (const f of frames) {
  const out = `${dir}/f${String(f).padStart(4, "0")}.png`;
  await renderStill({ serveUrl, composition, frame: f, output: out, scale: 1, browserExecutable: BX });
  console.log(out);
}
