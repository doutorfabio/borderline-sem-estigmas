import subprocess, sys, math, random, json, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance, ImageChops
import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
CL = os.path.join(ROOT, '..', 'clips')
FD = os.path.join(ROOT, '..', 'fonts')
ICON = os.path.join(ROOT, '..', 'icone', 'icone-fabio-2k.png')
W, H, FPS = 1080, 1920, 30
SAFE = (54, 150, 950, 1536)  # x0,y0,x1,y1
CREAM = (242, 234, 219); INK = (22, 20, 19); RED = (200, 38, 32); WHITE = (255, 255, 255)
PREVIEW = len(sys.argv) > 1 and sys.argv[1] == 'preview'

def font(name, size, wght=None):
    f = ImageFont.truetype(os.path.join(FD, name), size)
    if wght:
        try: f.set_variation_by_axes([wght] if name.startswith('Mont') else None)
        except Exception: pass
    return f
def mont(size, w=800):
    f = ImageFont.truetype(os.path.join(FD, 'Montserrat.ttf'), size); f.set_variation_by_axes([w]); return f
def anton(size): return ImageFont.truetype(os.path.join(FD, 'Anton.ttf'), size)
def mono(size): return ImageFont.truetype('/mnt/skills/examples/canvas-design/canvas-fonts/IBMPlexMono-Regular.ttf', size)

# ---------------- timeline ----------------
GAP0, GAP = 10.55, 3.60
def nt(t): return t if t < 7.84 else (t + 1.3 if t < 10.6 else t + 4.9)   # narration time -> output time
SEG = [
    ('teto',  'c01', 0.40, 0.00, 3.40, 1.11, 1.17, 1.0),
    ('fone',  'c08', 6.00, 3.40, 4.55, 1.00, 1.04, 0.5),
    ('micro', 'c03', 6.00, 4.55, 5.70, 1.00, 1.05, 0.5),
    ('bolo',  'c04', 0.50, 5.70, 7.85, 1.00, 1.05, 0.6),
    ('crise', 'c06', 6.75, 7.85, 11.85, 1.00, 1.08, 0.3),
    ('pai',   'c10', 9.20, 11.85, 15.45, 1.00, 1.03, 0.45),
    ('sofa',  'c07', 0.40, 15.45, 17.60, 1.00, 1.04, 0.45),
    ('colagem', None, 0, 17.60, 29.20, 1, 1, .5),
    ('cta',   'c07', 10.08, 29.20, 32.30, 1.00, 1.05, 0.5),
]
TOTAL = 32.3
NF = int(TOTAL * FPS)

BIG = {  # scene -> list of (text, fontkind, size, color)
    'teto':  [('QUANDO ALGUÉM', 'm', 62, WHITE), ('DA CASA TEM', 'm', 62, WHITE), ('BORDERLINE', 'a', 196, WHITE)],
    'fone':  [('TEM QUEM', 'm', 62, WHITE), ('PÕE O FONE', 'a', 150, WHITE)],
    'micro': [('TEM QUEM', 'm', 62, WHITE), ('ESPERA ACORDADA', 'a', 128, WHITE)],
    'bolo':  [('TEM DATA QUE PASSA', 'm', 62, WHITE), ('SEM NINGUÉM VER', 'a', 128, WHITE)],
    'crise': [('NA HORA DA CRISE', 'a', 128, WHITE), ('cada um faz o que consegue', 'm', 50, WHITE)],
    'sofa':  [('DÁ PRA APRENDER', 'm', 62, WHITE), ('O QUE FAZER NESSA HORA', 'a', 110, WHITE)],
    'cta':   [('PRA RECEBER, COMENTA', 'm', 62, WHITE)],
}
BIG_Y = {'teto': 250, 'fone': 250, 'micro': 250, 'bolo': 250, 'crise': 1090, 'sofa': 250, 'cta': 950}
BIG_DELAY = {'teto': 0.0, 'crise': 1.32}

WORDS = json.load(open(os.path.join(ROOT, 'words3.json')))
FIX = {'12': '12', '6': 'seis', 'para': 'pra'}
caps = []  # (t0,t1,[ (word, tstart) ])
def build_caps():
    ws = []
    for i, (a, b, w) in enumerate(WORDS):
        ws.append((nt(a), nt(b), w))
    # father lines (original clip audio)
    ws += [(12.15, 12.5, 'Tô'), (12.5, 13.0, 'aqui.'), (14.35, 14.7, 'Me'), (14.7, 14.95, 'conta.')]
    ws.sort()
    ws = [(a, b, 'Tem' if (w == 'tem' and ws[k-1][2].endswith('.')) else w) for k, (a, b, w) in enumerate(ws)]
    sizes = [2,3,1,3,2,2,2,3,3,1,2,2,3,3,2,3,3, 2,2, 3,3,2, 2,2,3,3,2, 2,2, 2,3,2, 2,2,3,2, 2,3,1]
    assert sum(sizes) == len(ws), (sum(sizes), len(ws))
    i = 0
    for n in sizes:
        caps.append(ws[i:i + n]); i += n
build_caps()
cap_spans = []
for i, g in enumerate(caps):
    t0 = g[0][0] - 0.03
    t1 = min(g[-1][1] + 0.45, caps[i + 1][0][0] - 0.03) if i + 1 < len(caps) else g[-1][1] + 0.5
    cap_spans.append((t0, t1, g))

# ---------------- helpers ----------------
violations = []
def check(box, tag):
    x0, y0, x1, y1 = box
    if x0 < SAFE[0] - 0.5 or x1 > SAFE[2] + 0.5 or y1 > SAFE[3] + 0.5 or y0 < SAFE[1]:
        violations.append((tag, box))

def text_layer(lines, y, tag, align='left'):
    """lines: (text, kind, size, color). returns RGBA layer (full frame) + bbox"""
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    yy = y; bx0, by0, bx1, by1 = 9999, 9999, 0, 0
    for (txt, kind, size, col) in lines:
        while True:
            f = anton(size) if kind == 'a' else mont(size, 800)
            bb = d.textbbox((0, 0), txt, font=f)
            if bb[2] - bb[0] <= SAFE[2] - SAFE[0] - 12: break
            size -= 4
        x = SAFE[0] + 6 - bb[0]
        d.text((x, yy - bb[1]), txt, font=f, fill=col + (255,))
        bx0 = min(bx0, x + bb[0]); bx1 = max(bx1, x + bb[2]); by0 = min(by0, yy); by1 = max(by1, yy + bb[3] - bb[1])
        yy += (bb[3] - bb[1]) + (26 if kind == 'm' else 30)
    check((bx0, by0, bx1, by1 + 24), tag)  # +24 = max rise during entrance
    a = lay.split()[3]
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sh.putalpha(a.filter(ImageFilter.GaussianBlur(10)).point(lambda v: min(255, int(v * 0.85))))
    sh2 = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh2.paste(sh, (0, 5), sh)
    return Image.alpha_composite(sh2, lay)

def ease_out(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3
def ease_back(x):
    x = max(0, min(1, x)); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2

def paste_fade(base, lay, alpha, dy=0):
    if alpha <= 0: return
    if alpha < 1:
        l2 = lay.copy(); l2.putalpha(lay.split()[3].point(lambda v: int(v * alpha)))
    else: l2 = lay
    if dy:
        tmp = Image.new('RGBA', lay.size, (0, 0, 0, 0)); tmp.paste(l2, (0, int(round(dy)))); l2 = tmp
    base.alpha_composite(l2)

# captions
CAPF = mont(50, 800)
cap_cache = {}
def cap_layer(gi, nshown):
    key = (gi, nshown)
    if key in cap_cache: return cap_cache[key]
    g = cap_spans[gi][2]
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    full = ' '.join(w for _, _, w in g)
    bb = d.textbbox((0, 0), full, font=CAPF)
    tw = bb[2] - bb[0]; th = 62
    cx = (SAFE[0] + SAFE[2]) // 2
    x0 = cx - tw // 2; y0 = 1400
    pad = 26
    box = (x0 - pad, y0 - 16, x0 + tw + pad, y0 + th + 16)
    check(box, 'legenda:' + full)
    d.rounded_rectangle(box, radius=20, fill=(12, 11, 10, 205))
    d.text((x0 - bb[0], y0), full, font=CAPF, fill=(255, 255, 255, 105))
    shown = ' '.join(w for _, _, w in g[:nshown])
    d.text((x0 - bb[0], y0), shown, font=CAPF, fill=(255, 255, 255, 255))
    cap_cache[key] = lay
    return lay

def draw_caption(fr, t):
    for gi, (t0, t1, g) in enumerate(cap_spans):
        if t0 <= t < t1:
            n = sum(1 for (a, b, w) in g if a - 0.03 <= t)
            fr.alpha_composite(cap_layer(gi, max(1, n)))
            return

# ---------------- collage ----------------
def paper(color, size, seed=1, amt=10):
    rnd = np.random.RandomState(seed)
    n = rnd.normal(0, amt, (size[1] // 2 + 1, size[0] // 2 + 1))
    n = np.array(Image.fromarray(n.astype(np.float32)).resize(size, Image.BILINEAR))
    arr = np.clip(np.array(color, dtype=np.float32)[None, None, :] + n[:, :, None], 0, 255).astype(np.uint8)
    return Image.fromarray(arr, 'RGB')

def halftone(img, step=8):
    g = ImageOps.grayscale(img); g = ImageOps.autocontrast(g, cutoff=1)
    g = g.point(lambda v: int(255 * (v / 255) ** 0.55)); g = ImageEnhance.Contrast(g).enhance(1.25)
    g = g.filter(ImageFilter.GaussianBlur(1.5))
    Wd, Hd = g.size; px = g.load()
    ht = Image.new('L', (Wd, Hd), 255); d = ImageDraw.Draw(ht)
    ca = sa = math.sqrt(0.5); R = int(max(Wd, Hd) * 1.5)
    for i in range(-R, R, step):
        for j in range(-R, R, step):
            x = Wd / 2 + i * ca - j * sa; y = Hd / 2 + i * sa + j * ca
            if 0 <= x < Wd and 0 <= y < Hd:
                r = step * 0.64 * math.sqrt((255 - px[int(x), int(y)]) / 255)
                if r > 0.5: d.ellipse([x - r, y - r, x + r, y + r], fill=0)
    out = Image.composite(Image.new('RGB', (Wd, Hd), (246, 240, 228)), Image.new('RGB', (Wd, Hd), INK), ht)
    return out

def cutout(frame_png, box, out_w, out_h, seed, rot):
    im = Image.open(frame_png).convert('RGB'); w, h = im.size
    c = im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h))).resize((out_w * 2, out_h * 2), Image.LANCZOS)
    ht = halftone(c, 9).resize((out_w, out_h), Image.LANCZOS)
    rnd = random.Random(seed)
    # hand-cut polygon mask
    def edge(n, a, b, fixed, axis, j=7):
        pts = []
        for k in range(n + 1):
            v = a + (b - a) * k / n
            pts.append((v, fixed + rnd.uniform(-j, j)) if axis == 'h' else (fixed + rnd.uniform(-j, j), v))
        return pts
    m = 10
    poly = edge(4, m, out_w - m, m, 'h') + edge(4, m, out_h - m, out_w - m, 'v') + edge(4, out_w - m, m, out_h - m, 'h') + edge(4, out_h - m, m, m, 'v')
    K = 12
    big = Image.new('RGBA', (out_w + 2 * K, out_h + 2 * K), (0, 0, 0, 0))
    mask = Image.new('L', (out_w, out_h), 0); ImageDraw.Draw(mask).polygon(poly, fill=255)
    kmask = Image.new('L', big.size, 0); kmask.paste(mask, (K, K)); kmask = kmask.filter(ImageFilter.MaxFilter(2 * (K - 3) + 1))
    key = Image.new('RGBA', big.size, (252, 248, 238, 255)); key.putalpha(kmask)
    ph = ht.convert('RGBA'); ph.putalpha(mask)
    big = Image.alpha_composite(big, key); big.alpha_composite(ph, (K, K))
    big = big.rotate(rot, resample=Image.BICUBIC, expand=True)
    return big

def with_shadow(im, off=(8, 14), blur=14, op=0.30):
    pad = 40
    out = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    a = Image.new('L', out.size, 0); a.paste(im.split()[3].point(lambda v: int(v * op)), (pad + off[0], pad + off[1]))
    sh = Image.new('RGBA', out.size, (0, 0, 0, 255)); sh.putalpha(a.filter(ImageFilter.GaussianBlur(blur)))
    out = Image.alpha_composite(out, sh); out.alpha_composite(im, (pad, pad))
    return out, pad

def card(w, h, color, seed, rot=0, keyline=None):
    p = paper(color, (w, h), seed, 6).convert('RGBA')
    if keyline:
        k = Image.new('RGBA', (w + 16, h + 16), keyline + (255,)); k.alpha_composite(p, (8, 8)); p = k
    return p

class Col:
    def __init__(s):
        s.bg = paper(CREAM, (W, H), 7, 7)
        defs = [('k_mae.png', (0.00, 0.09, 0.55, 0.34), 5, -3.0, (60, 400), 0.50, 'L'),
                ('k_irmao.png', (0.15, 0.20, 0.95, 0.563), 9, 2.2, (505, 425), 0.80, 'R'),
                ('k_pai.png', (0.62, 0.185, 1.0, 0.357), 13, 2.6, (75, 740), 1.10, 'L'),
                ('k_filha.png', (0.02, 0.215, 0.44, 0.405), 17, -2.2, (500, 760), 1.40, 'R')]
        s.cuts = []
        for (f, box, seed, rot, pos, t0, side) in defs:
            c = cutout(os.path.join(ROOT, f), box, 420, 338, seed, rot)
            sh, pad = with_shadow(c)
            s.cuts.append((sh, pad, pos, t0, side))
        # red circle behind the daughter cut-out
        rc = Image.new('RGBA', (300, 300), (0, 0, 0, 0)); ImageDraw.Draw(rc).ellipse([0, 0, 299, 299], fill=RED + (255,))
        tex = paper(RED, (300, 300), 3, 8).convert('RGBA'); tex.putalpha(rc.split()[3]); s.red, s.redpad = with_shadow(tex, (6, 10), 10, 0.25)
        # icon
        ic = Image.open(ICON).convert('RGBA'); ic = ic.resize((176, int(176 * ic.height / ic.width)), Image.LANCZOS); s.icon = ic
        # title strip
        f = anton(88); d = ImageDraw.Draw(Image.new('RGB', (10, 10)))
        txt = 'PROTOCOLO 7 DIAS'; bb = d.textbbox((0, 0), txt, font=f)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        st = card(tw + 64, th + 52, INK, 21)
        ImageDraw.Draw(st).text((32 - bb[0], 26 - bb[1]), txt, font=f, fill=(246, 240, 228, 255))
        st = st.rotate(-1.6, resample=Image.BICUBIC, expand=True)
        s.title, s.tpad = with_shadow(st); s.title_pos = (258, 240)
        check((s.title_pos[0], s.title_pos[1], s.title_pos[0] + st.width, s.title_pos[1] + st.height), 'colagem:titulo')
        check((60, 205, 60 + s.icon.width, 205 + s.icon.height), 'colagem:icone')
        # data cards (all occupy x 60..944, y 1100..1350)
        CW, CH = 884, 252
        def base_card(seed):
            return card(CW - 16, CH - 16, (252, 248, 238), seed, keyline=INK)
        a = base_card(31); d = ImageDraw.Draw(a)
        d.text((40, 20), 'PRA QUEM MORA COM ALGUÉM', font=mont(44, 800), fill=INK + (255,))
        d.text((40, 78), 'COM BORDERLINE', font=anton(124), fill=RED + (255,))
        s.cardA = a
        s.cardB = base_card(32)
        c = base_card(33); d = ImageDraw.Draw(c)
        d.text((40, 20), 'A pessoa com borderline', font=mont(40, 700), fill=INK + (255,))
        d.text((40, 70), 'NÃO PRECISA ASSISTIR', font=anton(74), fill=INK + (255,))
        d.text((40, 152), 'NEM CONCORDAR', font=anton(74), fill=RED + (255,))
        s.cardC = c
        s.card_pos = (60, 1100)
        check((60, 1100, 60 + CW, 1100 + CH + 20), 'colagem:cartoes')
        s.tag = None
        f = anton(50); tg = card(418, 80, RED, 41); ImageDraw.Draw(tg).text((22, 6), 'FRASE DE PRESENÇA', font=f, fill=(250, 245, 233, 255))
        s.tag = tg.rotate(2.0, resample=Image.BICUBIC, expand=True)

    def cardB_frame(s, l):
        c = s.cardB.copy(); d = ImageDraw.Draw(c)
        d.text((40, 16), 'UM PROCEDIMENTO POR DIA', font=anton(64), fill=INK + (255,))
        f = anton(72)
        for k in range(7):
            tk = 4.35 + k * 0.13
            if l < tk: break
            sc = ease_back((l - tk) / 0.2)
            cx = 40 + 52 + k * 114; cy = 160; r = int(48 * sc)
            d.rounded_rectangle([cx - r, cy - r, cx + r, cy + r], radius=10, fill=INK + (255,))
            if sc > 0.8:
                t = str(k + 1); bb = d.textbbox((0, 0), t, font=f)
                d.text((cx - (bb[2] + bb[0]) / 2, cy - (bb[3] + bb[1]) / 2), t, font=f, fill=(246, 240, 228, 255))
        return c

    def frame(s, l):
        fr = s.bg.convert('RGBA')
        ls = math.floor(l * 12) / 12  # stop-motion stepping
        jit = random.Random(int(l * 6))
        # icon
        if l > 0.12:
            a = ease_out((l - 0.12) / 0.3)
            ic = s.icon
            if a < 1:
                ic = s.icon.copy(); ic.putalpha(s.icon.split()[3].point(lambda v: int(v * a)))
            fr.alpha_composite(ic, (60, int(205 + 18 * (1 - a))))
        # title
        if l > 0.3:
            a = ease_out((l - 0.3) / 0.3)
            t = s.title
            if a < 1:
                t = s.title.copy(); t.putalpha(s.title.split()[3].point(lambda v: int(v * a)))
            fr.alpha_composite(t, (s.title_pos[0] - s.tpad, int(s.title_pos[1] - s.tpad + 16 * (1 - a))))
        # red circle
        if l > 1.35:
            k = ease_back((ls - 1.35) / 0.35)
            sz = max(2, int(s.red.width * k)); r = s.red.resize((sz, sz), Image.BICUBIC)
            cx, cy = 800, 800
            fr.alpha_composite(r, (cx - sz // 2, cy - sz // 2))
        # cut-outs
        for (im, pad, pos, t0, side) in s.cuts:
            if l < t0: continue
            k = ease_back((ls - t0) / 0.42)
            start = -im.width - 40 if side == 'L' else W + 40
            x = start + (pos[0] - pad - start) * k
            dx = jit.choice([-1, 0, 1]) if k >= 1 else 0
            dst = (int(x) + dx, pos[1] - pad)
            if dst[0] < W and dst[0] + im.width > 0:
                # crop to canvas
                sx0 = max(0, -dst[0]); sx1 = min(im.width, W - dst[0])
                fr.alpha_composite(im.crop((sx0, 0, sx1, im.height)), (max(0, dst[0]), dst[1]))
        # data cards
        def put(cardimg, tin, tout):
            if l < tin or l > tout + 0.25: return
            a = ease_out((l - tin) / 0.28)
            if l > tout: a = 1 - ease_out((l - tout) / 0.25)
            ci, pad = with_shadow(cardimg)
            if a < 1: ci.putalpha(ci.split()[3].point(lambda v: int(v * a)))
            fr.alpha_composite(ci, (s.card_pos[0] - pad, int(s.card_pos[1] - pad + 20 * (1 - a))))
        put(s.cardA, 1.75, 3.85)
        if 4.0 <= l <= 7.95: put(s.cardB_frame(l), 4.05, 7.6)
        put(s.cardC, 7.8, 99)
        if 5.45 < l < 7.85:
            a = ease_out((l - 5.45) / 0.22)
            if l > 7.6: a = 1 - ease_out((l - 7.6) / 0.25)
            tg, pad = with_shadow(s.tag, (5, 8), 8, 0.3)
            if a < 1: tg.putalpha(tg.split()[3].point(lambda v: int(v * a)))
            fr.alpha_composite(tg, (506 - pad, int(1004 - pad + 12 * (1 - a))))
        return fr

# ---------------- video base ----------------
def seg_reader(clip, ss, dur):
    src = os.path.join(CL, clip + '.mp4')
    vf = "minterpolate=fps=30:mi_mode=blend,scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,unsharp=5:5:0.6:5:5:0.0,eq=saturation=0.94"
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(max(0, ss - 0.5)), '-i', src, '-ss', str(min(0.5, ss)), '-t', str(dur + 0.2), '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    return p

def zoomed(img, z, ay):
    if abs(z - 1) < 1e-4: return img
    cw, ch = W / z, H / z
    x0 = (W - cw) / 2; y0 = (H - ch) * ay
    return img.transform((W, H), Image.AFFINE, (1 / z, 0, x0, 0, 1 / z, y0), resample=Image.BICUBIC)

def main():
    col = Col()
    big_layers = {k: text_layer(v, BIG_Y[k], 'grande:' + k) for k, v in BIG.items()}
    # final-scene icon + handle
    ic = Image.open(ICON).convert('RGBA'); ic = ic.resize((150, int(150 * ic.height / ic.width)), Image.LANCZOS)
    sofa_extra = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sofa_extra.alpha_composite(ic, (60, 172))
    hl = text_layer([('@drfabioschmidt', 'm', 40, WHITE)], 240, 'arroba');
    tmp = Image.new('RGBA', (W, H), (0, 0, 0, 0)); tmp.paste(hl, (170, 0)); sofa_extra.alpha_composite(tmp)
    check((60, 172, 60 + 150, 172 + ic.height), 'icone final')
    # COMEÇAR block
    f = anton(210); dd = ImageDraw.Draw(Image.new('RGB', (10, 10))); bb = dd.textbbox((0, 0), 'COMEÇAR', font=f)
    cw, chh = bb[2] - bb[0] + 70, bb[3] - bb[1] + 60
    blk = card(cw, chh, RED, 55); ImageDraw.Draw(blk).text((35 - bb[0], 30 - bb[1]), 'COMEÇAR', font=f, fill=(250, 245, 233, 255))
    blk, bpad = with_shadow(blk, (8, 12), 14, 0.4)
    CTA_POS = (60, 1040)
    check((CTA_POS[0], CTA_POS[1] - 16, CTA_POS[0] + cw, CTA_POS[1] + chh), 'COMEÇAR')
    for gi in range(len(cap_spans)): cap_layer(gi, 1)
    if violations:
        print('FORA DA AREA SEGURA:', violations); sys.exit(1)
    print('area segura ok;', len(cap_spans), 'legendas')
    if PREVIEW:
        os.makedirs(os.path.join(ROOT, 'prev2'), exist_ok=True)
    out = None
    if not PREVIEW:
        out = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                                '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-maxrate', '6500k', '-bufsize', '13M', '-pix_fmt', 'yuv420p', os.path.join(ROOT, 'video2.mp4')], stdin=subprocess.PIPE)
    want = set(int(float(x) * FPS) for x in sys.argv[2:]) if PREVIEW else None
    fi = 0
    for (name, clip, ss, t0, t1, z0, z1, ay) in SEG:
        f0, f1 = int(round(t0 * FPS)), int(round(t1 * FPS))
        rd = seg_reader(clip, ss, t1 - t0) if clip else None
        last = None
        for f in range(f0, f1):
            t = f / FPS; l = t - t0
            if rd:
                raw = rd.stdout.read(W * H * 3)
                if len(raw) == W * H * 3: last = Image.frombytes('RGB', (W, H), raw)
            if PREVIEW and f not in want: continue
            if rd:
                k = l / (t1 - t0)
                fr = zoomed(last, z0 + (z1 - z0) * k, ay).convert('RGBA')
                # soft darkening behind text block for legibility
                if name in big_layers:
                    d0 = BIG_DELAY.get(name, 0.05)
                    a = ease_out((l - d0) / 0.2)
                    paste_fade(fr, big_layers[name], a, dy=22 * (1 - a))
                if name == 'cta':
                    a = ease_out((l - 0.2) / 0.25); paste_fade(fr, sofa_extra, a)
                    if t >= 31.15:
                        k = ease_back((t - 31.15) / 0.25); a2 = ease_out((t - 31.15) / 0.12)
                        b2 = blk if a2 >= 1 else blk.copy()
                        if a2 < 1: b2.putalpha(blk.split()[3].point(lambda v: int(v * a2)))
                        fr.alpha_composite(b2, (CTA_POS[0] - bpad, int(CTA_POS[1] - bpad + 16 * (1 - k))))
            else:
                fr = col.frame(l)
            draw_caption(fr, t)
            # white flash into/out of collage, fade to black at end
            if name == 'colagem' and l < 0.1:
                fr = Image.blend(fr, Image.new('RGBA', (W, H), (255, 255, 255, 255)), 0.75 * (1 - l / 0.1))
            if name == 'cta' and l < 0.1:
                fr = Image.blend(fr, Image.new('RGBA', (W, H), (255, 255, 255, 255)), 0.75 * (1 - l / 0.1))
            if t > TOTAL - 0.1:
                fr = Image.blend(fr, Image.new('RGBA', (W, H), (0, 0, 0, 255)), min(1, (t - (TOTAL - 0.1)) / 0.1))
            rgb = fr.convert('RGB')
            if PREVIEW: rgb.resize((360, 640), Image.LANCZOS).save(os.path.join(ROOT, 'prev2', f'f{f:04d}.jpg'), quality=85)
            else: out.stdin.write(rgb.tobytes())
        if rd: rd.kill()
        print(name, 'ok', flush=True)
    if out:
        out.stdin.close(); out.wait()

main()
