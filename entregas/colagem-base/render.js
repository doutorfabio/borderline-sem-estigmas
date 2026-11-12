// uso: node render.js <pasta-da-peca> <pasta-saida> [stills|all] [duracao]
// A peça tem comp.html e, se narrada, words.json (entra no lugar de __WORDS__).
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const P=path.resolve(process.argv[2]),OUT=process.argv[3],MODE=process.argv[4]||'all',DUR=parseFloat(process.argv[5]||'15'),FPS=30;
const wf=path.join(P,'words.json');const words=fs.existsSync(wf)?fs.readFileSync(wf,'utf8'):'[]';
fs.writeFileSync(path.join(P,'_comp.html'),fs.readFileSync(path.join(P,'comp.html'),'utf8').replace('__WORDS__',words));
(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1920}});
 pg.on('pageerror',e=>console.log('ERRO',e.message));
 await pg.goto('file://'+path.join(P,'_comp.html'));await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(600);
 fs.mkdirSync(OUT,{recursive:true});const bad=[];
 if(MODE==='stills')for(let k=0;k<14;k++){const t=k===13?DUR-.1:k*DUR/13;await pg.evaluate(t=>seek(t),t);await pg.screenshot({path:`${OUT}/s${String(k).padStart(2,'0')}.png`})}
 const n=Math.round(FPS*DUR);
 for(let i=0;i<n;i++){const t=i/FPS;await pg.evaluate(t=>seek(t),t);
  if(i%3===0)for(const [tx,l,tp,r,bt] of await pg.evaluate(()=>boxes()))if(l<54||r>950||bt>1536||tp<190)bad.push([t.toFixed(2),tx,l,tp,r,bt].join(' | '));
  if(MODE==='all')await pg.screenshot({path:`${OUT}/f${String(i).padStart(4,'0')}.png`})}
 console.log('fora da area segura:',bad.length);bad.slice(0,20).forEach(x=>console.log(x));await b.close();fs.unlinkSync(path.join(P,'_comp.html'))})();
