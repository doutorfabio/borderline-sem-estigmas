const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1920}});
await pg.goto('file://'+process.cwd()+'/card.html');await pg.evaluate(()=>document.fonts.ready);
const fps=30,dur=5.4;for(let i=0;i<Math.round(fps*dur);i++){await pg.evaluate(t=>render(t),i/fps);await pg.screenshot({path:`fr2/${String(i).padStart(4,'0')}.png`});}
// safe-area check on final state
await pg.evaluate(()=>render(5));
const r=await pg.evaluate(()=>[...document.querySelectorAll('#b2 *, #b1 *')].filter(e=>e.offsetParent).map(e=>{const b=e.getBoundingClientRect();return [e.id||e.className,Math.round(b.left),Math.round(b.right),Math.round(b.top),Math.round(b.bottom)]}));
await pg.evaluate(()=>render(1));
const r1=await pg.evaluate(()=>[...document.querySelectorAll('#b1 *')].map(e=>{const b=e.getBoundingClientRect();return [e.id,Math.round(b.left),Math.round(b.right),Math.round(b.top),Math.round(b.bottom)]}));
console.log(JSON.stringify(r),JSON.stringify(r1));await b.close();})();
