import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H=1080,1920
def font(sz,wt=800):
    f=ImageFont.truetype("fonts/Montserrat.ttf",sz); f.set_variation_by_axes([wt]); return f
def make(src,out,lines,cy,shade):
    im=Image.open(src).convert("RGB")
    # leve escurecimento atrás do texto
    g=np.zeros((H,W),np.float32); y0,y1,k=shade
    yy=np.arange(H)
    a=np.clip(np.minimum((yy-y0)/160,(y1-yy)/160),0,1)*k
    arr=np.array(im).astype(np.float32)*(1-a[:,None,None]); im=Image.fromarray(arr.astype(np.uint8))
    lay=Image.new("RGBA",(W,H),(0,0,0,0)); sh=Image.new("RGBA",(W,H),(0,0,0,0))
    d=ImageDraw.Draw(lay); ds=ImageDraw.Draw(sh)
    hs=[]; 
    for t,sz,wt,band in lines:
        f=font(sz,wt); b=f.getbbox(t.replace("[","").replace("]","")); hs.append((f,b))
    gap=26; total=sum(b[3]-b[1] for f,b in hs)+gap*(len(lines)-1); y=cy-total/2
    for (t,sz,wt,band),(f,b) in zip(lines,hs):
        plain=t.replace("[","").replace("]",""); w=f.getlength(plain); x=(W-w)/2
        if "[" in t:
            pre,rest=t.split("["); word,post=rest.split("]")
            xw=x+f.getlength(pre); ww=f.getlength(word)
            d.rounded_rectangle([xw-14,y-10,xw+ww+14,y+(b[3]-b[1])+12],8,fill=(204,0,0,255))
        ds.text((x+3,y-b[1]+5),plain,font=f,fill=(0,0,0,200))
        d.text((x,y-b[1]),plain,font=f,fill=(242,234,219,255) if True else None)
        y+=(b[3]-b[1])+gap
    sh=sh.filter(ImageFilter.GaussianBlur(7))
    im=im.convert("RGBA"); im.alpha_composite(sh); im.alpha_composite(lay)
    a=np.array(lay)[:,:,3]; ys,xs=np.where(a>8)
    print(out,"x",xs.min(),xs.max(),"y",ys.min(),ys.max(),"| margens lat %.1f%% %.1f%%"%(xs.min()/W*100,(W-xs.max())/W*100),"| altura %.1f%% a %.1f%%"%(ys.min()/H*100,ys.max()/H*100))
    assert xs.min()>=108 and xs.max()<=W-108 and ys.min()>=240 and ys.max()<=1680
    im.convert("RGB").save(out,quality=95)
    im.convert("RGB").crop((0,240,W,1680)).resize((405,540)).save(out.replace(".jpg","_grid.jpg"))
make("tc_18.5.png","capa-churrasco.jpg",[("QUEM TEM",70,800,0),("BORDERLINE",122,900,0),("PODE ESTAR NA SUA MESA,",54,800,0),("[OUVINDO] TUDO.",84,900,0)],1330,(1020,1700,0.55))
make("tb_13.6.png","capa-bar.jpg",[("BORDERLINE",122,900,0),("TERMINA [ANTES]",84,900,0),("DE SER DEIXADO",84,900,0)],1340,(1080,1700,0.45))
