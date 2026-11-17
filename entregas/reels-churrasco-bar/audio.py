import subprocess, numpy as np, soundfile as sf
SR=48000
def load(f):
    r=subprocess.run(["ffmpeg","-v","error","-i",f,"-vn","-ac","2","-ar",str(SR),"-f","f32le","-"],capture_output=True,check=True).stdout
    return np.frombuffer(r,np.float32).reshape(-1,2).copy()
def xfade(a,b,d):
    n=int(round(d*SR)); t=np.linspace(0,1,n)[:,None]
    # equal-power
    mid=a[-n:]*np.cos(t*np.pi/2)+b[:n]*np.sin(t*np.pi/2)
    return np.concatenate([a[:-n],mid,b[n:]])
def seg(x,a,b): return x[int(round(a*SR)):int(round(b*SR))]
def finish(x,T,name):
    n=int(round(T*SR)); x=x[:n]
    assert len(x)==n,(len(x),n)
    f=int(0.5*SR); x[-f:]*=np.linspace(1,0,f)[:,None]
    sf.write(name,x,SR,subtype="PCM_16"); print(name,len(x)/SR)
c=load("churrasco_src.mp4")
# scene audio up to scene end + 0.15, crossfade 0.3 centred on the cut
sc=481/24
x=seg(c,0,sc+0.15); k=seg(c,10.5,13.5)
x=xfade(x,k,0.3); x=xfade(x,k,0.3)
finish(x,565/24,"churrasco_audio.wav")
b=load("bar_src.mp4")
d=2/24
x=xfade(seg(b,0,31/24+d/2),seg(b,114/24-d/2,19.6),d)
finish(x,385/24,"bar_audio.wav")
