const fs=require('fs');
const H=JSON.parse(fs.readFileSync('hand.json'));
const hand=(id,k,x,y,color)=>`<svg class="hand t" id="${id}" style="left:${x}px;top:${y-70}px" width="${H[k].w+20}" height="100" viewBox="0 -70 ${H[k].w+20} 100">`+
  H[k].glyphs.map(d=>`<path class="g" pathLength="1" d="${d}" stroke="${color}" fill="${color}"/>`).join('')+`</svg>`;
const sq=[1,2,3,4,5,6,7].map(n=>{const r=n<=4?0:1;const i=n<=4?n-1:n-5;const x=r?199+i*198:100+i*198;const y=r?760:560;
  return `<div class="sq" id="sq${n}" style="left:${x}px;top:${y}px"><span class="t">${n}</span></div>`}).join('');
const html=`<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<title>Protocolo 7 Dias</title>
<script src="assets/js/gsap.min.js"></script>
<style>
@font-face{font-family:"Anton";src:url("assets/fonts/anton-latin-400-normal.woff2") format("woff2");font-weight:400;}
@font-face{font-family:"Montserrat";src:url("assets/fonts/montserrat-latin-600-normal.woff2") format("woff2");font-weight:600;}
@font-face{font-family:"Caveat";src:url("assets/fonts/caveat-latin-700-normal.woff2") format("woff2");font-weight:700;}
:root{--paper:#F2EADB;--ink:#0D0D0D;--red:#CC0000;--navy:#1B2A4A;}
*{margin:0;padding:0;box-sizing:border-box;}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--ink);}
#root{position:relative;width:100%;height:100%;overflow:hidden;}
.scene{position:absolute;inset:0;overflow:hidden;}
.bg{position:absolute;inset:0;}
.light .bg{background:var(--paper);}
.dark .bg{background:var(--ink);}
.grain{position:absolute;inset:0;opacity:.07;pointer-events:none;}
.big{position:absolute;left:72px;font-family:"Anton";color:var(--ink);text-transform:none;}
.dark .big{color:var(--paper);}
.ln{display:block;width:max-content;line-height:1;white-space:nowrap;transform-origin:0% 100%;}
.hand{position:absolute;overflow:visible;}
.hand .g{stroke-width:2.6;stroke-linejoin:round;stroke-linecap:round;stroke-dasharray:1;stroke-dashoffset:1;fill-opacity:0;}
.mark{position:absolute;left:0;top:0;overflow:visible;}
.mark path{fill:none;stroke-linecap:round;stroke-linejoin:round;}
.sq{position:absolute;width:170px;height:170px;background:var(--ink);border-radius:6px;display:flex;align-items:center;justify-content:center;transform-origin:50% 100%;}
.sq span{font-family:"Anton";font-size:112px;line-height:1;color:var(--paper);}
.card{position:absolute;left:0;right:0;text-align:center;color:var(--paper);white-space:nowrap;}
.card span{display:inline-block;}
.vid{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;}
.mont{font-family:"Montserrat";font-weight:600;}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="15" data-width="1080" data-height="1920">
<svg width="0" height="0" style="position:absolute"><filter id="grainf" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="2" seed="7" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter></svg>

<section id="s12" class="scene light clip" data-start="0" data-duration="3.8" data-track-index="0">
  <div class="bg"></div>
  <svg class="grain" width="1080" height="1920"><rect width="1080" height="1920" filter="url(#grainf)"/></svg>
  <div class="big" id="b1" style="top:610px">
    <span class="ln t" id="b1a" style="font-size:104px">ESPERANDO</span>
    <span class="ln t" id="b1b" style="margin-top:6px"><span style="font-size:60px;margin-right:14px">QUEM TEM</span><span style="font-size:134px;color:var(--red)">BORDERLINE</span></span>
    <span class="ln t" id="b1c" style="font-size:104px;margin-top:6px">ACEITAR AJUDA?</span>
  </div>
  <div class="big" id="b2" style="top:740px">
    <span class="ln t" id="b2a" style="font-size:182px">E AS CRISES</span>
    <span class="ln t" id="b2b" style="font-size:182px">CONTINUAM.</span>
  </div>
  <svg class="mark" width="1080" height="1920"><g transform="translate(0,180)"><path id="arrow1" pathLength="1" stroke="var(--navy)" stroke-width="7" d="M 612 342 C 640 392, 628 446, 572 474"/><path id="arrow1h" pathLength="1" stroke="var(--navy)" stroke-width="7" d="M 600 486 L 571 475 L 586 449"/></g></svg>
  ${hand('hand1','faz',380,480,'var(--navy)')}
</section>

<section id="s34" class="scene dark clip" data-start="3.8" data-duration="5.2" data-track-index="0">
  <div class="bg"></div>
  <div class="big" id="b3" style="top:780px">
    <span class="ln t" id="b3a" style="font-size:104px">O PROTOCOLO 7 DIAS</span>
    <span class="ln t" id="b3b" style="font-size:104px;margin-top:4px">É PRA QUEM CONVIVE.</span>
  </div>
  <div class="big" id="b4" style="top:620px">
    <span class="ln t" id="b4a" style="font-size:99px">QUEM TEM BORDERLINE</span>
    <span class="ln t" id="b4b" style="font-size:99px;margin-top:4px">NÃO PRECISA ASSISTIR.</span>
  </div>
  ${hand('hand2','nem',84,960,'var(--red)')}
  <svg class="mark" width="1080" height="1920"><path id="ul1" pathLength="1" stroke="var(--red)" stroke-width="8" d="M 88 1000 C 200 994, 380 1003, 586 992"/><path id="ul2" pathLength="1" stroke="var(--red)" stroke-width="8" d="M 104 1026 C 260 1019, 420 1028, 572 1020"/></svg>
</section>

<section id="s5" class="scene light clip" data-start="9.0" data-duration="2.0" data-track-index="0">
  <div class="bg"></div>
  <svg class="grain" width="1080" height="1920"><rect width="1080" height="1920" filter="url(#grainf)"/></svg>
  ${sq}
  <div class="big" id="b5" style="top:1010px">
    <span class="ln t" id="b5a" style="font-size:290px">7 DIAS.</span>
    <span class="ln t" id="b5b" style="font-size:81px;margin-top:-6px">UM PROCEDIMENTO POR DIA.</span>
  </div>
  <svg class="mark" width="1080" height="1920"><path id="circ" pathLength="1" stroke="var(--red)" stroke-width="8" d="M 300 600 C 292 548, 230 522, 172 526 C 102 531, 62 584, 66 648 C 70 716, 122 760, 188 758 C 258 756, 312 712, 306 640 C 304 610, 290 586, 262 566"/></svg>
  ${hand('hand3','voce',330,520,'var(--red)')}
</section>

<section id="s6" class="scene dark clip" data-start="11.0" data-duration="4.0" data-track-index="0">
  <div class="bg"></div>
  <div class="card" style="top:640px"><span class="t" id="c1" style="font-family:Anton;font-size:116px;line-height:1">PROTOCOLO 7 DIAS</span></div>
  <svg class="mark" width="1080" height="1920"><path id="ul3" pathLength="1" stroke="var(--red)" stroke-width="8" d="M 166 796 C 330 788, 620 796, 914 786"/></svg>
  <div class="card mont" style="top:826px"><span class="t" id="c2" style="font-size:42px;line-height:1.2">Para quem convive com borderline</span></div>
  <div class="card mont" style="top:938px"><span class="t" id="c7" style="font-size:40px;line-height:1.2">Cupom <span style="color:var(--red)">BLACK26</span>: 25% de desconto</span></div>
  <div class="card" style="top:1000px"><span class="t" id="c8" style="font-family:Anton;font-size:100px;line-height:1">R$ 164,25 até 25/11</span></div>
  <div class="card mont" style="top:1140px"><span class="t" id="c4" style="font-size:42px;line-height:1.2">Garantia de 7 dias</span></div>
  <div class="card mont" style="top:1398px;opacity:.78"><span class="t" id="c5" style="font-size:24px;line-height:1.4">Conteúdo educativo. Não substitui avaliação nem tratamento.</span></div>
  <div class="card mont" style="top:1434px;opacity:.78"><span class="t" id="c6" style="font-size:24px;line-height:1.4">Dr. Fabio Schmidt, médico, CRM-SP 183549</span></div>
</section>
<video id="vA" class="clip vid" src="assets/cozinha-1080.mp4" data-start="3.8" data-duration="1.8" data-media-start="3.4" data-track-index="1" muted playsinline></video>
<video id="vB" class="clip vid" src="assets/cozinha-1080.mp4" data-start="11.0" data-duration="1.6" data-media-start="6.0" data-track-index="1" muted playsinline></video>
</div>
<script>
const tl = gsap.timeline({ paused: true });
const S = (sel,t,stg=0.07)=>{ // slam in with stretch, land with squash, settle
  tl.fromTo(sel,{opacity:0,y:-70,scaleY:1.35,scaleX:0.9},{opacity:1,y:0,scaleY:0.86,scaleX:1.015,duration:0.2,ease:"power3.in",stagger:stg},t);
  tl.to(sel,{scaleY:1,scaleX:1,duration:0.34,ease:"elastic.out(1,0.45)",stagger:stg},t+0.2);
};
const X = (sel,t)=> tl.to(sel,{opacity:0,scaleY:0,duration:0.13,ease:"power3.in",stagger:0.03,transformOrigin:"0% 0%"},t);
const write=(id,t,dur)=>{const g=document.querySelectorAll('#'+id+' .g');const st=dur/g.length;
  g.forEach((p,i)=>{tl.fromTo(p,{strokeDashoffset:1,fillOpacity:0},{strokeDashoffset:0,duration:st*2.2,ease:"none"},t+i*st);
    tl.to(p,{fillOpacity:1,duration:st*1.6,ease:"power1.out"},t+i*st+st*1.2);});};
const draw=(sel,t,d,ease="power2.inOut")=>tl.fromTo(sel,{strokeDasharray:1,strokeDashoffset:1},{strokeDashoffset:0,duration:d,ease},t);

// Cena 1: primeiro quadro já com ESPERANDO visível
tl.fromTo("#b1a",{opacity:1,scaleY:1.06,scaleX:0.98},{scaleY:1,scaleX:1,duration:0.3,ease:"elastic.out(1,0.5)"},0);
S(["#b1b","#b1c"],0.08,0.1);
draw("#arrow1",1.3,0.26,"power2.out"); draw("#arrow1h",1.52,0.1,"none");
write("hand1",1.5,0.62);
// Cena 2
X(["#b1a","#b1b","#b1c"],2.2);
tl.set("#b2a,#b2b",{opacity:0},0);
S(["#b2a","#b2b"],2.36,0.08);
// Cena 3
tl.set("#b3a,#b3b",{opacity:0},0);
S(["#b3a","#b3b"],5.6,0.08);
// Cena 4
X(["#b3a","#b3b"],7.0);
tl.set("#b4a,#b4b",{opacity:0},0);
S(["#b4a","#b4b"],7.16,0.08);
write("hand2",7.6,0.6);
draw("#ul1",8.24,0.15); draw("#ul2",8.42,0.14);
// Cena 5: quadrados caem com gravidade, quicam pouco
const rot=[-7,5,-4,8,-6,4,-5];
for(let n=1;n<=7;n++){const s="#sq"+n,t=9.02+(n-1)*0.075,off=n<=4?-370:-560;const T=n<=4?0.36:0.44;
  tl.fromTo(s,{y:off,opacity:0,rotation:rot[n-1],scaleY:1.12,scaleX:0.93},{opacity:1,duration:0.05,ease:"none"},t);
  tl.to(s,{y:0,rotation:0,duration:T,ease:"power2.in"},t);
  tl.to(s,{scaleY:1.12,scaleX:0.93,duration:T,ease:"none"},t);
  tl.to(s,{scaleY:0.8,scaleX:1.16,duration:0.06,ease:"power2.out"},t+T);
  tl.to(s,{y:-26,scaleY:1.05,scaleX:0.97,duration:0.15,ease:"power2.out"},t+T+0.06);
  tl.to(s,{y:0,scaleY:1,scaleX:1,duration:0.15,ease:"power2.in"},t+T+0.21);
  tl.to(s,{scaleY:0.94,scaleX:1.04,duration:0.05,ease:"power1.out"},t+T+0.36);
  tl.to(s,{scaleY:1,scaleX:1,duration:0.2,ease:"elastic.out(1,0.5)"},t+T+0.41);
}
tl.set("#b5a,#b5b",{opacity:0},0);
S(["#b5a","#b5b"],9.22,0.1);
draw("#circ",10.1,0.32,"power1.inOut");
write("hand3",10.4,0.5);
// Cena 6: cartão final, tudo parado a partir de 13,5 s
tl.set("#c1,#c2,#c4,#c5,#c6,#c7,#c8",{opacity:0},0);
S("#c1",12.62,0);
draw("#ul3",13.0,0.24,"power2.out");
tl.fromTo(["#c2","#c7"],{opacity:0,y:28},{opacity:1,y:0,duration:0.42,ease:"power3.out",stagger:0.1},12.8);
S("#c8",12.95,0);
tl.fromTo(["#c4"],{opacity:0,y:28},{opacity:1,y:0,duration:0.38,ease:"power3.out",stagger:0.12},13.08);
tl.fromTo(["#c5","#c6"],{opacity:0},{opacity:1,duration:0.35,ease:"power1.out"},13.1);
tl.set({},{},15);
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body>
</html>`;
fs.writeFileSync('/home/user/borderline-sem-estigmas/videos/protocolo-7-dias-motion/index.html',html);
