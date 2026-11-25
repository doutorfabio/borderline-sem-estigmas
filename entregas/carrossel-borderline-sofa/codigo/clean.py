import sys
from PIL import Image, ImageFilter
import numpy as np
B = sys.argv[1]
for k in 'abcd':
    im = Image.open(f'{B}/bg-{k}.png').convert('RGB')
    W, H = im.size
    small = im.resize((W // 8, H // 8), Image.BOX).filter(ImageFilter.MedianFilter(7))
    est = np.array(small.resize((W, H), Image.BICUBIC)).astype(float)
    a = np.array(im).astype(float)
    L = a @ [0.299, 0.587, 0.114]; Le = est @ [0.299, 0.587, 0.114]
    mask = (L < Le - 18) & (Le > 135)
    m = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.2))
    m = np.array(m).astype(float)[..., None] / 255.0
    # mantém o grão fino: soma o ruído de alta frequência fraco do próprio papel
    out = a * (1 - m) + est * m
    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(f'{B}/bg-{k}.png')
    print(k, 'pixels limpos', int(mask.sum()))
