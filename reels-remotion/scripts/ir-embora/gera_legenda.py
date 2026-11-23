# Gera src/IrEmbora/legenda.ts a partir da transcrição palavra por palavra.
# Cada bloco tem até 3 palavras (ou até 16 letras). *x* = recorte creme, **x** = recorte vermelho.
# Linhas com # ficam fora da legenda (trechos com texto grande na tela), mas consomem as palavras.
import json, re, unicodedata, os
aqui = os.path.dirname(os.path.abspath(__file__))
ws = [w for s in json.load(open(os.path.join(aqui, 'words.json'))) for w in s['words']]
BLOCOS = """
E se eu tiver
as duas coisas
ao mesmo tempo,
**BORDERLINE**
e *PÂNICO?*
Uma parte minha
quer correr
e a outra
morre de pavor
de ficar sozinha.
Então eu faço
o pior dos dois,
**EU FICO.**
Fico no lugar
que me assusta,
perto de pessoas
que *NÃO ME ATURAM,*
mas tendo que
fazer aquele
*SORRISINHO*
e dizer que
tá adorável.
Então você fica
com o celular
na mão esperando
uma resposta
que *NÃO VEM,*
daí você olha
de novo
e não vem
de novo,
daí você pede
*DESCULPA*
por perguntar,
pede desculpa
por *EXISTIR,*
aí todo mundo
pergunta,
mas por que você
**NÃO TERMINA ENTÃO?**
# E embora sempre vai parecer mais perigoso do que ficar.
# Relação ruim ainda parece melhor do que relação nenhuma.
Não é que eu
goste de sofrer,
mas é que
o meu **MEDO**
já escolheu
por mim.
No dia que
esse medo
*AMENIZA,*
# você volta a ter controle sobre si.
Se você também
é assim,
deixa um *LIKE* aqui.
""".strip().split('\n')
def norm(s):
    s = unicodedata.normalize('NFD', s.lower())
    return re.sub(r'[^a-z]', '', ''.join(c for c in s if unicodedata.category(c) != 'Mn'))
i = 0
blocos = []
for linha in BLOCOS:
    fora = linha.startswith('#')
    txt = linha.lstrip('# ').strip()
    toks = []
    for m in re.finditer(r'\*\*(.+?)\*\*|\*(.+?)\*|([^*]+)', txt):
        if m.group(1): toks.append((m.group(1).strip(), 'vermelho'))
        elif m.group(2): toks.append((m.group(2).strip(), 'creme'))
        else:
            for p in m.group(3).split():
                toks.append((p, 'n'))
    saida = []
    for t, tipo in toks:
        n = len(t.split())
        falado = ''.join(norm(w['w']) for w in ws[i:i+n])
        assert norm(t) == falado, (t, [w['w'] for w in ws[i:i+n]])
        saida.append({'t': t, 'f': round(ws[i]['s'] * 30), 'tipo': tipo})
        i += n
    fim = round(ws[i-1]['e'] * 30)
    if not fora:
        blocos.append({'de': saida[0]['f'], 'fim': fim, 'tokens': saida})
    else:
        blocos.append({'de': saida[0]['f'], 'fim': fim, 'tokens': [], 'fora': True})
assert i == len(ws), (i, len(ws))
out = []
for k, b in enumerate(blocos):
    if b.get('fora'): continue
    prox = blocos[k+1]['de'] if k + 1 < len(blocos) else 1291
    ate = min(prox, b['fim'] + 10)
    for corte in (776, 1102):  # entrada de B-roll: a legenda antiga não atravessa
        if b['de'] < corte < ate: ate = corte
    out.append({'de': b['de'], 'ate': ate, 'tokens': b['tokens']})
out[0]['de'] = 0
out[0]['tokens'][0]['f'] = 0
ts = "// Gerado por scripts/ir-embora/gera_legenda.py. Não editar à mão.\n"
ts += "export type Token = { t: string; f: number; tipo: 'n' | 'creme' | 'vermelho' };\n"
ts += "export type Bloco = { de: number; ate: number; tokens: Token[] };\n"
ts += "export const BLOCOS: Bloco[] = " + json.dumps(out, ensure_ascii=False, indent=1) + ";\n"
open(os.path.join(aqui, '../../src/IrEmbora/legenda.ts'), 'w').write(ts)
print(len(out), 'blocos;', sum(1 for b in out for t in b['tokens'] if t['tipo'] != 'n'), 'destaques')
for b in out:
    print(b['de'], b['ate'], ' '.join(t['t'] for t in b['tokens']))
