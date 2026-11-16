const {chromium}=require('playwright');const path=require('path');
(async()=>{const [,,comp,dir,w,nw]=process.argv;const W=+w,N=+nw;const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto('file://'+path.resolve(comp));await p.evaluate(()=>window.__ready);
for(let f=W;f<600;f+=N){await p.evaluate(t=>window.__seek(t),f/60);
await p.screenshot({path:`${dir}/f${String(f).padStart(4,'0')}.png`,clip:{x:0,y:0,width:1080,height:1920}});}
await b.close();})();
