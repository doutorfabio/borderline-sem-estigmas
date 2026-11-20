from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
W,H=1080,1920; L,R=108,972
SER="/mnt/skills/examples/canvas-design/canvas-fonts/Gloock-Regular.ttf"; HEV="/usr/share/fonts/opentype/inter/Inter-Black.otf"
CREAM=(0xF4,0xE9,0xD5); AMBER=(0xF2,0xB5,0x44)
bg=Image.open("thumb_bg.png").convert("RGB")
a=np.asarray(bg).astype(np.float32)
y=np.arange(H)[:,None,None]; g=np.clip((y-760)/260,0,1)*0.62   # escurece só a parte de baixo, onde fica o texto
bg=Image.fromarray((a*(1-g)).astype(np.uint8)).convert("RGBA")
lines=[("TODO MUNDO VIU A FESTA",SER,CREAM,0.07),("O BORDERLINE",HEV,AMBER,0.0),("JÁ TINHA SE DESPEDIDO",SER,CREAM,0.07)]
def fit(path,txt,tr,maxw,start):
    s=start
    while True:
        f=ImageFont.truetype(path,s); w=sum(f.getlength(c) for c in txt)+tr*s*(len(txt)-1)
        if w<=maxw: return f,w
        s-=2
def draw(d,x,yb,txt,f,tr,fill):
    for c in txt: d.text((x,yb),c,font=f,anchor="ls",fill=fill); x+=f.getlength(c)+tr*f.size
fs=[fit(lines[0][1],lines[0][0],0.07,R-L,80),fit(HEV,"O BORDERLINE",0,R-L,200),fit(SER,lines[2][0],0.07,R-L,80)]
# serifas no mesmo tamanho
s=min(fs[0][0].size,fs[2][0].size); fs[0]=fit(SER,lines[0][0],0.07,R-L,s); fs[2]=fit(SER,lines[2][0],0.07,R-L,s)
txt=Image.new("RGBA",(W,H)); sh=Image.new("RGBA",(W,H)); d=ImageDraw.Draw(txt); ds=ImageDraw.Draw(sh)
bases=[1060,1060+fs[1][0].size*0.80+16,0]; bases[2]=bases[1]+s*1.05+22
boxes=[]
for (t,p,col,tr),(f,w),yb in zip(lines,fs,bases):
    x=(W-w)/2
    draw(ds,x,yb+6,t,f,tr,(0,0,0,200)); draw(d,x,yb,t,f,tr,col+(255,))
    bb=f.getbbox(t,anchor="ls"); boxes.append((x,yb+bb[1],x+w,yb+bb[3]))
out=Image.alpha_composite(Image.alpha_composite(bg,sh.filter(ImageFilter.GaussianBlur(10))),txt).convert("RGB")
out.save("thumb.png")
print([tuple(int(v) for v in b) for b in boxes], "recorte 3:4 = y 240..1680, laterais 108..972")
out.crop((0,240,1080,1680)).resize((540,720)).save("thumb_3x4.png")
