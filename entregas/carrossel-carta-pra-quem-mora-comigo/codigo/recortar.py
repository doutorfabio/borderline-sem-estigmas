# Leva cada base 3:4 para 1080 de largura e corta 90 px embaixo (fecha 4:5). O topo e a borda rasgada ficam inteiros.
# Decide a cor do @ pela luz da foto atrás dele (foto escura: creme; foto clara: preto).
# Uso: python3 recortar.py <pasta-das-bases> <pasta-de-trabalho>
import sys, os, json
import numpy as np
from PIL import Image
bases, out = sys.argv[1], sys.argv[2]
nomes = ['1_capa', '2_tese', '3_embora', '4_pergunte', '5_silencio', '6_grito', '7_acumulo']
cores = []
for i, n in enumerate(nomes, 1):
    arq = next(os.path.join(bases, n + e) for e in ('.png', '.jpg') if os.path.exists(os.path.join(bases, n + e)))
    im = Image.open(arq).convert('RGB')
    im = im.resize((1080, round(im.height * 1080 / im.width)), Image.LANCZOS).crop((0, 0, 1080, 1350))
    im.save(os.path.join(out, f'crop{i}.png'))
    a = np.asarray(im).astype(float)
    L = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    cores.append('creme' if np.median(L[1254:1284, 128:290]) < 118 else 'preto')
json.dump(cores, open(os.path.join(out, 'rodape.json'), 'w'))
print(cores)
