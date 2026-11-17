# Monta src/timeline.json (duracao de cada cena = audio medido com ffprobe + 0,4 s) e out/legenda.srt
import json, subprocess, os
KEEP=[int(x) for x in os.environ.get('KEEP','1,2,3,4,5,6,7,8,9,10,11,12').split(',')]
SRT=os.environ.get('SRT','out/legenda.srt')
FPS=30; RESPIRO=0.4; FECHO_EXTRA=2.4
W=json.load(open('audio_src/words_cenas.json'))
# legenda fiel ao roteiro, numeros em algarismos; o numero e o indice da palavra (transcricao) onde o trecho comeca
CH={
1:[("Você já ouviu essa frase.",0),("Cuidado com ele.",5),("Não é psiquiatra, só atende psiquiatria.",8)],
2:[("Soa como proteção.",0),("Não é.",3)],
3:[("Pela norma dos conselhos de medicina,",0),("todo médico com CRM pode atender em qualquer área.",6),("Proibido é outra coisa:",15),("anunciar especialidade sem registro.",19)],
4:[("Eu sou médico, pós-graduado em psiquiatria.",0),("Não tenho título de especialista.",7),("Trabalhei mais de 5 anos em CAPS.",12)],
5:[("Agora faça a conta que ninguém faz.",0),("Os CAPS do país têm 10.129 vínculos de médico.",6),("3.127 são de clínico geral.",16),("Mais 434 de residente.",22)],
6:[("Aplique a frase.",0),("Só atende quem tem título.",3),("No mesmo dia,",8),("quase 4 em cada 10 postos de médico ficam vazios.",11),("E esse é o mínimo.",21)],
7:[("269 cidades ficam com o CAPS",0),("sem médico nenhum.",6)],
8:[("E quem entra no lugar?",0),("No país inteiro,",5),("13.581 médicos têm título de psiquiatra.",8),("A residência recebe 650 por ano.",15)],
9:[("Não fecha.",0),("Nem perto.",2)],
10:[("Repare em quem repete a frase.",0),("Ele nunca diz quem vai atender",5),("a pessoa em crise",11),("numa cidade pequena do interior.",15)],
11:[("Título é formação séria.",0),("Ninguém aqui está diminuindo residência.",4),("O que eu não aceito",9),("é usar o título para tirar o médico",14),("de 269 cidades.",22)],
12:[("Quem está em crise",0),("não pergunta o número do registro.",4),("Pergunta se tem médico.",10)],
}
# momentos-chave (indice de palavra) usados pela animacao e pelos efeitos
KEYS={5:{'n10129':11,'n3127':16,'n434':23},6:{'quase':11,'vazios':19,'minimo':21},7:{'n269':0},8:{'n13581':8,'n650':18},9:{'nem':2},11:{'n269':23},12:{'pergunta':10},3:{'pode':10,'proibido':15},2:{'naoe':3},1:{'cuidado':5},4:{'trabalhei':12},10:{'ele':5}}
def dur(p): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout)
scenes=[];t=0;srt=[];n=1
def ts(x):
    ms=int(round(x*1000)); return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"
for k in KEEP:
    d=dur(f'public/audio/cena-{k:02d}.wav')
    sec=d+RESPIRO+(FECHO_EXTRA if k==12 else 0)
    frames=round(sec*FPS)
    ws=W[str(k)]
    st=lambda i: max(0.0, ws[i][0]-0.05) if ws[i][0]>0 else 0.1
    chunks=[]
    for j,(txt,i) in enumerate(CH[k]):
        a=st(i)
        b=st(CH[k][j+1][1]) if j+1<len(CH[k]) else ws[-1][1]+0.35
        chunks.append(dict(text=txt,start=round(a,2),end=round(b,2)))
        srt.append(f"{n}\n{ts(t+a)} --> {ts(t+b)}\n{txt}\n"); n+=1
    keys={kk:round(st(v),2) for kk,v in KEYS.get(k,{}).items()}
    scenes.append(dict(id=k,audio=f'audio/cena-{k:02d}.wav',audioDur=round(d,3),from_=round(t*FPS),frames=frames,chunks=chunks,keys=keys,speechEnd=round(ws[-1][1],2)))
    t+=frames/FPS
json.dump(dict(fps=FPS,total=sum(s['frames'] for s in scenes),scenes=scenes),open('src/timeline.json','w'),ensure_ascii=False,indent=1)
open(SRT,'w').write('\n'.join(srt))
print('total s',round(t,2)); [print(s['id'],s['audioDur'],s['frames'],s['keys']) for s in scenes]
