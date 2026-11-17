import subprocess, json
def run(cmd): return subprocess.run(cmd,capture_output=True,text=True)
def loud(f):
    r=run(['ffmpeg','-hide_banner','-i',f,'-af','loudnorm=I=-14:TP=-1.5:print_format=json','-f','null','-'])
    j=json.loads(r.stderr[r.stderr.rindex('{'):]); return float(j['input_i']),float(j['input_tp'])
HP='highpass=f=120:poles=2,highpass=f=120:poles=2'
run(['ffmpeg','-v','error','-y','-i','music_raw.wav','-af',HP,'-c:a','pcm_s24le','music_hp.wav'])
Im,_=loud('music_hp.wav'); Iv,_=loud('voice.wav')
TARGET_BELOW=9.0
g=(Iv-TARGET_BELOW)-Im
print('music hp I',Im,'voice I',Iv,'music gain',round(g,2))
# ducked music stem (for measurement) and full mix
fc=(f"[0:a]{HP},volume={g:.2f}dB[m];[1:a]asplit=2[v1][v2];"
    f"[m][v2]sidechaincompress=threshold=0.10:ratio=2:attack=15:release=400:knee=4:makeup=1[md];"
    f"[md]asplit=2[md1][md2];"
    f"[v1]asplit=2[v1a][v1b];[2:a][v1b]sidechaincompress=threshold=0.10:ratio=1.6:attack=10:release=250:knee=4:makeup=1[sd];"
    f"[v1a][md1][sd]amix=inputs=3:normalize=0:dropout_transition=0[mix]")
r=run(['ffmpeg','-v','error','-y','-i','music_raw.wav','-i','voice.wav','-i','sfx_bus.wav','-filter_complex',fc,
       '-map','[mix]','-c:a','pcm_s24le','mix2_raw.wav','-map','[md2]','-c:a','pcm_s24le','music_ducked.wav'])
print(r.stderr[-400:])
Id,_=loud('music_ducked.wav'); print('music ducked I',Id,'-> below voice by',round(Iv-Id,1),'LU')
I,TP=loud('mix2_raw.wav'); print('mix raw I',I,'TP',TP)
best=None
for extra in [0.0,0.3,0.6,0.9]:
    gg=-14.0-I+extra
    run(['ffmpeg','-v','error','-y','-i','mix2_raw.wav','-af',f'volume={gg:.2f}dB,aresample=192000,alimiter=limit=0.76:level=false:attack=2:release=50,aresample=48000','-c:a','pcm_s24le',f'mix2_{extra}.wav'])
    I2,TP2=loud(f'mix2_{extra}.wav'); print(' extra',extra,'-> I',I2,'TP',TP2)
    if best is None or abs(I2+14.0)<abs(best[1]+14.0): best=(extra,I2,TP2)
print('best',best)
import shutil; shutil.copy(f'mix2_{best[0]}.wav','audio_final4.wav')
