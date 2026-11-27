import numpy as np, json, subprocess, sys
S=sys.argv[1]; TL=sys.argv[2]; OUT=sys.argv[3]
LIB='/workspace/borderline-sem-estigmas/memoria/sfx/editorpro/'
SR=48000
def load(f,maxdur=None):
    raw=subprocess.run(['ffmpeg','-loglevel','error','-i',LIB+f,'-ac','2','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
    a=np.frombuffer(raw,np.float32).reshape(-1,2).copy()
    if maxdur:
        n=int(maxdur*SR); a=a[:n]; f=min(len(a),int(0.08*SR)); a[-f:]*=np.linspace(1,0,f)[:,None]
    # high-pass 150 Hz (rule: no low end)
    from numpy.fft import rfft,irfft,rfftfreq
    for c in range(2):
        X=rfft(a[:,c]); fr=rfftfreq(len(a),1/SR); X[fr<150]*=0; a[:,c]=irfft(X,len(a))
    return a
LIBMAP={'click':[('Futurista_Click4.mp3',None),('Futurista_Click7.mp3',None)],'shutter2':[('Shutter_Camera2.mp3',None)],
 'shutter':[('Shutter_Camera.mp3',None)],'hud':[('HUD_Pop-Up2.mp3',None)],
 'whoosh0':[('Whoosh_Swipe9.mp3',None)],'whoosh1':[('Whoosh_Fino6.mp3',None)],'impact':[('Digital_Camera2.mp3',None)]}
PEAK={'click':-31,'shutter2':-27,'shutter':-28,'hud':-27,'whoosh0':-27,'whoosh1':-27,'impact':-26}
tl=json.load(open(TL)); N=int((tl['total']+0.3)*SR); mix=np.zeros((N,2),np.float32)
cache={}; cnt={}
for name,t in sorted(tl['events'],key=lambda e:e[1]):
    opts=LIBMAP[name]; i=cnt.get(name,0); cnt[name]=i+1
    f,md=opts[i%len(opts)]
    if f not in cache: cache[f]=load(f,md)
    a=cache[f]; env=np.abs(a).max(1); pk=int(np.argmax(env))
    g=10**(PEAK[name]/20)/max(env.max(),1e-6)
    st=int(t*SR)-(pk if name.startswith('whoosh') else 0)
    st=max(0,st); seg=a[:max(0,min(len(a),N-st))]*g
    mix[st:st+len(seg)]+=seg
print('peak dBFS',20*np.log10(np.abs(mix).max()+1e-9))
mix=mix[:int(tl['total']*SR)]
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','f32le','-ar',str(SR),'-ac','2','-i','-','-c:a','pcm_s16le',OUT],input=mix.tobytes())
