# Converts each engraving into an ink-coverage map (alpha) so it sits on the piece's own paper.
# Optional red map for the painted crab (remapped to the single accent, brick red).
import sys, os, numpy as np
from PIL import Image
from scipy import ndimage as ndi
RAW, OUT, PREV = sys.argv[1], sys.argv[2], sys.argv[3]
PAPER=np.array([0xEF,0xE5,0xD0],float); INK=np.array([0x1A,0x1A,0x1A],float); RED=np.array([0x8B,0x1E,0x1A],float)
def load(name):
    return np.asarray(Image.open(os.path.join(RAW,name)).convert('RGB')).astype(np.float32)
def paper_of(a):
    lum=a@np.array([.299,.587,.114],np.float32)
    thr=np.percentile(lum,70)
    return np.median(a[lum>=thr].reshape(-1,3),axis=0)
def maps(a, red=False):
    P=paper_of(a)
    T=np.clip(a/P,0,1)
    lum=T@np.array([.299,.587,.114],np.float32)
    d=1-lum
    ak=np.clip((d-0.055)/(0.80-0.055),0,1)
    ak=ak**0.9
    s=np.zeros_like(ak)
    if red:
        s=np.clip((T[...,0]-T[...,1]-0.085)/0.14,0,1)
        s=ndi.gaussian_filter(s,1.2)
        ar=np.clip((d-0.04)/0.60,0,1)**0.8
        a_out=ak*(1-s)+ar*s
    else:
        a_out=ak
    # paper far from the drawing becomes fully transparent (no visible image rectangle on the page)
    core=ndi.gaussian_filter(a_out,5)>0.05
    core=ndi.binary_dilation(core,iterations=22)
    a_out=a_out*ndi.gaussian_filter(core.astype(np.float32),12)
    # image borders that are plain paper fade to nothing (scanner edge residue); borders the drawing crosses stay
    D=28; h,w=a_out.shape; ramp=np.clip(np.arange(D)/D,0,1)**1.5
    sstep=lambda x:np.clip((x-0.03)/0.07,0,1)
    for edge in range(4):
        v=np.rot90(a_out,edge)                       # view with the edge on top
        prof=ndi.gaussian_filter1d(v[:D].mean(axis=0),30)
        wgt=sstep(prof)[None,:]
        v[:D]*=(ramp[:,None]*(1-wgt)+wgt)
    return a_out, s, P
def preview(a_out,s,path,scale=None):
    col=INK[None,None,:]*(1-s[...,None])+RED[None,None,:]*s[...,None]
    out=PAPER[None,None,:]*(1-a_out[...,None])+col*a_out[...,None]
    im=Image.fromarray(np.clip(out,0,255).astype(np.uint8))
    if scale: im=im.resize((int(im.width*scale),int(im.height*scale)),Image.LANCZOS)
    im.save(path,quality=92)
def save_gray(arr,path,q=90,size=None):
    im=Image.fromarray(np.clip(arr*255+0.5,0,255).astype(np.uint8),'L')
    if size: im=im.resize(size,Image.LANCZOS)
    im.save(path,'WEBP',quality=q,method=6)
    return os.path.getsize(path)
big=[('A01_crab',True,1080),('A02_shell',False,0),('A03_dinner',False,1080),('A04_vanity',False,1188),('A05_door',False,1080),('A06_mirror',False,1242),('A07_cup',True,1210)]
for name,red,tw in big:
    a=load(name+'.png'); ao,s,P=maps(a,red)
    h,w=ao.shape
    if name=='A02_shell':
        # keep only the shell, small (it is drawn at about 190 px)
        m=ndi.gaussian_filter(ao,4)>0.05; lab,nn=ndi.label(m); sz=ndi.sum(m,lab,range(1,nn+1)); m=lab==(1+int(np.argmax(sz))); ys,xs=np.where(m); y0,y1,x0,x1=max(0,ys.min()-30),min(h,ys.max()+30),max(0,xs.min()-30),min(w,xs.max()+30); print('A02 bbox',x0/w,y0/h,x1/w,y1/h)
        ao=ao[y0:y1,x0:x1]; hh,ww=ao.shape; size=(300,int(round(300*hh/ww)))
    else:
        size=(tw,int(round(tw*h/w)))
    n=save_gray(ao,os.path.join(OUT,name+'_a.webp'),q=86,size=size)
    msg=f'{name} paper={P.round()} size={size} a.webp={n//1024}KB'
    if red:
        n2=save_gray(s,os.path.join(OUT,name+'_s.webp'),q=80,size=(size[0]//2,size[1]//2)); msg+=f' s.webp={n2//1024}KB'
    if name!='A02_shell': preview(ao,s,os.path.join(PREV,name+'.jpg'),scale=0.5)
    print(msg)
icons=['I01_frog','I02_shell','I03_key','I04_tear','I05_pearls','I06_hands']
meta={}
for name in icons:
    a=load(name+'.png'); ao,s,P=maps(a,False)
    # kill isolated paper specks, then crop to the ink
    m=ndi.gaussian_filter(ao,3)>0.06
    lab,n=ndi.label(m)
    if n>1:
        sizes=ndi.sum(m,lab,range(1,n+1)); keep=[i+1 for i,sz in enumerate(sizes) if sz>0.002*m.size]
        m=np.isin(lab,keep)
    m=ndi.binary_dilation(m,iterations=10)
    ao=ao*ndi.gaussian_filter(m.astype(np.float32),4)
    ys,xs=np.where(m); y0,y1,x0,x1=ys.min(),ys.max(),xs.min(),xs.max()
    cy,cx=(y0+y1)//2,(x0+x1)//2; half=int(max(y1-y0,x1-x0)/2*1.10)
    crop=ao[max(0,cy-half):cy+half, max(0,cx-half):cx+half]
    S=640
    n=save_gray(crop,os.path.join(OUT,name+'_a.webp'),q=90,size=(S,S))
    # silhouette for the morph: solid shape, small holes filled, big holes kept
    c=np.asarray(Image.fromarray((crop*255).astype(np.uint8)).resize((320,320),Image.LANCZOS)).astype(np.float32)/255
    g=ndi.gaussian_filter(c,1.3)
    sil=ndi.binary_closing(g>0.10,iterations=2)
    filled=ndi.binary_fill_holes(sil)
    hl,hn=ndi.label(filled&~sil)
    g2=ndi.gaussian_filter(c,2.5)
    for i in range(1,hn+1):
        reg=hl==i
        # a hole stays open only if it is real paper and big enough to read
        if not (reg.sum()>0.0022*320*320 and g2[reg].mean()<0.035): sil|=reg
    lab,n2=ndi.label(sil)
    if n2>1:
        sizes=ndi.sum(sil,lab,range(1,n2+1)); sil=lab==(1+int(np.argmax(sizes)))
    silf=ndi.gaussian_filter(sil.astype(np.float32),1.0)
    Image.fromarray((silf*255).astype(np.uint8),'L').save(os.path.join(OUT,name+'_m.png'),optimize=True)
    preview(crop,np.zeros_like(crop),os.path.join(PREV,name+'.jpg'),scale=0.5)
    Image.fromarray((255-silf*255).astype(np.uint8),'L').save(os.path.join(PREV,name+'_sil.png'))
    print(f'{name} a.webp={n//1024}KB sil={os.path.getsize(os.path.join(OUT,name+"_m.png"))//1024}KB crop={crop.shape}')
