import json,random,math
from PIL import Image,ImageDraw,ImageFont,ImageFilter
F='/workspace/Novo/.claude/skills/ui-styling/canvas-fonts/'
BIG=F+'BigShoulders-Bold.ttf'; SER=F+'InstrumentSerif-Italic.ttf'; SANS=F+'InstrumentSans-Bold.ttf'
W,H=1080,1920; RED=(204,0,0); INK=(18,16,14); PAPER=(239,230,210)
random.seed(7)
def torn(w,h,j=7):
    pts=[]
    for x in range(0,w+1,14): pts.append((x,random.randint(0,j)))
    for x in range(w,-1,-14): pts.append((x,h-random.randint(0,j)))
    return pts
def label(lines,size,center,rot=0,pad=(44,26),fill=PAPER,gap=8):
    f=ImageFont.truetype(BIG,size)
    ws=[f.getbbox(t)[2]-f.getbbox(t)[0] for t,_ in lines]; lh=f.getbbox('ÂG')[3]-f.getbbox('ÂG')[1]
    w=max(ws)+2*pad[0]; h=len(lines)*lh+(len(lines)-1)*gap+2*pad[1]+10
    im=Image.new('RGBA',(w+40,h+40),(0,0,0,0)); d=ImageDraw.Draw(im)
    sh=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(sh).polygon([(x+26,y+28) for x,y in torn(w,h)],fill=(0,0,0,90))
    im=Image.alpha_composite(im,sh.filter(ImageFilter.GaussianBlur(8))); d=ImageDraw.Draw(im)
    d.polygon([(x+20,y+20) for x,y in torn(w,h)],fill=fill+(255,))
    y=20+pad[1]
    for (t,c),tw in zip(lines,ws):
        bb=f.getbbox(t); d.text((20+(w-tw)//2-bb[0],y-bb[1]),t,font=f,fill=c); y+=lh+gap
    im=im.rotate(rot,resample=Image.BICUBIC,expand=True)
    can=Image.new('RGBA',(W,H),(0,0,0,0)); can.paste(im,(int(center[0]-im.width/2),int(center[1]-im.height/2)),im); return can
def save(im,n): im.save(n+'.png')
save(label([('POR QUE O BORDERLINE',96,) and ('POR QUE O BORDERLINE',INK),('SE DEFENDE?',RED)],118,(540,300),rot=-1.5),'t_title')
save(label([('ME MACHUCOU',INK)],112,(560,830),rot=1.2),'t_machucou')
save(label([('PESSOA RUIM',RED)],124,(520,1215),rot=-1.8),'t_ruim')
save(label([('JULGAMENTO',INK)],132,(525,955),rot=0,fill=(232,220,196)),'t_julgamento')
# cover patch for AI gibberish label (top-left of hands scene)
p=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(p)
d.polygon([(x+10,y+40) for x,y in torn(470,360,9)],fill=(231,216,190,255)); save(p,'t_patch')
# stamp text inside rectangle x155-919 y756-1125
f=ImageFont.truetype(BIG,150); can=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(can)
for i,t in enumerate(['EU ENTENDI','QUE DOEU.']):
    bb=f.getbbox(t); tw=bb[2]-bb[0]; d.text((537-tw//2-bb[0],790+i*160-bb[1]),t,font=f,fill=(178,24,28))
# stamp texture: knock out random specks
import numpy as np
a=np.array(can); m=a[:,:,3]>0; noise=np.random.RandomState(3).rand(*m.shape)<0.07; a[m&noise,3]=0
save(Image.fromarray(a),'t_stamp')
# CTA
f=ImageFont.truetype(SER,64); can=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(can)
for i,t in enumerate(['Manda pra quem você magoou','e ainda não conseguiu','pedir desculpa.']):
    bb=f.getbbox(t); tw=bb[2]-bb[0]; d.text((540-tw//2-bb[0],1230+i*80-bb[1]),t,font=f,fill=INK)
save(can,'t_cta')
# captions
tl=json.load(open('tl.json')); words=tl['words']; OFF=0.10
phr=[[0,1,2],[3,4,5],[6,7],[8,9,10],[11],[12,13],[14,15],[16,17,18],[19,20,21],[22,23],[24,25],[26,27],[28,29,30],[31,32],[33,34],[35,36],[37,38],[39,40],[41,42]]
f=ImageFont.truetype(SANS,58); caps=[]
for k,g in enumerate(phr):
    t=' '.join(words[i]['w'] for i in g)
    s=words[g[0]]['s']+OFF; e=(words[phr[k+1][0]]['s']+OFF) if k+1<len(phr) else words[g[-1]]['e']+OFF+0.3
    e=min(e,words[g[-1]]['e']+OFF+0.45)
    can=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(can)
    bb=f.getbbox(t); tw=bb[2]-bb[0]
    d.text((540-tw//2-bb[0],1450-bb[1]),t,font=f,fill=(255,255,255),stroke_width=5,stroke_fill=(20,16,14))
    n=f'c{k:02d}'; save(can,n); caps.append((n,round(s,2),round(e,2)))
json.dump(caps,open('caps.json','w'))
print(caps)
