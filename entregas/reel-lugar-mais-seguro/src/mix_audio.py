# Builds the 35.00 s soundtrack: Suno music locked to the picture + foley cues on exact frames.
# usage: python3 mix_audio.py <audio_dir> <pop.mp3> <out.wav>
import sys, subprocess, numpy as np, soundfile as sf
from scipy import signal
D, POP, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
SR=48000; N=35*SR; t=np.arange(N)/SR
def load(path, ch=2):
    raw=subprocess.run(['ffmpeg','-v','error','-i',path,'-map','0:a:0','-f','f32le','-ac',str(ch),'-ar',str(SR),'-'],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).reshape(-1,ch).astype(np.float64)
db=lambda x:20*np.log10(max(x,1e-9))

# ---------- music: start on the first note, jump on a bar line to the real ending
mus=load(f'{D}/A_Warm_Resolve.m4a')
O1=0.160       # first pizzicato note sits on frame 0
O2=28.159      # from 20.0 s on: 56 beats later in the song, so its slowing ending and last chord close the film
XC,XF=19.955,0.060
def at(off):
    i=np.round((t+off)*SR).astype(int); ok=i<len(mus); o=np.zeros((N,2)); o[ok]=mus[i[ok]]; return o
p=np.clip((t-(XC-XF/2))/XF,0,1)
music=at(O1)*np.cos(p*np.pi/2)[:,None]+at(O2)*np.sin(p*np.pi/2)[:,None]
music*=np.clip(t/0.004,0,1)[:,None]
music*=(0.5+0.5*np.cos(np.pi*np.clip((t-34.25)/0.75,0,1)))[:,None]

# ---------- foley
fa=load(f'{D}/Dry_Foley_Sequence.m4a',1)[:,0]; fb=load(f'{D}/Eight_Foley_Sounds.m4a',1)[:,0]; pop=load(POP,1)[:,0]
sos=signal.butter(2,115,'hp',fs=SR,output='sos')
def clip(src,a,b,fo=0.03,hp=True):
    x=src[int(a*SR):int(b*SR)].copy()
    if hp: x=signal.sosfilt(sos,x)
    e=np.abs(x); thr=e.max()*0.06; i0=max(0,np.argmax(e>thr)-int(0.002*SR)); x=x[i0:]
    n=len(x); f=np.ones(n); k=int(0.002*SR); f[:k]=np.linspace(0,1,k); k=min(n,int(fo*SR)); f[-k:]*=np.linspace(1,0,k)
    return x*f
fx=np.zeros(N); cues=[]
def put(x,when,peak_db,name):
    x=x*(10**(peak_db/20)/np.abs(x).max()); i=int(round(when*SR)); n=min(len(x),N-i)
    fx[i:i+n]+=x[:n]; cues.append((when,name,peak_db))
# pieces, cut by their shape (see README of this folder)
thud  =clip(fa,1.660,2.110,0.08)                     # one dry wooden impact
latch =clip(fb,2.785,2.985,0.04)                     # sharp click
swish =[clip(fb,0.020,0.190,0.05),clip(fb,0.235,0.420,0.05)]   # short brushed noise
scr   =[clip(fb,2.295,2.400,0.03),clip(fb,3.095,3.215,0.03),clip(fb,3.410,3.570,0.03),clip(fb,2.505,2.590,0.03)]   # pencil scratches
keys  =[clip(fa,a,a+0.085,0.02) for a in (0.060,0.160,0.262,0.343,2.905,3.170,3.340,3.415)]                 # light key clicks
pp=clip(pop,0,0.5,0.12,hp=True)
drop=signal.resample_poly(pp,5,8)                      # same pop, higher and shorter, for the tear
# cues (seconds on the picture)
for tc in (4.0,8.5,10.5,12.5,17.0,20.0,24.5,29.0): put(pp,tc-0.02,-15.5,'pop troca de icone')
put(swish[0],1.25,-13,'pincel circulo caranguejo'); put(swish[1],5.25,-13.5,'pincel sorriso-sapo'); put(swish[0],5.70,-15,'pincel volta no sapo')
put(swish[1],4.66,-17,'paineis se juntam'); put(swish[0],23.0,-13,'pincel circulo maos'); put(swish[1],24.46,-16,'cartao cai')
put(thud,11.24,-8.5,'porta fecha'); put(latch,11.265,-11.5,'trinco'); put(scr[3],11.29,-15,'sublinhado PORTA')
put(drop,14.5,-11.5,'gota da lagrima'); put(scr[0],18.50,-12.5,'sublinhado CONFIA')
put(latch,25.0,-10.5,'alfinete')
r=np.random.default_rng(7); k=0
for a,b in ((25.03,25.3),(25.33,25.73),(25.88,26.48),(26.62,26.98)):
    x=a
    while x<b-0.03:
        put(keys[k%len(keys)],x,-17.5+r.uniform(-1.5,1.5),'tecla'); k+=1; x+=0.078+r.uniform(-0.012,0.016)
for i,tc in enumerate((25.75,26.5,27.0)): put(scr[i],tc,-11.5,'check')
fx*=(0.5+0.5*np.cos(np.pi*np.clip((t-34.6)/0.4,0,1)))

# ---------- mix to -14 LUFS, true peak under -1 dBFS
def lufs(x):
    sf.write('/tmp/_m.wav',x,SR,subtype='PCM_24')
    o=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i','/tmp/_m.wav','-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
    I=float(o.split('I:')[-1].split('LUFS')[0]); TP=float(o.split('Peak:')[-1].split('dBFS')[0]); return I,TP
g=1.0
for _ in range(4):
    mix=music*g+fx[:,None]; I,TP=lufs(mix); g*=10**((-14.0-I)/20)
mix=music*g+fx[:,None]; I,TP=lufs(mix)
# peaks above the ceiling: transparent brick-wall limiter, then trim back to -14
for _ in range(3):
    sf.write('/tmp/_pre.wav',mix,SR,subtype='PCM_24')
    subprocess.run(['ffmpeg','-y','-v','error','-i','/tmp/_pre.wav','-af','alimiter=limit=0.80:attack=4:release=80:level=disabled:asc=1','-c:a','pcm_s24le','/tmp/_lim.wav'],check=True)
    lim,_=sf.read('/tmp/_lim.wav'); I,TP=lufs(lim)
    if abs(I+14.0)<0.08: break
    g*=10**((-14.0-I)/20); mix=music*g+fx[:,None]
mix=lim
sf.write(OUT,mix,SR,subtype='PCM_24')
print('music gain %.2f dB | mix %.1f LUFS, true peak %.1f dBFS | music peak %.1f dBFS | cues %d'%(db(g),I,TP,db(np.abs(music*g).max()),len(cues)))
for c in sorted(cues):
    if c[1]!='tecla': print('  %6.2f s  %-28s pico %.1f dBFS'%c)
print('  teclas: %d cliques entre 25.08 e 27.13 s, picos de -19 a -16 dBFS'%sum(1 for c in cues if c[1]=='tecla'))
np.save('/tmp/_fx.npy',fx); np.save('/tmp/_mus.npy',(music*g).mean(1))
