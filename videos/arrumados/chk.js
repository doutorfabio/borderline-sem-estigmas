// node chk.js arquivo.html saida t1 t2 ...
const { chromium } = require('playwright'); const path=require('path');
(async()=>{ const [f,out,...ts]=process.argv.slice(2);
  const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1080,height:1920}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto('file://'+path.resolve(f)); await p.evaluate(()=>document.fonts.ready);
  for(const t of ts){ await p.evaluate(t=>seek(+t),t); await p.screenshot({path:`${out}_${t}.png`});
    const bad = await p.evaluate(()=>[...document.querySelectorAll('text')].filter(e=>{ let n=e; while(n&&n.tagName!=='svg'){ if(n.style&&n.style.display==='none') return false; if(n.getAttribute&&n.getAttribute('opacity')==='0') return false; n=n.parentNode;} const r=e.getBoundingClientRect(); return r.width>0 && r.bottom>0 && r.top<1920 && r.right>0 && r.left<1080 && (r.left<54||r.right>950||r.bottom>1536); }).map(e=>{const r=e.getBoundingClientRect(); return e.textContent+` [${r.left|0},${r.top|0},${r.right|0},${r.bottom|0}]`;}));
    if(bad.length) console.log('t='+t,'FORA:',bad.join(' | ')); }
  if(errs.length) console.log('ERROS',errs); await b.close(); })();
