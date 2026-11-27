import cv2, numpy as np, pickle, sys, math, subprocess, json, random
S=sys.argv[1]; PREVIEW=len(sys.argv)>2
W,H=1080,1920; FPS=30; K=0.75
random.seed(7)
allp=pickle.load(open(f'{S}/work/pieces.pkl','rb'))
KEY={1:{(2,1)},2:{(2,2)},3:{(2,0)},4:{(2,0)},5:{(1,1)},6:{(0,0)}}
SIDE={'L':(-760,140,-7),'R':(760,140,7),'B':(0,900,0),'S':(0,0,0)}
ART_FROM={1:(-380,420,-6),2:(-420,300,5),3:(0,620,0),4:(0,560,0),5:(-300,500,-5),6:(0,-700,4)}
def eob(p,s=1.6): p=p-1; return p*p*((s+1)*p+s)+1
def eoc(p): return 1-(1-p)**3
cards=[]
for n in range(1,7):
    im=cv2.imread(f'{S}/src/0{n}.png')
    im=cv2.resize(im,(W,H),interpolation=cv2.INTER_AREA)
    U=np.zeros((H,W),np.uint8)
    pcs=[]
    for p in allp[n]:
        m=cv2.resize(p['mask'].astype(np.uint8)*255,(W,H),interpolation=cv2.INTER_AREA)
        if m.max()==0: continue
        a=cv2.dilate(m,np.ones((7,7),np.uint8)); a=cv2.GaussianBlur(a,(3,3),0)
        ys,xs=np.nonzero(a>8); x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
        rgba=np.dstack([im[y0:y1,x0:x1],a[y0:y1,x0:x1]]).astype(np.float32)
        U=np.maximum(U,a)
        q=dict(p); del q['mask']; q.update(rgba=rgba,x0=x0,y0=y0,cx=(x0+x1)/2,cy=(y0+y1)/2)
        pcs.append(q)
    # base fill
    Md=cv2.dilate(U,np.ones((9,9),np.uint8))
    sm=cv2.resize(im,(W//8,H//8),interpolation=cv2.INTER_AREA)
    smm=(cv2.resize(Md,(W//8,H//8))>0).astype(np.uint8)
    smm=cv2.dilate(smm,np.ones((3,3),np.uint8))
    labs=cv2.cvtColor(sm,cv2.COLOR_BGR2LAB).astype(np.float32)
    bgc=np.median(labs[smm==0],axis=0)
    far=(np.linalg.norm(labs-bgc,axis=2)>22).astype(np.uint8)
    smm=np.maximum(smm,cv2.dilate(far,np.ones((3,3),np.uint8)))
    fill=cv2.inpaint(sm,smm,6,cv2.INPAINT_TELEA)
    fill=cv2.GaussianBlur(cv2.resize(fill,(W,H),interpolation=cv2.INTER_CUBIC),(0,0),6).astype(np.float32)
    rng=np.random.default_rng(n)
    grain=rng.normal(0,7,(H,W,1)).astype(np.float32)
    specks=(rng.random((H,W))<0.0009).astype(np.float32); specks=cv2.GaussianBlur(specks,(3,3),0)[...,None]*-140
    fill=np.clip(fill+grain+specks,0,255)
    Mf=(cv2.GaussianBlur(Md,(0,0),2)/255.0)[...,None]
    base=im.astype(np.float32)*(1-Mf)+fill*Mf
    # timing
    t=0.05 if n==1 else 0.20
    stag=0.085 if n==1 else 0.11
    events=[]
    lastline=None
    words=[q for q in pcs if q['kind']=='word']
    for q in words:
        if lastline is not None and q['line']!=lastline: t+=0.10
        key=(q['line'],q['idx']) in KEY[n]
        q.update(t0=t,dur=0.34 if key else 0.28,key=key,r0=random.uniform(-7,7) if not key else random.choice([-9,9]))
        if q['line']!=lastline: events.append(('click',t+0.10))
        if key: events.append(('shutter2',t+0.14))
        lastline=q['line']; t+=stag if not key else stag+0.06
    t+=0.22
    ta=t
    for q in sorted([q for q in pcs if q['kind']=='art'],key=lambda q:-q['area']):
        q.update(t0=ta,dur=0.55); events.append(('shutter',ta+0.42)); tart=ta+0.55; ta+=0.16
    if n==3: events.append(('impact',tart-0.12))
    t=tart
    accs=[q for q in pcs if q['kind']=='acc']
    for i,q in enumerate(accs): q.update(t0=t-0.1+i*0.03,dur=0.16)
    if accs: t+=len(accs)*0.03
    for q in pcs:
        if q['kind']=='cta': q.update(t0=t+0.05,dur=0.3); events.append(('hud',t+0.2)); t+=0.35
        if q['kind']=='num': q.update(t0=t,dur=0.18)
    hold={1:1.7,2:1.4,3:1.5,4:1.4,5:1.5,6:2.2}[n]
    D=t+0.2+hold
    import os
    if os.path.exists('targets.json'):
        TD=json.load(open('targets.json'))[n-1]
        tend=t+0.2
        f=min(1.0,(TD-0.45)/tend)
        for q in pcs:
            if 't0' in q: q['t0']*=f; q['dur']*=max(f,0.8)
        events=[(e,tt*f) for e,tt in events]
        D=TD
    cards.append(dict(n=n,base=base,pcs=pcs,D=D,events=events))
# global times
T=0; 
for c in cards: c['T']=T; T+=c['D']
TOTAL=T
print('total',round(TOTAL,2),[round(c['D'],2) for c in cards])

def paste(dst,rgba,M,shadow=None):
    h,w=rgba.shape[:2]
    pts=np.array([[0,0,1],[w,0,1],[0,h,1],[w,h,1]],np.float32)@M.T
    pad=30
    X0=int(max(0,pts[:,0].min()-pad)); X1=int(min(W,pts[:,0].max()+pad))
    Y0=int(max(0,pts[:,1].min()-pad)); Y1=int(min(H,pts[:,1].max()+pad))
    if X1<=X0 or Y1<=Y0: return
    M2=M.copy(); M2[0,2]-=X0; M2[1,2]-=Y0
    out=cv2.warpAffine(rgba,M2,(X1-X0,Y1-Y0),flags=cv2.INTER_LINEAR,borderValue=(0,0,0,0))
    a=out[...,3:4]/255.0
    reg=dst[Y0:Y1,X0:X1]
    if shadow:
        ox,oy,bl,op=shadow
        sa=cv2.GaussianBlur(out[...,3],(0,0),bl)/255.0*op
        Ms=np.float32([[1,0,ox],[0,1,oy]])
        sa=cv2.warpAffine(sa,Ms,(X1-X0,Y1-Y0))[...,None]
        reg*= (1-sa*0.75)
    reg[:]=reg*(1-a)+out[...,:3]*a

def piece_pose(q,lt):
    if 't0' not in q: return None
    p=(lt-q['t0'])/q['dur']
    if p<0: return None
    k=q['kind']
    if k in('word','cta','num','acc'):
        p=min(1,math.floor(p*q['dur']*15)/(q['dur']*15)+1e-9) if p<1 else 1
        e=eob(min(p,1))
        A=0.55 if q.get('key') else 0.30
        if k=='acc': return dict(s=max(0.01,e),r=0,dx=0,dy=0,h=0)
        if k=='num': return dict(s=max(0.01,e),r=0,dx=0,dy=0,h=0)
        return dict(s=1+A*(1-e),r=q.get('r0',3)*(1-e),dx=0,dy=-40*(1-e),h=max(0,1-e))
    if k=='art':
        fx,fy,fr=SIDE[q['side']]
        pp=min(1,p); e=eob(pp,1.2)
        if q['side']=='S':
            e=eob(min(1,math.floor(pp*9)/9),2.2)
            return dict(s=max(0.01,0.2+0.8*e),r=-6*(1-e),dx=0,dy=0,h=0.5*(1-e))
        idle=lt-(q['t0']+q['dur'])
        bob=math.sin(max(0,idle)*2*math.pi/2.6)*min(1,max(0,idle)*2)
        return dict(s=1+0.06*(1-e),r=fr*(1-e)+0.7*bob,dx=fx*(1-e),dy=fy*(1-e)+3*bob,h=0.6*(1-e))

def render_card(c,lt):
    fr=c['base'].copy()
    for q in c['pcs']:
        q['n']=c['n']
        pz=piece_pose(q,lt)
        if pz is None: continue
        rgba=q['rgba']; h,w=rgba.shape[:2]
        M=cv2.getRotationMatrix2D((w/2,h/2),pz['r'],pz['s'])
        M[0,2]+=q['x0']+pz['dx']; M[1,2]+=q['y0']+pz['dy']
        hgt=pz['h']
        sh=(4+18*hgt,6+26*hgt,3+8*hgt,0.30+0.25*hgt) if q['kind'] in('word','art','cta') else None
        paste(fr,rgba,M,sh)
    # camera push
    z=1+0.035*min(1,lt/c['D'])
    Mc=cv2.getRotationMatrix2D((W/2,H*0.42),0,z)
    if c['n']==3:
        arts=[q for q in c['pcs'] if q['kind']=='art']
        tl_=arts[0]['t0']+arts[0]['dur']*0.62
        k=lt-tl_
        if 0<=k<0.25:
            amp=9*(1-k/0.25); Mc[0,2]+=amp*math.sin(k*90); Mc[1,2]+=amp*0.6*math.cos(k*77)
    return cv2.warpAffine(fr,Mc,(W,H),borderMode=cv2.BORDER_REFLECT)

TR=0.32
def frame_at(t):
    for i,c in enumerate(cards):
        if c['T']<=t<c['T']+c['D'] or i==len(cards)-1:
            lt=t-c['T']; break
    if i>0 and lt<TR:
        prev=cards[i-1]; under=render_card(prev,prev['D'])
        p=eoc(lt/TR)
        top=render_card(c,lt)
        p=eob(min(1,lt/TR),1.3)
        sc=1+0.10*(1-p); rot=-4*(1-p)
        Mt=cv2.getRotationMatrix2D((W*0.2,H*0.1),rot,sc); Mt[0,2]+=-W*0.9*(1-p); Mt[1,2]+=-H*0.35*(1-p)
        sheet=cv2.warpAffine(np.dstack([top,np.full((H,W),255,np.float32)]),Mt,(W,H),borderValue=(0,0,0,0))
        a=sheet[...,3:4]/255.0
        sa=cv2.GaussianBlur(sheet[...,3],(0,0),14)/255.0
        sa=np.roll(np.roll(sa,16,axis=0),12,axis=1)[...,None]*0.55
        out=under*(1-sa)
        return out*(1-a)+sheet[...,:3]*a
    return render_card(c,lt)

if PREVIEW:
    ts=[float(x) for x in sys.argv[2].split(',')]
    ims=[cv2.resize(np.clip(frame_at(t),0,255).astype(np.uint8),(270,480)) for t in ts]
    cv2.imwrite(f'{S}/work/sheet.jpg',np.hstack(ims)); sys.exit()
json.dump(dict(total=TOTAL,events=[(e,c['T']+tt) for c in cards for e,tt in c['events']]+[('whoosh%d'%(i%2),c['T']+0.22) for i,c in enumerate(cards) if i>0]),open(f'{S}/work/timeline.json','w'))
N=int(round(TOTAL*FPS))
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p',f'{S}/work/video.mp4'],stdin=subprocess.PIPE)
for f in range(N):
    t=f/FPS
    fr=frame_at(t)
    if t>TOTAL-0.12: fr=fr*max(0,(TOTAL-t)/0.12)
    ff.stdin.write(np.clip(fr,0,255).astype(np.uint8).tobytes())
ff.stdin.close(); ff.wait(); print('frames',N)
