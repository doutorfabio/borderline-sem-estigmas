// uso: node render.js <pasta-saida> [stills|all|check]
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const ROOT=__dirname,OUT=process.argv[2],MODE=process.argv[3]||'all',FPS=30,DUR=15;
const words=fs.readFileSync(path.join(ROOT,'words.json'),'utf8');
fs.writeFileSync(path.join(ROOT,'_comp.html'),fs.readFileSync(path.join(ROOT,'comp.html'),'utf8').replace('__WORDS__',words));
(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1920}});
 pg.on('pageerror',e=>console.log('ERRO',e.message));
 await pg.goto('file://'+path.join(ROOT,'_comp.html'));await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(500);
 fs.mkdirSync(OUT,{recursive:true});const bad=[];
 if(MODE==='stills')for(const t of [0,0.5,2.2,3.5,5.0,5.6,6.6,7.3,9.4,11.0,12.3,13.3,14.9]){await pg.evaluate(t=>seek(t),t);await pg.screenshot({path:`${OUT}/s${t.toFixed(2).padStart(5,'0')}.png`})}
 const n=FPS*DUR;
 for(let i=0;i<n;i++){const t=i/FPS;await pg.evaluate(t=>seek(t),t);
  if(i%3===0)for(const [tx,l,tp,r,bt] of await pg.evaluate(()=>boxes()))if(l<54||r>950||bt>1536||tp<190)bad.push([t.toFixed(2),tx,l,tp,r,bt].join(' | '));
  if(MODE==='all')await pg.screenshot({path:`${OUT}/f${String(i).padStart(4,'0')}.png`})}
 console.log('fora da area segura:',bad.length);bad.slice(0,25).forEach(x=>console.log(x));await b.close()})();
