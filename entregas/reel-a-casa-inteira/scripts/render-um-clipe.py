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
def nt(t): return t + 1.28 if t < 5.4 else (t + 2.96 if t < 12.9 else t + 4.85)   # narration time -> output time
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
TOTAL = 33.2
NF = int(TOTAL * FPS)

BIG = {
    'f1': [('QUANDO ALGUÉM', 'm', 62, WHITE), ('DA CASA TEM', 'm', 62, WHITE), ('BORDERLINE', 'a', 196, WHITE)],
    'f2': [('NA HORA, CADA UM', 'm', 62, WHITE), ('FAZ O QUE CONSEGUE', 'a', 112, WHITE)],
    'f3': [('DÁ PRA APRENDER', 'm', 62, WHITE), ('O QUE FAZER NESSA HORA', 'a', 110, WHITE)],
    'cta': [('PRA RECEBER, COMENTA', 'm', 62, WHITE)],
}
BIG_Y = {'f1': 960, 'f2': 1090, 'f3': 1090, 'cta': 950}
BIG_DELAY = {'teto': 0.0, 'crise': 1.32}

WORDS = json.load(open(os.path.join(ROOT, 'words4.json')))
FIX = {'12': '12', '6': 'seis', 'para': 'pra'}
caps = []  # (t0,t1,[ (word, tstart) ])
def build_caps():
    ws = []
    for i, (a, b, w) in enumerate(WORDS):
        ws.append((nt(a), nt(b), w))
    # father lines (original clip audio)
    ws.sort()
    ws = [(a, b, 'Tem' if (w == 'tem' and ws[k-1][2].endswith('.')) else w) for k, (a, b, w) in enumerate(ws)]
    sizes = [2,3,1,3,3, 2,3,3, 2,2,2, 3,3,2, 2,2,3,3,2, 2,2, 2,3,1]
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
    g = g.point(lambda v: int(255 * (v / 255) ** 0.42)); g = ImageEnhance.Contrast(g).enhance(1.15)
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


def seg_frames(ss, dur):
    src = os.path.join(CL, 'c06up.mp4')
    vf = "minterpolate=fps=30:mi_mode=blend,scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,eq=saturation=0.94"
    p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(max(0, ss - 0.5)), '-i', src, '-ss', str(min(0.5, ss)), '-t', str(dur), '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    n = len(p) // (W * H * 3)
    return [Image.frombytes('RGB', (W, H), p[i * W * H * 3:(i + 1) * W * H * 3]) for i in range(n)]

def fade(im, a):
    if a >= 1: return im
    o = im.copy(); o.putalpha(im.split()[3].point(lambda v: int(v * max(0, a)))); return o

def strip(txt, kind, size, bg, fg, rot, seed, padx=26, pady=16):
    f = anton(size) if kind == 'a' else mont(size, 800)
    d = ImageDraw.Draw(Image.new('RGB', (10, 10))); bb = d.textbbox((0, 0), txt, font=f)
    c = card(bb[2] - bb[0] + 2 * padx, bb[3] - bb[1] + 2 * pady, bg, seed)
    ImageDraw.Draw(c).text((padx - bb[0], pady - bb[1]), txt, font=f, fill=fg + (255,))
    c = c.rotate(rot, resample=Image.BICUBIC, expand=True)
    sh, pad = with_shadow(c, (5, 8), 9, 0.32)
    return sh, pad, c.size

class Strip:
    def __init__(s, txt, kind, size, bg, fg, rot, seed, pos, tag):
        s.im, s.pad, s.size = strip(txt, kind, size, bg, fg, rot, seed); s.pos = pos
        check((pos[0], pos[1], pos[0] + s.size[0], pos[1] + s.size[1] + 16), tag)
    def draw(s, fr, a):
        if a <= 0: return
        k = ease_out(a)
        fr.alpha_composite(fade(s.im, k), (s.pos[0] - s.pad, int(s.pos[1] - s.pad + 16 * (1 - k))))

CREAMT = (246, 240, 228)
class Print:
    """freeze frame as a halftone photo print on paper"""
    def __init__(s, frame, crop, dest, rot, seed):
        s.frame = frame; s.crop = crop; s.dest = dest; s.rot = rot
        x0, y0, x1, y1 = crop; dw, dh = dest[2], dest[3]
        c = frame.crop(crop).resize((dw * 2, dh * 2), Image.LANCZOS)
        s.ht = halftone(c, 9).resize((dw, dh), Image.LANCZOS)
        s.col = frame.crop(crop).resize((dw, dh), Image.LANCZOS)
        B = 16
        pr = Image.new('RGBA', (dw + 2 * B, dh + 2 * B), (252, 248, 238, 255)); pr.paste(s.ht, (B, B))
        pr = pr.rotate(rot, resample=Image.BICUBIC, expand=True)
        s.pr, s.ppad = with_shadow(pr, (10, 16), 18, 0.35); s.B = B
        s.cx = dest[0] + dw / 2; s.cy = dest[1] + dh / 2
    def draw_final(s, fr, scale=1.0):
        im = s.pr
        if abs(scale - 1) > 1e-4:
            im = im.resize((int(im.width * scale), int(im.height * scale)), Image.BICUBIC)
        fr.alpha_composite(im, (int(s.cx - im.width / 2), int(s.cy - im.height / 2)))
    def draw_trans(s, fr, k):
        # k: 0 = full-frame live image, 1 = final print
        x0, y0, x1, y1 = s.crop; dx, dy, dw, dh = s.dest
        cb = (x0 * k, y0 * k, W + (x1 - W) * k, H + (y1 - H) * k)
        rx = dx * k; ry = dy * k; rw = W + (dw - W) * k; rh = H + (dh - H) * k
        im = s.frame.crop(tuple(int(v) for v in cb)).resize((int(rw), int(rh)), Image.BILINEAR)
        hb = s.ht.resize((int(rw), int(rh)), Image.BILINEAR)
        im = Image.blend(im, hb, max(0, min(1, (k - 0.35) / 0.65)))
        B = int(s.B * k)
        pr = Image.new('RGBA', (int(rw) + 2 * B, int(rh) + 2 * B), (252, 248, 238, 255)); pr.paste(im, (B, B))
        if k > 0.02: pr = pr.rotate(s.rot * k, resample=Image.BICUBIC, expand=True)
        cx = rx + rw / 2; cy = ry + rh / 2
        fr.alpha_composite(pr, (int(cx - pr.width / 2), int(cy - pr.height / 2)))

def main():
    col = Col()
    M1 = (1.32, 1.63); M2 = (6.08, 2.08); M3 = (11.50, 2.70)
    T = [0, 1.63, 6.50, 8.58, 15.50, 18.20, TOTAL]
    m1 = seg_frames(*M1); m2 = seg_frames(*M2); m3 = seg_frames(*M3)
    paper_bg = paper(CREAM, (W, H), 7, 7).convert('RGBA')
    P1 = Print(m1[-1], (0, 60, 1080, 1410), (108, 185, 864, 1080), -1.4, 1)
    P2 = Print(m2[-1], (0, 60, 1080, 1410), (108, 185, 864, 1080), 1.2, 2)
    P3 = Print(m3[-1], (0, 60, 1080, 885), (108, 185, 864, 660), -1.0, 3)
    # opening title over live video (white, shadow)
    open_txt = text_layer([('QUANDO ALGUÉM', 'm', 62, WHITE), ('DA CASA TEM', 'm', 62, WHITE), ('BORDERLINE', 'a', 196, WHITE)], 960, 'abertura')
    A1 = Strip('QUANDO ALGUÉM DA CASA TEM', 'm', 46, INK, CREAMT, -1.4, 11, (60, 1012), 'f1a')
    A2 = Strip('BORDERLINE', 'a', 186, RED, (250, 245, 233), -1.4, 12, (60, 1092), 'f1b')
    B1 = Strip('NA HORA, CADA UM', 'm', 46, INK, CREAMT, 1.2, 13, (60, 1060), 'f2a')
    B2 = Strip('FAZ O QUE CONSEGUE', 'a', 108, INK, CREAMT, 1.2, 14, (60, 1136), 'f2b')
    G1 = Strip('UM GRITA', 'a', 60, RED, (250, 245, 233), -2.0, 61, (610, 745), 'tag grita')
    G2 = Strip('A OUTRA TENTA SEGURAR', 'a', 54, RED, (250, 245, 233), 1.6, 62, (60, 945), 'tag segurar')
    C1 = Strip('DÁ PRA APRENDER', 'm', 46, INK, CREAMT, -1.0, 15, (60, 905), 'f3a')
    C2 = Strip('O QUE FAZER NESSA HORA', 'a', 88, INK, CREAMT, -1.0, 16, (60, 980), 'f3b')
    f = mont(46, 800); dd = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    cta_txt = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(cta_txt).text((66, 1034), 'PRA RECEBER, COMENTA', font=f, fill=INK + (255,))
    bb = dd.textbbox((66, 1034), 'PRA RECEBER, COMENTA', font=f); check(bb, 'cta txt')
    f = anton(168); bb = dd.textbbox((0, 0), 'COMEÇAR', font=f)
    cw, chh = bb[2] - bb[0] + 70, bb[3] - bb[1] + 56
    blk = card(cw, chh, RED, 55); ImageDraw.Draw(blk).text((35 - bb[0], 28 - bb[1]), 'COMEÇAR', font=f, fill=(250, 245, 233, 255))
    blk, bpad = with_shadow(blk, (8, 12), 14, 0.35); CTA_POS = (60, 1106)
    check((CTA_POS[0], CTA_POS[1] - 16, CTA_POS[0] + cw, CTA_POS[1] + chh), 'COMEÇAR')
    STRIP_Y = 884
    check((258, STRIP_Y, 258 + col.title.width - 2 * col.tpad, STRIP_Y + col.title.height - 2 * col.tpad), 'faixa protocolo')
    for gi in range(len(cap_spans)): cap_layer(gi, 1)
    if violations: print('FORA DA AREA SEGURA:', violations); sys.exit(1)
    print('area segura ok;', len(cap_spans), 'legendas', len(m1), len(m2), len(m3), flush=True)
    out = None
    if PREVIEW: os.makedirs(os.path.join(ROOT, 'prev4'), exist_ok=True)
    else:
        out = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                                '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-maxrate', '7000k', '-bufsize', '14M', '-pix_fmt', 'yuv420p', os.path.join(ROOT, 'video4.mp4')], stdin=subprocess.PIPE)
    want = set(int(float(x) * FPS) for x in sys.argv[2:]) if PREVIEW else None
    TCOME = nt(27.17) - 0.05
    TIN, TOUT = 0.30, 0.20
    def freeze(fr, P, t, t0, t1, last):
        """returns base composed; k progress"""
        l = t - t0
        if l < TIN:
            k = ease_out(l / TIN); fr.alpha_composite(paper_bg); P.draw_trans(fr, k); return k
        if (not last) and t > t1 - TOUT:
            k = 1 - ease_out((t - (t1 - TOUT)) / TOUT); fr.alpha_composite(paper_bg); P.draw_trans(fr, k); return k
        fr.alpha_composite(paper_bg); P.draw_final(fr, 1.0 + 0.025 * (l / (t1 - t0))); return 1.0
    for fi in range(int(round(TOTAL * FPS))):
        t = fi / FPS
        if PREVIEW and fi not in want: continue
        fr = Image.new('RGBA', (W, H), (0, 0, 0, 255))
        if t < T[1]:
            fr = m1[min(len(m1) - 1, fi)].convert('RGBA'); paste_fade(fr, open_txt, 1)
        elif t < T[2]:
            k = freeze(fr, P1, t, T[1], T[2], False); l = t - T[1]
            if k < 1 and l < TIN: paste_fade(fr, open_txt, 1 - k)
            a = (l - 0.22) / 0.2 if t < T[2] - TOUT else k
            A1.draw(fr, a); A2.draw(fr, a - 0.3 if t < T[2] - TOUT else k)
        elif t < T[3]:
            fr = m2[min(len(m2) - 1, int(round((t - T[2]) * FPS)))].convert('RGBA')
        elif t < T[4]:
            k = freeze(fr, P2, t, T[3], T[4], False); l = t - T[3]
            endp = t >= T[4] - TOUT
            B1.draw(fr, k if endp else (l - 0.22) / 0.2); B2.draw(fr, k if endp else (l - 0.36) / 0.2)
            ta = nt(9.48) - 0.05; tb = nt(10.72) - 0.05
            if t >= ta: G1.draw(fr, k if endp else (t - ta) / 0.18)
            if t >= tb: G2.draw(fr, k if endp else (t - tb) / 0.18)
        elif t < T[5]:
            fr = m3[min(len(m3) - 1, int(round((t - T[4]) * FPS)))].convert('RGBA')
        else:
            k = freeze(fr, P3, t, T[5], T[6], True); l = t - T[5]
            tP = nt(17.88) - T[5] - 0.15; tA = nt(19.28) - T[5] - 0.1; tB = nt(22.43) - T[5] - 0.15; tC = nt(24.67) - T[5] - 0.2
            if l < tP + 0.05:
                o = 1 if l < tP - 0.2 else max(0, (tP - l) / 0.2) * 1.0
                C1.draw(fr, min((l - 0.25) / 0.2, 1) * o if o < 1 else (l - 0.25) / 0.2)
                C2.draw(fr, min((l - 0.4) / 0.2, 1) * o if o < 1 else (l - 0.4) / 0.2)
            if l >= tP:
                a = ease_out((l - tP) / 0.3)
                fr.alpha_composite(fade(col.icon, a), (60, int(STRIP_Y - 35 + 16 * (1 - a))))
                fr.alpha_composite(fade(col.title, a), (258 - col.tpad, int(STRIP_Y - col.tpad + 16 * (1 - a))))
            def put(cardimg, tin, tout):
                if l < tin or l > tout + 0.25: return
                a = ease_out((l - tin) / 0.28)
                if l > tout: a = 1 - ease_out((l - tout) / 0.25)
                ci, pad = with_shadow(cardimg)
                fr.alpha_composite(fade(ci, a), (col.card_pos[0] - pad, int(col.card_pos[1] - pad + 20 * (1 - a))))
            put(col.cardA, tA, tB - 0.3)
            if tB - 0.05 <= l <= tC + 0.3: put(col.cardB_frame(l - tB + 4.05), tB, tC)
            if l >= tC + 0.2:
                paste_fade(fr, cta_txt, ease_out((l - tC - 0.2) / 0.25))
            if t >= TCOME:
                kk = ease_back((t - TCOME) / 0.25); a2 = ease_out((t - TCOME) / 0.12)
                fr.alpha_composite(fade(blk, a2), (CTA_POS[0] - bpad, int(CTA_POS[1] - bpad + 16 * (1 - kk))))
        draw_caption(fr, t)
        for tf in (T[1], T[3], T[5]):
            if 0 <= t - tf < 0.1:
                fr = Image.blend(fr, Image.new('RGBA', (W, H), (255, 255, 255, 255)), 0.6 * (1 - (t - tf) / 0.1))
        if t > TOTAL - 0.1:
            fr = Image.blend(fr, Image.new('RGBA', (W, H), (0, 0, 0, 255)), min(1, (t - (TOTAL - 0.1)) / 0.1))
        rgb = fr.convert('RGB')
        if PREVIEW: rgb.resize((360, 640), Image.LANCZOS).save(os.path.join(ROOT, 'prev4', f'f{fi:04d}.jpg'), quality=88)
        else: out.stdin.write(rgb.tobytes())
    if out: out.stdin.close(); out.wait()
    print('ok')

main()
