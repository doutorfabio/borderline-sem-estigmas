import subprocess, json, re
SFX='/home/user/borderline-sem-estigmas/memoria/sfx/editorpro/'
def run(cmd): return subprocess.run(cmd,capture_output=True,text=True)
# 1) voice: p1[0,24.0] + p2[0.29167,end], tiny fades at the join (cut sits in silence, -61 dB)
run(['ffmpeg','-v','error','-y','-i','src/p1.mov','-i','src/p2.mov','-filter_complex',
 '[0:a]atrim=0:24.0,asetpts=PTS-STARTPTS,afade=t=out:st=23.99:d=0.01[a];[1:a]atrim=start=0.291667,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.01[b];[a][b]concat=n=2:v=0:a=1,aresample=48000[v]',
 '-map','[v]','-ac','2','-c:a','pcm_s24le','voice_raw.wav'])
def loud(f):
    r=run(['ffmpeg','-hide_banner','-i',f,'-af','loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-f','null','-'])
    j=json.loads(r.stderr[r.stderr.rindex('{'):]); return float(j['input_i']),float(j['input_tp'])
I,TP=loud('voice_raw.wav'); g=-14.5-I
print('voice I',I,'TP',TP,'gain',round(g,2))
run(['ffmpeg','-v','error','-y','-i','voice_raw.wav','-af',f'volume={g:.2f}dB','-c:a','pcm_s24le','voice.wav'])
# 2) sfx events: (file, event time, align offset in file, target peak dBFS, file peak dBFS)
P={'Whoosh_Swipe9':(0.160,-2.4),'Whoosh_Fino6':(0.747,-9.2),'Futurista_Click4':(0.086,4.4),'Futurista_Click7':(0.053,6.3),'HUD_Pop-Up2':(0.062,-2.3)}
EV=[('Whoosh_Swipe9',13.48,-16),('Futurista_Click4',16.04,-20),('Whoosh_Fino6',19.98,-15),('Futurista_Click4',22.90,-20),
    ('Whoosh_Swipe9',25.20,-16),('Futurista_Click4',26.61,-20),('Whoosh_Fino6',35.92,-15),('HUD_Pop-Up2',37.08,-18),
    ('Whoosh_Swipe9',41.70,-16),('Futurista_Click7',43.10,-21),
    ('Futurista_Click7',9.04,-22),('Futurista_Click7',16.60,-22),('Futurista_Click7',24.01,-22),('Futurista_Click7',29.57,-22),('Futurista_Click7',41.19,-22),
    ('Futurista_Click4',6.02,-23),('Futurista_Click4',33.03,-23),('Futurista_Click4',47.17,-23)]
inputs=['-i','voice.wav']; fl=[]; lab=['[0:a]']
for i,(f,t,tp) in enumerate(EV):
    off,pk=P[f]; d=max(0,t-off); gain=tp-pk
    inputs+=['-i',SFX+f+'.mp3']
    fl.append(f'[{i+1}:a]aresample=48000,aformat=channel_layouts=stereo,volume={gain:.2f}dB,adelay={int(d*1000)}|{int(d*1000)}[s{i}]'); lab.append(f'[s{i}]')
fl.append(''.join(lab)+f'amix=inputs={len(lab)}:normalize=0:dropout_transition=0,alimiter=limit=0.89:level=false:attack=3:release=60[m]')
r=run(['ffmpeg','-v','error','-y']+inputs+['-filter_complex',';'.join(fl),'-map','[m]','-t','49.7083','-c:a','pcm_s24le','mix.wav'])
print(r.stderr[-500:])
I2,TP2=loud('mix.wav'); g2=-14.0-I2
run(['ffmpeg','-v','error','-y','-i','mix.wav','-af',f'volume={g2:.2f}dB,alimiter=limit=0.87:level=false:attack=3:release=60','-c:a','pcm_s24le','mix_final.wav'])
I3,TP3=loud('mix_final.wav'); print('final I',I3,'TP',TP3)
