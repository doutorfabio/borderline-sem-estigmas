import numpy as np, sys, os
from PIL import Image, ImageOps, ImageFilter
W,H=1080,1920; SS=2; CELL=13.0
YEL=np.array([247,224,64],np.float32); INK=np.array([22,20,18],np.float32)
a=np.deg2rad(45); ca,sa=np.cos(a),np.sin(a)
ys,xs=np.mgrid[0:H*SS,0:W*SS].astype(np.float32)
xs=(xs+0.5)/SS-W/2; ys=(ys+0.5)/SS-H/2
u=xs*ca+ys*sa; v=-xs*sa+ys*ca
ui=np.round(u/CELL)*CELL; vi=np.round(v/CELL)*CELL
cx=ui*ca-vi*sa+W/2; cy=ui*sa+vi*ca+H/2
d=np.hypot(u-ui,v-vi)
cxi=np.clip(cx.astype(np.int32),0,W-1); cyi=np.clip(cy.astype(np.int32),0,H-1)
del xs,ys,u,v,ui,vi,cx,cy
def ht(im):
    g=ImageOps.autocontrast(ImageOps.grayscale(im),cutoff=2).filter(ImageFilter.GaussianBlur(1.2))
    g=(np.asarray(g,np.float32)/255.0)**0.75
    dark=1-g[cyi,cxi]
    r=CELL*0.64*np.power(np.clip(dark,0,1),0.85)
    cov=np.clip(r-d+0.5,0,1)  # antialias
    cov[dark<0.04]=0
    out=YEL*(1-cov[...,None])+INK*cov[...,None]
    o=Image.fromarray(out.astype(np.uint8)).resize((W,H),Image.LANCZOS)
    return o
if __name__=='__main__':
    src,dst=sys.argv[1],sys.argv[2]; os.makedirs(dst,exist_ok=True)
    files=sorted(os.listdir(src))[int(sys.argv[3])::int(sys.argv[4])]
    for f in files:
        ht(Image.open(os.path.join(src,f)).convert('RGB')).save(os.path.join(dst,f.replace('.png','.jpg')),quality=92)
