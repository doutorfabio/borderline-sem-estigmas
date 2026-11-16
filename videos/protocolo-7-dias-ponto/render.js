const {chromium}=require('playwright');const path=require('path');
(async()=>{const [,,comp,dir,w,nw,fps,dur]=process.argv;const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto('file://'+path.resolve(comp));await p.evaluate(()=>window.__ready);
const N=Math.round(+fps*+dur);for(let f=+w;f<N;f+=+nw){await p.evaluate(t=>window.__seek(t),f/+fps);
await p.screenshot({path:`${dir}/f${String(f).padStart(5,'0')}.png`,clip:{x:0,y:0,width:1080,height:1920}});}
await b.close();})();
