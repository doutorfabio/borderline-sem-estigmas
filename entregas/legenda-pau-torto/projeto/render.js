const {chromium}=require('/opt/node-tools/node_modules/playwright');
const path=require('path');const N=1110,P=4,R=process.argv[2];const only=process.argv[3]?process.argv[3].split(',').map(Number):null;
(async()=>{const br=await chromium.launch({args:['--allow-file-access-from-files']});const bad=[];
 const list=only||[...Array(N).keys()];
 await Promise.all([...Array(P).keys()].map(async p=>{const pg=await br.newPage({viewport:{width:1080,height:1920}});
  await pg.goto('file://'+R+'/index.html');await pg.evaluate(()=>init());
  for(let i=p;i<list.length;i+=P){const n=list[i];const t=n/30;
    const b=await pg.evaluate(([t,s])=>setT(t,s),[t,'frames/'+String(n+1).padStart(4,'0')+'.jpg']);
    if(b.length)bad.push([n,b]);
    await pg.screenshot({path:R+'/out/'+String(n+1).padStart(4,'0')+'.jpg',type:'jpeg',quality:93});}
 }));
 await br.close();console.log('bad',JSON.stringify(bad.slice(0,20)),bad.length);})();
