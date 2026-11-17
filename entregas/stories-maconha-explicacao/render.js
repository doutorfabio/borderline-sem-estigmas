const { chromium } = require('playwright');
(async () => {
  const S = process.argv[2];
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 2 });
  await p.goto('file://' + S + '/stories.html');
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(400);
  const fonts = await p.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight));
  console.log('fonts', JSON.stringify(fonts));
  for (let i = 1; i <= 6; i++) {
    const el = await p.$('#s' + i);
    // overflow check: content bounds inside safe zone
    const r = await p.evaluate((id) => {
      const s = document.getElementById(id); const sb = s.getBoundingClientRect();
      let minY = 1e9, maxY = -1e9, minX = 1e9, maxX = -1e9;
      s.querySelectorAll('.k,.h,.b,.src,.safe,.card,.cta,.n').forEach(e => { const r = e.getBoundingClientRect(); minY = Math.min(minY, r.top - sb.top); maxY = Math.max(maxY, r.bottom - sb.top); minX = Math.min(minX, r.left - sb.left); maxX = Math.max(maxX, r.right - sb.left); });
      const over = [...s.querySelectorAll('.h,.b,.k')].filter(e => e.scrollWidth > e.clientWidth + 1).length;
      return { minY: Math.round(minY), maxY: Math.round(maxY), minX: Math.round(minX), maxX: Math.round(maxX), over };
    }, 's' + i);
    console.log('s' + i, JSON.stringify(r));
    await el.screenshot({ path: S + '/out/story-' + i + '.png' });
  }
  await b.close();
})();
