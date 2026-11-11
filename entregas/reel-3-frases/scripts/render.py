import subprocess, numpy as np, math, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=1080,1920,30
BIG='fonts/BigShoulders-Bold.ttf'; MONO='fonts/IBMPlexMono-Bold.ttf'
BLACK=(18,16,15); RED=(204,0,0); CREAM=(239,235,227)
def font(p,s): return ImageFont.truetype(p,s)
def fit(lines,path,maxw,maxs):
    s=maxs
    while s>20:
        f=font(path,s)
        if max(f.getbbox(l)[2]-f.getbbox(l)[0] for l in lines)<=maxw: return f,s
        s-=2
    return font(path,s),s
def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3

# blocos grandes: (t_in, t_out, linhas, cor por linha, caixa x0,y0,x1,y1, alinhamento, risco_em, fundo)
BLOCKS=[
 dict(t0=0.10,t1=3.70,lines=['3 FRASES QUE','PIORAM A CRISE'],cols=[BLACK,RED],box=(80,150,920,520),align='c',strike=None,bg=False,maxs=190),
 dict(t0=3.85,t1=7.15,lines=['VAI FICAR','TUDO BEM'],cols=[BLACK,BLACK],box=(80,130,575,500),align='l',strike=4.95,bg=False,maxs=220),
 dict(t0=7.30,t1=11.00,lines=['VOCÊ ESTÁ EXAGERANDO'],cols=[BLACK],box=(90,110,910,260),align='c',strike=8.50,bg=False,maxs=140),
 dict(t0=11.15,t1=13.98,lines=['CALMA'],cols=[BLACK],box=(300,150,780,345),align='c',strike=11.75,bg=True,maxs=200),
 dict(t0=14.60,t1=17.18,lines=['QUER QUE EU FIQUE','OU PREFERE','ESPAÇO?'],cols=[BLACK,BLACK,RED],box=(262,150,816,494),align='c',strike=None,bg=False,maxs=120),
 dict(t0=17.30,t1=20.10,lines=['MANDA PRA QUEM','QUER AJUDAR','E NÃO SABE','O QUE DIZER.'],cols=[RED,BLACK,BLACK,BLACK],box=(70,170,940,760),align='c',strike=None,bg=False,maxs=170),
]
CAPS=[
 (0.00,0.78,[('Na',0),('crise',0),('de',0)]),
 (0.78,2.00,[('quem',0),('tem',0),('BORDERLINE',1)]),
 (2.00,3.70,[('evite',0),('TRÊS FRASES',1)]),
 (5.18,5.82,[('Soa',0),('como',0),('se',0)]),
 (5.82,6.46,[('você',0),('não',0),('visse',0)]),
 (6.46,7.15,[('a',0),('DOR',1)]),
 (8.70,9.54,[('Soa',0),('como',0),('se',0)]),
 (9.54,10.16,[('a',0),('dor',0),('estivesse',0)]),
 (10.16,11.00,[('ERRADA',1)]),
 (12.04,12.78,[('Se',0),('desse,',0)]),
 (12.78,13.44,[('já',0),('teria',0),('se',0)]),
 (13.44,13.98,[('ACALMADO',1)]),
 (14.08,14.60,[('PERGUNTE:',1)]),
]
SMALL=dict(t0=17.80,t1=20.10,text='Se houver risco: CVV 188',y=1330)
FB=font(MONO,58); FH=font(BIG,92); FS=font(MONO,40)

def draw_block(img,b,t):
    if not (b['t0']<=t<b['t1']): return
    x0,y0,x1,y1=b['box']; f,s=fit(b['lines'],BIG,x1-x0,b['maxs'])
    lh=int(s*0.98); tot=lh*len(b['lines'])
    k=ease((t-b['t0'])/0.18); sc=0.94+0.06*k
    layer=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(layer)
    ys=y0+((y1-y0)-tot)//2
    bbs=[]
    for i,(l,c) in enumerate(zip(b['lines'],b['cols'])):
        bb=f.getbbox(l); w=bb[2]-bb[0]
        x=x0 if b['align']=='l' else x0+((x1-x0)-w)//2
        y=ys+i*lh
        bbs.append((x-bb[0]+bb[0],y+bb[1],x+w,y+bb[3]))
        if b['bg'] and i==0:
            pad=40
            d.rectangle((x-pad,y+bb[1]-pad*0.7,x+w+pad,y+bb[3]+pad*0.7),fill=CREAM+(255,))
        d.text((x-bb[0],y),l,font=f,fill=c+(255,))
    if b['strike'] is not None and t>=b['strike']:
        p=ease((t-b['strike'])/0.25)
        for (ax,ay,bx,by) in bbs:
            cy=(ay+by)/2; th=max(10,int((by-ay)*0.13))
            xe=ax-14+(bx-ax+28)*p
            d.polygon([(ax-14,cy-th/2+3),(xe,cy-th/2-3),(xe,cy+th/2-3),(ax-14,cy+th/2+3)],fill=RED+(255,))
    if sc<0.999:
        cx=(x0+x1)/2; cy=(y0+y1)/2
        layer=layer.resize((int(W*sc),int(H*sc)),Image.LANCZOS)
        L=Image.new('RGBA',(W,H),(0,0,0,0)); L.paste(layer,(int(cx-cx*sc),int(cy-cy*sc)))
        layer=L
    if k<1: layer.putalpha(layer.getchannel('A').point(lambda v:int(v*k)))
    img.alpha_composite(layer)

def draw_caption(img,t):
    for t0,t1,ws in CAPS:
        if t0<=t<t1:
            k=ease((t-t0)/0.12)
            parts=[];tw=0
            for w,h in ws:
                f=FH if h else FB; txt=w.upper() if h else w
                bb=f.getbbox(txt); parts.append((txt,f,RED if h else BLACK,bb)); tw+=bb[2]-bb[0]
            gap=22; tw+=gap*(len(parts)-1)
            cy=1462; padx,pady=34,22
            lim=940-60-2*padx
            if tw>lim:
                r=lim/tw; parts2=[];tw=0
                for txt,f,c,bb in parts:
                    f2=font(BIG if f is FH else MONO,int((92 if f is FH else 58)*r)); bb2=f2.getbbox(txt); parts2.append((txt,f2,c,bb2)); tw+=bb2[2]-bb2[0]
                parts=parts2; gap=int(gap*r); tw+=gap*(len(parts)-1)
            x=60+padx+((940-60-2*padx)-tw)//2
            layer=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(layer)
            hmax=max(p[3][3]-p[3][1] for p in parts)
            sh=Image.new('RGBA',(W,H),(0,0,0,0)); ds=ImageDraw.Draw(sh)
            rect=(x-padx,cy-hmax//2-pady,x+tw+padx,cy+hmax//2+pady)
            ds.rectangle((rect[0]+6,rect[1]+8,rect[2]+6,rect[3]+8),fill=(0,0,0,70))
            sh=sh.filter(ImageFilter.GaussianBlur(8)); layer.alpha_composite(sh)
            d.rectangle(rect,fill=CREAM+(255,))
            for txt,f,c,bb in parts:
                d.text((x-bb[0],cy-(bb[1]+bb[3])//2),txt,font=f,fill=c+(255,)); x+=bb[2]-bb[0]+gap
            if k<1: layer.putalpha(layer.getchannel('A').point(lambda v:int(v*k)))
            img.alpha_composite(layer); return

def draw_small(img,t):
    if SMALL['t0']<=t<SMALL['t1']:
        k=ease((t-SMALL['t0'])/0.2); d=ImageDraw.Draw(img)
        bb=FS.getbbox(SMALL['text']); w=bb[2]-bb[0]
        a=int(255*k); d.text(((W-w)//2-bb[0],SMALL['y']),SMALL['text'],font=FS,fill=BLACK+(a,))

def frame_at(raw,i):
    base=Image.frombuffer('RGB',(W,H),raw,'raw','RGB',0,1).convert('RGBA'); t=i/FPS
    for b in BLOCKS: draw_block(base,b,t)
    draw_caption(base,t); draw_small(base,t)
    return base.convert('RGB')

if __name__=='__main__':
    mode=sys.argv[1]
    dec=subprocess.Popen(['ffmpeg','-v','error','-i','base.mp4','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    if mode=='stills':
        want={int(float(x)*FPS) for x in sys.argv[2:]}; i=0
        while True:
            raw=dec.stdout.read(W*H*3)
            if not raw: break
            if i in want: frame_at(raw,i).save(f'still_{i/FPS:05.2f}.png')
            i+=1
    else:
        enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-crf','14','-preset','medium','-pix_fmt','yuv420p','video_txt.mp4'],stdin=subprocess.PIPE)
        i=0
        while True:
            raw=dec.stdout.read(W*H*3)
            if not raw: break
            enc.stdin.write(frame_at(raw,i).tobytes()); i+=1
        enc.stdin.close(); enc.wait(); print('quadros',i)
