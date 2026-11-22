// node render.js <html> <outdir> [stills|audit|video]
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path'); const { spawn } = require('child_process');
(async () => {
  const [html, out, mode] = process.argv.slice(2);
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(html) + '?render=1');
  await p.waitForFunction(() => window.ready === true);
  const grab = async t => Buffer.from((await p.evaluate(t => { seek(t); return document.getElementById('c').toDataURL('image/png'); }, t)).split(',')[1], 'base64');
  if (mode === 'stills') {
    const ts = (process.env.TS || '1.40,1.75,2.60,3.60,3.95,4.80,5.60,6.45,7.00,7.60,9.00,9.98').split(',').map(Number);
    for (const t of ts) fs.writeFileSync(path.join(out, `still_${t.toFixed(2)}.png`), await grab(t));
  } else if (mode === 'audit') {
    const SL = 90, SR = 950, ST = 90, SB = 1536; let bad = [];
    for (let f = 0; f < 600; f++) {
      const boxes = await p.evaluate(t => audit(t), f / 60);
      for (const bx of boxes) if (bx.x0 < SL - 0.5 || bx.x1 > SR + 0.5 || bx.y0 < ST - 0.5 || bx.y1 > SB + 0.5) bad.push({ f, ...bx });
    }
    console.log('violations', bad.length); console.log(JSON.stringify(bad.slice(0, 30)));
    const L = await p.evaluate(() => JSON.stringify({ anchor: L.anchor, brand: { barTop: L.brand.barTop, cy: L.brand.cy } }));
    console.log(L);
  } else {
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', '60', '-c:v', 'png', '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-pix_fmt', 'yuv420p', '-r', '60', '-movflags', '+faststart', path.join(out, 'protocolo-7-dias-bumper.mp4')], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let f = 0; f < 600; f++) { const buf = await grab(f / 60); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  await b.close();
})();
