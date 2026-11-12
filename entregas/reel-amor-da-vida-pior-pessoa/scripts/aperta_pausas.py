# Encurta pausas longas dentro do mesmo take (nao emenda takes). Corta so o meio do silencio medido.
import sys, wave, json, numpy as np
src,dst,keep=sys.argv[1],sys.argv[2],float(sys.argv[3])
w=wave.open(src); sr=w.getframerate(); ch=w.getnchannels(); sw=w.getsampwidth()
x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).reshape(-1,ch).astype(np.float64)
m=np.abs(x).max(axis=1)/32768
win=int(sr*0.01); n=len(m)//win
env=np.array([m[i*win:(i+1)*win].max() for i in range(n)])
sil=env<10**(-50/20)
segs=[];i=0
while i<n:
    if sil[i]:
        j=i
        while j<n and sil[j]: j+=1
        segs.append((i*win,j*win)); i=j
    else: i+=1
out=[];pos=0;cuts=[];fade=int(sr*0.008)
for a,b in segs:
    d=(b-a)/sr
    if a==0 or b>=n*win-win or d<=keep: continue
    rm=int((d-keep)*sr); mid=(a+b)//2; c0=mid-rm//2; c1=c0+rm
    seg=x[pos:c0].copy(); seg[-fade:]*=np.linspace(1,0,fade)[:,None]; out.append(seg)
    cuts.append((round(c0/sr,3),round(c1/sr,3))); pos=c1
    x[pos:pos+fade]*=np.linspace(0,1,fade)[:,None]
out.append(x[pos:])
y=np.concatenate(out).astype(np.int16)
o=wave.open(dst,'w'); o.setnchannels(ch); o.setsampwidth(sw); o.setframerate(sr); o.writeframes(y.tobytes())
print(json.dumps({'cuts':cuts,'dur':round(len(y)/sr,3),'sil':[(round(a/sr,2),round(b/sr,2)) for a,b in segs]}))
