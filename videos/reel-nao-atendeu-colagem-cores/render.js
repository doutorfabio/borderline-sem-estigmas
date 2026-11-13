const {chromium}=require('/opt/node-tools/node_modules/playwright');const fs=require('fs');const path=require('path');
const dir=process.argv[2],mode=process.argv[3]||'all';const FPS=30,N=Math.round((+process.env.DUR||38.9)*FPS);
(async()=>{const br=await chromium.launch();let frames=[],jpg=true;
 if(mode==='all'){for(let f=1;f<=N;f++)frames.push(f)}else if(mode.startsWith('range:')){const [a,b]=mode.slice(6).split('-').map(Number);for(let f=a;f<=b;f++)frames.push(f)}else{frames=mode.split(',').map(Number);jpg=false}
 const WK=(mode==='all'||mode.startsWith('range:'))?4:1;fs.mkdirSync(path.join(dir,'out'),{recursive:true});let viol=[];
 await Promise.all([...Array(WK).keys()].map(async k=>{const pg=await br.newPage({viewport:{width:1080,height:1920}});
  await pg.goto('file://'+path.join(dir,'index.html'));await pg.evaluate(async()=>{for(const f of ['800 64px Mont','900 64px Mont','600 40px Mont','italic 900 100px Frau'])await document.fonts.load(f)});
  for(let j=k;j<frames.length;j+=WK){const f=frames[j],t=(f-1)/FPS;const b=await pg.evaluate(t=>window.setT(t),t);await pg.evaluate(()=>Promise.all([...document.images].map(i=>i.decode().catch(()=>0))));
   if(b&&(b[0]<54||b[2]>950||b[3]>1536))viol.push([f,b.map(Math.round)]);
   await pg.screenshot({path:path.join(dir,'out',String(f).padStart(4,'0')+(jpg?'.jpg':'.png')),type:jpg?'jpeg':'png',quality:jpg?95:undefined})}
  await pg.close()}));await br.close();console.log('violations',viol.length,JSON.stringify(viol.slice(0,8)))})();
