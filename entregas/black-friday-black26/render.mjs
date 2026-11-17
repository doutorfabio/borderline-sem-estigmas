// node render.mjs frames <outdir> <startFrame> <endFrame>   (FPS env, default 60; 3 subframes each)
// node render.mjs times <outdir> t1,t2,...                  (stills)
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const [mode, out, a, b] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
const errs = [];
page.on('pageerror', e => errs.push(e.message));
page.on('console', m => m.type() === 'error' && errs.push(m.text()));
await page.goto('file://' + path.resolve('index.html'));
await page.waitForFunction(() => window.__ready === true, null, { timeout: 20000 });
const shot = async (t, file, type) => {
  await page.evaluate(t => window.seek(t), t);
  await page.screenshot({ path: file, type, ...(type === 'jpeg' ? { quality: 94 } : {}) });
};
if (mode === 'times') {
  for (const t of a.split(',').map(Number)) await shot(t, `${out}/t_${t.toFixed(3)}.png`, 'png');
} else {
  for (let f = +a; f < +b; f++) for (let s = 0; s < 3; s++) {
    const FPS = +(process.env.FPS || 60); const t = Math.max(0, f / FPS + (s - 1) / (3 * FPS));
    await shot(t, `${out}/s_${String(f * 3 + s).padStart(5, '0')}.jpg`, 'jpeg');
  }
}
console.log(errs.length ? 'ERRORS:\n' + errs.join('\n') : 'no errors');
await browser.close();
