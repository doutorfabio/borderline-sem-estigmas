import sys, glob
from PIL import Image
d = sys.argv[1]
ESQ, DIR, TOPO, BASE = 54, 950, 96, 1536
fs = sorted(glob.glob(d + '/element-*.png'))
mn = [9999, 9999]; mx = [0, 0]; fora = []
jan = {'ins1': (776, 878), 'rosto': (878, 985), 'ins2txt': (1168, 1239)}
porjan = {k: [9999, 9999, 0, 0] for k in list(jan) + ['legenda']}
for f in fs:
    i = int(f.split("element-")[1].split(".")[0])
    a = Image.open(f).getchannel('A')
    # ignora a sombra suave: conta só alfa acima de 40%
    bb = a.point(lambda v: 255 if v > 102 else 0).getbbox()
    if not bb: continue
    k = 'legenda'
    for n, (x, y) in jan.items():
        if x <= i < y: k = n
    p = porjan[k]
    p[0] = min(p[0], bb[0]); p[1] = min(p[1], bb[1]); p[2] = max(p[2], bb[2]); p[3] = max(p[3], bb[3])
    if bb[0] < ESQ or bb[2] > DIR or bb[1] < TOPO or bb[3] > BASE:
        fora.append((i, bb))
for k, p in porjan.items():
    print(k, 'esq=%d topo=%d dir=%d base=%d' % tuple(p), '| margem esq %.1f%% dir %.1f%% topo %.1f%% base %.1f%%' % (p[0]/10.8, (1080-p[2])/10.8, p[1]/19.2, (1920-p[3])/19.2))
print('quadros fora da área segura:', len(fora), fora[:12])
