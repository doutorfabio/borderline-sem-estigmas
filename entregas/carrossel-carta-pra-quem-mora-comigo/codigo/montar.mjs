// Monta as 7 telas (1080x1350) com o texto por cima das bases recortadas.
// Uso: node montar.mjs <pasta-de-trabalho (crop1..7.png + rodape.json)> <pasta-de-saida>
import { createRequire } from 'module';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
const { chromium } = createRequire(import.meta.url)('playwright');
const here = path.dirname(fileURLToPath(import.meta.url));
const [cropDir, outDir] = process.argv.slice(2);
const PRETO = '#111111', VERMELHO = '#B3261E', CREME = '#F3EBDD';
const M = 64, LARG = 1080, ALT = 1350, MAXW = LARG * 0.88, F0 = 92, LH = 0.92;
// Cada tela: opções de quebra (linhas = [preto, vermelho]) e limite = base da tinta do título, acima do começo da foto.
// O código escolhe a quebra que dá a maior letra (teto 92 px) sem passar da largura nem do limite.
const telas = [
  { id: '01-capa', limite: 262, sub: 'DE UMA PACIENTE COM BORDERLINE.', subTopo: 322,
    opcoes: [[['CARTA PRA QUEM', ''], ['', 'MORA COMIGO.']]] },
  { id: '02-tese', limite: 266,
    opcoes: [[['NÃO PRECISA ENTENDER A CRISE.', ''], ['PRECISA ', 'FICAR.']]] },
  { id: '03-embora', limite: 286,
    opcoes: [[['SE EU DISSER QUE VOU EMBORA,', ''], ['NÃO LEVE A SÉRIO ANTES DE ', 'AMANHÃ.']],
             [['SE EU DISSER QUE VOU EMBORA,', ''], ['NÃO LEVE A SÉRIO', ''], ['ANTES DE ', 'AMANHÃ.']]] },
  { id: '04-pergunte', limite: 260,
    opcoes: [[['NÃO ME PERGUNTE O QUE FOI TRÊS VEZES.', ''], ['UMA, E DEPOIS ', 'SENTE.']],
             [['NÃO ME PERGUNTE O QUE FOI', ''], ['TRÊS VEZES.', ''], ['UMA, E DEPOIS ', 'SENTE.']]] },
  { id: '05-silencio', limite: 540,
    opcoes: [[['SE EU ESTIVER CALADA,', ''], ['O SILÊNCIO NÃO É CASTIGO.', ''], ['É ', 'ECONOMIA.']],
             [['SE EU ESTIVER CALADA,', ''], ['O SILÊNCIO', ''], ['NÃO É CASTIGO.', ''], ['É ', 'ECONOMIA.']]] },
  { id: '06-grito', limite: 456,
    opcoes: [[['SE EU GRITAR,', ''], ['O GRITO NÃO É SOBRE VOCÊ.', ''], ['MAS ', 'TAMBÉM É.']],
             [['SE EU GRITAR,', ''], ['O GRITO NÃO É', ''], ['SOBRE VOCÊ.', ''], ['MAS ', 'TAMBÉM É.']]] },
  { id: '07-acumulo', limite: 282,
    opcoes: [[['E SE UM DIA EU FOR EMBORA DE VERDADE,', ''], ['NÃO FOI DO DIA. FOI DO ', 'ACÚMULO.']],
             [['E SE UM DIA EU FOR EMBORA', ''], ['DE VERDADE, NÃO FOI DO DIA.', ''], ['FOI DO ', 'ACÚMULO.']]] },
];
const rodape = JSON.parse(fs.readFileSync(path.join(cropDir, 'rodape.json'), 'utf8'));
const fontB64 = fs.readFileSync(path.join(here, '../../../reels-remotion/public/fonts/anton.woff2')).toString('base64');
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: LARG, height: ALT }, deviceScaleFactor: 1 });
const relatorio = [];
for (let i = 0; i < telas.length; i++) {
  const t = telas[i];
  const img = fs.readFileSync(path.join(cropDir, `crop${i + 1}.png`)).toString('base64');
  await page.setContent(`<!doctype html><html><head><meta charset="utf-8"><style>
    @font-face{font-family:'Anton';src:url(data:font/woff2;base64,${fontB64}) format('woff2');}
    html,body{margin:0;padding:0;background:#fff} svg{display:block}
    text{font-family:'Anton';font-kerning:normal;white-space:pre}
  </style></head><body><svg id="s" xmlns="http://www.w3.org/2000/svg" width="${LARG}" height="${ALT}" viewBox="0 0 ${LARG} ${ALT}">
    <image href="data:image/png;base64,${img}" x="0" y="0" width="${LARG}" height="${ALT}"/></svg></body></html>`);
  await page.evaluate(() => document.fonts.load('92px Anton'));
  await page.evaluate(() => document.fonts.ready);
  const info = await page.evaluate(({ t, M, MAXW, F0, LH, PRETO, VERMELHO, CREME, corRodape, ALT, LARG }) => {
    const NS = 'http://www.w3.org/2000/svg', svg = document.getElementById('s');
    const cv = document.createElement('canvas'), ctx = cv.getContext('2d', { willReadFrequently: true });
    ctx.font = '1000px Anton';
    const cap = ctx.measureText('H').actualBoundingBoxAscent / 1000;
    const desc = ctx.measureText('p').actualBoundingBoxDescent / 1000;
    const asc = ctx.measureText('d').actualBoundingBoxAscent / 1000;
    // perfil de tinta de uma linha (a 100 px): por coluna, quanto sobe acima e desce abaixo da linha de base
    const R = 100;
    const perfil = (txt) => {
      cv.width = 3200; cv.height = 300; ctx.font = `${R}px Anton`; ctx.letterSpacing = `${-0.01 * R}px`; ctx.fillStyle = '#000';
      ctx.clearRect(0, 0, cv.width, cv.height); ctx.fillText(txt, 10, 180);
      const d = ctx.getImageData(0, 0, cv.width, cv.height).data, up = new Float32Array(cv.width).fill(-1e9), dn = new Float32Array(cv.width).fill(-1e9);
      for (let x = 0; x < cv.width; x++) for (let y = 0; y < cv.height; y++) if (d[(y * cv.width + x) * 4 + 3] > 40) { if (up[x] < -1e8) up[x] = 180 - y; dn[x] = y - 180; }
      return { up, dn };
    };
    // entrelinha mínima (em) para nenhum acento encostar na linha de cima: folga de 0,045 em; piso de 0,92
    const entrelinha = (linhas) => {
      let need = LH; const ps = linhas.map(([a, b]) => perfil(a + b));
      for (let k = 0; k + 1 < ps.length; k++) for (let x = 0; x < 3200; x++) {
        let dn = -1e9; for (let j = Math.max(0, x - 4); j <= Math.min(3199, x + 4); j++) dn = Math.max(dn, ps[k].dn[j]);
        if (dn < -1e8 || ps[k + 1].up[x] < -1e8) continue;
        need = Math.max(need, (ps[k + 1].up[x] + Math.max(dn, 0) + 4.5) / R);
      }
      return need;
    };
    const mk = (x, y, size, ls) => { const e = document.createElementNS(NS, 'text'); e.setAttribute('x', x); e.setAttribute('y', y); e.setAttribute('font-size', size); e.setAttribute('letter-spacing', ls); svg.appendChild(e); return e; };
    const span = (e, txt, fill) => { if (!txt) return; const s = document.createElementNS(NS, 'tspan'); s.setAttribute('fill', fill); s.textContent = txt; e.appendChild(s); };
    const eb = mk(M, M + cap * 28, 28, '-0.01em'); span(eb, 'BORDERLINE:', VERMELHO);
    const topo = M + cap * 28 + 18; // topo da tinta do título
    let melhor = null;
    for (const linhas of t.opcoes) {
      const lh = entrelinha(linhas);
      const els = linhas.map(([a, b]) => { const e = mk(M, -500, F0, '-0.01em'); span(e, a, PRETO); span(e, b, VERMELHO); return e; });
      let f = F0, larg = 0, base = 0;
      for (; f >= 40; f--) {
        els.forEach(e => e.setAttribute('font-size', f));
        larg = Math.max(...els.map(e => e.getComputedTextLength()));
        base = topo + (els.length - 1) * lh * f + cap * f;
        if (larg <= MAXW && base <= t.limite) break;
      }
      const cand = { els, f, larg, base, lh, linhas };
      if (!melhor || f > melhor.f) { if (melhor) melhor.els.forEach(e => e.remove()); melhor = cand; } else els.forEach(e => e.remove());
    }
    const { els, f, larg, base, lh } = melhor;
    els.forEach((e, k) => e.setAttribute('y', (topo + cap * f + k * lh * f).toFixed(2)));
    if (t.sub) { const s = mk(M, t.subTopo + cap * 30, 30, '-0.01em'); span(s, t.sub, PRETO); }
    // rodapé: tinta mais baixa a 68 px da base (5%)
    const X = 128, fundo = ALT - 68, baseR = fundo - desc * 24;
    const h = mk(X, baseR, 24, '0.02em'); span(h, '@drfabioschmidt', corRodape === 'creme' ? CREME : PRETO);
    if (corRodape === 'creme') { // sombra leve só atrás do @ claro, para ele não sumir em trecho claro da foto
      svg.insertAdjacentHTML('afterbegin', '<defs><filter id="sombra" x="-10%" y="-40%" width="120%" height="180%"><feDropShadow dx="0" dy="1" stdDeviation="2.2" flood-color="#000" flood-opacity="0.55"/></filter></defs>');
      h.setAttribute('filter', 'url(#sombra)');
    }
    const r = document.createElementNS(NS, 'rect'); r.setAttribute('x', X); r.setAttribute('y', Math.round(baseR - asc * 24 - 12 - 4)); r.setAttribute('width', 64); r.setAttribute('height', 4); r.setAttribute('fill', VERMELHO); svg.appendChild(r);
    return { fonte: f, linhas: els.length, entrelinha: +lh.toFixed(3), largura: +larg.toFixed(1), baseTitulo: +base.toFixed(1), texto: melhor.linhas.map(l => l.join('')).join(' / ') };
  }, { t, M, MAXW, F0, LH, PRETO, VERMELHO, CREME, corRodape: rodape[i], ALT, LARG });
  await page.screenshot({ path: path.join(outDir, `${t.id}.png`), clip: { x: 0, y: 0, width: LARG, height: ALT } });
  relatorio.push({ tela: t.id, ...info, limite: t.limite, rodape: rodape[i] });
}
await browser.close();
fs.writeFileSync(path.join(outDir, 'relatorio.json'), JSON.stringify(relatorio, null, 1));
for (const r of relatorio) console.log(r.tela, r.fonte + 'px', r.linhas + ' linhas', 'entrelinha', r.entrelinha, 'larg', r.largura, 'base', r.baseTitulo, '/', r.limite, '@' + r.rodape, '|', r.texto);
