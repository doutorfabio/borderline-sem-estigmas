# Som: papel (sintetizado, a biblioteca nao tem papel amassado) + efeitos de memoria/sfx. Sem musica. Silencio no ultimo segundo.
import numpy as np, subprocess, sys
from scipy.signal import butter, sosfilt
SR=48000; DUR=10.0; N=int(SR*DUR)
SFX='/home/user/borderline-sem-estigmas/memoria/sfx/'
def load(path):
    raw=subprocess.run(['ffmpeg','-loglevel','error','-i',path,'-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).astype(np.float64)
def bp(x,lo,hi,order=2):
    if lo and hi: sos=butter(order,[lo,hi],'bandpass',fs=SR,output='sos')
    elif lo: sos=butter(order,lo,'highpass',fs=SR,output='sos')
    else: sos=butter(order,hi,'lowpass',fs=SR,output='sos')
    return sosfilt(sos,x)
def norm(x,peak_db): return x/np.abs(x).max()*10**(peak_db/20)
def fade(x,a=0.004,r=0.03):
    x=x.copy(); na=int(a*SR); nr=int(r*SR)
    x[:na]*=np.linspace(0,1,na); x[-nr:]*=np.linspace(1,0,nr)**2; return x
def crackle(n,dens,rng,tau=0.0012,klen=0.006):
    """estalos de fibra: impulsos esparsos com amplitude desigual, cada um um sopro curto de ruido"""
    p=dens/SR; imp=(rng.random(n)<p)*rng.lognormal(0,0.9,n)*rng.choice([-1,1],n)
    k=rng.normal(0,1,int(klen*SR))*np.exp(-np.arange(int(klen*SR))/(tau*SR))
    return np.convolve(imp,k)[:n]
def crumple(dur,seed):
    rng=np.random.default_rng(seed); n=int(dur*SR); t=np.arange(n)/SR
    dens=1100*(np.exp(-((t-0.20)/0.13)**2)+0.75*np.exp(-((t-0.58)/0.12)**2)+0.35*np.exp(-((t-0.83)/0.06)**2))+50
    a=bp(crackle(n,dens,rng),1300,9500)
    b=bp(crackle(n,dens*0.35,rng,tau=0.003,klen=0.014),450,1800)*0.45
    am=np.clip(bp(rng.normal(0,1,n),None,28),0,None); am/=am.max()
    r=bp(rng.normal(0,1,n),2200,7500)*(dens/dens.max())**1.3*(0.35+0.65*am)*0.22
    return fade(a/np.abs(a).max()+b/np.abs(b).max()*0.45+r/np.abs(r).max()*0.30,0.015,0.10)
def rustle(dur,seed,bright=1.0):
    """papel que desliza ou encosta"""
    rng=np.random.default_rng(seed); n=int(dur*SR); t=np.arange(n)/SR
    env=np.exp(-t/(dur*0.28))
    a=bp(crackle(n,1600*env+40,rng),1500*bright,8500)
    r=bp(rng.normal(0,1,n),1800*bright,6500)*env
    return fade(a/np.abs(a).max()+0.55*r/np.abs(r).max(),0.003,dur*0.4)
mix=np.zeros(N)
def put(x,t,peak_db):
    i=int(t*SR); x=norm(x,peak_db); j=min(N,i+len(x)); mix[i:j]+=x[:j-i]
F=lambda f: f/24.0
# 0,0-1,0 s: papel amassado
put(crumple(0.97,3),0.02,-6.0)
# biblioteca dele
ficha=load(SFX+'gerados/Ficha_deslizando_e_carimbo.m4a')
slide=fade(bp(ficha[int(1.44*SR):int(1.95*SR)],220,None),0.01,0.12)
stamp=fade(bp(ficha[int(3.17*SR):int(3.85*SR)],150,None),0.004,0.18)
letr=load(SFX+'gerados/Letreiro_de_aeroporto.m4a')
flap=fade(bp(letr[int(1.30*SR):int(1.50*SR)],220,None),0.003,0.08)
shut=load(SFX+'editorpro/Shutter_Camera.mp3')
proj=fade(bp(shut[int(0.11*SR):int(0.47*SR)],250,None),0.004,0.06)
# 1,0 s: a tira do chao entra
put(slide,F(24)-0.02,-14)
# mao sobe em 3 saltos (o som cai no salto, depois da antecipacao)
for k,f in enumerate((30,38,46)): put(rustle(0.16,10+k,1.0+0.12*k),F(f),-13+k)
# figura cai e e apanhada
put(rustle(0.30,20,1.35),F(49),-24)
put(rustle(0.11,21,0.9),F(58),-11)
# A GENTE ENDURECE: uma batida por palavra
for k,f in enumerate((84,87,90)): put(flap,F(f),-10+ (1.5 if k==2 else 0))
# falha de projetor e a mao abre
put(proj,F(132)-0.01,-12)
# pisa no papel
put(rustle(0.08,30,0.8),F(150),-18)
# digital batida
put(stamp,F(152)-0.012,-4.0)
# mao sai de quadro
put(slide[::-1].copy(),F(161),-17)
# frase vermelha: uma batida por palavra
for k in range(6): put(flap,F(192+3*k),-11.5+(1.5 if k==5 else 0))
mix=bp(mix,140,None)
mix[int(9.0*SR):]=0.0                      # silencio no ultimo segundo
mix[int(8.9*SR):int(9.0*SR)]*=np.linspace(1,0,int(0.1*SR))
print('pico %.1f dBFS'%(20*np.log10(np.abs(mix).max())))
st=np.stack([mix,mix],1).astype(np.float32)
import wave
with wave.open(sys.argv[1],'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(st,-1,1)*32767).astype(np.int16).tobytes())
