# A GENTE ENDURECE / NO FORMATO DE QUEM NOS SEGUROU
# 10 s, 1080x1920, 24 qps com poses a cada 2 quadros (stop motion 12 qps). Tudo em degraus.
import numpy as np, cv2, json, sys, subprocess, zlib
from PIL import ImageFont
from redtext import word_mask, ink, FONT
W,H,FPS,NF=1080,1920,24,240
TEXT=True
L=dict(np.load('layers.npz')); meta=json.load(open('meta.json'))

# ------------------------------------------------------------------ layout
TW=690; TX0=(W-TW)//2; TY0=250                 # bloco preto: largura, canto
ts=TW/1813.0
YF=1530                                         # linha do chao (borda rasgada da tira)
PX=540                                          # eixo da figura / ponto da pinca
FIG=L['fig']; COL=np.array(meta['fig_collar']); FEET=np.array(meta['fig_feet']); BACK=np.array(meta['fig_back'])
STAND_Y=YF+28-FEET[1]+COL[1]                    # y da gola com os pes no chao
DROP=104
PY=STAND_Y-DROP                                 # y da gola (e da pinca) com a figura pendurada
HAND_ROT=11.0                                   # mao fechada girada para o punho sumir atras do chao
PINCH=np.array(meta['handC_pinch'])
PDX=-34                                         # pinca um pouco a esquerda do eixo: pega a gola pela borda
_s=PINCH[0]/940.0
_poly=(np.array([(950,346),(1010,346),(1010,640),(640,640),(700,512),(790,438),(860,390),(915,360)],np.float32)*_s).astype(np.int32)
_m=np.zeros(L['handC'].shape[:2],np.uint8); cv2.fillPoly(_m,[_poly],255,lineType=cv2.LINE_AA)
THUMB=L['handC']*(_m.astype(np.float32)/255.0)[...,None]
RED=np.array([204,0,0],np.float32)/255.0
CREAM=np.array([240,229,206],np.float32)/255.0
SH=(2,2)                                        # sombra de contato, 2 px

# ------------------------------------------------------------------ tipo preto (multiply)
def scale_to(im,s): return cv2.resize(im,(max(1,round(im.shape[1]*s)),max(1,round(im.shape[0]*s))),interpolation=cv2.INTER_AREA)
BLACK=[]
for k,f0 in (('A',84),('GENTE',87),('ENDURECE',90)):
    m=scale_to(L['w_'+k],ts); ox,oy=meta['w_'+k]
    BLACK.append(dict(m=m,x=TX0+(ox-121)*ts,y=TY0+(oy-185)*ts,f0=f0,name=k))
BLOCK_BOTTOM=TY0+(1849-185)*ts
# ------------------------------------------------------------------ frase vermelha
XS=0.90
def layout_line(text,width,seed):
    S=4; f=ImageFont.truetype(FONT,400); caph=f.getbbox('H')[3]-f.getbbox('H')[1]
    bb=f.getbbox(text); w400=(bb[2]-bb[0])*XS
    cap=width/w400*caph                                   # altura de versal que fecha a largura
    size=int(400*cap*S/caph); f=ImageFont.truetype(FONT,size); bb=f.getbbox(text)
    out=[]; words=text.split(' ')
    for i,wd in enumerate(words):
        pre=' '.join(words[:i])+(' ' if i else '')
        x=(f.getlength(pre)+f.getbbox(wd)[0]-bb[0])*XS/S - 4*XS
        y=(f.getbbox(wd)[1]-bb[1])/S - 4
        a=ink(word_mask(wd,cap,XS),seed+i)
        out.append(dict(word=wd,a=a,x=x,y=y))
    return out,cap
REDW=[]; y=BLOCK_BOTTOM+24
for li,(txt,seed) in enumerate((('NO FORMATO DE',11),('QUEM NOS SEGUROU',23))):
    ws,cap=layout_line(txt,TW,seed)
    for w_ in ws:
        mult=1-w_['a'][...,None]*(1-RED)[None,None,:]
        REDW.append(dict(m=mult.astype(np.float32),x=TX0+w_['x'],y=y+w_['y'],name=w_['word'],a=w_['a']))
    y+=cap+16
RED_BOTTOM=y-16
for i,r in enumerate(REDW): r['f0']=192+3*i
# ------------------------------------------------------------------ chao
FLOOR=L['floor']
fa=FLOOR[...,3]; c0=(FLOOR.shape[1]-W)//2
edge=np.array([np.argmax(fa[:,c]>0.5) for c in range(c0,c0+W)])
FLOOR_EDGE=float(np.median(edge)); FLOOR_POS=np.array([-c0, YF-FLOOR_EDGE])
# ------------------------------------------------------------------ meio-tom
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
p=6.0; u=(xx+yy)/np.sqrt(2); v=(xx-yy)/np.sqrt(2)
dd=np.sqrt(((u%p)-p/2)**2+((v%p)-p/2)**2)
DOT=np.clip((2.35-dd)+0.5,0,1)                   # pontos de reticula fixos no papel
HT=0.30+0.70*DOT
# ------------------------------------------------------------------ digital carimbada na figura
def stamped(fig, s, ang, off=(0,0)):
    t=L['print_t']; hu=L['print_hull']
    h,w=fig.shape[:2]
    M=cv2.getRotationMatrix2D((t.shape[1]/2,t.shape[0]/2),ang,s)
    M[0,2]+=BACK[0]+off[0]-t.shape[1]/2; M[1,2]+=BACK[1]+off[1]-t.shape[0]/2
    tt=cv2.warpAffine(t,M,(w,h),flags=cv2.INTER_AREA); hh=cv2.warpAffine(hu,M,(w,h),flags=cv2.INTER_AREA)
    a=fig[...,3:4]; rgb=fig[...,:3]/np.maximum(a,1e-4)
    gy,gx=np.mgrid[0:h,0:w].astype(np.float32)
    win=np.clip((1-((gx-BACK[0]-off[0])/(86*s/0.21))**2-((gy-BACK[1]-10-off[1])/(128*s/0.21))**2)/0.22,0,1)   # so no tronco
    tt*=win; hh*=win
    rgb=rgb*(1-0.72*hh[...,None])+CREAM*(0.72*hh[...,None])        # corpo claro da tinta, como no recorte de referencia
    rgb=rgb*(1-tt[...,None]*(1-RED))                                # sulcos em multiply
    return np.dstack([rgb*a,a]).astype(np.float32)
FIG_STAMP=stamped(FIG,0.21,0)
FIG_STAMP_BIG=stamped(FIG,0.29,-9,(3,-5))
# ------------------------------------------------------------------ utilidades
def jit(name,pose,amp=1.0):
    r=np.random.default_rng(zlib.crc32(f'{name}:{pose}'.encode()))
    c=np.array([-2,-1,-1,0,0,1,1,2])
    return float(r.choice(c))*amp, float(r.choice(c))*amp, float(r.uniform(-0.18,0.18))
def warp(layer,pivot,pos,ang=0.0,sc=1.0,border=0.0):
    M=cv2.getRotationMatrix2D((float(pivot[0]),float(pivot[1])),ang,sc)
    M[0,2]+=pos[0]-pivot[0]; M[1,2]+=pos[1]-pivot[1]
    return cv2.warpAffine(layer,M,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=border)
def shift(a,dx,dy):
    return cv2.warpAffine(a,np.float32([[1,0,dx],[0,1,dy]]),(a.shape[1],a.shape[0]))
def over(canvas,lay,shadow=True):
    a=lay[...,3]
    if shadow:
        s=shift(a,SH[0],SH[1])
        canvas*= (1-0.78*s*HT)[...,None]
    canvas*= (1-a)[...,None]; canvas+=lay[...,:3]
def mult(canvas,m,x,y,ang=0.0):
    h,w=m.shape[:2]
    if ang==0.0 and float(x).is_integer() and float(y).is_integer():
        x=int(x); y=int(y); canvas[y:y+h,x:x+w]*=m; return
    full=warp(m,(w/2,h/2),(x+w/2,y+h/2),ang,1.0,border=(1.0,1.0,1.0))
    canvas*=full
# ------------------------------------------------------------------ linha do tempo
RISE=640.0
def hand_closed_y(f):
    """y da pinca. sobe em 3 saltos: 4 quadros de antecipacao, 2 de assentamento."""
    if f<26: return None
    tg=[PY+RISE, PY+RISE*2/3, PY+RISE/3, PY]
    k=min(2,(f-26)//8); r=f-26-8*k
    if f>=50: y=PY
    elif r<2: y=tg[k]+9
    elif r<4: y=tg[k]+16
    elif r<6: y=tg[k+1]-11
    else: y=tg[k+1]
    if f in (58,59): y+=6
    if f in (60,61): y+=2
    return y
FALL_ROT=[-20,13,-10,15,-7]; FALL_DX=[14,-10,8,-6,3]
SWING={58:7,60:-5,62:4,64:-3,66:2,68:-1.5,70:1,72:-0.5}
def figure_state(f):
    """(x, y da gola, angulo) ou None"""
    if f<48: return None
    if f<58:
        i=(f-48)//2; return PX+FALL_DX[i], PY-240*(5-i), FALL_ROT[i]
    if f<74:
        k=(f//2)*2; return PX, PY+(8 if f<60 else 0), SWING.get(k,0)
    if f<134: return PX, PY, 0.0
    if f<136: return PX, PY, 0.0                      # suspensa um quadro no ar
    if f<150:
        i=(f-136)//2; return PX, PY+DROP*(i+1)/8.0, 0.0   # desce devagar, em degraus iguais
    y=STAND_Y
    if f in (153,154): y+=3
    return PX, y, 0.0
def open_hand_y(f):
    if f<133: return None
    if f<160: return 0
    if f<162: return -10
    if f<164: return 220
    if f<166: return 460
    if f<168: return 700
    return None
def scene_off(f):
    if 84<=f<132:
        r=np.random.default_rng(900+f//2); return float(r.choice([-1,0,1])), float(r.choice([-1,0,1]))
    if f in (153,154): return 2.0,2.0
    if f in (155,156): return -1.0,-1.0
    return 0.0,0.0
OPEN_TOP=950; OPEN_CX=306; OPEN_ROT=-7.0
def frame(f, state_f=None):
    sf=f if state_f is None else state_f
    pose=sf//2
    if sf>=228: return close_frame(sf)
    c=L['bg'].copy(); sx,sy=scene_off(sf)
    # --- mao
    hand_lay=None; thumb_lay=None
    hy=hand_closed_y(sf)
    if hy is not None and sf<133:
        jx,jy,jr=jit('hand',pose)
        hand_lay=warp(L['handC'],PINCH,(PX+PDX+jx+sx,hy+jy+sy),HAND_ROT+jr)
        thumb_lay=warp(THUMB,PINCH,(PX+PDX+jx+sx,hy+jy+sy),HAND_ROT+jr)
        over(c,hand_lay)
    oy=open_hand_y(sf)
    if oy is not None:
        jx,jy,jr=jit('handO',pose); ho=L['handO']
        piv=(ho.shape[1]/2,0)
        over(c,warp(ho,piv,(OPEN_CX+jx+sx,OPEN_TOP+oy+jy+sy),OPEN_ROT+jr))
    # --- chao
    if sf>=24:
        jx,jy,jr=jit('floor',pose,0.5)
        if sf<26: over(c,warp(FLOOR,(640,0),(640+FLOOR_POS[0]+18,FLOOR_POS[1]+70),2.2))
        else: over(c,warp(FLOOR,(640,0),(640+FLOOR_POS[0]+jx+sx,FLOOR_POS[1]+jy+sy),jr*0.3))
    # --- figura
    fs=figure_state(sf)
    if fs is not None:
        x,y,ang=fs; jx,jy,jr=jit('fig',pose)
        if sf>=150:    # sombra de contato no chao, em meio-tom
            cx,cy=x+4,STAND_Y-COL[1]+FEET[1]+3
            e=np.clip(1-((xx-cx)/92.0)**2-((yy-cy)/11.0)**2,0,1)**0.5
            c*=(1-0.62*e*DOT)[...,None]
        lay=FIG
        if sf==152: lay=FIG_STAMP_BIG
        elif sf>152: lay=FIG_STAMP
        fl=warp(lay,COL,(x+jx+sx,y+jy+sy),ang+jr)
        over(c,fl)
        if thumb_lay is not None and 58<=sf<133:   # polegar por cima da gola: a figura fica presa entre os dedos
            c*=(1-thumb_lay[...,3])[...,None]; c+=thumb_lay[...,:3]
    # --- tipo
    for b in (BLACK if TEXT else []):
        if sf>=b['f0']:
            jx,jy,_=jit(b['name'],pose,0.5)
            if sf<b['f0']+2: mult(c,b['m'],b['x']+3,b['y']-13,-1.3)
            else: mult(c,b['m'],round(b['x']+jx+sx),round(b['y']+jy+sy))
    for r in (REDW if TEXT else []):
        if sf>=r['f0']:
            jx,jy,_=jit('r'+r['name'],pose,0.5)
            if sf<r['f0']+2: mult(c,r['m'],r['x']-2,r['y']-9,1.2)
            else: mult(c,r['m'],round(r['x']+jx),round(r['y']+jy))
    return np.clip(c,0,1)
# --- close na digital (recorte de referencia dele, corte seco)
FD=L['figdig']
def close_frame(f):
    pose=f//2; c=L['bg_close'].copy()
    s=1.86; jx,jy,jr=jit('close',pose,0.5)
    lay=warp(FD,(278,760),(540+jx,930+jy),jr*0.3,s)      # centro da digital no meio do quadro
    a=lay[...,3]; sh=shift(a,4,4); c*=(1-0.78*sh*HT)[...,None]
    c*=(1-a)[...,None]; c+=lay[...,:3]
    return np.clip(c,0,1)
# --- falha de projetor (2 quadros)
def glitch(img,kind):
    if kind=='A':
        roll=int(0.36*H); out=np.roll(img,-roll,axis=0); seam=H-roll; out=np.roll(out,9,axis=1)
        out=out*1.10+0.03; bar=64
        out[seam-bar//2:seam+bar//2]=np.array([0.07,0.055,0.05])
        out[seam-bar//2-3:seam-bar//2]*=0.55; out[seam+bar//2:seam+bar//2+3]*=0.55
        for xs,al in ((212,0.5),(741,0.35),(748,0.22)): out[:,xs:xs+2]=out[:,xs:xs+2]*(1-al)+al
    else:
        roll=int(0.075*H); out=np.roll(img,roll,axis=0); out=np.roll(out,-5,axis=1)
        out=out*0.90; bar=64
        out[roll-bar//2:roll+bar//2]=np.array([0.07,0.055,0.05])
        out[roll+bar//2:roll+bar//2+3]*=0.55
        out[:,455:457]=out[:,455:457]*0.6+0.4
    return np.clip(out,0,1)
def render(f):
    if f==132: return glitch(frame(132,131),'A')
    if f==133: return glitch(frame(133),'B')
    return frame(f)
def to8(img): return (img*255+0.5).astype(np.uint8)
if __name__=='__main__':
    print('bloco preto ate y=%.0f, vermelho ate y=%.0f, cabeca da figura no chao em y=%.0f, pinca y=%.0f'%(BLOCK_BOTTOM,RED_BOTTOM,STAND_Y-COL[1]+9,PY))
    if sys.argv[1]=='still':
        for f in [int(x) for x in sys.argv[2].split(',')]:
            cv2.imwrite(f'f_{f:03d}.png',to8(render(f))[...,::-1])
    elif sys.argv[1]=='video':
        out=sys.argv[2]
        p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
            '-c:v','libx264','-preset','slow','-crf','13','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',out],stdin=subprocess.PIPE)
        prev=None
        for f in range(NF):
            p.stdin.write(to8(render(f)).tobytes())
        p.stdin.close(); p.wait(); print('ok',out)
