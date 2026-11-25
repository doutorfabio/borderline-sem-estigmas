import sys
from PIL import Image, ImageFilter, ImageDraw
import numpy as np
B = sys.argv[1]
im = Image.open(B + '/capa.png').convert('RGB')
a = np.array(im).astype(float)
# clarear o papel da capa: papel ~ (206,202,200) vira branco; tinta fica
paper = np.array([207.0, 203.0, 201.0])
w = np.clip(a / paper * 255.0, 0, 255)

def feather_mask(wd, ht, l, r, t, b):
    m = np.ones((ht, wd))
    xs = np.arange(wd); ys = np.arange(ht)
    def ramp(d, f):
        return np.clip(d / f, 0, 1) if f > 0 else np.ones_like(d, dtype=float)
    mx = np.minimum(ramp(xs, l), ramp(wd - 1 - xs, r))
    my = np.minimum(ramp(ys, t), ramp(ht - 1 - ys, b))
    m = np.outer(my, mx)
    m = m * m * (3 - 2 * m)  # suave
    return m

def save_rgba(arr, mask, path):
    rgba = np.dstack([arr, mask * 255]).astype(np.uint8)
    Image.fromarray(rgba, 'RGBA').save(path)

# 1) bolha no sofá (slide 2)
x0, y0, x1, y1 = 490, 905, 1290, 1950
c = w[y0:y1, x0:x1]
save_rgba(c, feather_mask(x1-x0, y1-y0, 120, 120, 40, 130), B + '/rec-bolha-sofa.png')

# 2) mulher com a caneca (slide 6): esquerda é parede lisa, direita sangra na borda do slide
x0, y0, x1, y1 = 150, 1020, 530, 1800
c = w[y0:y1, x0:x1]
save_rgba(c, feather_mask(x1-x0, y1-y0, 30, 0, 30, 90), B + '/rec-mulher.png')

# 3) bolha menor: disco da própria bolha
cx, cy, r = 890, 1314, 368
x0, y0 = cx - r, cy - r
c = w[y0:y0+2*r, x0:x0+2*r]
yy, xx = np.mgrid[0:2*r, 0:2*r]
d = np.sqrt((xx - r + 0.5)**2 + (yy - r + 0.5)**2)
m = np.clip((r - d) / 3.0, 0, 1)
save_rgba(c, m, B + '/rec-bolha-disco.png')
print('ok')
