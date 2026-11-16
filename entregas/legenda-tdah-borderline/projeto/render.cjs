const {chromium}=require('/opt/node-tools/node_modules/playwright');
const [,,a,b,out,list]=process.argv;
(async()=>{const br=await chromium.launch({args:['--allow-file-access-from-files']});
const pg=await br.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
await pg.goto('file://'+process.cwd()+'/index.html');await pg.waitForFunction('window.READY');
const fs=require('fs');fs.mkdirSync(out,{recursive:true});
const idx=list?list.split(',').map(Number):[...Array(+b-+a+1).keys()].map(k=>k+ +a);
for(const i of idx){await pg.evaluate(([i,t])=>frame(i,t),[i,(i-1)/30]);await pg.screenshot({path:`${out}/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:94});}
await br.close();})();
