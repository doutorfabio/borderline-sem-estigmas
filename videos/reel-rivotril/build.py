import json,unicodedata
W=json.load(open('words.json'))
C=[(0,"DOUTOR,/PELO AMOR"),(3,"DE DEUS,"),(5,"FALA AQUI"),(7,"PARA O/PESSOAL"),(10,"QUE *RIVOTRIL"),(12,"NÃO É/LEGAL,"),
(15,"*BENZODIAZEPÍNICOS.","hero"),(16,"É, A GENTE"),(19,"*EVITA,"),(20,"*EVITA/MUITO,"),(22,"EVITA MUITO/*MESMO."),
(25,"MAS É"),(27,"*EVITÁVEL,/NÉ?"),(29,"PORQUE,/INCLUSIVE,"),(31,"O BENZODIAZEPÍNICO"),(33,"TEM A/TENDÊNCIA"),(36,"A *PIORAR"),
(38,"ALGUMAS DAS/SITUAÇÕES"),(41,"QUE A/GENTE VÊ"),(45,"CORRIQUEIRAMENTE"),(46,"NOS PACIENTES"),(48,"COM O/*BORDERLINE."),
(51,"ENTÃO, É/EVITAR"),(54,"AO *MÁXIMO/MESMO,"),(57,"É *EVITAR.","hero")]
norm=lambda s:''.join(c for c in unicodedata.normalize('NFD',s.lower()) if c.isalnum())
chunks=[];used=set()
for c in C:
    i=c[0];lines=[]
    for ln in c[1].split('/'):
        L=[]
        for tok in ln.split():
            hl=tok.startswith('*');t=tok.lstrip('*')
            assert norm(t)==norm(W[i]['text']),(t,W[i]['text'],i)
            L.append({'w':t,'s':W[i]['start'],'e':W[i]['end'],'hl':hl});used.add(i);i+=1
        lines.append(L)
    chunks.append({'lines':lines,'hero':len(c)>2,'t0':lines[0][0]['s'],'e':lines[-1][-1]['e']})
assert used==set(range(len(W)))
for a,b in zip(chunks,chunks[1:]): a['t1']=b['t0']-0.02 if b['t0']-a['e']<0.9 else a['e']+0.5
chunks[-1]['t1']=99
chunks[0]['t0']=-1
for w in chunks[0]['lines'][0]: w['s']=-1
open('data.js','w').write('window.DATA='+json.dumps({'chunks':chunks},ensure_ascii=False))
print(len(chunks))
