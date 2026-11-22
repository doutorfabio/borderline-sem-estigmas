import numpy as np, wave
w=wave.open('track.wav');sr=w.getframerate();x=np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2).mean(1)/32768
hop=256;win=1024
frames=[x[i:i+win]*np.hanning(win) for i in range(0,len(x)-win,hop)]
S=np.abs(np.fft.rfft(frames,axis=1))
flux=np.maximum(0,np.diff(np.log1p(S*50),axis=0)).sum(1)
thr=flux.mean()+1.5*flux.std()
peaks=[i for i in range(1,len(flux)-1) if flux[i]>thr and flux[i]>=flux[i-1] and flux[i]>flux[i+1]]
ts=[];
for p in peaks:
    t=(p+1)*hop/sr+win/2/sr*0  # frame start
    t=(p+1)*hop/sr
    if not ts or t-ts[-1]>0.5: ts.append(t)
import json;json.dump([round(t,3) for t in ts],open("beats.json","w"));print(len(ts),[round(t,3) for t in ts])
d=np.diff(ts); print('mean ibi',d.mean().round(4),'bpm',round(60/d.mean(),2))
