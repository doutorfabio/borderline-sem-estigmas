const { chromium } = require('playwright');
const fs = require('fs'); const path=require('path');
(async()=>{
  const mode = process.argv[2] || 'stills';
  const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1080,height:1920}, deviceScaleFactor:1});
  const errs=[]; p.on('pageerror', e=>errs.push(String(e))); p.on('console', m=>{ if(m.type()==='error') errs.push(m.text()); });
  await p.goto('file://'+path.resolve('../protocolo-7-dias-tipografico.html'));
  await p.waitForFunction(()=>typeof window.seek==='function');
  const grab = async (t, f, s) => { const d = await p.evaluate(([t,s])=>{ window.seek(t, s); return document.getElementById('c').toDataURL('image/png'); }, [t,s||0]); fs.writeFileSync(f, Buffer.from(d.split(',')[1],'base64')); };
  if (mode==='stills'){
    fs.mkdirSync('stills',{recursive:true});
    const ts = process.argv[3].split(',').map(Number);
    for (const t of ts) await grab(t, `stills/t${t.toFixed(2)}.png`);
  } else if (mode==='info'){
    console.log(JSON.stringify(await p.evaluate(()=>({hS:L.hS, YB0:L.YB0, YB1:L.YB1, YB2:L.YB2, YBF:L.YBF, s1:L.l1.size, impCap:L.impCap, impScale:L.impSrcScale, rest:L.props.map(p=>+p.rest.toFixed(2)), exit:L.exitT, pisoCap:L.pisoCap, colH:L.cols.map(c=>+c.h.toFixed(1)), p7:L.p7.size, pq:L.pq.size, cada:L.cada.size, bf1:[L.bf1a.size,L.bf1b.size]}))));
  } else if (mode==='measure'){
    // medição por pixel, com o recorte da área segura desligado: qualquer pixel de texto fora da área segura aparece aqui
    const res = await p.evaluate(()=>{
      window.setSafeClip(false); const S = window.SAFE; const c = document.getElementById('c'); const g = c.getContext('2d', {willReadFrequently:true});
      const out = []; const bg=[13,13,13];
      const cnt = (x,y,w,h)=>{ const d=g.getImageData(x,y,w,h).data; let n=0; for(let i=0;i<d.length;i+=4){ if(Math.abs(d[i]-13)>10||Math.abs(d[i+1]-13)>10||Math.abs(d[i+2]-13)>10) n++; } return n; };
      for (let n=0;n<450;n++){ window.seek(n/30);
        const l=cnt(0,0,Math.floor(S.l),1920), r=cnt(Math.ceil(S.r),0,1080-Math.ceil(S.r),1920), t=cnt(0,0,1080,Math.floor(S.t)), b=cnt(0,Math.ceil(S.b),1080,1920-Math.ceil(S.b));
        if (l||r||t||b) out.push([n,l,r,t,b]); }
      window.setSafeClip(true); return out; });
    const agg={esq:[],dir:[],topo:[],base:[]};
    for (const [n,l,r,t,b] of res){ if(l)agg.esq.push(n); if(r)agg.dir.push(n); if(t)agg.topo.push(n); if(b)agg.base.push(n); }
    for (const k in agg) console.log(k, agg[k].length ? ('quadros '+agg[k][0]+'..'+agg[k][agg[k].length-1]+' n='+agg[k].length) : 'nenhum');
    fs.writeFileSync('measure.json', JSON.stringify(res));
  } else if (mode==='render'){
    fs.mkdirSync('frames',{recursive:true});
    for (let n=0;n<450;n++) await grab(n/30, `frames/f${String(n).padStart(4,'0')}.png`);
  }
  if (errs.length) console.log('ERROS', errs.slice(0,5)); await b.close();
})();
