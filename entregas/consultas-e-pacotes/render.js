const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 510, height: 1104 } });
  await p.goto('file://' + __dirname + '/consultas-e-pacotes.html');
  await p.evaluate(() => document.fonts.ready);
  console.log(JSON.stringify(await p.evaluate(() => [...document.querySelectorAll('.page')].map(pg => {
    const f = pg.querySelector('.foot'); const prev = f.previousElementSibling;
    return { overflow: pg.scrollHeight - pg.clientHeight,
             gapBeforeFoot: Math.round(f.getBoundingClientRect().top - prev.getBoundingClientRect().bottom),
             footToBottom: Math.round(pg.getBoundingClientRect().bottom - f.getBoundingClientRect().bottom) };
  }))));
  await p.emulateMedia({ media: 'print' });
  await p.pdf({ path: 'Consultas-e-Pacotes.pdf', printBackground: true, preferCSSPageSize: true });
  await b.close();
})();
