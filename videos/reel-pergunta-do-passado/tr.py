import sys, json
from faster_whisper import WhisperModel
m = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
import wave, numpy as np
w=wave.open(sys.argv[1]); a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768.0
segs, info = m.transcribe(a, language="pt", word_timestamps=True, vad_filter=False, beam_size=5,
    initial_prompt="Borderline, transtorno de personalidade borderline, Dr. Fabio Schmidt.")
out=[]
for s in segs:
    for w in s.words:
        out.append({"text":w.word.strip(),"start":round(w.start,3),"end":round(w.end,3),"p":round(w.probability,2)})
    print(round(s.start,2), round(s.end,2), s.text, flush=True)
json.dump(out, open(sys.argv[2],"w"), ensure_ascii=False, indent=0)
