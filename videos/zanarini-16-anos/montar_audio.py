# Corta cada linha nas pontas medidas (-55 dB), monta a narração e grava os tempos reais.
import json, subprocess, re
W = json.load(open("audio/words.json"))
GAP_AFTER = {"L01":0.55,"L02":0.25,"L03":1.0,"L04":0.6,"L05":0.2,"L06":0.45,"L07":0.25,"L08":0.75,"L09":0.3,"L10":2.2}
LEAD = 0.6
def speech_bounds(f):
    o = subprocess.run(["ffmpeg","-hide_banner","-i",f,"-af","silencedetect=n=-55dB:d=0.08","-f","null","-"],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r"silence_start: ([0-9.]+)",o)]
    en=[float(x) for x in re.findall(r"silence_end: ([0-9.]+)",o)]
    return en[0], st[-1]
t = LEAD; out=[]; parts=[]
for k in sorted(W):
    a,b = speech_bounds(f"audio/{k}.mp3")
    cs, ce = max(0,a-0.06), b+0.12          # margem nas pontas, nada cortado
    subprocess.run(["ffmpeg","-y","-v","error","-i",f"audio/{k}.mp3","-ss",f"{cs:.3f}","-to",f"{ce:.3f}","-ar","48000","-ac","1",f"audio/{k}_cut.wav"],check=True)
    start = t; dur = ce-cs
    words=[{"w":x["w"],"s":round(start+x["s"]-cs,3),"e":round(start+x["s"]-cs+x["d"],3)} for x in W[k].get("words",[])]  # voz própria: deixe "words" vazio
    out.append({"id":k,"texto":W[k]["text"],"inicio":round(start,3),"fim":round(start+dur,3),"fala_inicio":round(start+a-cs,3),"fala_fim":round(start+b-cs,3),"palavras":words})
    parts.append((start,f"audio/{k}_cut.wav"))
    t = start+dur+GAP_AFTER[k]
total = round(t,3)
json.dump({"duracao_total":total,"linhas":out},open("tempos.json","w"),ensure_ascii=False,indent=1)
# mix
inputs=[];filt=[]
for i,(s,f) in enumerate(parts):
    inputs+=["-i",f]; filt.append(f"[{i}]adelay={int(s*1000)}|{int(s*1000)}[a{i}]")
filt.append("".join(f"[a{i}]" for i in range(len(parts)))+f"amix=inputs={len(parts)}:normalize=0,apad,atrim=0:{total}[o]")
subprocess.run(["ffmpeg","-y","-v","error",*inputs,"-filter_complex",";".join(filt),"-map","[o]","-ar","48000","audio/narracao.wav"],check=True)
def ts(x): h=int(x//3600);m=int(x%3600//60);s=x%60;return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".",",")
with open("legenda.srt","w") as f:
    for i,l in enumerate(out,1): f.write(f"{i}\n{ts(l['fala_inicio'])} --> {ts(l['fala_fim']+0.25)}\n{l['texto']}\n\n")
print(total); [print(l["id"],l["inicio"],l["fim"],l["texto"]) for l in out]
