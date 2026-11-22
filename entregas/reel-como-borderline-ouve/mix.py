import subprocess,numpy as np,json
SR=48000; S='/home/user/borderline-sem-estigmas/memoria/sfx/editorpro/'
def load(f,a=None,b=None):
    x=np.frombuffer(subprocess.run(['ffmpeg','-v','quiet','-i',S+f,'-af','highpass=f=120','-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout,dtype=np.float32).copy()
    if a is not None: x=x[int(a*SR):int(b*SR)]
    n=int(.015*SR); x[:n]*=np.linspace(0,1,n); x[-n*3:]*=np.linspace(1,0,n*3)
    return x
slides=[(2.4,None)]  # (dur, rip)
D=[2.4,3.0,3.0,3.2,3.3,3.4,3.5,4.2]; R=[None,1.00,1.05,1.25,1.00,1.30,1.20,1.40]
T=sum(D); out=np.zeros(int((T+0.5)*SR),np.float32)
def place(x,peak_t,at,db):
    x=x/np.abs(x).max()*10**(db/20); s=int((at-peak_t)*SR)
    if s<0: x=x[-s:]; s=0
    out[s:s+len(x)]+=x[:len(out)-s]
sw=load('Whoosh_Swipe9.mp3'); fi=load('Whoosh_Fino6.mp3',0.45,1.05); ck=load('Futurista_Click7.mp3')
pk=lambda x:np.abs(x).argmax()/SR
t=0; log=[]
for d,r in zip(D,R):
    if r is not None:
        place(sw,pk(sw),t+0.28,-20); place(fi,pk(fi),t+r+0.10,-18); place(ck,pk(ck),t+r+0.12,-22)
        log.append(dict(queda=round(t+.28,2),rasgo=round(t+r+.1,2)))
    t+=d
out=out[:int(T*SR)]
st=np.repeat(out[:,None],2,1)
open('work/sfx.f32','wb').write(st.astype(np.float32).tobytes())
print(json.dumps(log)); print('peak dBFS %.1f'%(20*np.log10(np.abs(out).max())))
