import cv2, numpy as np, sys, json, os, pickle
S=sys.argv[1]; W,H=1080,1920
LINES={1:[(130,482),(482,922),(922,1215)],
       2:[(85,482),(482,878),(878,1225)],
       3:[(50,448),(448,815),(815,1195)],
       4:[(365,850),(850,1190)],
       5:[(120,515),(515,925)],
       6:[(150,775),(775,1120)]}
def runs(on,mingap,minlen):
    out=[];s=None
    for i,v in enumerate(list(on)+[False]):
        if v and s is None:s=i
        if not v and s is not None:
            if out and s-out[-1][1]<mingap: out[-1]=(out[-1][0],i)
            else: out.append((s,i))
            s=None
    return [r for r in out if r[1]-r[0]>=minlen]
allp={}
for n in range(1,7):
    im=cv2.imread(f'{S}/src/0{n}.png'); h,w=im.shape[:2]
    m=cv2.imread(f'{S}/work/mask_0{n}.png',0)>0
    # kill border frame
    m0=m.copy()
    b=40; m[:b,:]=0;m[-b:,:]=0;m[:,:b]=0;m[:,-b:]=0
    used=np.zeros_like(m)
    pieces=[]
    for li,(y0,y1) in enumerate(LINES[n]):
        band=m[y0:y1]
        cols=band.sum(0)>2
        ws=runs(cols,22,15)
        for wi,(x0,x1) in enumerate(ws):
            pm=np.zeros_like(m); pm[y0:y1,x0:x1]=m[y0:y1,x0:x1]
            if pm.sum()<4000: continue
            pieces.append(dict(kind='word',line=li,idx=wi,mask=pm,box=(x0,y0,x1,y1)))
            used|=pm
    ytext=LINES[n][-1][1]
    rest=m.copy(); rest[:ytext]=0
    # page number: bottom-right corner
    pn=np.zeros_like(m); pn[int(h*.9):,int(w*.86):]=rest[int(h*.9):,int(w*.86):]
    rest&=~pn
    # card 6: bottom box separately
    if n==6:
        bx=np.zeros_like(m); bx[2150:2420,:]=rest[2150:2420,:]; rest&=~bx
        pieces.append(dict(kind='cta',mask=bx))
    num,lab,stats,cent=cv2.connectedComponentsWithStats(rest.astype(np.uint8),8)
    main=np.zeros_like(m); acc=[]
    for i in range(1,num):
        a=stats[i,4]
        if a<180: continue
        cm=lab==i
        if a>12000: main|=cm
        else: acc.append((cent[i],cm))
    near=cv2.dilate(main.astype(np.uint8),np.ones((91,91),np.uint8))>0
    edge=np.zeros_like(m); edge[ytext:,:]=True; edge[b:-b,b:-b]=False
    main|=m0&near&edge
    pieces.append(dict(kind='art',mask=main))
    # group accents left-to-right-ish by angle order around art centroid
    if acc:
        ys,xs=np.nonzero(main); cx,cy=(xs.mean(),ys.mean()) if len(xs) else (w/2,h/2)
        bys,bxs=np.nonzero(main); X0,X1,Y0,Y1=bxs.min()-160,bxs.max()+160,bys.min()-200,bys.max()+160
        acc=[c for c in acc if X0<c[0][0]<X1 and Y0<c[0][1]<Y1]
        acc.sort(key=lambda c: np.arctan2(c[0][1]-cy,c[0][0]-cx))
        for k,(c,cm) in enumerate(acc): pieces.append(dict(kind='acc',idx=k,mask=cm))
    pieces.append(dict(kind='num',mask=pn))
    # debug overlay
    dbg=im.copy()
    for p in pieces:
        ys,xs=np.nonzero(p['mask'])
        if len(xs)==0: continue
        col={'word':(255,0,0),'art':(0,255,0),'acc':(0,255,255),'num':(255,0,255),'cta':(0,0,255)}[p['kind']]
        cv2.rectangle(dbg,(xs.min(),ys.min()),(xs.max(),ys.max()),col,5)
    cv2.imwrite(f'{S}/work/dbg_0{n}.jpg',cv2.resize(dbg,(360,640)))
    print(n, [(p['kind'],p.get('line'),p.get('idx')) for p in pieces if p['kind']=='word'], 'acc',len(acc))
    allp[n]=pieces
pickle.dump(allp,open(f'{S}/work/pieces.pkl','wb'))
