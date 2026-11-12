const {chromium}=require('/opt/node-tools/node_modules/playwright');const fs=require('fs');const path=require('path');
const dir=process.argv[2],mode=process.argv[3]||'all';const FPS=30,N=1238;
(async()=>{const br=await chromium.launch();const WK=mode==='all'?4:1;
 let frames=[];if(mode==='all'){for(let f=1;f<=N;f++)frames.push(f)}else frames=mode.split(',').map(Number);
 fs.mkdirSync(path.join(dir,'out'),{recursive:true});let viol=[];
 await Promise.all([...Array(WK).keys()].map(async k=>{const pg=await br.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
  await pg.goto('file://'+path.join(dir,'index.html'));await pg.evaluate(()=>document.fonts.ready);
  await pg.evaluate(async()=>{await Promise.all([document.fonts.load('800 68px Mont'),document.fonts.load('900 58px Mont'),document.fonts.load('italic 900 100px Frau')])});
  for(let j=k;j<frames.length;j+=WK){const f=frames[j],t=(f-1)/FPS;const b=await pg.evaluate(([t,f])=>window.setT(t,f),[t,f]);
   if(b&&(b[0]<54||b[2]>950||b[3]>1536))viol.push([f,b.map(x=>Math.round(x))]);
   await pg.screenshot({path:path.join(dir,'out',String(f).padStart(4,'0')+(mode==='all'?'.jpg':'.png')),type:mode==='all'?'jpeg':'png',quality:mode==='all'?96:undefined,clip:{x:0,y:0,width:1080,height:1920}})}
  await pg.close()}));
 await br.close();console.log('violations',viol.length,JSON.stringify(viol.slice(0,12)))})();
