const { chromium } = require('playwright');
const fs=require('fs'); const path=require('path');
(async()=>{
 const [mode, outDir, ...rest]=process.argv.slice(2);
 const browser=await chromium.launch();
 const page=await browser.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
 await page.goto('file://'+path.resolve(__dirname,'comp/index.html'));
 await page.evaluate(()=>window.ready);
 fs.mkdirSync(outDir,{recursive:true});
 let times=[];
 if(mode==='test'){ times=rest.map(Number); }
 else { const [a,b]=rest.map(Number); for(let i=a;i<b;i++) times.push(i); }
 const viol=[];
 for(const x of times){
  const t= mode==='test'? x : x/24;
  if(mode==='test'){ const bg=path.resolve(__dirname,'bg',`${x.toFixed(3)}.jpg`); if(fs.existsSync(bg)) await page.evaluate(u=>{document.body.style.background=`url(${u}) center/cover`},'file://'+bg); }
  await page.evaluate(t=>window.render(t),t);
  const v=await page.evaluate(t=>window.audit(t),t); if(v.length) viol.push([t.toFixed(3),v]);
  const name= mode==='test'? `t_${x.toFixed(3)}.jpg` : `f_${String(x).padStart(5,'0')}.png`;
  await page.screenshot({path:path.join(outDir,name), omitBackground: mode!=='test', type: mode==='test'?'jpeg':'png', quality: mode==='test'?80:undefined});
 }
 fs.writeFileSync(path.join(outDir, mode==='test'?'audit_test.json':`audit_${rest[0]}.json`), JSON.stringify(viol));
 console.log('done', times.length, 'violations frames:', viol.length);
 if(viol.length) console.log(JSON.stringify(viol.slice(0,15)));
 await browser.close();
})();
