// Utilidades comuns: tudo calculado a partir de t dentro de seek(t).
const NS = 'http://www.w3.org/2000/svg';
function el(tag, attrs, parent){ const e=document.createElementNS(NS,tag); for(const k in attrs) e.setAttribute(k,attrs[k]); parent.appendChild(e); return e; }
function txt(parent, s, x, y, o={}){
  const t = el('text',{x, y, 'text-anchor':o.anchor||'middle', fill:o.fill||'#fff', 'font-size':o.size||40,
    'font-family':o.font||'Lato', 'font-weight':o.weight||700, 'font-style':o.style||'normal'}, parent);
  t.textContent = s; return t;
}
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const prog=(t,a,d)=>clamp((t-a)/d);
const eio=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
const eout=x=>1-Math.pow(1-x,3);
const eback=x=>{const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2);};
const lerp=(a,b,x)=>a+(b-a)*x;
// entrada (sobe e aparece) e saída (sobe e some) de um grupo
function inout(g, t, tin, tout, d=0.35, dy=24){
  const a=eout(prog(t,tin,d)), b=eio(prog(t,tout,0.3));
  const op=a*(1-b);
  g.setAttribute('opacity',op);
  g.setAttribute('transform',`translate(0 ${(1-a)*dy - b*dy})`);
  g.style.display = op<=0.001 ? 'none' : '';
}
function pop(g, t, tin, cx, cy, d=0.4, tout=1e9){
  const a=prog(t,tin,d), s=a<=0?0:eback(a), b=eio(prog(t,tout,0.25));
  const sc=s*(1-b);
  g.setAttribute('transform',`translate(${cx} ${cy}) scale(${Math.max(0,sc)}) translate(${-cx} ${-cy})`);
  g.style.display = sc<=0.001 ? 'none' : '';
}
