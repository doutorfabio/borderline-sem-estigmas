import sys,os,numpy as np
sys.path.insert(0,os.path.dirname(__file__))
import htfast
from PIL import Image, ImageOps, ImageFilter
from multiprocessing import Pool
clip,a,b,ref=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])
src='src/%s_png'%clip; dst='src/%s_ht'%clip; os.makedirs(dst,exist_ok=True)
r=np.asarray(ImageOps.grayscale(Image.open('%s/%04d.png'%(src,ref))),np.float32)
lo,hi=np.percentile(r,2),np.percentile(r,98)
def ht(i):
    im=Image.open('%s/%04d.png'%(src,i)).convert('RGB')
    g=np.asarray(ImageOps.grayscale(im).filter(ImageFilter.GaussianBlur(1.2)),np.float32)
    g=np.clip((g-lo)/(hi-lo),0,1)**0.75
    dark=1-g[htfast.cyi,htfast.cxi]
    rr=htfast.CELL*0.64*np.power(np.clip(dark,0,1),0.85)
    cov=np.clip(rr-htfast.d+0.5,0,1); cov[dark<0.04]=0
    out=htfast.YEL*(1-cov[...,None])+htfast.INK*cov[...,None]
    Image.fromarray(out.astype(np.uint8)).resize((1080,1920),Image.LANCZOS).save('%s/%04d.jpg'%(dst,i),quality=92)
with Pool(4) as p: p.map(ht,range(a,b+1))
