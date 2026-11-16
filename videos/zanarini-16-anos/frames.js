// node frames.js t1 t2 ... -> frames/check_t.png ; também mede a área segura e conta palavras visíveis
const { chromium } = require('playwright'); const path=require('path'); const fs=require('fs');
(async()=>{
  const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto('file://'+path.resolve('render.html')); await p.evaluate(()=>document.fonts.ready);
  fs.mkdirSync('checagem',{recursive:true});
  const ts = process.argv.slice(2).map(Number);
  for(const t of ts){
    const info = await p.evaluate(t=>{ seek(t);
      const out=[]; let words=0;
      LABELS.forEach(l=>{ if(l.g.style.display==='none') return;
        const r=l.inner.getBoundingClientRect(); const c={width:+l.rect.getAttribute('width'),height:+l.rect.getAttribute('height')};
        const vis = r.right>0 && r.left<1080 && r.bottom>0 && r.top<1920;
        if(!vis||c.width<1||c.height<1) return; words+=l.words;
        const txt=[...l.inner.querySelectorAll('text')].map(x=>x.textContent).join(' / ');
        const bad = (r.left<54||r.right>950||r.bottom>1536||r.top<96);
        out.push(`${bad?'FORA ':''}${txt} [${r.left|0},${r.top|0} ${r.right|0},${r.bottom|0}] fonte ${(parseFloat(l.inner.querySelector('text').getAttribute('font-size'))*r.width/l.box.w).toFixed(0)}px`);
      }); return {out,words};
    },t);
    await p.screenshot({path:`checagem/t${t.toFixed(2)}.png`});
    console.log(`t=${t}  palavras=${info.words}`); info.out.forEach(x=>console.log('   ',x));
  }
  if(errs.length) console.log('ERROS',errs);
  await b.close();
})();
