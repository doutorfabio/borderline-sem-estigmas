import numpy as np, cv2, json
U='/root/.claude/uploads/ce587ab4-daad-5a2a-9622-f6e319c367bd/'
N=json.load(open('names.json'))
def load(k): return cv2.imread(U+N[k]+'-image.png', cv2.IMREAD_COLOR).astype(np.float32)
def bgcol(im):
    b=12
    s=np.concatenate([im[:b].reshape(-1,3),im[-b:].reshape(-1,3),im[:,:b].reshape(-1,3),im[:,-b:].reshape(-1,3)])
    return np.median(s,0)
def bgmask(im, chroma=18, lumup=12, seeds=None):
    """background + baked shadow = low-chroma, not brighter than bg, connected to image border"""
    bg=bgcol(im); lum=im.mean(2); ch=im.max(2)-im.min(2)
    cand=((ch<chroma)&(lum<bg.mean()+lumup)).astype(np.uint8)
    cand=cv2.erode(cand,np.ones((3,3),np.uint8))
    n,lab=cv2.connectedComponents(cand,connectivity=4)
    border=set(np.unique(lab[0]))|set(np.unique(lab[-1]))|set(np.unique(lab[:,0]))|set(np.unique(lab[:,-1]))
    border.discard(0)
    m=np.isin(lab,list(border)).astype(np.uint8)
    m=cv2.dilate(m,np.ones((5,5),np.uint8))   # undo erosion + 1px bite into edge
    return m,bg
def alpha_from(m):
    a=1-cv2.GaussianBlur(m.astype(np.float32),(0,0),0.8)
    return np.clip((a-0.15)/0.7,0,1)
def crop_save(name, im, a, pad=6):
    ys,xs=np.where(a>0.1); x0,y0,x1,y1=max(0,xs.min()-pad),max(0,ys.min()-pad),min(a.shape[1],xs.max()+1+pad),min(a.shape[0],ys.max()+1+pad)
    out=np.dstack([im,a*255])[y0:y1,x0:x1].clip(0,255).astype(np.uint8)
    cv2.imwrite(name,out); print(name,(x0,y0,x1,y1),out.shape); return (int(x0),int(y0))
def largest(a,t=0.5):
    n,lab,st,_=cv2.connectedComponentsWithStats((a>t).astype(np.uint8))
    k=1+np.argmax(st[1:,4]); return a*(cv2.dilate((lab==k).astype(np.uint8),np.ones((5,5),np.uint8)))
off={}
for k in ['fig','figdig','handO']:
    im=load(k); m,bg=bgmask(im); a=largest(alpha_from(m)); off[k]=crop_save(f'c_{k}.png',im,a)

# strips: yellow / red separated
im=load('strips'); m,bg=bgmask(im); a=alpha_from(m)
n,lab,st,_=cv2.connectedComponentsWithStats((a>0.5).astype(np.uint8))
big=[i for i in range(1,n) if st[i,4]>100000]
for i in big:
    comp=cv2.dilate((lab==i).astype(np.uint8),np.ones((5,5),np.uint8))
    col=im[lab==i].mean(0); name='yellow' if col[1]>120 else 'red'   # BGR: yellow has high G
    off['strip_'+name]=crop_save(f'c_strip_{name}.png',im,a*comp,pad=2)
# torn pieces
im=load('pieces'); m,bg=bgmask(im); a=alpha_from(m)
n,lab,st,_=cv2.connectedComponentsWithStats((a>0.5).astype(np.uint8))
for j,i in enumerate([i for i in range(1,n) if st[i,4]>100000]):
    comp=cv2.dilate((lab==i).astype(np.uint8),np.ones((5,5),np.uint8))
    crop_save(f'c_piece_{j}.png',im,a*comp)

# closed hand: contour cut from the scrap
im=load('handC'); m,bg=bgmask(im); scrap=largest(alpha_from(m))
ys,xs=np.where(scrap>0.1); X0,Y0=xs.min()-6,ys.min()-6          # same origin as the grid view (398,277)
print('handC origin',X0,Y0)
lum=im.mean(2)
ink=((lum<120)&(scrap>0.9)).astype(np.uint8)
wall=cv2.dilate(ink,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9)))
# close the open wrist end (grid coords -> full coords)
def P(x,y): return (int(x+X0),int(y+Y0))
cv2.line(wall,P(140,1108),P(165,1190),1,9); cv2.line(wall,P(165,1190),P(250,1285),1,9); cv2.line(wall,P(250,1285),P(420,1358),1,9)
free=(1-wall).astype(np.uint8)
n,lab=cv2.connectedComponents(free,connectivity=4)
outside=lab[P(60,60)[1],P(60,60)[0]]; hole=lab[P(760,620)[1],P(760,620)[0]]; assert hole!=0 and outside!=0 and hole!=outside
print('labels outside/hole',outside,hole, 'hole area',(lab==hole).sum())
sil=((lab!=outside)&(lab!=hole)).astype(np.uint8)
sil=largest(sil.astype(np.float32))
# paper border like the open hand (~14px) with slight irregular wobble
rng=np.random.default_rng(7)
d_in=cv2.distanceTransform((sil<0.5).astype(np.uint8),cv2.DIST_L2,5)       # distance outside silhouette
noise=cv2.GaussianBlur(rng.normal(0,1,sil.shape).astype(np.float32),(0,0),14); noise/=noise.std()
noise2=cv2.GaussianBlur(rng.normal(0,1,sil.shape).astype(np.float32),(0,0),3); noise2/=noise2.std()
border=10+3.5*noise+1.2*noise2
cut=((sil>0.5)|(d_in<np.maximum(border,3))).astype(np.float32)*(scrap>0.5)
cut=largest(cut)
a=np.clip((cv2.GaussianBlur(cut,(0,0),0.9)-0.15)/0.7,0,1)
off['handC']=crop_save('c_handC.png',im,a)
off['handC_grid_origin']=[int(X0),int(Y0)]
json.dump(off,open('off.json','w'))
