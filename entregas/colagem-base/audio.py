# uso: audio.py <pasta-da-peca> <duracao> <saida.wav>   (le sfx.json da peca: [[arquivo, t, dur], ...]; voz opcional em assets/voz.wav)
import subprocess,re,sys,json,os
P,TOTAL,OUT=sys.argv[1],float(sys.argv[2]),sys.argv[3]
SFX=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','memoria','sfx','editorpro')+'/'
ev=json.load(open(os.path.join(P,'sfx.json')))
def peak(f):
    r=subprocess.run(['ffmpeg','-i',f,'-af','volumedetect','-f','null','-'],capture_output=True,text=True).stderr
    return float(re.search(r'max_volume: (-?[0-9.]+)',r).group(1))
voz=os.path.join(P,'assets','voz.wav'); tem=os.path.exists(voz); alvo=-27 if tem else -18
args=[];fc=[]
for i,(f,t,dur) in enumerate(ev):
    args+=['-i',SFX+f]; g=alvo-peak(SFX+f); d=int(t*1000)
    fc.append(f"[{i}:a]atrim=0:{dur},aformat=channel_layouts=stereo,aresample=48000,volume={g:.1f}dB,afade=t=out:st={dur-0.15}:d=0.15,adelay={d}|{d}[s{i}]")
fc.append(''.join(f'[s{i}]' for i in range(len(ev)))+f"amix=inputs={len(ev)}:normalize=0,apad,atrim=0:{TOTAL}[x]")
subprocess.run(['ffmpeg','-v','error','-y']+args+['-filter_complex',';'.join(fc),'-map','[x]','/tmp/_sfx.wav'],check=True)
if tem:
    subprocess.run(['ffmpeg','-v','error','-y','-i',voz,'-i','/tmp/_sfx.wav','-filter_complex',
     f"[0:a]aformat=channel_layouts=stereo,aresample=48000,loudnorm=I=-15:TP=-1.5,apad,atrim=0:{TOTAL}[v];[v][1:a]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1:LRA=11,afade=t=out:st={TOTAL-0.12}:d=0.12[m]",
     '-map','[m]','-ar','48000',OUT],check=True)
else:
    subprocess.run(['ffmpeg','-v','error','-y','-i','/tmp/_sfx.wav','-ar','48000',OUT],check=True)
