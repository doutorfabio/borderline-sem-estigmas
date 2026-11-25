const { chromium } = require('playwright');
const fs = require('fs');
const S = process.argv[2]; const B = S + '/build'; const O = S + '/out'; const M = S + '/measure';
const which = (process.argv[3] || '2,3,4,5,6,7,8').split(',').map(Number);
fs.mkdirSync(M, { recursive: true });
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1792, height: 2240 }, deviceScaleFactor: 1 });
  const report = {};
  for (const n of which) {
    await p.goto('file://' + B + '/slide-' + n + '.html');
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(150);
    if (n === 4) {
      await p.evaluate(() => {
        const svg = document.getElementById('arrows'); const NS = 'http://www.w3.org/2000/svg';
        const pills = [...document.querySelectorAll('.pill')].map(e => e.getBoundingClientRect());
        const ink = '#111111'; const sw = 9;
        const line = d => { const e = document.createElementNS(NS, 'path'); e.setAttribute('d', d); e.setAttribute('fill', 'none'); e.setAttribute('stroke', ink); e.setAttribute('stroke-width', sw); e.setAttribute('stroke-linecap', 'round'); e.setAttribute('stroke-linejoin', 'round'); svg.appendChild(e); };
        const head = (x, y, dir) => { // ponta triangular
          const e = document.createElementNS(NS, 'path'); const s = 34;
          let d;
          if (dir === 'down') d = `M${x - s} ${y - s * 1.2} L${x + s} ${y - s * 1.2} L${x} ${y} Z`;
          if (dir === 'left') d = `M${x + s * 1.2} ${y - s} L${x + s * 1.2} ${y + s} L${x} ${y} Z`;
          e.setAttribute('d', d); e.setAttribute('fill', ink); svg.appendChild(e);
        };
        for (let i = 0; i < pills.length - 1; i++) {
          const a = pills[i], c = pills[i + 1]; const x = a.left + a.width / 2;
          const y1 = a.bottom + 16, y2 = c.top - 14;
          line(`M${x} ${y1} L${x} ${y2 - 30}`); head(x, y2, 'down');
        }
        // volta: de MAIS VERGONHA para CRISE, pela direita
        const last = pills[pills.length - 1], first = pills[0];
        const lane = 1560; const r = 70;
        const yb = last.top + last.height / 2, yt = first.top + first.height / 2;
        line(`M${last.right + 16} ${yb} L${lane - r} ${yb} Q${lane} ${yb} ${lane} ${yb - r} L${lane} ${yt + r} Q${lane} ${yt} ${lane - r} ${yt} L${first.right + 16 + 40} ${yt}`);
        head(first.right + 16, yt, 'left');
      });
    }
    await p.evaluate(() => document.body.classList.remove('m'));
    await p.screenshot({ path: O + '/slide-' + n + '.png' });
    // medição: cada linha sozinha, texto preto em branco
    await p.evaluate(() => document.body.classList.add('m'));
    const lines = await p.evaluate(() => [...document.querySelectorAll('.ln')].map(e => { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); return { t: e.textContent, top: r.top, bottom: r.bottom, left: r.left, right: r.right, fs: parseFloat(cs.fontSize), fam: cs.fontFamily }; }));
    report[n] = [];
    for (let i = 0; i < lines.length; i++) {
      await p.evaluate(i => document.querySelectorAll('.ln').forEach((e, j) => e.style.visibility = j === i ? 'visible' : 'hidden'), i);
      const f = M + `/s${n}-l${i}.png`;
      await p.screenshot({ path: f });
      report[n].push({ ...lines[i], img: f });
    }
  }
  fs.writeFileSync(M + '/report.json', JSON.stringify(report, null, 1));
  await b.close();
})();
