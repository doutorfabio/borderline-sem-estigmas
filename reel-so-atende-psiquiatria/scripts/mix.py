# Mixagem: voz (12 arquivos, cada um no inicio da sua cena) + tique nos numeros + som abafado quando os postos somem. Final -14 LUFS.
import json, subprocess, re
tl=json.load(open('src/timeline.json')); S={s['id']:s for s in tl['scenes']}
start=lambda i: S[i]['from_']/30
ticks=[(5,'n10129'),(5,'n3127'),(5,'n434'),(6,'quase'),(7,'n269'),(8,'n13581'),(8,'n650'),(11,'n269')]
inputs=[];filt=[];labels=[]
for i in range(1,13):
    inputs+=['-i',f'public/audio/cena-{i:02d}.wav']; d=int(round(start(i)*1000))
    filt.append(f'[{len(inputs)//2-1}:a]aresample=48000,pan=stereo|c0=c0|c1=c0,adelay={d}|{d}[v{i}]'); labels.append(f'[v{i}]')
for j,(i,k) in enumerate(ticks):
    inputs+=['-i','public/sfx/tique.wav']; d=int(round((start(i)+S[i]['keys'][k])*1000))
    filt.append(f'[{len(inputs)//2-1}:a]aresample=48000,pan=stereo|c0=c0|c1=c0,volume=-33dB,adelay={d}|{d}[t{j}]'); labels.append(f'[t{j}]')
inputs+=['-i','public/sfx/abafado.wav']; d=int(round((start(6)+S[6]['keys']['vazios'])*1000))
filt.append(f'[{len(inputs)//2-1}:a]aresample=48000,pan=stereo|c0=c0|c1=c0,volume=-24dB,adelay={d}|{d}[ab]'); labels.append('[ab]')
total=tl['total']/30
filt.append(''.join(labels)+f'amix=inputs={len(labels)}:normalize=0:duration=longest,apad,atrim=0:{total:.3f}[m]')
fc=';'.join(filt)
subprocess.run(['ffmpeg','-v','error','-y',*inputs,'-filter_complex',fc,'-map','[m]','-c:a','pcm_s24le','out/tmp/mix_raw.wav'],check=True)
r=subprocess.run(['ffmpeg','-hide_banner','-i','out/tmp/mix_raw.wav','-af','loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True).stderr
m=json.loads(r[r.rindex('{'):])
ln=f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
subprocess.run(['ffmpeg','-v','error','-y','-i','out/tmp/mix_raw.wav','-af',ln+',aresample=48000','-c:a','pcm_s16le','out/tmp/mix.wav'],check=True)
print(subprocess.run(['ffmpeg','-hide_banner','-i','out/tmp/mix.wav','-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr.split('Summary:')[1])
