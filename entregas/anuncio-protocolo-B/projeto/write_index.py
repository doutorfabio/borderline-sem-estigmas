import json
S='/tmp/claude-0/-workspace-borderline-sem-estigmas/26c5b3dd-eefd-58ca-8efd-78a3cdd68057/scratchpad/'
W=json.load(open(S+'ad/words3_timeline.json'))['W']
DUR=27.1667
T_CARD=15.5667
txt=[x['text'] for x in W]
def clean(t): return t.rstrip(',.')
# small caption groups: (first,last, line break before index or None)
GROUPS=[(0,2,None),(3,7,None),(8,12,11),(13,21,19),(22,25,None)]
groups=[]
for gi,(a,b,br) in enumerate(GROUPS):
    words=[{'t':clean(txt[i]),'s':W[i]['start'],'br':(i==br)} for i in range(a,b+1)]
    groups.append({'words':words})
# center build: FALAR, ABRAÇAR / OU SAIR DO QUARTO
C=[('FALAR,',30,0),('ABRAÇAR',32,0),('OU',33,1),('SAIR',35,1),('DO',36,1),('QUARTO',37,1)]
center=[{'t':t,'s':W[i]['start'],'line':l} for t,i,l in C]
C_START=center[0]['s']
for gi,g in enumerate(groups):
    g['start']=g['words'][0]['s']
    g['end']=groups[gi+1]['words'][0]['s'] if gi+1<len(groups) else C_START
html=open(S+'index_template.html').read()
html=html.replace('__GROUPS__',json.dumps(groups,ensure_ascii=False)).replace('__CENTER__',json.dumps(center,ensure_ascii=False))
html=html.replace('__DUR__',str(DUR)).replace('__TCARD__',str(T_CARD))
open(S+'hf/anuncio/index.html','w').write(html)
print(json.dumps(groups,ensure_ascii=False)[:600]); print(center)
