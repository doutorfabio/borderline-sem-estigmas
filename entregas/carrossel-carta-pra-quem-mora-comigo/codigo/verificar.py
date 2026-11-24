# Mede a tinta do texto em cada tela (diferença contra a base) e exporta JPG 92 + PDF.
# Uso: python3 verificar.py <pasta-de-trabalho> <pasta-dos-png> <pasta-final>
import sys, os, json
import numpy as np
from PIL import Image
import img2pdf
work, png, final = sys.argv[1:4]
ids = ['01-capa', '02-tese', '03-embora', '04-pergunte', '05-silencio', '06-grito', '07-acumulo']
rel = json.load(open(os.path.join(png, 'relatorio.json')))
def lum(a):
    a = a / 255.0; a = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
ok = True
for i, n in enumerate(ids, 1):
    base = np.asarray(Image.open(os.path.join(work, f'crop{i}.png')).convert('RGB')).astype(int)
    im = Image.open(os.path.join(png, n + '.png')).convert('RGB'); a = np.asarray(im).astype(int)
    assert a.shape == (1350, 1080, 3)
    ink = np.abs(a - base).max(axis=2) > 28
    ys, xs = np.where(ink[:900]); fy, fx = np.where(ink[900:]); fy = fy + 900
    red = ink & (a[..., 0] > 130) & (a[..., 1] < 95) & (a[..., 2] < 95)
    ry, rx = np.where(red[100:900]); ry = ry + 100
    # contraste do @ contra a foto atrás dele
    hy, hx = np.where(ink[1255:1300] & ~red[1255:1300]); hy = hy + 1255
    Lt = lum(a[hy, hx].astype(float)).mean(); Lb = lum(base[hy, hx].astype(float))
    c = np.where(Lt > Lb, (Lt + .05) / (Lb + .05), (Lb + .05) / (Lt + .05))
    r = rel[i - 1]
    linha = dict(tela=n, fonte=r['fonte'], esq=int(xs.min()), dir=int(1080 - 1 - xs.max()), topo=int(ys.min()), base_titulo=int(ys.max()), limite_foto=r['limite'],
                 vermelho_titulo=(int(rx.min()), int(ry.min()), int(rx.max()), int(ry.max())), rodape_x=(int(fx.min()), int(fx.max())), rodape_base=int(1350 - 1 - fy.max()),
                 contraste_arroba=(round(float(np.percentile(c, 10)), 1), round(float(np.median(c)), 1)))
    falhas = []
    if linha['esq'] < 62: falhas.append('margem esquerda')
    if linha['dir'] < 1080 * 0.12 - 66 and xs.max() > 64 + 1080 * 0.88 + 1: falhas.append('largura 88%')
    if linha['topo'] < 63: falhas.append('margem de cima')
    if n != '01-capa' and linha['base_titulo'] > r['limite'] + 14: falhas.append('título na foto')
    if linha['rodape_base'] < 67: falhas.append('rodapé a menos de 5%')
    print(linha, 'FALHAS:', falhas or 'nenhuma'); ok &= not falhas
    im.save(os.path.join(final, n + '.jpg'), quality=92, subsampling=0, optimize=True)
jpgs = [os.path.join(final, n + '.jpg') for n in ids]
with open(os.path.join(final, 'carta-pra-quem-mora-comigo.pdf'), 'wb') as f:
    f.write(img2pdf.convert(jpgs, layout_fun=img2pdf.get_fixed_dpi_layout_fun((72, 72))))
print('tudo certo' if ok else 'HÁ FALHAS')
