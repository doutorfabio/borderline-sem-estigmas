// Motor comum das colagens. Tudo é função pura do tempo t (s).
const $=id=>document.getElementById(id);
const cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const pr=(t,a,d)=>cl((t-a)/d);
const eo=x=>1-Math.pow(1-x,3), eio=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
const back=x=>{const c=1.70158;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
const lerp=(a,b,x)=>a+(b-a)*x;
function pop(el,t,a,rot=0){const p=pr(t,a,.28);el.style.opacity=p>0?1:0;el.style.transform=`rotate(${rot}deg) scale(${p>0?lerp(.55,1,back(p)):0})`}
function draw(path,frac){const L=path.getTotalLength();path.style.strokeDasharray=L;path.style.strokeDashoffset=L*(1-cl(frac))}
function cardIn(t,a){const c=$('card');const ci=eo(pr(t,a,.55));c.style.opacity=cl(ci*1.6);c.style.transform=`translateY(${lerp(40,0,ci)}px) rotate(${lerp(-4,-1.2,ci)}deg) scale(${lerp(.9,1,ci)})`}
function headShrink(t,a){$('head').style.transform=`scale(${lerp(1,.5,eio(pr(t,a,.55)))})`}
function cta(t,a){const ct=$('cta');const cp=pr(t,a,.32);ct.style.opacity=cp>0?1:0;ct.style.transform=`rotate(-1.5deg) scaleX(${lerp(.2,1,eo(cp))}) scale(${1+.012*Math.sin((t-a)*5)*(cp>=1)})`;$('cred').style.opacity=pr(t,a,.3)}
function speaker(t,W,G,HI){ // legenda de até 3 palavras + ícone que pulsa quando há fala
 let gi=-1;for(let i=0;i<G.length;i++){if(t>=W[G[i][0]][1]-.04)gi=i}
 let html='',speaking=false;
 if(gi>=0){const[g0,g1]=G[gi];const endT=(gi+1<G.length?W[G[gi+1][0]][1]-.04:W[g1][2]+.5);
  if(t<Math.min(endT,W[g1][2]+.6))for(let k=g0;k<=g1;k++)html+=`<span class="txt ${HI.has(k)?'hi':''}" style="opacity:${t>=W[k][1]-.04?1:.28}">${W[k][0]}</span>`}
 for(const w of W)if(t>=w[1]&&t<=w[2]+.06)speaking=true;
 $('cap').innerHTML=html;
 const rp=speaking?(.5+.5*Math.sin(t*22)):0;$('ring').style.transform=`scale(${1+.07*rp})`;$('ring').style.opacity=speaking?.9:0;
 $('ico').style.transform=`rotate(${Math.sin(t*1.7)*1.5-2}deg)`}
window.boxes=function(){const out=[];document.querySelectorAll('.txt').forEach(e=>{let o=1,n=e;while(n&&n!==document.body){o*=parseFloat(getComputedStyle(n).opacity);n=n.parentElement}if(o<.05)return;const r=e.getBoundingClientRect();if(r.width<2)return;out.push([e.textContent.slice(0,24),Math.round(r.left),Math.round(r.top),Math.round(r.right),Math.round(r.bottom)])});return out};
const GRAIN='<svg id="grain" class="abs" width="1080" height="1920"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="7"/><feColorMatrix values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 .5 0"/></filter><rect width="100%" height="100%" filter="url(#n)"/></svg>';
const FOOTER='<div id="cta" class="abs txt"></div><div id="ico" class="abs"><div id="ring"></div><img src="../colagem-base/icone-fabio.png"></div><div id="cap" class="abs"></div><div id="cred" class="abs txt">Dr. Fabio Schmidt, médico, pós-graduado em psiquiatria.<br>Conteúdo educativo.</div>';
