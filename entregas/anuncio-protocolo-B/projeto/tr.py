import sys, json, subprocess, numpy as np
from faster_whisper import WhisperModel
wav=sys.argv[1]; size=sys.argv[2]
raw=subprocess.run(['ffmpeg','-v','error','-i',wav,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
a=np.frombuffer(raw,np.float32)
fala="Você leu tudo, assistiu a todos os vídeos e tentou entender cada crise, mas na hora em que ela desaba no chão nada disso te diz se é hora de falar, de abraçar ou de sair do quarto. O Protocolo 7 Dias é um curso online para familiares de quem tem borderline, com sete procedimentos para saber o que fazer na crise."
m=WhisperModel(size,device='cpu',compute_type='int8')
segs,_=m.transcribe(a,language='pt',word_timestamps=True,initial_prompt=fala,beam_size=5)
out=[]
for s in segs:
  for w in s.words: out.append([round(w.start,3),round(w.end,3),w.word.strip()])
json.dump(out,open(sys.argv[3],'w'),ensure_ascii=False)
print(' '.join(w[2] for w in out))
for w in out: print(w)
