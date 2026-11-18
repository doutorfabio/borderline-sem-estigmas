// Headless renderer. usage:
//   node render.mjs <reel.html> stills <outDir> 1.9,6.5,...      full-size PNG stills (4 sub-frames blended)
//   node render.mjs <reel.html> safe                              text bounding box over every sub-frame vs the safe area
//   node render.mjs <reel.html> frames <outDir> [from] [to]       JPEG frames (resumable)
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');   // pre-installed globally
import { mkdirSync, writeFileSync, existsSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';
const [html, mode, a1, a2, a3] = process.argv.slice(2);
const browser = await chromium.launch({ args: ['--no-sandbox', '--allow-file-access-from-files', '--disable-background-timer-throttling'] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
page.on('console', m => { if (['error', 'warning'].includes(m.type())) console.log('[page]', m.text()); });
page.on('pageerror', e => console.log('[page error]', e.message));
await page.goto(pathToFileURL(resolve(html)).href + '?render', { waitUntil: 'load' });
await page.waitForFunction('window.ready === true', null, { timeout: 120000 });
const b64 = u => Buffer.from(u.split(',')[1], 'base64');
if (mode === 'stills') {
  mkdirSync(a1, { recursive: true });
  for (const t of a2.split(',').map(Number)) {
    const u = await page.evaluate(i => window.framePNG(i), Math.round(t * 30));
    writeFileSync(`${a1}/still_${t.toFixed(2).padStart(5, '0')}.png`, b64(u));
  }
  console.log(await page.evaluate(() => JSON.stringify({ T1: T1.base, T2: T2.base, T3: T3.base, T4: T4.base, T5: T5.base, T6a: T6a.base, T6b: T6b.base, T8a: T8a.base, T8b: T8b.base,
    bottoms: [T1.bottom, T2.bottom, T3.bottom, T4.bottom, T5.bottom, T6a.bottom, T6b.bottom, T8a.bottom, T8b.bottom].map(Math.round), lock: LOCK.by, sup2: SUP2.by, sup4: SUP4.by })));
} else if (mode === 'safe') {
  const r = await page.evaluate(() => {
    const S = { x0: 0.07 * 1080, x1: 0.88 * 1080, y0: 0.14 * 1920, y1: 0.78 * 1920 };
    let g = [1e9, 1e9, -1, -1], bad = [], n = 0, at = [0, 0, 0, 0];
    for (let i = 0; i < 1050; i++) for (let k = 0; k < 4; k++) {
      const t = (i + k * 0.125) / 30, b = window.textBBox(t); n++;
      if (!b) continue;
      if (b[0] < g[0]) { g[0] = b[0]; at[0] = t; } if (b[1] < g[1]) { g[1] = b[1]; at[1] = t; }
      if (b[2] > g[2]) { g[2] = b[2]; at[2] = t; } if (b[3] > g[3]) { g[3] = b[3]; at[3] = t; }
      if (b[0] < S.x0 || b[2] > S.x1 || b[1] < S.y0 || b[3] > S.y1) bad.push([+t.toFixed(3), b]);
    }
    return { checked: n, safe: S, extremes: g, at: at.map(v => +v.toFixed(3)), violations: bad.length, first: bad.slice(0, 12) };
  });
  console.log(JSON.stringify(r, null, 1));
} else if (mode === 'frames') {
  mkdirSync(a1, { recursive: true });
  const from = +(a2 ?? 0), to = +(a3 ?? 1050);
  const t0 = Date.now();
  for (let i = from; i < to; i++) {
    const f = `${a1}/f${String(i).padStart(5, '0')}.jpg`;
    if (existsSync(f)) continue;
    const u = await page.evaluate(i => window.frameJPEG(i, 0.98), i);
    writeFileSync(f, b64(u));
    if ((i - from) % 60 === 0) console.log(`frame ${i} (${((Date.now() - t0) / 1000).toFixed(0)}s)`);
  }
}
await browser.close();
