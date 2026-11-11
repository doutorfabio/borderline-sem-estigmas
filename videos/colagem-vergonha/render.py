import json,subprocess,re
V='/workspace/Novo/videos/colagem-vergonha/original-sem-audio.mp4'
N='/workspace/Novo/videos/colagem-vergonha/narracao-raw.wav'
SFX='/workspace/Novo/memoria/sfx/editorpro/'
OUT='/workspace/Novo/videos/colagem-vergonha/'
tl=json.load(open('tl.json')); caps=json.load(open('caps.json')); OFF=0.10; TOTAL=24.54
# 1 narration retimed
fc=[];ins=[]
for i,p in enumerate(tl['pieces']):
    s,e=p['src']; d=int((p['dst']+OFF)*1000)
    fc.append(f"[0:a]atrim={s}:{e},asetpts=PTS-STARTPTS,adelay={d}|{d}[p{i}]")
fc.append(''.join(f'[p{i}]' for i in range(len(tl['pieces'])))+f"amix=inputs={len(tl['pieces'])}:normalize=0,apad,atrim=0:{TOTAL},loudnorm=I=-16:TP=-1.5[v]")
subprocess.run(['ffmpeg','-v','error','-y','-i',N,'-filter_complex',';'.join(fc),'-map','[v]','-ar','48000','-ac','2','voz.wav'],check=True)
# 2 sfx track
ev=[('HUD_Pop-Up2.mp3',0.08,None),('Shutter_Vintage4.mp3',4.15,0.9),('Whoosh_Fino6.mp3',4.4,None),('HUD_Pop-Up2.mp3',7.0,None),
    ('HUD_Pop-Up2.mp3',10.8,None),('Whoosh_Fino6.mp3',11.95,None),('HUD_Pop-Up2.mp3',15.14,None),('Whoosh_Fino6.mp3',17.05,None),
    ('Shutter_Camera.mp3',19.45,None),('Futurista_Click4.mp3',21.3,None)]
def peak(f):
    r=subprocess.run(['ffmpeg','-i',f,'-af','volumedetect','-f','null','-'],capture_output=True,text=True).stderr
    return float(re.search(r'max_volume: (-?[0-9.]+)',r).group(1))
args=[];fc=[]
for i,(f,t,dur) in enumerate(ev):
    args+=['-i',SFX+f]; g=-27-peak(SFX+f); d=int(t*1000)
    tr=f"atrim=0:{dur}," if dur else ""
    fc.append(f"[{i}:a]{tr}aformat=channel_layouts=stereo,aresample=48000,volume={g:.1f}dB,afade=t=out:st={(dur or 3)-0.2 if dur else 2.8}:d=0.2,adelay={d}|{d}[s{i}]")
fc.append(''.join(f'[s{i}]' for i in range(len(ev)))+f"amix=inputs={len(ev)}:normalize=0,apad,atrim=0:{TOTAL}[x]")
subprocess.run(['ffmpeg','-v','error','-y']+args+['-filter_complex',';'.join(fc),'-map','[x]','sfx.wav'],check=True)
# 3 mix + loudness
subprocess.run(['ffmpeg','-v','error','-y','-i','voz.wav','-i','sfx.wav','-filter_complex',
 "[1:a][0:a]sidechaincompress=threshold=0.05:ratio=4:attack=10:release=250[d];[0:a][d]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1:LRA=11[m]",
 '-map','[m]','-ar','48000','mix.wav'],check=True)
# 4 video
segs=[(0,3.6,1.26),(3.6,4.2,1.0),(4.2,8.0,1.78),(8.0,14.0,0.8833),(14.0,15.3,1.6923),(15.3,18.0417,1.0)]
fc=[]
for i,(a,b,k) in enumerate(segs):
    fc.append(f"[0:v]trim={a}:{b},setpts=(PTS-STARTPTS)*{k}[g{i}]")
fc.append(''.join(f'[g{i}]' for i in range(len(segs)))+f"concat=n={len(segs)}:v=1:a=0,fps=30,scale=1080:1920:flags=lanczos,unsharp=5:5:0.6,tpad=stop_mode=clone:stop_duration=3,trim=0:{TOTAL},setsar=1[base]")
ovs=[('t_title',0.0,4.4),('t_machucou',7.0,11.9),('t_ruim',10.8,11.9),('t_patch',12.3,17.2),('t_julgamento',15.14,17.2),('t_stamp',19.75,TOTAL),('t_cta',21.3,TOTAL)]+[(c,s,e) for c,s,e in caps]
inputs=['-i',V]; last='base'
for j,(n,s,e) in enumerate(ovs):
    inputs+=['-loop','1','-t',str(TOTAL),'-i',n+'.png']
    fade=f",fade=t=in:st={s}:d=0.12:alpha=1" if not n.startswith('c') and n not in ('t_patch','t_title') else ""
    fc.append(f"[{j+1}:v]format=rgba{fade}[o{j}]")
    fc.append(f"[{last}][o{j}]overlay=0:0:enable='between(t,{s},{e})'[b{j}]"); last=f'b{j}'
inputs+=['-i','mix.wav']
subprocess.run(['ffmpeg','-v','error','-y']+inputs+['-filter_complex',';'.join(fc),'-map',f'[{last}]','-map',f'{len(ovs)+1}:a',
 '-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t',str(TOTAL),'-movflags','+faststart',OUT+'colagem-vergonha-v2.mp4'],check=True)
print('ok')
