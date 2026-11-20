"""Halftone duotone no estilo das referencias (pontos pretos sobre amarelo, ceu coral).
uso: python3 halftone.py entrada.png saida.png [modo] [crop x,y,w,h]
modo: plain | sky
"""
import sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

W, H = 1080, 1920
YEL = (247, 224, 64)
CORAL = (234, 96, 96)
INK = (22, 20, 18)
CELL = 13          # tamanho da celula da retícula em px finais
SS = 3             # supersample para borda limpa


def load(path, crop=None):
    im = Image.open(path).convert("RGB")
    if crop:
        x, y, w, h = crop
        im = im.crop((x, y, x + w, y + h))
    # preenche 9:16
    r = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    l = (im.width - W) // 2
    t = (im.height - H) // 2
    return im.crop((l, t, l + W, t + H))


def halftone(gray, paper, ink, angle=45):
    g = np.asarray(gray, dtype=np.float32) / 255.0
    g = np.clip(g, 0, 1) ** 0.75  # clareia meios-tons
    big = Image.new("RGB", (W * SS, H * SS), paper)
    d = ImageDraw.Draw(big)
    a = math.radians(angle)
    ca, sa = math.cos(a), math.sin(a)
    diag = int(math.hypot(W, H)) + CELL * 2
    n = diag // CELL + 2
    cx0, cy0 = W / 2, H / 2
    for i in range(-n // 2, n // 2 + 1):
        for j in range(-n // 2, n // 2 + 1):
            u, v = i * CELL, j * CELL
            x = cx0 + u * ca - v * sa
            y = cy0 + u * sa + v * ca
            if x < -CELL or y < -CELL or x > W + CELL or y > H + CELL:
                continue
            xi, yi = min(max(int(x), 0), W - 1), min(max(int(y), 0), H - 1)
            dark = 1.0 - g[yi, xi]
            if dark < 0.04:
                continue
            rad = CELL * 0.64 * dark ** 0.85
            R = rad * SS
            X, Y = x * SS, y * SS
            d.ellipse((X - R, Y - R, X + R, Y + R), fill=ink)
    return big.resize((W, H), Image.LANCZOS)


def main():
    src, out = sys.argv[1], sys.argv[2]
    mode = sys.argv[3] if len(sys.argv) > 3 else "plain"
    crop = tuple(int(v) for v in sys.argv[4].split(",")) if len(sys.argv) > 4 else None
    im = load(src, crop)
    gray = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=2).filter(ImageFilter.GaussianBlur(1.2))
    ht = halftone(gray, YEL, INK)
    if mode == "sky":
        # area clara de cima vira ceu coral liso; borda amarela deslocada como na referencia
        lum = np.asarray(gray.filter(ImageFilter.GaussianBlur(18)), dtype=np.float32)
        yy = np.arange(H)[:, None] / H
        sky = (lum > 175) & (yy < 0.42)
        m = Image.fromarray((sky * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(31))
        # contorno amarelo: area que nao e ceu, dilatada para cima
        ground = ImageOps.invert(m).filter(ImageFilter.MaxFilter(41))
        out_im = Image.new("RGB", (W, H), CORAL)
        out_im.paste(Image.new("RGB", (W, H), YEL), mask=ground)
        out_im.paste(ht, mask=ImageOps.invert(m))
        ht = out_im
    ht.save(out)


if __name__ == "__main__":
    main()
