import subprocess,re,sys
SFX='../../memoria/sfx/editorpro/'; TOTAL=15.0
ev=[('Shutter_Camera.mp3',0.03,0.8),('HUD_Pop-Up2.mp3',1.58,0.7),('Whoosh_Swipe9.mp3',3.05,0.6),('Shutter_Camera2.mp3',4.78,0.8),('Whoosh_Fino6.mp3',5.25,1.2),
    ('Futurista_Click4.mp3',6.9,0.8),('Whoosh_Swipe9.mp3',7.62,0.6),('HUD_Pop-Up2.mp3',10.62,0.7),('HUD_Pop-Up2.mp3',11.64,0.7),('Shutter_Camera.mp3',12.53,0.8)]
def peak(f):
    r=subprocess.run(['ffmpeg','-i',f,'-af','volumedetect','-f','null','-'],capture_output=True,text=True).stderr
    return float(re.search(r'max_volume: (-?[0-9.]+)',r).group(1))
args=[];fc=[]
for i,(f,t,dur) in enumerate(ev):
    args+=['-i',SFX+f]; g=-27-peak(SFX+f); d=int(t*1000)
    fc.append(f"[{i}:a]atrim=0:{dur},aformat=channel_layouts=stereo,aresample=48000,volume={g:.1f}dB,afade=t=out:st={dur-0.15}:d=0.15,adelay={d}|{d}[s{i}]")
fc.append(''.join(f'[s{i}]' for i in range(len(ev)))+f"amix=inputs={len(ev)}:normalize=0,apad,atrim=0:{TOTAL}[x]")
subprocess.run(['ffmpeg','-v','error','-y']+args+['-filter_complex',';'.join(fc),'-map','[x]','/tmp/sfx.wav'],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i','assets/voz.wav','-i','/tmp/sfx.wav','-filter_complex',
 f"[0:a]aformat=channel_layouts=stereo,aresample=48000,loudnorm=I=-15:TP=-1.5,apad,atrim=0:{TOTAL}[v];[v][1:a]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1:LRA=11,afade=t=out:st={TOTAL-0.12}:d=0.12[m]",
 '-map','[m]','-ar','48000',sys.argv[1]],check=True)
