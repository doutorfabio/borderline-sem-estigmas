const {chromium}=require('playwright');(async()=>{
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/index.html');await p.evaluate(()=>window.ready);
const ts=process.argv.slice(2).map(Number);
for(const t of ts){await p.evaluate(t=>seek(t),t);await p.locator('canvas').screenshot({path:`still_${t.toFixed(3)}.png`});}
console.log(JSON.stringify(await p.evaluate(()=>({L:{F7:getL().F7,FP:getL().FP,FW:getL().FW,sk:getL().sk},boxes:boxes(0).filter(b=>!b.ok)}))));
await b.close();})();
