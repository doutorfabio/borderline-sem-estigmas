import json, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D='/tmp/claude-0/-workspace-borderline-sem-estigmas/26c5b3dd-eefd-58ca-8efd-78a3cdd68057/scratchpad/'
SEMI=D+'fonts/m1.ttf'; XB=D+'fonts/m2.ttf'
W,H=1080,1920; ML=int(W*0.12); MAXW=W-2*ML-28; TOP=int(H*0.12)
def width(t,f): return f.getbbox(t)[2]-f.getbbox(t)[0]
def render(lines,font,color,cy=None,top=None,lh=1.22,shadow=True,align_center=True):
    img=Image.new('RGBA',(W,H),(0,0,0,0))
    asc,desc=font.getmetrics(); step=int(font.size*lh)
    capH=font.getbbox('H')[3]-font.getbbox('H')[1]
    total=step*(len(lines)-1)+capH
    y0 = (cy-total/2) if cy is not None else top
    boxes=[]
    txt=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(txt)
    for i,l in enumerate(lines):
        w=width(l,font); x=(W-w)/2-font.getbbox(l)[0]
        y=y0+i*step-font.getbbox('H')[1]
        d.text((x,y),l,font=font,fill=color)
    if shadow:
        a=txt.split()[3]
        sh=Image.new('RGBA',(W,H),(0,0,0,0)); sh.putalpha(a.point(lambda v:int(v*0.65)))
        sh=sh.filter(ImageFilter.GaussianBlur(5))
        img.alpha_composite(sh,(0,3))
    img.alpha_composite(txt)
    bb=txt.getbbox()
    return img,bb
def split2(text,font):
    words=text.split()
    if width(text,font)<=MAXW and len(words)<=6: return [text]
    best=None
    for k in range(1,len(words)):
        a=' '.join(words[:k]); b=' '.join(words[k:])
        if len(words[:k])==1 or len(words[k:])==1: continue
        m=max(width(a,font),width(b,font))
        if best is None or m<best[0]: best=(m,[a,b])
    return best[1]
out={}
# small captions
cap=ImageFont.truetype(SEMI,54)
chunks=json.load(open(D+'ad/chunks.json'))
for i,c in enumerate(chunks):
    lines=c.get('lines') or split2(c['text'],cap)
    img,bb=render(lines,cap,(255,255,255,255),cy=int(H*0.68))
    p=f'ov/cap{i}.png'; img.save(D+'ad/'+p); out[p]=(bb,lines)
# center emphasis
lines=['FALAR, ABRAÇAR','OU SAIR DO QUARTO']
s=140
while True:
    f=ImageFont.truetype(XB,s)
    if max(width(l,f) for l in lines)<=MAXW: break
    s-=2
img,bb=render(lines,f,(255,255,255,255),cy=H//2,lh=1.18); img.save(D+'ad/ov/centro.png'); out['ov/centro.png']=(bb,lines,s)
# card headline
lines=['CURSO ONLINE PARA','FAMILIARES DE QUEM','TEM BORDERLINE']
STAMP_TOP=532; GAP=44
BC=D+'fonts/bc2.ttf'
s=120
while True:
    f=ImageFont.truetype(BC,s); step=int(s*1.05); capH=f.getbbox('H')[3]-f.getbbox('H')[1]
    if max(width(l,f) for l in lines)<=MAXW and step*2+capH<=STAMP_TOP-GAP-TOP: break
    s-=1
img,bb=render(lines,f,(231,218,200,255),top=TOP+4,lh=1.05,shadow=False)
img.save(D+'ad/ov/titulo.png'); out['ov/titulo.png']=(bb,lines,s)
# CTA
f=ImageFont.truetype(SEMI,46)
img,bb=render(['Toque em Saiba mais'],f,(230,222,210,255),top=1322+58,shadow=False)
img.save(D+'ad/ov/cta.png'); out['ov/cta.png']=(bb,40)
for k,v in out.items(): print(k,v)
