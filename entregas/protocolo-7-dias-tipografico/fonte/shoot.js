const { chromium } = require('playwright');
const fs = require('fs'); const path=require('path');
(async()=>{
  const mode = process.argv[2] || 'stills';
  const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1080,height:1920}, deviceScaleFactor:1});
  const errs=[]; p.on('pageerror', e=>errs.push(String(e))); p.on('console', m=>{ if(m.type()==='error') errs.push(m.text()); });
  await p.goto('file://'+path.resolve('protocolo-7-dias-tipografico.html'));
  await p.waitForFunction(()=>typeof window.seek==='function');
  if (errs.length) { console.log(errs); }
  const grab = async (t, f) => { const d = await p.evaluate(t=>{ window.seek(t); return document.getElementById('c').toDataURL('image/png'); }, t); fs.writeFileSync(f, Buffer.from(d.split(',')[1],'base64')); };
  if (mode==='stills'){
    fs.mkdirSync('stills',{recursive:true});
    const ts = (process.argv[3]||'0.5,1.5,2.5,2.8,3.1,3.6,4.5,5.6,6.5,7.6,8.9,10,11.4,12.3,13,14.5').split(',').map(Number);
    for (const t of ts) await grab(t, `stills/t${t.toFixed(2)}.png`);
  } else if (mode==='measure'){
    const res = await p.evaluate(()=>{
      window.__measure = true; const S = window.SAFE; const out=[]; const tol=0.5;
      for (let n=0;n<450;n++){ const t=n/30; const R = window.seek(t);
        for (const r of R){ const inside = r.x1 > S.l && r.x0 < S.r && r.y1 > S.t && r.y0 < S.b; if (!inside) continue; const v=[]; if (r.x0 < S.l-tol) v.push('esq '+(S.l-r.x0).toFixed(1)); if (r.x1 > S.r+tol) v.push('dir '+(r.x1-S.r).toFixed(1));
          if (r.y0 < S.t-tol) v.push('topo '+(S.t-r.y0).toFixed(1)); if (r.y1 > S.b+tol) v.push('base '+(r.y1-S.b).toFixed(1));
          if (v.length) out.push(n+' '+r.name+' '+v.join(',')); } }
      window.__measure=false; return out; });
    const by={}; for (const l of res){ const [n,name,...rest]=l.split(' '); (by[name]=by[name]||[]).push(+n); }
    for (const k in by) console.log(k, 'quadros', by[k][0]+'..'+by[k][by[k].length-1], 'n='+by[k].length);
    console.log('total violações', res.length); fs.writeFileSync('measure.txt', res.join('\n'));
  } else if (mode==='render'){
    fs.mkdirSync('frames',{recursive:true});
    for (let n=0;n<450;n++) await grab(n/30, `frames/f${String(n).padStart(4,'0')}.png`);
  }
  console.log('errs', errs.length); await b.close();
})();
