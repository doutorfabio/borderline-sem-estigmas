const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const dir=process.argv[2], mode=process.argv[3];
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+dir+'/reel.html');await p.evaluate(()=>document.fonts.ready);
let times;
if(mode==='stills'){times=process.argv[4].split(',').map(Number);fs.mkdirSync(dir+'/stills',{recursive:true});}
else{const a=+process.argv[4],z=+process.argv[5];times=[];for(let i=a;i<z;i++)times.push(i/30);fs.mkdirSync(dir+'/fr',{recursive:true});}
for(const t of times){await p.evaluate(t=>seek(t),t);
 const name=mode==='stills'?dir+'/stills/s_'+t.toFixed(2)+'.png':dir+'/fr/'+String(Math.round(t*30)).padStart(5,'0')+'.jpg';
 await p.screenshot(mode==='stills'?{path:name}:{path:name,type:'jpeg',quality:95});}
await b.close()})();
