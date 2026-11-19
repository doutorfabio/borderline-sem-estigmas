// Uso: node render.mjs probe 0,1.5,3.3   (quadros de conferência em probe/)
//      node render.mjs safe               (mede a área segura do texto)
//      node render.mjs full               (600 quadros em frames/)
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)(process.env.PW || 'playwright');
import { mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const dir = path.dirname(fileURLToPath(import.meta.url));
const mode = process.argv[2] || 'probe';
const FPS = 30;
const cuesFile = process.env.CUES; // arquivo .js com window.CUES=...
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
page.on('console', m => console.log('[page]', m.text()));
page.on('pageerror', e => console.log('[erro]', e.message));
if (cuesFile) await page.addInitScript({ path: cuesFile });
await page.goto('file://' + path.join(dir, 'index.html'));
await page.waitForFunction('window.ready===true');
const DUR = await page.evaluate(() => window.DUR);
const NF = Math.round(DUR * FPS);
console.log('duração', DUR, 'quadros', NF);

if (mode === 'probe') {
  mkdirSync(path.join(dir, 'probe'), { recursive: true });
  for (const s of (process.argv[3] || '0').split(',')) {
    const t = parseFloat(s);
    await page.evaluate(t => window.seek(t), t);
    await page.screenshot({ path: path.join(dir, 'probe', 't' + t.toFixed(2).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 80 });
  }
} else if (mode === 'safe') {
  // área segura: 5% à esquerda, 12% à direita, 20% embaixo. Mede a tinta visível de cada linha.
  const L = 54, R = 1080 - 130, B = 1920 - 384;
  let worst = { l: 9999, r: 0, b: 0 }, fails = [];
  for (let f = 0; f < NF; f++) {
    const t = f / FPS;
    const res = await page.evaluate(t => {
      window.seek(t);
      const out = [];
      document.querySelectorAll('.ln>span,.at').forEach(sp => {
        const sc = sp.closest('.sc');
        if (!sc || getComputedStyle(sc).visibility === 'hidden') return;
        if (+getComputedStyle(sp).opacity === 0) return;
        const r = sp.getBoundingClientRect();
        let top = r.top, bot = r.bottom, left = r.left, right = r.right;
        const ln = sp.parentElement.classList.contains('ln') ? sp.parentElement.getBoundingClientRect() : null;
        if (ln) { top = Math.max(top, ln.top); bot = Math.min(bot, ln.bottom); if (bot <= top) return; }
        // a caixa da linha tem folga de entrelinha: desconta 18% em cima e embaixo para chegar perto da tinta
        const h = r.height;
        out.push({ txt: sp.textContent, left, right, bot: Math.min(bot, r.bottom - h * 0.16) });
      });
      return out;
    }, t);
    for (const e of res) {
      worst.l = Math.min(worst.l, e.left); worst.r = Math.max(worst.r, e.right); worst.b = Math.max(worst.b, e.bot);
      if (e.left < L || e.right > R || e.bot > B) fails.push(t.toFixed(2) + ' ' + e.txt + ' ' + JSON.stringify([Math.round(e.left), Math.round(e.right), Math.round(e.bot)]));
    }
  }
  console.log('limites', { L, R, B }, 'extremos medidos', worst);
  console.log(fails.length ? 'FORA: ' + fails.length + '\n' + fails.slice(0, 20).join('\n') : 'OK: todo texto dentro da área segura em todos os quadros');
} else {
  mkdirSync(path.join(dir, 'frames'), { recursive: true });
  for (let f = 0; f < NF; f++) {
    await page.evaluate(t => window.seek(t), f / FPS);
    await page.screenshot({ path: path.join(dir, 'frames', String(f).padStart(4, '0') + '.png') });
  }
}
await browser.close();
