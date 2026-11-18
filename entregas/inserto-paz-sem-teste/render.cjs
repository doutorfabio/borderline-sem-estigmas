// node render.cjs beats | full
const { chromium } = require('playwright');
const { mkdirSync } = require('fs');
const { execSync } = require('child_process');
(async () => {
const mode = process.argv[2] || 'beats';
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await p.goto('file://' + process.cwd() + '/index.html');
await p.evaluate(() => window.ready);
if (mode === 'beats') {
  mkdirSync('beats', { recursive: true });
  for (let i = 0; i <= 32; i++) { await p.evaluate(t => window.seek(t), i * 0.25); await p.screenshot({ path: `beats/b${String(i).padStart(2, '0')}.png` }); }
} else {
  mkdirSync('frames', { recursive: true });
  const N = 8 * 180;
  for (let i = 0; i < N; i++) { await p.evaluate(t => window.seek(t), i / 180); await p.screenshot({ path: `frames/f${String(i).padStart(5, '0')}.png` }); }
  execSync(`ffmpeg -y -loglevel error -framerate 180 -i frames/f%05d.png -vf "tmix=frames=3,select='not(mod(n-2\\,3))',setpts=N/60/TB" -r 60 -an -c:v libx264 -crf 12 -preset slow -pix_fmt yuv420p -movflags +faststart inserto-paz-sem-teste.mp4`);
}
await b.close();
})();
