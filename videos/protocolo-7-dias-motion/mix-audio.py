import subprocess
U='/root/.claude/uploads/26cd057b-9dac-5e89-bcf6-11acc79ab25e/'
B=U+'72806f02-Seven_Blocks_One_Stack.m4a'; M1=U+'51bfb766-Marker_Underline.m4a'; M2=U+'011458c8-Marker_Underline.m4a'; F1=U+'5333c1e5-Dry_Room_Foley.m4a'
def cut(name,src,ss,t,fi=0.005,fo=0.03,hp=90):
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(ss),'-t',str(t),'-i',src,'-af',f'highpass=f={hp},afade=t=in:d={fi},afade=t=out:st={t-fo}:d={fo},aformat=sample_rates=48000:channel_layouts=stereo',name+'.wav'],check=True)
knocks=[1.02,1.81,2.785,3.785,4.675,5.615,6.41]
for i,k in enumerate(knocks): cut(f'k{i}',B,k-0.01,0.28,hp=140)
cut('stack',B,18.44,0.5,hp=140)
cut('scrape',M1,18.2,0.26)
cut('write',M2,20.2,0.8,fi=0.05,fo=0.12,hp=400)
cut('flip',F1,0.05,0.4,hp=200)
# (file, time, gain dB)
ev=[]
# tipo grande caindo (só uma batida leve por bloco)
for t in [0.28,2.56,4.8,6.36,12.24]: ev.append(('k1',t-0.005,-10))
# trocas secas: virada de papel com pico no corte
for t in [3.8,8.4,11.2]: ev.append(('flip',t-0.17,-5))
# canetão
ev+= [('scrape',1.3,-12),('scrape',7.86,-11),('scrape',8.04,-13),('scrape',10.0,-11),('scrape',12.5,-13)]
for t0 in [1.5,7.2,10.3]:
    ev+=[('scrape',t0,-12),('scrape',t0+0.21,-14),('scrape',t0+0.42,-13)]
# sete blocos: pouso e quique
for n in range(1,8):
    t=8.42+(n-1)*0.075; T=0.36 if n<=4 else 0.44
    ev.append((f'k{n-1}',t+T-0.005,-7)); ev.append((f'k{n-1}',t+T+0.36-0.005,-16))
ins=[];fl=[]
for i,(f,t,g) in enumerate(ev):
    ins+=['-i',f+'.wav']; ms=int(round(t*1000)); fl.append(f'[{i}]adelay={ms}|{ms},volume={g}dB[a{i}]')
fl.append(''.join(f'[a{i}]' for i in range(len(ev)))+f'amix=inputs={len(ev)}:normalize=0,apad=whole_dur=15,atrim=0:15[mx]')
subprocess.run(['ffmpeg','-v','error','-y',*ins,'-filter_complex',';'.join(fl),'-map','[mx]','-ar','48000','stem_raw.wav'],check=True)
