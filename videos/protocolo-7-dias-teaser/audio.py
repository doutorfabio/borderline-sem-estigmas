import numpy as np
SR=48000; D=10.0; n=int(SR*D); t=np.arange(n)/SR
def load(name):
    a=np.fromfile(f'sfx_{name}.raw',dtype=np.float32).reshape(-1,2); return a
def env_ad(tt,a,d): return np.where(tt<a,tt/a,np.exp(-(tt-a)/d))
L=np.zeros((n,2))
def note(f): return 440*2**((f-69)/12)
# 5 bars of 4 beats at 120 BPM; Am F C G Am(sus) keeps the loop calm
chords=[[57,60,64,69],[53,57,60,65],[48,55,60,64],[55,59,62,67],[57,60,64,71]]
bass=[45,41,48,43,45]
for b,ch in enumerate(chords):
    t0=b*2.0; seg=(t>=t0)&(t<t0+2.0+0.6); tt=t[seg]-t0
    pad=np.zeros(seg.sum())
    for m in ch:
        f=note(m)
        for det in (-0.12,0.12):
            pad+=np.sin(2*np.pi*f*(1+det/100)*tt+det)*0.5
    e=np.clip(tt/0.5,0,1)*np.clip((2.6-tt)/0.6,0,1)
    L[seg,0]+=pad*e*0.018; L[seg,1]+=pad*e*0.018
    # soft bass on beat 1 and 3
    for bb in (0,1.0):
        s=(t>=t0+bb)&(t<t0+bb+1.0); x=t[s]-t0-bb; f=note(bass[b])
        v=(np.sin(2*np.pi*f*x)+0.3*np.sin(4*np.pi*f*x))*env_ad(x,0.01,0.35)*0.10
        L[s]+=v[:,None]
    # gentle pluck arpeggio on each beat (felt piano feel)
    for k in range(4):
        s=(t>=t0+k*0.5)&(t<t0+k*0.5+0.6); x=t[s]-t0-k*0.5; f=note(ch[(k*2)%4]+12)
        v=(np.sin(2*np.pi*f*x)+0.25*np.sin(2*np.pi*2*f*x))*env_ad(x,0.004,0.18)*0.045
        pan=0.35 if k%2 else -0.35
        L[s,0]+=v*(1-pan); L[s,1]+=v*(1+pan)
# very soft shaker on off-beats
rng=np.random.default_rng(7)
for k in range(20):
    s0=int((k*0.5+0.25)*SR); m=int(0.06*SR); nz=rng.standard_normal(m)
    nz=np.diff(np.concatenate([[0],nz]))*np.exp(-np.arange(m)/(0.015*SR))*0.012
    L[s0:s0+m,0]+=nz*0.8; L[s0:s0+m,1]+=nz
# SFX at the contacts
def put(name,at,g,dur=None):
    a=load(name); 
    if dur: m=int(dur*SR); a=a[:m]*np.clip((m-np.arange(len(a[:m])))/(0.03*SR),0,1)[:,None]
    i=int(at*SR); j=min(n,i+len(a)); L[i:j]+=a[:j-i]*g
db=lambda x:10**(x/20)
put('Futurista_Click4',0.5,db(-12),0.25)
put('Futurista_Click4',1.5,db(-16),0.2)
for s in [1.75,2,2.25,2.5,2.75,3.0]: put('Futurista_Click7',s,db(-22),0.12)
for s in [3.5,4.0,4.5]: put('HUD_Pop-Up2',s-0.05,db(-15),0.4)
put('Futurista_Click4',5.0,db(-16),0.2)
put('Whoosh_Fino6',5.05,db(-24),0.6)
for s in [5.75+i*0.25 for i in range(7)]: put('Futurista_Click7',s,db(-18),0.1)
put('UI_Interface6',7.5,db(-14),0.6)
put('Futurista_Click4',9.35,db(-16),0.2)
put('Futurista_Click7',9.5,db(-20),0.12)
L[-int(0.05*SR):]*=np.linspace(1,0,int(0.05*SR))[:,None]
L/=np.max(np.abs(L))*1.12
L.astype(np.float32).tofile('mix.raw')
