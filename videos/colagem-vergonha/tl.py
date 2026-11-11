import json
segs=[(0.0,4.534),(6.034,6.522),(7.630,9.448),(11.242,12.207),(13.235,14.805),(16.037,17.437),(18.716,21.416),(22.422,24.082),(24.785,26.1)]
gaps=[0.65,0.45,0.55,0.45,0.65,0.45,0.70,0.50]
PRE,POST=0.12,0.30
pieces=[];t=0.0
for i,(a,b) in enumerate(segs):
    s=max(0,a-PRE); e=min(26.1,b+POST)
    if i==0: s=0
    pieces.append({'src':[s,e],'dst':t}); t+= (e-s)
    if i<len(gaps): t+= gaps[i]-(PRE+POST)
total=t
words=[l.split() for l in """0.00 0.22 Por
0.22 0.36 que
0.36 0.42 o
0.42 0.94 borderline
0.94 1.10 se
1.10 1.66 defende
1.66 2.40 até
2.40 3.14 quando
3.14 3.82 sabe
3.82 4.06 que
4.06 4.42 errou?
5.68 6.44 Ouviu:
7.28 7.92 aquela
7.92 8.40 frase
8.40 8.78 me
8.78 9.42 machucou.
10.56 11.32 Por
11.32 11.68 dentro,
11.68 12.02 chegou:
13.22 13.56 você
13.56 13.92 é
13.92 14.02 uma
14.02 14.36 pessoa
14.36 14.68 ruim.
16.24 16.50 Aí
16.50 16.74 vem
16.74 16.84 a
16.84 17.30 explicação.
19.12 19.38 E
19.38 19.46 a
19.46 19.78 briga
19.78 20.22 vira
20.22 20.68 julgamento
20.68 20.90 de
20.90 21.38 caráter.
22.58 23.18 Dá
23.18 23.34 para
23.34 23.74 começar
23.74 24.02 por:
24.88 24.88 eu
24.88 25.44 entendi
25.44 25.70 que
25.70 26.02 doeu.""".strip().split('\n')]
def remap(x):
    for p in pieces:
        s,e=p['src']
        if s-0.05<=x<=e+0.05: return p['dst']+(x-s)
    # in a removed gap: map to nearest following piece start
    for p in pieces:
        if x<p['src'][0]: return p['dst']
    return total
W=[{'w':w[2],'s':round(remap(float(w[0])),3),'e':round(remap(float(w[1])),3)} for w in words]
W[-4]['s']=round(remap(24.79),3)
json.dump({'pieces':pieces,'total':total,'words':W},open('tl.json','w'),ensure_ascii=False,indent=1)
print(round(total,2));
for p in pieces: print([round(v,2) for v in p['src']],round(p['dst'],2))
for w in W: print(w)
