import json,re
W=json.load(open("words.json"))
# fixes
W=[[a,b,("Rivotril" if w.startswith("Ribotril") else w)] for a,b,w in W]
W=[x for x in W if x[0]<30]
W+= [[30.84,31.06,"Então,"],[31.06,31.34,"graças"],[31.34,31.44,"a"],[31.44,31.72,"Deus,"],[31.72,31.84,"eu"],[31.84,31.94,"estou"],[31.94,32.22,"bem."],
     [32.28,32.66,"Pode"],[32.66,33.04,"ficar..."],[33.04,33.28,"Pera"],[33.28,33.6,"aí."],[34.26,34.70,"Que"],[34.70,35.1,"foi?"]]
W[0][0]=0.10;W[1][0]=0.10;W[0][1]=0.10
HL={"tudo","remédio","dois","dias.","semana","nem","tomei.","Rivotril","tranquilo.","dez","anos,","vicia,","natural.","CBD,","gotinhas.","terra","arsênico.","bem.","Pera","aí."}
# group: max 3 words, break after punctuation or pause>0.25
PL="Ah, doutor,|meu caso é|complicado, viu?|Porque eu já|tomei tudo isso|aqui de remédio|e nada adiantou.|Esse aqui eu|tomei dois dias.|Foi uma semana|quase.|Daí esse daqui|eu nem tomei.|Ah, doutor,|o Rivotril é|super tranquilo.|Eu uso|tem dez anos,|todos os dias.|Não vicia, não.|Doutor, eu queria|fazer um tratamento|mais natural.|De repente, CBD,|umas gotinhas.|Tudo que vem|da terra|é bom, né?|Menos arsênico.|Então,|graças a Deus,|eu estou bem.|Pode ficar...|Pera aí.|Que foi?".split("|")
groups=[];i=0
for p in PL:
  n=len(p.split()); g=W[i:i+n]; assert [x[2] for x in g]==p.split(),(p,[x[2] for x in g]); groups.append(g); i+=n
assert i==len(W)
def t(s):
  h=int(s//3600);m=int(s%3600//60);sec=s%60;return f"{h}:{m:02d}:{sec:05.2f}"
FLASH=[0.033,8.033,13.367,21.433,30.900]
LAB=[("O QUE JÁ TOMOU","DE TUDO"),("O FIEL DO","RIVOTRIL"),("O DO TRATAMENTO","NATURAL"),("O QUE OLHA COM","ESSA CARA"),("O QUE SE DEU","ALTA SOZINHO")]
ENDS=[8.033,13.367,19.833,30.900,35.43]
CX=502
hdr=f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Montserrat ExtraBold,108,&H00FFFFFF,&H00FFFFFF,&H00000000,&H78000000,0,0,0,0,100,100,0,0,1,0,4,5,0,0,0,1
Style: Lab,Montserrat ExtraBold,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H8C000000,0,0,0,0,100,100,0,0,1,0,3,5,0,0,0,1
Style: Pill,Montserrat ExtraBold,58,&H00FFFFFF,&H00FFFFFF,&H000D0D0D,&H00000000,0,0,0,0,100,100,2,0,3,10,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev=[]
RED="&H303BFF&"
CY=1290
for gi,g in enumerate(groups):
  s=g[0][0]; e=g[-1][1]
  for j,(a,b,w) in enumerate(g):
    st=a; en=(g[j+1][0] if j+1<len(g) else min(e+0.35, (groups[gi+1][0][0] if gi+1<len(groups) else 35.4)))
    parts=[]
    for k,(a2,b2,w2) in enumerate(g):
      if k>j: break
      word=w2
      if w2 in HL: txt=r"{\c"+RED+r"\fs124}"+word.upper()+r"{\r}"
      else: txt=word
      if k==j: txt=r"{\fscx112\fscy112\t(0,90,\fscx100\fscy100)}"+txt+r"{\fscx100\fscy100}"
      parts.append(txt)
    ev.append(f"Dialogue: 2,{t(st)},{t(en)},Cap,,0,0,0,,{{\\an2\\pos({CX},1335)\\blur1.2}}"+" ".join(parts))
import json
P=json.load(open("labpos.json")) if __import__("os").path.exists("labpos.json") else {"pill":200,"l1":302,"l2":402}
def mv(y): return f"\\move({CX},{y+24},{CX},{y},0,200)\\fad(120,100)"
for i,(f,(l1,l2),end) in enumerate(zip(FLASH,LAB,ENDS)):
  a,b=f,end
  ev.append(f"Dialogue: 4,{t(a)},{t(b)},Pill,,0,0,0,,{{{mv(P['pill'])}\\c&H303BFF&}}PACIENTE {i+1}")
  ev.append(f"Dialogue: 4,{t(a)},{t(b)},Lab,,0,0,0,,{{{mv(P['l1'])}\\fs80\\blur1}}{l1}")
  ev.append(f"Dialogue: 4,{t(a)},{t(b)},Lab,,0,0,0,,{{{mv(P['l2'])}\\fs124\\blur1}}{l2}")
open("cap.ass","w").write(hdr+"\n".join(ev)+"\n")
