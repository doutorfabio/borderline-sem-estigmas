import json,sys
S=sys.argv[1]
W=json.load(open(S+'/work/words.json'))
# (first index, spec) ; "/" = line break ; "*" = highlight ; words map in order
C=[
(0,"O *BORDERLINE/PERGUNTA"),(3,"DO SEU/*PASSADO"),(6,"MESMO SABENDO QUE"),(9,"VOCÊ ESCOLHEU/FICAR"),
(12,"DE FORA"),(14,"ISSO GANHA"),(16,"NOME DE"),(18,"*CIÚME/*DOENTIO"),
(20,"POR BAIXO"),(22,"TEM *MEDO"),(24,"DE NÃO *BASTAR"),
(27,"SÃO *TRÊS/PERGUNTAS"),(30,"E QUASE SEMPRE"),(33,"AS MESMAS"),
(36,"COMO QUE ERA"),(39,"COM A PESSOA"),(42,"DE *ANTES?"),
(45,"VOCÊ ERA"),(47,"MAIS *FELIZ"),(49,"NAQUELA ÉPOCA?"),
(52,"SE ESSA PESSOA"),(55,"VOLTASSE"),(56,"VOCÊ IA/*EMBORA?"),
(59,"PERCEBE QUE"),(61,"AS TRÊS/PERGUNTAM"),(64,"A *MESMA *COISA?"),
(67,"EU *BASTO","hero"),(69,"PRA VOCÊ/*FICAR?","hero"),
(72,"SE É VOCÊ"),(75,"QUEM RESPONDE"),(77,"UMA RESPOSTA/*CALMA"),
(80,"UMA VEZ"),(82,"AQUELA PESSOA/EXISTIU"),(85,"HOJE EU"),(87,"*ESCOLHO/*VOCÊ"),
(89,"VOCÊ NÃO PRECISA"),(92,"ABRIR O CELULAR"),(95,"E CONTAR TUDO"),(98,"PRA *PROVAR"),
(100,"SE VOCÊ É"),(103,"QUEM PERGUNTA"),
(105,"A *QUARTA/PERGUNTA"),(108,"*NÃO *ACALMA"),(110,"MAIS QUE"),(112,"A PRIMEIRA"),
(114,"ESSE MEDO"),(116,"SE *TRATA"),
(118,"E A RESPOSTA"),(121,"NUNCA VAI"),(123,"DAR CONTA DELA"),(126,"*SOZINHA"),
(127,"*MANDA/PRA QUEM"),(130,"VOCÊ QUERIA"),(132,"QUE ENTENDESSE"),(134,"DE ONDE VEM"),(137,"TODAS ESSAS/PERGUNTAS"),
]
skip={35,44,51}
import unicodedata
def norm(s): return ''.join(c for c in unicodedata.normalize('NFD',s.lower()) if c.isalnum())
chunks=[];used=set()
for c in C:
    i=c[0]; lines=[]
    for ln in c[1].split('/'):
        L=[]
        for tok in ln.split():
            hl=tok.startswith('*'); t=tok.lstrip('*')
            assert norm(t)==norm(W[i]['text']),(t,W[i]['text'],i)
            L.append({'w':t,'s':W[i]['start'],'e':W[i]['end'],'hl':hl}); used.add(i); i+=1
        lines.append(L)
    chunks.append({'lines':lines,'hero':len(c)>2,'t0':lines[0][0]['s'],'e':lines[-1][-1]['e']})
assert used|skip==set(range(len(W))), set(range(len(W)))-used-skip
for a,b in zip(chunks,chunks[1:]): a['t1']=b['t0']-0.02 if b['t0']-a['e']<0.9 else a['e']+0.5
chunks[-1]['t1']=99
for l in chunks[0]['lines']:
    for w in l: w['s']=-1
chunks[0]['t0']=-1
cuts=[3.7333,5.6667,6.7333,8.5333,9.8,10.6333,11.1333,13.0333,14.6,15.4667,16.4333,17.8333,21.5667,24.4667,27.5,30.6,31.1,34.7333,38.4333]
zooms=[[6.7333,8.5333,1.0,1.06],[17.8333,21.5667,1.0,1.09],[24.4667,27.5,1.0,1.07],[34.7333,38.4333,1.0,1.07],[38.4333,41.27,1.03,1.08]]
chip=[{'n':1,'t0':W[35]['start'],'t1':W[44]['start']},{'n':2,'t0':W[44]['start'],'t1':W[51]['start']},{'n':3,'t0':W[51]['start'],'t1':17.76},{'n':4,'t0':17.76,'t1':19.9,'merge':W[65]['start']}]
json.dump({'chunks':chunks,'cuts':cuts,'zooms':zooms,'chip':chip,'dur':41.2667},open('data.js','w'),ensure_ascii=False)
s=open('data.js').read(); open('data.js','w').write('window.DATA='+s)
print(len(chunks))
