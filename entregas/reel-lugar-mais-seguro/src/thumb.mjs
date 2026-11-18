// Reel cover built with the film's own system (paper, Anton, red Bodoni italic, the engraving), composed for the 3:4 grid crop.
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');
import { writeFileSync } from 'node:fs';
const [html,out]=process.argv.slice(2);
const b=await chromium.launch({args:['--no-sandbox','--allow-file-access-from-files']});
const p=await b.newPage({viewport:{width:1080,height:1920}});
p.on('pageerror',e=>console.log('[page error]',e.message));
await p.goto('file://'+process.cwd()+'/'+html+'?render'); await p.waitForFunction('window.ready===true',null,{timeout:120000});
const r=await p.evaluate(()=>{
  const c=document.createElement('canvas'); c.width=1080; c.height=1920; const x=c.getContext('2d',{willReadFrequently:true});
  x.imageSmoothingQuality='high'; x.drawImage(paperC,0,0);
  const B=mkBlock({cx:540,top:336,maxW:864,maxH:548,gap:0.21,lines:[{k:1.38,segs:['SE O BORDERLINE']},{segs:['DESABA NA SUA FRENTE,']},{segs:['VOCÊ É O LUGAR']},{k:1.27,segs:['*MAIS SEGURO']},{segs:['QUE ELE TEM.']}]});
  const T=tr('A01',0.47,0.675,507.6,1452,1.0); drawT(x,T);
  const cc=pt(T,0.47,0.678); brush(x,ellipsePts(cc[0],cc[1],0.246*T.w,0.099*T.h,-0.1,-2.3,1.07,3),0,1,10.5);
  // text-only pass for measuring
  const m=document.createElement('canvas'); m.width=1080; m.height=1920; const mx=m.getContext('2d',{willReadFrequently:true});
  for(const l of B.lines){drawLine(x,l,ON); drawLine(mx,l,ON);}
  const d=new Uint32Array(mx.getImageData(0,0,1080,1920).data.buffer); let x0=1080,y0=1920,x1=-1,y1=-1;
  for(let y=0;y<1920;y++)for(let xx=0;xx<1080;xx++)if((d[y*1080+xx]>>>24)>10){if(xx<x0)x0=xx;if(xx>x1)x1=xx;if(y<y0)y0=y;if(y>y1)y1=y;}
  return {png:c.toDataURL('image/png'),sizes:B.lines.map(l=>Math.round(l.size)),bbox:[x0,y0,x1,y1],circleBottom:Math.round(cc[1]+0.099*T.h*1.03)};
});
writeFileSync(out,Buffer.from(r.png.split(',')[1],'base64')); console.log(JSON.stringify({sizes:r.sizes,bbox:r.bbox,circleBottom:r.circleBottom})); await b.close();
