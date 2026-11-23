# Prepara as camadas finais (ja no tamanho de tela) a partir dos recortes.
import numpy as np, cv2, json
from PIL import Image, ImageDraw, ImageFont
U='/root/.claude/uploads/ce587ab4-daad-5a2a-9622-f6e319c367bd/'
N=json.load(open('names.json'))
W,H=1080,1920
def rgba(path):
    im=cv2.imread(path,cv2.IMREAD_UNCHANGED).astype(np.float32)/255.0
    im=im[...,[2,1,0,3]]; im[...,:3]*=im[...,3:4]; return im   # premultiplied RGBA
def scale(im,s):
    h,w=im.shape[:2]; return cv2.resize(im,(max(1,round(w*s)),max(1,round(h*s))),interpolation=cv2.INTER_AREA if s<1 else cv2.INTER_CUBIC)
def rot(im,ang):
    h,w=im.shape[:2]; M=cv2.getRotationMatrix2D((w/2,h/2),ang,1.0)
    c,s_=abs(M[0,0]),abs(M[0,1]); nw,nh=int(h*s_+w*c),int(h*c+w*s_)
    M[0,2]+=nw/2-w/2; M[1,2]+=nh/2-h/2
    return cv2.warpAffine(im,M,(nw,nh),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT,borderValue=0),M
L={}; meta={}
# ---- fundo
bg=cv2.imread(U+N['bg']+'-image.png').astype(np.float32)[...,::-1]/255.0
b=cv2.resize(bg,(W,round(bg.shape[0]*W/bg.shape[1])),interpolation=cv2.INTER_AREA); y0=(b.shape[0]-H)//2
L['bg']=np.ascontiguousarray(b[y0:y0+H])
cw,ch=int(bg.shape[1]/1.5),int(bg.shape[0]/1.5); cx,cy=(bg.shape[1]-cw)//2,(bg.shape[0]-ch)//2+120
bc=cv2.resize(bg[cy:cy+ch,cx:cx+cw],(W,round(ch*W/cw)),interpolation=cv2.INTER_CUBIC); L['bg_close']=np.ascontiguousarray(bc[:H])
# ---- chao: tira amarela, borda rasgada para cima
st=rgba('c_strip_yellow.png'); r,_=rot(st,135)
r=scale(r,0.97)
a=r[...,3]; rows=np.where((a>0.5).sum(1)>0)[0]; cols=np.where((a>0.5).sum(0)>0)[0]
print('strip rotated',r.shape,'rows',rows.min(),rows.max(),'cols',cols.min(),cols.max())
cxm=(cols.min()+cols.max())//2; r=r[rows.min()-4:rows.max()+2, cxm-640:cxm+640]; L['floor']=np.ascontiguousarray(r); print('floor',r.shape)
# ---- maos, figura
SH=0.66
L['handC']=scale(rgba('c_handC.png'),SH); meta['handC_pinch']=[940*SH,356*SH]
L['handO']=scale(rgba('c_handO.png'),SH*0.76)
SF=0.87
L['fig']=scale(rgba('c_fig.png'),SF); meta['fig_collar']=[101*SF,84*SF]; meta['fig_feet']=[108*SF,452*SF]; meta['fig_back']=[102*SF,222*SF]
L['figdig']=rgba('c_figdig.png')
# ---- digital: tinta (t) e mancha clara (hull)
d=cv2.imread(U+N['digital']+'-image.png').astype(np.float32)
bgc=np.median(np.concatenate([d[:12].reshape(-1,3),d[-12:].reshape(-1,3)]),0)
t=np.clip((bgc[1]-d[...,1])/(bgc[1]-50.0),0,1)
t=np.clip((t-0.12)/0.75,0,1)
ys,xs=np.where(t>0.5); x0,y0,x1,y1=xs.min()-20,ys.min()-20,xs.max()+20,ys.max()+20
t=t[y0:y1,x0:x1]
hull=cv2.morphologyEx((t>0.4).astype(np.uint8),cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(41,41)))
hull=cv2.GaussianBlur(hull.astype(np.float32),(0,0),6)
L['print_t']=t; L['print_hull']=hull; print('print',t.shape,'ink col',d[d[...,1]<70].mean(0)[::-1])
# ---- tipo preto (camadas multiply) a partir do recorte dele
ty=cv2.imread(U+N['type']+'-image.png').astype(np.float32)[...,::-1]
paper=np.median(ty.reshape(-1,3),0)
m=np.clip(ty/paper,0,1); m=np.clip(m/0.90,0,1)
m=np.where(m.min(2,keepdims=True)>0.93,1.0,m)
meta['type_box']=[121,185,1934,1849]
words={'A':(214,185,477,1015),'GENTE':(612,185,1833,1015),'ENDURECE':(121,1030,1934,1849)}
for k,(xa,ya,xb,yb) in words.items():
    p=16; L['w_'+k]=m[ya-p:yb+p,xa-p:xb+p].astype(np.float32); meta['w_'+k]=[xa-p,ya-p]
np.savez_compressed('layers.npz',**L); json.dump(meta,open('meta.json','w'))
print({k:v.shape for k,v in L.items()})
