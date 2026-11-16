const {chromium}=require('playwright');
(async()=>{const [,,comp,out,...ts]=process.argv;const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1080,height:1920}});const errs=[];p.on('pageerror',e=>errs.push(String(e)));
await p.goto('file://'+require('path').resolve(comp));await p.evaluate(()=>window.__ready);
for(const t of ts){await p.evaluate(t=>window.__seek(+t),t);await p.screenshot({path:`${out}-${t}.png`,clip:{x:0,y:0,width:1080,height:1920}});}
console.log('errors',errs);await b.close();})();
