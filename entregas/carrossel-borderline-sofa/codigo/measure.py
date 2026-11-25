import json, sys
from PIL import Image
import numpy as np
S = sys.argv[1]; R = json.load(open(S + '/measure/report.json'))
W, H = 1792, 2240; LIM = 0.078 * W
CAP = {'Anton': 0.859375, 'DM Serif Display': 0.671875}
bad = 0; mins = []
for n, lines in R.items():
    xs0, xs1 = [], []
    for L in lines:
        a = np.array(Image.open(L['img']).convert('L'))
        ys, xs = np.where(a < 128)
        fam = 'Anton' if 'Anton' in L['fam'] else 'DM Serif Display'
        cap = L['fs'] * CAP[fam]
        ink_h = ys.max() - ys.min() + 1
        x0, x1 = xs.min(), xs.max()
        xs0.append(x0); xs1.append(x1)
        ok_cap = cap >= 0.06 * H
        ok_m = x0 >= LIM and (W - 1 - x1) >= LIM
        mins.append((cap / H * 100, n, L['t']))
        flag = '' if ok_cap and ok_m else '  <<< FALHA'
        if flag: bad += 1
        print(f"s{n} {L['t']:<24} maiúscula {cap:6.1f}px {cap/H*100:5.2f}%  tinta {ink_h:4d}px  esq {x0/W*100:5.2f}%  dir {(W-1-x1)/W*100:5.2f}%{flag}")
    print(f"   s{n} margens: esq {min(xs0)/W*100:.2f}%  dir {(W-1-max(xs1))/W*100:.2f}%")
m = min(mins); print(f"menor linha: {m[0]:.2f}% (s{m[1]} {m[2]})  falhas: {bad}")
# distância vertical entre a tinta de linhas vizinhas (acento encostando na linha de cima)
print('--- folga entre linhas (tinta) ---')
worst = []
for n, lines in R.items():
    boxes = []
    for L in lines:
        a = np.array(Image.open(L['img']).convert('L')); ys, xs = np.where(a < 128)
        boxes.append((ys.min(), ys.max(), xs.min(), xs.max(), L['t'], a < 128))
    for i in range(len(boxes)):
        for j in range(len(boxes)):
            if i == j: continue
            t0, b0, l0, r0, n0, m0 = boxes[i]; t1, b1, l1, r1, n1, m1 = boxes[j]
            if t1 <= t0: continue
            if r0 < l1 or r1 < l0: continue
            # menor distância vertical por coluna onde as duas têm tinta
            cols = np.where(m0.any(0) & m1.any(0))[0]
            if len(cols) == 0: continue
            bot = np.array([np.where(m0[:, c])[0].max() for c in cols]); top = np.array([np.where(m1[:, c])[0].min() for c in cols])
            g = int((top - bot).min())
            if g < 400: worst.append((g, n, n0, n1))
worst.sort()
for g, n, a_, b_ in worst[:8]: print(f'  s{n}: {g:4d}px  {a_} / {b_}' + ('   <<< ENCOSTA' if g < 22 else ''))
