const {chromium}=require('/opt/node-tools/node_modules/playwright');
(async()=>{const br=await chromium.launch();const pg=await br.newPage({viewport:{width:1080,height:1920}});
await pg.goto('file://'+process.cwd()+'/index.html');await pg.waitForFunction('window.READY');
const r=await pg.evaluate(()=>{let L=1e9,R=0,B=0,bad=[];for(let i=0;i<963;i++){setT(i/30);for(const el of document.querySelectorAll('.w')){if(+el.style.opacity<0.05)continue;const b=el.getBoundingClientRect();L=Math.min(L,b.left);R=Math.max(R,b.right);B=Math.max(B,b.bottom);if(b.left<54||b.right>950||b.bottom>1536)bad.push([i,el.textContent,Math.round(b.left),Math.round(b.right),Math.round(b.bottom)])}}return {L,R,B,bad:bad.slice(0,20),n:bad.length}});
console.log(JSON.stringify(r));await br.close();})();
