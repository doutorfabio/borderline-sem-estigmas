const ot=require('opentype.js'),fs=require('fs');
const C=ot.parse(fs.readFileSync('node_modules/@fontsource/caveat/files/caveat-latin-700-normal.woff').buffer);
const out={};
for(const [k,t,s] of [['faz','faz quanto tempo?',84],['nem','nem concordar',96],['voce','você começa aqui',78]]){
  const glyphs=[];let x=0;
  const gs=C.stringToGlyphs(t);
  gs.forEach((g,i)=>{const p=g.getPath(x,0,s);const f=v=>(Math.round(v*10)/10).toString();const d=p.commands.map(c=>c.type==='Z'?'Z':c.type==='M'||c.type==='L'?c.type+f(c.x)+' '+f(c.y):c.type==='Q'?'Q'+f(c.x1)+' '+f(c.y1)+' '+f(c.x)+' '+f(c.y):'C'+f(c.x1)+' '+f(c.y1)+' '+f(c.x2)+' '+f(c.y2)+' '+f(c.x)+' '+f(c.y)).join(' ');if(d)glyphs.push(d);
    x+=g.advanceWidth*s/C.unitsPerEm; if(i<gs.length-1)x+=C.getKerningValue(g,gs[i+1])*s/C.unitsPerEm;});
  const bb=C.getPath(t,0,0,s).getBoundingBox();
  out[k]={glyphs,w:Math.ceil(x),bb:[bb.x1,bb.y1,bb.x2,bb.y2].map(Math.round)};
  console.log(k,Math.ceil(x),out[k].bb, glyphs.length);
}
fs.writeFileSync('hand.json',JSON.stringify(out));
