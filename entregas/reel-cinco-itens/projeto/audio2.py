import subprocess, json, numpy as np, wave
SR=48000
LIB='/home/user/borderline-sem-estigmas/memoria/sfx/editorpro/'
AUD='aud/'
def run(cmd): return subprocess.run(cmd,capture_output=True,text=True)
def load(p,a=None,b=None):
    cmd=['ffmpeg','-v','error']
    if a is not None: cmd+=['-ss',f'{a:.4f}']
    if b is not None: cmd+=['-t',f'{b-a:.4f}']
    cmd+=['-i',p,'-ac','2','-ar',str(SR),'-f','f32le','-']
    raw=subprocess.run(cmd,capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.float32).reshape(-1,2).copy()
def save(p,x):
    x=np.clip(x,-1,1); subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','2','-i','-','-c:a','pcm_s24le',p],input=x.astype(np.float32).tobytes())
def fade(x,fi=0.01,fo=0.03):
    n=len(x); a=int(fi*SR); b=int(fo*SR); y=x.copy()
    if a>0: y[:a]*=np.linspace(0,1,a)[:,None]
    if b>0: y[-b:]*=np.linspace(1,0,b)[:,None]
    return y
def peak_db(x): return 20*np.log10(np.abs(x).max()+1e-9)
def to_peak(x,db): return x*10**((db-peak_db(x))/20)
def hp(x,fc):  # 2x cascaded one-pole high-pass (12 dB/oct), zero-phase not needed
    import math
    y=x.astype(np.float64).copy()
    for _ in range(2):
        rc=1/(2*math.pi*fc); dt=1/SR; al=rc/(rc+dt)
        out=np.zeros_like(y); prev_x=y[0].copy(); prev_y=np.zeros(2)
        # vectorised via lfilter-like recursion
        from numpy import empty
        for ch in range(2):
            xi=y[:,ch]; o=np.empty_like(xi); py=0.0; px=xi[0]
            for i in range(len(xi)):
                py=al*(py+xi[i]-px); px=xi[i]; o[i]=py
            out[:,ch]=o
        y=out
    return y.astype(np.float32)
def resample(x,factor):  # play faster by 'factor' (pitch up)
    n=int(len(x)/factor); idx=np.linspace(0,len(x)-1,n)
    return np.stack([np.interp(idx,np.arange(len(x)),x[:,c]) for c in range(2)],1).astype(np.float32)
DUR=49.7083; N=int(DUR*SR)
sfx=np.zeros((N+SR,2),np.float32)
def put(x,t):
    i=int(round(t*SR)); 
    if i<0: x=x[-i:]; i=0
    j=min(len(sfx),i+len(x)); sfx[i:j]+=x[:j-i]
log=[]
# ---- 1 wire (take 79a20e47): creak while INDO EMBORA hangs, release while it recedes
w=fade(load(AUD+'79a20e47-Taut_Steel_Wire.wav',0.10,1.95),0.02,0.25); w=to_peak(w,-18.0); put(w,14.56-0.07); log.append(('fio',14.49,peak_db(w)))
# ---- 2 coin (take e9d6eb5e): wobble under the orbit, hit on VERDADE, last click on 'dentro.'
c=fade(load(AUD+'e9d6eb5e-Coin_Wobble.wav',0.0,3.15),0.03,0.08); c=to_peak(c,-18.0); put(c,23.54-2.955); log.append(('moeda',23.54-2.955,peak_db(c)))
# ---- 3 ticks (take f63c7ffe): six knocks transposed up one to two octaves, rising, during the growth of REAÇÃO
src=load(AUD+'f63c7ffe-Rising_Ticks.wav')
on=[0.145,0.355,0.530,0.710,0.895,1.115]
tk=np.zeros((int(1.6*SR),2),np.float32)
for k,o in enumerate(on):
    seg=src[int((o-0.012)*SR):int((o+0.16)*SR)]
    seg=to_peak(seg,-3.0)                                   # even out the six knocks
    f=2**((12+2.4*k)/12); r=fade(resample(seg,f),0.002,0.02)
    i=int((o-0.10-0.012/f)*SR); tk[i:i+len(r)]+=r
tk=hp(tk,170); tk=to_peak(tk,-18.0); put(tk,25.50); log.append(('trena',25.50,peak_db(tk)))
# ---- 4 flaps (take 66ccb64b): fast run under the scrolling rows, last flap on DEIXA / MAIS / FACIL
fl=fade(load(AUD+'66ccb64b-Final_Flap-Clacks.wav',2.55,3.75),0.09,0.07); fl=to_peak(fl,-20.5); put(fl,35.85)
one=fade(load(AUD+'66ccb64b-Final_Flap-Clacks.wav',4.06,4.40),0.004,0.08)
for t,db in [(37.108,-17.5),(37.668,-19.0),(38.088,-18.0)]: put(to_peak(one,db),t-0.04)
log.append(('letreiro',35.85,-13.0))
# ---- 5 card (take 2fca42ad): slide when the card comes in, stamp on RESUMO
sl=fade(load(AUD+'2fca42ad-Card_Slide_and_Soft_Stamp.wav',1.50,1.84),0.01,0.08); sl=to_peak(sl,-19.0); put(sl,41.25-0.05)
stp=fade(load(AUD+'2fca42ad-Card_Slide_and_Soft_Stamp.wav',3.20,3.62),0.004,0.12); stp=hp(stp,100); stp=to_peak(stp,-17.5); put(stp,43.748-0.04)
log.append(('ficha',41.61,-13.0))
# ---- library: transitions that have no custom sound, numerals, zooms
P={'Whoosh_Swipe9':0.160,'Whoosh_Fino6':0.747,'Futurista_Click4':0.086,'Futurista_Click7':0.053}
EV=[('Whoosh_Swipe9',3.75,-20.5),('Whoosh_Swipe9',13.48,-20),('Whoosh_Fino6',19.98,-20),('Futurista_Click4',16.04,-21.5),('Futurista_Click4',26.61,-21.5),
    ('Futurista_Click7',9.04,-22),('Futurista_Click7',16.875,-22),('Futurista_Click7',24.06,-22),('Futurista_Click7',29.57,-22),
    ('Futurista_Click4',6.125,-23),('Futurista_Click4',33.167,-23),('Futurista_Click4',47.292,-23)]
for f,t,db in EV:
    x=load(LIB+f+'.mp3'); put(to_peak(x,db),t-P[f])
sfx=hp(sfx[:N],90)
save('sfx_bus.wav',sfx)
# ---- music (take 069a2a0b, 53.2 s): drop the first bar so the real ending lands on the last words
T0=2.345
m=load(AUD+'069a2a0b-Alert_Motif.wav',T0,T0+DUR+0.4)[:N]
m=fade(m,0.02,0.12)
save('music_raw.wav',m)
for name,t,p in log: print(f'{name:9s} entra em {t:6.2f}s  pico {p:5.1f} dBFS')
