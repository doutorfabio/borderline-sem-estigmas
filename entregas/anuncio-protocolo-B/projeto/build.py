import os, sys, json, subprocess, math, numpy as np
A='/tmp/claude-0/-workspace-borderline-sem-estigmas/26c5b3dd-eefd-58ca-8efd-78a3cdd68057/scratchpad/ad/'
narr=sys.argv[1]; words=json.load(open(sys.argv[2])); out=sys.argv[3]
def run(c): return subprocess.run(c,capture_output=True,text=True)
raw=subprocess.run(['ffmpeg','-v','error','-i',narr,'-ac','1','-ar','24000','-f','f32le','-'],capture_output=True).stdout
a=np.frombuffer(raw,np.float32); sr=24000; win=120
db=20*np.log10(np.array([np.sqrt(np.mean(a[i*win:(i+1)*win]**2))+1e-9 for i in range(len(a)//win)]))
dt=win/sr
on=next(i for i in range(len(db)) if db[i]>-55)*dt
trim=on-0.03
assert db[int(trim/dt)-2:int(trim/dt)].max()<-60, ('trim not silent', db[int(trim/dt)-4:int(trim/dt)])
# O Protocolo
wi=[i for i,w in enumerate(words) if w[2].lower().startswith('quarto')][0]
qend=words[wi][1]; ostart_w=words[wi+1][0]
i0=int(qend/dt)
while not (db[i0:i0+30]<-60).all(): i0+=1
oon=next(i for i in range(i0,len(db)) if db[i]>-55)*dt
last=max(i for i in range(len(db)) if db[i]>-55)*dt
off=0.2-trim
T_CARD=round((oon+off)*30)/30
CTA=math.ceil((last+off+0.25)*30)/30; END=CTA+2.0
NF=round(END*30); NCARD=round(T_CARD*30)
print('onset',on,'O',oon,'last',last,'T_CARD',T_CARD,'CTA',CTA,'END',END,'pause before O',oon-qend)
def ws(k): return words[k][0]+off
idx=lambda txt,start=0: next(i for i in range(start,len(words)) if words[i][2].lower().strip(',.').startswith(txt))
i_ass=idx('assistiu'); i_e=idx('e',i_ass+1); i_mas=idx('mas'); i_nada=idx('nada'); i_se=idx('se',i_nada)
t=[0.2,ws(i_ass),ws(i_e),ws(i_mas),ws(i_nada),ws(i_se)]
t=[round(x*30)/30 for x in t]
print('caption times',t)
# audio: linear gain + limiter
n=run(['ffmpeg','-v','info','-i',narr,'-af','ebur128','-f','null','-']).stderr
I=float([l for l in n.split('\n') if l.strip().startswith('I:')][-1].split()[1])
g=-14-I
af=f"[2:a]atrim=start={trim:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.005,areverse,afade=t=in:d=0.04,areverse,aresample=48000,volume={g+0.7:.2f}dB,adelay=200|200[na];[3:a]aresample=48000,volume=0.15,afade=t=out:st=13.88:d=0.2[sa];[4:a]aresample=48000,volume=0.4,adelay={int(T_CARD*1000)}|{int(T_CARD*1000)}[ca];[na][sa][ca]amix=inputs=3:normalize=0:duration=longest,apad,atrim=0:{END:.3f},aresample=192000,alimiter=limit=0.81:attack=1:release=60:level=disabled,aresample=48000[aout]"
vf=f"""[0:v]tpad=stop_mode=clone:stop_duration=5,trim=end_frame={NCARD},setpts=PTS-STARTPTS[a];
[1:v]tpad=stop_mode=clone:stop_duration=15,trim=end_frame={NF-NCARD},setpts=PTS-STARTPTS[b];
[a][b]concat=n=2:v=1:a=0,fps=30,format=yuv420p[v0];
[11:v]format=rgba,fade=t=in:st={T_CARD+3:.3f}:d=0.25:alpha=1[ti];
[12:v]format=rgba,fade=t=in:st={CTA:.3f}:d=0.2:alpha=1[ct];
[v0][5:v]overlay=0:0:enable='between(t,{t[0]},{t[1]-0.001:.3f})'[v1];
[v1][6:v]overlay=0:0:enable='between(t,{t[1]:.3f},{t[2]-0.001:.3f})'[v2];
[v2][7:v]overlay=0:0:enable='between(t,{t[2]:.3f},{t[3]-0.001:.3f})'[v3];
[v3][8:v]overlay=0:0:enable='between(t,{t[3]:.3f},{t[4]-0.001:.3f})'[v4];
[v4][9:v]overlay=0:0:enable='between(t,{t[4]:.3f},{t[5]-0.001:.3f})'[v5];
[v5][10:v]overlay=0:0:enable='between(t,{t[5]:.3f},{T_CARD-0.004:.3f})'[v6];
[v6][ti]overlay=0:0:enable='gte(t,{T_CARD+3:.3f})'[v7];
[v7][ct]overlay=0:0:enable='gte(t,{CTA:.3f})',trim=end_frame={NF},setpts=PTS-STARTPTS[vout];"""
cmd=['ffmpeg','-v','error','-y','-i',A+'cena30.mp4','-i',A+'cartao30.mp4','-i',narr,'-i',A+'cena.mp4','-i',A+'cartao.mp4']
for n_ in ['cap0','cap1','cap2','cap3','cap4','centro','titulo','cta']: cmd+=['-loop','1','-i',A+os.environ.get('OVDIR','ov')+'/'+n_+'.png']
cmd+=['-filter_complex',vf+af,'-map','[vout]','-map','[aout]','-c:v','libx264','-crf','16','-preset','slow','-profile:v','high','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','192k','-movflags','+faststart','-t',f'{END:.3f}',out]
r=run(cmd); print(r.stderr[-2000:])
