import json, subprocess, numpy as np
S='/tmp/claude-0/-workspace-borderline-sem-estigmas/26c5b3dd-eefd-58ca-8efd-78a3cdd68057/scratchpad/'
w=json.load(open(S+'ad/words3.json'))
# offset same as build.py
raw=subprocess.run(['ffmpeg','-v','error','-i',S+'ad/narracao_B3.wav','-ac','1','-ar','24000','-f','f32le','-'],capture_output=True).stdout
a=np.frombuffer(raw,np.float32); win=120
db=20*np.log10(np.array([np.sqrt(np.mean(a[i*win:(i+1)*win]**2))+1e-9 for i in range(len(a)//win)]))
on=next(i for i in range(len(db)) if db[i]>-55)*win/24000; off=0.2-(on-0.03)
W=[{'text':x[2],'start':round(x[0]+off,3),'end':round(x[1]+off,3)} for x in w]
W[0]['start']=max(W[0]['start'],0.2)
for i,x in enumerate(W): print(i,x)
json.dump({'W':W},open(S+'ad/words3_timeline.json','w'),ensure_ascii=False)
# refine starts: if a silence (>=0.12s below -50dB) lies inside the word window, start after it
dt=win/24000
for i,x in enumerate(W):
    s=x['start']-off; e=x['end']-off
    i0=int(s/dt); i1=int(e/dt); run=0; last_sil=None
    for k in range(i0,i1):
        if db[k]<-50: run+=1
        else:
            if run*dt>=0.2: last_sil=k
            run=0
    if last_sil is not None:
        ns=round(last_sil*dt+off,3); print('refine',i,x['text'],x['start'],'->',ns); x['start']=ns
json.dump({'W':W},open(S+'ad/words3_timeline.json','w'),ensure_ascii=False)
