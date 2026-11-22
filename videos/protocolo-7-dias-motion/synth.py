import numpy as np, wave
sr=48000; bpm=90; spb=60/bpm; t0=0.30; dur=12.6
N=int(sr*dur); out=np.zeros(N)
def note(f, start, amp, length=2.2):
    n=int(sr*length); t=np.arange(n)/sr
    s=np.zeros(n)
    for h,a in [(1,1),(2,.45),(3,.22),(4,.12),(5,.06),(6,.03)]:
        fh=f*h*(1+0.0004*h*h)
        s+=a*np.sin(2*np.pi*fh*t)*np.exp(-t*(1.6+1.1*h))
    s*=np.minimum(1,t/0.004)  # hammer attack
    i=int(start*sr); j=min(N,i+n); out[i:j]+=amp*s[:j-i]
m=lambda k:440*2**((k-69)/12)
# chords per bar (beats 0-3,4-7,8-11,12-15): Am  F  C  G->C final
bars=[(57,[45,57,60,64]),(53,[41,53,57,60]),(55,[48,55,60,64]),(55,[43,55,59,62])]
pulse=[69,72,69,67]
for k in range(16):
    t=t0+k*spb; b=k//4
    if k%4==0:
        for p in bars[b][1]: note(m(p),t,0.20,3.5)
    note(m(pulse[b]+ (0 if k%2==0 else -0)),t,0.30 if k%4==0 else 0.17,1.6)
# final resolve on beat 16
t=t0+16*spb
for p in [36,48,55,60,64,67]: note(m(p),t,0.18,dur-t)
out/=np.max(np.abs(out))*1.15
fade=int(0.25*sr); out[-fade:]*=np.linspace(1,0,fade)
with wave.open('track_raw.wav','wb') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((out*32767).astype(np.int16).tobytes())
