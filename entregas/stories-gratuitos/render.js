const {chromium}=require('playwright');const fs=require('fs');
const base=fs.readFileSync(__dirname+'/story.html','utf8');
const S=[
 {id:'1-respira-ja',seed:7,vars:'--base:#F3EFE8;--ink:#17312d;--a1:#8fcfc0;--a2:#c7e6dc',
  icon:'<path d="M6 34 C 14 22, 22 22, 30 32 S 46 44, 58 28"/>',
  k:'APP GRATUITO',n:'RESPIRA JÁ!',d:'O peito apertou e a cabeça disparou.<br>Abra, escolha a situação<br>e respire junto.',f:''},
 {id:'2-radar-de-crise',seed:21,vars:'--base:#F4EEE6;--ink:#3a1f14;--a1:#e9b48f;--a2:#f2d6bf',
  icon:'<circle cx="32" cy="32" r="5"/><circle cx="32" cy="32" r="15" opacity=".7"/><circle cx="32" cy="32" r="26" opacity=".4"/>',
  k:'FERRAMENTA GRATUITA',n:'RADAR DE CRISE',d:'A crise começou e falta a frase certa.<br>Escolha o que aconteceu<br>e copie a resposta.',f:'Risco imediato: ligue 188 ou 192.'},
 {id:'3-tpb-no-caps',seed:44,vars:'--base:#EEF0F2;--ink:#232a36;--a1:#9fb0c8;--a2:#cfd8e4',
  icon:'<path d="M32 18 C 25 13, 14 13, 8 15 V 49 C 14 47, 25 47, 32 52 C 39 47, 50 47, 56 49 V 15 C 50 13, 39 13, 32 18 Z"/><path d="M32 18 V 52"/>',
  k:'LIVRO GRATUITO',n:'TPB NO CAPS',d:'Pensou em buscar o CAPS<br>por causa do borderline?<br>Leia antes de ir.',f:''},
];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:720,height:1280},deviceScaleFactor:2});
for(const s of S){let h=base.replace('SEED',s.seed).replace('ICON',s.icon).replace('KICKER',s.k).replace('NOME',s.n).replace('DESC',s.d).replace('FOOT',s.f).replace('<body>','<body style="'+s.vars+'">');
await p.setContent(h,{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
const r=await p.evaluate(()=>[...document.querySelectorAll('.k,.n,.d,.f,.ico')].map(e=>{const b=e.getBoundingClientRect();return [e.className.baseVal??e.className,Math.round(b.left),Math.round(b.right),Math.round(b.top),Math.round(b.bottom)]}));
const w=await p.evaluate(()=>{const n=document.querySelector('.n');const rg=document.createRange();rg.selectNodeContents(n);const b=rg.getBoundingClientRect();return [Math.round(b.left),Math.round(b.right)]});
console.log(s.id,JSON.stringify(r),'nome',w, await p.evaluate(()=>document.fonts.check("600 58px 'Cormorant Garamond'")));
await p.screenshot({path:__dirname+'/story-'+s.id+'.png'});}
await b.close();})();
