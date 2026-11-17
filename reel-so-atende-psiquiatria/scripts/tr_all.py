import json, numpy as np, subprocess
from faster_whisper import WhisperModel
m=WhisperModel('medium',device='cpu',compute_type='int8')
res={}
for k in range(1,13):
  p=f'public/audio/cena-{k:02d}.wav'
  raw=subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
  a=np.frombuffer(raw,np.float32)
  segs,_=m.transcribe(a,language='pt',word_timestamps=True,beam_size=5,initial_prompt='CAPS, CRM, psiquiatria.')
  ws=[[round(w.start,2),round(w.end,2),w.word.strip()] for s in segs for w in s.words]
  res[k]=ws; print(k,' '.join(f"{w[2]}[{w[0]}]" for w in ws))
json.dump(res,open('audio_src/words_cenas.json','w'),ensure_ascii=False)
