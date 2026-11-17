# Corta o take unico em 12 cenas, so dentro de silencio. Nao toca em palavra.
import numpy as np, subprocess, json, sys
SR=48000
raw=subprocess.run(['ffmpeg','-v','error','-i','audio_src/take.wav','-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
a=np.frombuffer(raw,np.float32).copy()
# cortes no meio dos silencios entre cenas (medidos com silencedetect e transcricao)
cuts=[0,6.4,10.30,19.6,26.2,37.70,50.3,54.8,65.1,68.4,75.9,85.7,len(a)/SR]
# observacao: entre cena 9 e 10 ha dois silencios (67.63-69.09 e 69.26-69.80); a regiao 69.09-69.26 e respiracao
cuts[9]=69.5
cuts[3]=19.5
START_OVERRIDE={3:19.9}  # cena 4 (indice 3): pula um clique isolado em 19,68 s
FR=int(SR*0.01)
def db(x): return 20*np.log10(np.sqrt(np.mean(x**2))+1e-12)
def speech_bounds(s,e,thr=-50):
    seg=a[int(s*SR):int(e*SR)]
    n=len(seg)//FR
    lv=np.array([db(seg[i*FR:(i+1)*FR]) for i in range(n)])
    on=np.where(lv>thr)[0]
    return s+on[0]*0.01, s+(on[-1]+1)*0.01, lv
def shorten_pauses(x, maxp=0.8, keep=0.7, thr=-50):
    # encurta pausas internas > maxp para keep, tirando o miolo do silencio
    n=len(x)//FR
    lv=np.array([db(x[i*FR:(i+1)*FR]) for i in range(n)])
    sil=lv<thr
    out=[];i=0;last=0
    while i<n:
        if sil[i]:
            j=i
            while j<n and sil[j]: j+=1
            L=(j-i)*0.01
            if L>maxp and i>0 and j<n:
                half=int(keep/2/0.01)
                out.append(x[last*FR:(i+half)*FR]); last=j-half
            i=j
        else: i+=1
    out.append(x[last*FR:])
    return np.concatenate(out)
meta=[]
for k in range(12):
    s,e=START_OVERRIDE.get(k,cuts[k]),cuts[k+1]
    on,off,_=speech_bounds(s,e)
    st=max(s,on-0.12); en=min(e,off+0.25)
    x=a[int(st*SR):int(en*SR)]
    x=shorten_pauses(x)
    # fade de 10 ms nas pontas, so sobre silencio
    f=int(0.01*SR); x[:f]*=np.linspace(0,1,f); x[-f:]*=np.linspace(1,0,f)
    fn=f'public/audio/cena-{k+1:02d}.wav'
    subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','1','-i','-','-c:a','pcm_s16le',fn],input=x.astype(np.float32).tobytes())
    d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',fn],capture_output=True,text=True).stdout)
    head=db(x[:int(0.1*SR)]); tail=db(x[-int(0.1*SR):])
    meta.append(dict(cena=k+1,src_start=float(round(st,3)),src_end=float(round(en,3)),dur=round(d,3),ponta_ini_db=float(round(head,1)),ponta_fim_db=float(round(tail,1))))
    print(meta[-1])
json.dump(meta,open('audio_src/split.json','w'),indent=1)
tot=sum(m['dur']+0.4 for m in meta); print('total',round(tot,2))
