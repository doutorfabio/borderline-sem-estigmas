const { chromium } = require('playwright');
const { spawn } = require('child_process');
(async () => {
  const mode = process.argv[2] || 'full';
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + __dirname + '/index.html');
  await p.evaluate(() => document.fonts.ready);
  for (const f of ['500 20px Mont','600 20px Mont','800 20px Mont','900 20px Mont','500 20px Corm','600 20px Corm','400 20px Inter','500 20px Inter']) await p.evaluate(x => document.fonts.load(x), f);
  const DUR = await p.evaluate(() => window.DUR);
  if (mode === 'test') {
    const ts = process.argv.slice(3).map(Number);
    for (const t of ts) { await p.evaluate(t => window.render(t), t); await p.screenshot({ path: __dirname + '/t_' + t.toFixed(2) + '.jpg', type: 'jpeg', quality: 85 }); }
  } else {
    const ff = spawn('ffmpeg', ['-v','error','-y','-f','image2pipe','-c:v','mjpeg','-r','30','-i','-','-c:v','libx264','-preset','slow','-crf','15','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-r','30', __dirname + '/video.mp4'], { stdio: ['pipe','inherit','inherit'] });
    const n = Math.round(DUR * 30);
    for (let i = 0; i < n; i++) {
      await p.evaluate(t => window.render(t), i / 30);
      const buf = await p.screenshot({ type: 'jpeg', quality: 96 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r)); console.log('frames', n);
  }
  await b.close();
})();
