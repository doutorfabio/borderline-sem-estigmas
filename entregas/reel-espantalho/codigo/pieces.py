import cv2, numpy as np, sys, json, os, pickle
S=sys.argv[1]; W,H=1080,1920
LINES={1:[(55,540),(540,860),(860,1075)],
       2:[(75,500),(500,905),(905,1205)],
       3:[(35,495),(495,712),(712,1105)],
       4:[(160,495),(495,845),(845,1180)],
       5:[(130,485),(485,825),(825,1045)],
       6:[(130,800),(800,1170)]}
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
        bx=np.zeros_like(m); bx[2060:2300,:]=rest[2060:2300,:]; rest&=~bx
        pieces.append(dict(kind='cta',mask=bx))
    num,lab,stats,cent=cv2.connectedComponentsWithStats(rest.astype(np.uint8),8)
    main=np.zeros_like(m); acc=[]; bigs=[]
    for i in range(1,num):
        a=stats[i,4]
        if a<180: continue
        cm=lab==i
        if a>12000: main|=cm; bigs.append(cm)
        else: acc.append((cent[i],cm))
    near=cv2.dilate(main.astype(np.uint8),np.ones((91,91),np.uint8))>0
    edge=np.zeros_like(m); edge[ytext:,:]=True; edge[b:-b,b:-b]=False
    extra=m0&near&edge&~main
    # merge small-ish bigs (<1.5% area) into the nearest larger one
    bigs.sort(key=lambda c:-c.sum())
    arts=[]
    for cm in bigs:
        if arts and cm.sum()<0.012*h*w:
            ys,xs=np.nonzero(cm); best=min(arts,key=lambda A: abs(np.nonzero(A)[0].mean()-ys.mean())+abs(np.nonzero(A)[1].mean()-xs.mean()))
            best|=cm
        else: arts.append(cm.copy())
    for A in arts:
        A|=extra&(cv2.dilate(A.astype(np.uint8),np.ones((91,91),np.uint8))>0)
        ys,xs=np.nonzero(A)
        dl,dr,dtop,db=xs.min(),w-xs.max(),ys.min(),h-ys.max()
        side='B' if db<60 else min([('L',dl),('R',dr),('B',db)],key=lambda z:z[1])[0]
        if n==6: side='S'
        pieces.append(dict(kind='art',mask=A,side=side,area=int(A.sum())))
    # group accents left-to-right-ish by angle order around art centroid
    if acc:
        ys,xs=np.nonzero(main); cx,cy=(xs.mean(),ys.mean()) if len(xs) else (w/2,h/2)
        bys,bxs=np.nonzero(main); X0,X1,Y0,Y1=bxs.min()-160,bxs.max()+160,bys.min()-200,bys.max()+160
        acc=[c for c in acc if X0<c[0][0]<X1 and Y0<c[0][1]<Y1]
        acc.sort(key=lambda c: np.arctan2(c[0][1]-cy,c[0][0]-cx))
        for k,(c,cm) in enumerate(acc): pieces.append(dict(kind='acc',idx=k,mask=cm))
    claimed=np.zeros_like(m)
    for q in pieces: claimed|=q['mask']
    left=rest&~claimed
    num2,lab2,st2,_=cv2.connectedComponentsWithStats(left.astype(np.uint8),8)
    arts_=[q for q in pieces if q['kind']=='art']
    if arts_:
        big=max(arts_,key=lambda q:q['area'])
        for i in range(1,num2):
            if st2[i,4]>=40: big['mask']|=(lab2==i)
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
