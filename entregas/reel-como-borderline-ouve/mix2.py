import subprocess,numpy as np,json
SR=48000; S='/home/user/borderline-sem-estigmas/memoria/sfx/editorpro/'
C=json.load(open('cues.json')); T=C['end']
def load(f,a=None,b=None):
    x=np.frombuffer(subprocess.run(['ffmpeg','-v','quiet','-i',S+f,'-af','highpass=f=120','-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout,dtype=np.float32).copy()
    if a is not None: x=x[int(a*SR):int(b*SR)]
    n=int(.01*SR); x[:n]*=np.linspace(0,1,n); x[-n*3:]*=np.linspace(1,0,n*3); return x
sfx=np.zeros(int(T*SR)+SR,np.float32)
def place(x,at,db):
    x=x/np.abs(x).max()*10**(db/20); pk=np.abs(x).argmax(); s=int(at*SR)-pk
    if s<0: x=x[-s:]; s=0
    sfx[s:s+len(x)]+=x[:len(sfx)-s]
sw=load('Whoosh_Swipe9.mp3'); fi=load('Whoosh_Fino6.mp3',0.45,1.05); ck=load('Futurista_Click7.mp3')
for st in C['starts'][1:]: place(fi,st-0.05,-30)          # folha caindo
for h in C['hear']: place(sw,h,-30); place(ck,h+0.13,-32)  # chicote e batida
v=np.fromfile('work/narr_cut.f32',dtype=np.float32)
v=np.pad(v,(0,max(0,len(sfx)-len(v))))[:len(sfx)]
open('work/voice.f32','wb').write(v.tobytes()); open('work/sfx2.f32','wb').write(sfx.tobytes())
