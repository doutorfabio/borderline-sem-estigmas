import os, sys, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

S = "/tmp/claude-0/-home-user-borderline-sem-estigmas/225ca122-7ddc-5f7b-8d3b-85fb58ddf29a/scratchpad"
FD = "/home/user/borderline-sem-estigmas/.claude/skills/onetake/looks/fonts/"
K = 1.5
W, H = 1080, 1920
N = 697


def L(i):
    return cv2.imread(f"{S}/all/{i+1:04d}.jpg")


def font(name, size, wght):
    f = ImageFont.truetype(FD + name, int(round(size)))
    axes = f.get_variation_axes()
    vals = []
    for a in axes:
        n = a["name"]
        n = n.decode() if isinstance(n, bytes) else n
        if n == "Weight":
            vals.append(wght)
        elif n == "Optical Size":
            vals.append(72)
        elif n == "Wonky":
            vals.append(0)
        else:
            vals.append(a["default"])
    f.set_variation_by_axes(vals)
    return f


def text_img(lines, f, fill, spacing=1.25, align="left", track=0.0, pad=12):
    """lines: list of str or (str, font, fill). returns RGBA PIL image"""
    items = []
    for l in lines:
        if isinstance(l, str):
            l = (l, f, fill)
        items.append(l)
    d = ImageDraw.Draw(Image.new("RGBA", (4, 4)))

    def width(t, ft):
        if track:
            return sum(d.textlength(c, font=ft) for c in t) + track * ft.size * (len(t) - 1)
        return d.textlength(t, font=ft)

    ws = [width(t, ft) for t, ft, _ in items]
    hs = [ft.size * spacing for _, ft, _ in items]
    Wt, Ht = int(max(ws)) + 2 * pad, int(sum(hs)) + 2 * pad
    im = Image.new("RGBA", (Wt, Ht), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    y = pad
    for (t, ft, fl), w, h in zip(items, ws, hs):
        x = pad if align == "left" else pad + (max(ws) - w) / 2
        yy = y + (h - ft.size) / 2
        if track:
            for c in t:
                dr.text((x, yy), c, font=ft, fill=fl)
                x += d.textlength(c, font=ft) + track * ft.size
        else:
            dr.text((x, yy), t, font=ft, fill=fl)
        y += h
    return im


def paste(frame, rgba, cx, cy, alpha=1.0, angle=0.0, scale=1.0, anchor="c"):
    """frame: BGR uint8 array; rgba: PIL RGBA. anchor c=center, tl=top-left"""
    im = rgba
    if scale != 1.0:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.LANCZOS)
    if angle:
        im = im.rotate(angle, resample=Image.BICUBIC, expand=True)
    a = np.asarray(im).astype(np.float32)
    h, w = a.shape[:2]
    x0 = int(round(cx - w / 2)) if anchor == "c" else int(round(cx))
    y0 = int(round(cy - h / 2)) if anchor == "c" else int(round(cy))
    xa, ya = max(0, x0), max(0, y0)
    xb, yb = min(frame.shape[1], x0 + w), min(frame.shape[0], y0 + h)
    if xb <= xa or yb <= ya:
        return
    sub = a[ya - y0:yb - y0, xa - x0:xb - x0]
    al = sub[..., 3:4] / 255.0 * alpha
    dst = frame[ya:yb, xa:xb].astype(np.float32)
    frame[ya:yb, xa:xb] = (dst * (1 - al) + sub[..., 2::-1] * al + 0.5).astype(np.uint8)


def fill_rows(f, y0, y1, x0, x1, ls, rs, src=None):
    """replace f[y0:y1, x0:x1] by a per-row linear fit from clean samples ls=(a,b), rs=(a,b)"""
    xs = np.concatenate([np.arange(*ls), np.arange(*rs)]).astype(np.float32)
    xt = np.arange(x0, x1, dtype=np.float32)
    reg = (f if src is None else src)[y0:y1].astype(np.float32)
    reg = cv2.blur(reg, (1, 9))
    samp = np.concatenate([reg[:, ls[0]:ls[1]], reg[:, rs[0]:rs[1]]], axis=1)  # rows, n, 3
    xm = xs.mean()
    xv = ((xs - xm) ** 2).sum()
    sm = samp.mean(1)  # rows,3
    slope = ((xs - xm)[None, :, None] * (samp - sm[:, None, :])).sum(1) / xv
    out = sm[:, None, :] + slope[:, None, :] * (xt - xm)[None, :, None]
    # feather the edges of the rectangle
    m = np.zeros((y1 - y0, x1 - x0), np.float32)
    m[6:-6, 6:-6] = 1
    if x0 == 0 and x1 == f.shape[1]:
        m[6:-6, :] = 1
        m = cv2.copyMakeBorder(m, 0, 0, 20, 20, cv2.BORDER_REPLICATE)
        m = cv2.GaussianBlur(m, (0, 0), 3)[:, 20:-20]
        if y1 == f.shape[0]:
            m[-30:] = 1
        m = m[..., None]
    else:
        m = cv2.GaussianBlur(m, (0, 0), 3)[..., None]
    cur = f[y0:y1, x0:x1].astype(np.float32)
    f[y0:y1, x0:x1] = np.clip(cur * (1 - m) + out * m + 0.5, 0, 255).astype(np.uint8)


def ease(t):
    t = min(1, max(0, t))
    return 1 - (1 - t) ** 3


def k(v):
    return int(round(v * K))


# ---------- assets ----------
INK = (24, 22, 26, 255)
RED = (204, 0, 0, 255)

# clean paper card from frame 140
src = L(140)
m = (src.min(2) > 200).astype(np.uint8)
m[:330] = 0
m[850:] = 0
m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
kk = 1 + np.argmax(st[1:, 4])
px, py, pw, ph = st[kk][:4]
pm = (lab == kk).astype(np.uint8)
crop = src[py:py + ph, px:px + pw].copy()
g = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
tm = ((g < 170) & (pm[py:py + ph, px:px + pw] > 0)).astype(np.uint8)
tm[:12] = 0; tm[-12:] = 0; tm[:, :12] = 0; tm[:, -12:] = 0
tm = cv2.dilate(tm, np.ones((9, 9), np.uint8))
crop = cv2.inpaint(crop, tm, 7, cv2.INPAINT_TELEA)
alpha = cv2.GaussianBlur(pm[py:py + ph, px:px + pw].astype(np.float32) * 255, (0, 0), 1.2)
paper = np.dstack([crop[..., ::-1], alpha.astype(np.uint8)])
PAPER = Image.fromarray(paper, "RGBA").resize((k(pw), k(ph)), Image.LANCZOS)
PCX, PCY = (px + pw / 2) * K, (py + ph / 2) * K
print("paper", px, py, pw, ph, file=sys.stderr)


def card(content_fn):
    im = PAPER.copy()
    content_fn(im)
    # soft shadow
    pad = 40
    sh = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    a = np.zeros((sh.height, sh.width), np.float32)
    a[pad + 10:pad + 10 + im.height, pad:pad + im.width] = np.asarray(im)[..., 3] * 0.28
    a = cv2.GaussianBlur(a, (0, 0), 12)
    sh = Image.fromarray(np.dstack([np.zeros((sh.height, sh.width, 3), np.uint8), a.astype(np.uint8)]), "RGBA")
    sh.alpha_composite(im, (pad, pad))
    return sh


def c1(im):
    d = ImageDraw.Draw(im)
    w, h = im.size
    r = 46
    cx, cy = int(w * 0.17), int(h * 0.36)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(200, 40, 60, 255))
    fx = font("Inter.ttf", 64, 800)
    d.text((cx, cy - 2), "!", font=fx, fill=(255, 255, 255, 255), anchor="mm")
    d.text((cx + r + 26, cy), "Chamada perdida", font=font("Inter.ttf", 46, 500), fill=(70, 66, 72, 255), anchor="lm")
    d.text((int(w * 0.11), int(h * 0.66)), "Não atendeu.", font=font("Inter.ttf", 104, 800), fill=INK, anchor="lm")


def c2(im):
    d = ImageDraw.Draw(im)
    w, h = im.size
    d.text((int(w * 0.09), int(h * 0.36)), "Quem vê de fora chama de", font=font("Inter.ttf", 45, 700), fill=INK, anchor="lm")
    t = text_img(["joguinho?"], font("Inter.ttf", 122, 900), INK, pad=30)
    t = t.transform(t.size, Image.AFFINE, (1, 0.2, -0.2 * t.height / 2, 0, 1, 0), resample=Image.BICUBIC)
    im.alpha_composite(t, (int(w * 0.09) - 30, int(h * 0.62) - t.height // 2))


CARD1, CARD2 = card(c1), card(c2)

T1 = text_img(["VOCÊ LIGOU E O"], font("Inter.ttf", 47, 600), (255, 255, 255, 255), track=0.13)
T3 = text_img(["NÃO ATENDEU"], font("Inter.ttf", 47, 600), (255, 255, 255, 255), track=0.13)
TCX = 343 * K

def hook():
    fa = font("Inter.ttf", 92, 900)
    t = text_img(["RECLAMOU QUE", "VOCÊ NÃO LIGOU."], fa, (255, 255, 255, 255), spacing=1.12, align="center", pad=40)
    al = np.asarray(t)[..., 3].astype(np.float32)
    sh = cv2.GaussianBlur(np.roll(al, 5, axis=0), (0, 0), 9) * 1.1
    out = Image.fromarray(np.dstack([np.zeros(al.shape + (3,), np.uint8), np.clip(sh, 0, 255).astype(np.uint8)]), "RGBA")
    out.alpha_composite(t)
    return out


HOOK = hook()
HOOK_Y = 1425
if os.environ.get("HOOKIMG"):
    _im = Image.open(os.environ["HOOKIMG"]).convert("RGBA")
    _w = 880
    _im = _im.resize((_w, int(_im.height * _w / _im.width)), Image.LANCZOS)
    _pad = 40
    _a = np.zeros((_im.height + 2 * _pad, _im.width + 2 * _pad), np.float32)
    _a[_pad + 10:_pad + 10 + _im.height, _pad:_pad + _im.width] = 150
    _a = cv2.GaussianBlur(_a, (0, 0), 14)
    HOOK = Image.fromarray(np.dstack([np.zeros(_a.shape + (3,), np.uint8), _a.astype(np.uint8)]), "RGBA")
    HOOK.alpha_composite(_im, (_pad, _pad))
    HOOK = HOOK.rotate(2, resample=Image.BICUBIC, expand=True)
    HOOK_Y = 1285
BUB = text_img(["Tô aqui", "quando você", "quiser."], font("Inter.ttf", 45, 700), INK, spacing=1.24, align="center")
WALL = text_img(["mais alguns minutos"], font("Fraunces.ttf", 74, 700), (20, 20, 20, 235))

REF_A = cv2.resize(L(90), (W, H), interpolation=cv2.INTER_LANCZOS4)
REF_B = cv2.resize(L(130), (W, H), interpolation=cv2.INTER_LANCZOS4)
plateC = cv2.resize(L(318), (W, H), interpolation=cv2.INTER_LANCZOS4)

# sticker mask
SCX, SCY, SR = 127, 825, 97
yy, xx = np.mgrid[0:H, 0:W]
smask = np.clip((SR * K - np.hypot(xx - SCX * K, yy - SCY * K)) / 2.0 + 0.5, 0, 1)[..., None].astype(np.float32)


def biggest(mask):
    n, lab, st, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)
    if n < 2:
        return None, None
    j = 1 + np.argmax(st[1:, 4])
    return st[j], (lab == j)


def filled(comp, grow, close_right=None, close_left=None):
    comp = cv2.dilate(comp.astype(np.uint8), np.ones((grow, grow), np.uint8))
    if close_right is not None:
        comp[close_right[0]:close_right[1], -3:] = 1
    if close_left is not None:
        comp[close_left[0]:close_left[1], :3] = 1
    cs, _ = cv2.findContours(comp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    out = np.zeros_like(comp)
    cv2.drawContours(out, cs, -1, 1, -1)
    return out


PHONE = []
if os.environ.get("PHONE"):
    _c = cv2.VideoCapture(os.environ["PHONE"])
    for _ in range(22):
        PHONE.append(_c.read()[1])


def process(i, small):
    if i < len(PHONE):
        small = PHONE[i]
    f = cv2.resize(small, (W, H), interpolation=cv2.INTER_LANCZOS4)

    # ---- 0: hook over the opening scene ----
    if i <= 64:
        e = ease((i + 1) / 5)
        paste(f, HOOK, 502, HOOK_Y, scale=0.9 + 0.1 * e)

    # ---- A: pink card scene ----
    if 65 <= i <= 165:
        orig = f.copy()
        fill_rows(f, k(98), k(148), k(140), k(545), (k(60), k(135)), (k(550), k(660)))
        fill_rows(f, k(230), k(278), k(160), k(520), (k(60), k(155)), (k(525), k(660)))
        ref = REF_A if i < 104 else REF_B
        fill_rows(f, k(290), H, 0, W, (0, k(10)), (W - k(22), W), src=ref)
        paste(f, T1, TCX, 124 * K)
        paste(f, T3, TCX, 255.5 * K)
        if i <= 104:
            e = ease((i - 64) / 5)
            out = ease((i - 100) / 4) if i >= 101 else 0
            paste(f, CARD1, PCX - 10 - out * 900, PCY - 20 + (1 - e) * 40, alpha=e * (1 - out), angle=3.0, scale=0.94 + 0.06 * e)
            if i <= 100:
                sa = smask * e
                f[:] = (f * (1 - sa) + orig * sa + 0.5).astype(np.uint8)
        if i >= 102:
            e = ease((i - 101) / 6)
            drift = (i - 102) / 63 * 10
            paste(f, CARD2, PCX + (1 - e) * 700, PCY - drift, alpha=min(1, e * 1.5), angle=-1.5 * (1 - e), scale=1 + 0.02 * (i - 102) / 63)

    # ---- B: blue card on lap ----
    if 166 <= i <= 226:
        s = small.astype(int)
        bl = (s[..., 0] > 170) & (s[..., 2] < 150) & (s[..., 0] - s[..., 2] > 60)
        st, comp = biggest(bl)
        if st is not None and st[4] > 15000:
            bx, by, bw = st[0], st[1], st[2]
            sc = bw / 292.0
            # small garbled label on the blue header
            x0, x1, y0, y1 = bx + 28 * sc, bx + 100 * sc, by + 20 * sc, by + 50 * sc
            col = np.median(small[int(by + 12 * sc):int(by + 18 * sc), int(bx + 40 * sc):int(bx + 100 * sc)].reshape(-1, 3), 0)
            lay = np.zeros((H, W), np.float32)
            cv2.rectangle(lay, (k(x0), k(y0)), (k(x1), k(y1)), 1, -1)
            lay = cv2.GaussianBlur(lay, (0, 0), 3)[..., None]
            f[:] = (f * (1 - lay) + col[None, None, :] * lay + 0.5).astype(np.uint8)
            # white strip
            quad = np.array([(36, 96), (270, 38), (290, 112), (54, 172)], np.float32) * sc + (bx, by)
            q = (quad * K).astype(np.int32)
            ss = 4
            lay = np.zeros((H, W), np.uint8)
            cv2.fillConvexPoly(lay, q, 255, lineType=cv2.LINE_AA)
            la = (lay.astype(np.float32) / 255)[..., None]
            f[:] = (f * (1 - la) + np.array([252, 252, 252], np.float32) * la + 0.5).astype(np.uint8)
            c = quad.mean(0) * K
            t = text_img(["Acabou."], font("Inter.ttf", 62 * sc, 800), INK)
            paste(f, t, c[0], c[1], angle=13.8)

    # ---- C: wall text ----
    if 320 <= i <= 367:
        x0, x1, y0, y1 = k(50), k(670), k(285), k(400)
        m = np.zeros((y1 - y0, x1 - x0), np.float32)
        m[14:-14, 14:-14] = 1
        m = cv2.GaussianBlur(m, (0, 0), 7)[..., None]
        cur = f[y0:y1, x0:x1].astype(np.float32)
        pl = plateC[y0:y1, x0:x1].astype(np.float32)
        ring_c = np.concatenate([f[y0 - 20:y0, x0:x1].reshape(-1, 3), f[y1:y1 + 20, x0:x1].reshape(-1, 3)]).mean()
        ring_p = np.concatenate([plateC[y0 - 20:y0, x0:x1].reshape(-1, 3), plateC[y1:y1 + 20, x0:x1].reshape(-1, 3)]).mean()
        pl = pl * (ring_c / max(1, ring_p))
        f[y0:y1, x0:x1] = np.clip(cur * (1 - m) + pl * m + 0.5, 0, 255).astype(np.uint8)
    if 300 <= i <= 367:
        e = ease((i - 299) / 7)
        paste(f, WALL, W / 2, 352 * K + (1 - e) * 18, alpha=e)

    # ---- D: stray marks inside the 10 ----
    if 368 <= i <= 429:
        g = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        dark = (g < 120).astype(np.uint8)
        n, lab, st, _ = cv2.connectedComponentsWithStats(dark, 8)
        kill = np.zeros_like(dark)
        for j in range(1, n):
            x, y, w, h, a = st[j]
            if 40 < a < 2600 and x > 380 and 330 < y < 640 and w < 110 and h < 80:
                kill[lab == j] = 1
        if kill.any():
            kill = cv2.dilate(kill, np.ones((11, 11), np.uint8))
            kb = cv2.resize(kill, (W, H), interpolation=cv2.INTER_LINEAR)
            f[:] = cv2.inpaint(f, kb, 5, cv2.INPAINT_TELEA)

    # ---- E: speech bubble ----
    if 472 <= i <= 550:
        w_ = (small.min(2) > 238).astype(np.uint8)
        w_[450:] = 0
        w_[:, :380] = 0
        w_ = cv2.erode(w_, np.ones((5, 5), np.uint8))
        st, comp = biggest(w_)
        if st is not None and st[4] > 15000:
            x, y, w, h = st[:4]
            fm = filled(comp, 3, close_right=(y + 4, y + int(h * 0.8)) if x + w >= 712 else None)
            fm = cv2.resize(fm, (W, H), interpolation=cv2.INTER_LINEAR).astype(np.float32)
            fm = cv2.GaussianBlur(fm, (0, 0), 1.5)[..., None]
            f[:] = (f * (1 - fm) + 255 * fm + 0.5).astype(np.uint8)
            hb = (h + 6) * K
            wb = 0.924 * hb
            vis = min(wb, W - (x - 3) * K)
            paste(f, BUB, (x - 3) * K + vis * 0.5, (y - 3) * K + hb * 0.425)

    # ---- F: white message card ----
    if 551 <= i <= 650:
        w_ = (small.min(2) > 246).astype(np.uint8)
        w_ = cv2.erode(w_, np.ones((9, 9), np.uint8))
        st, comp = biggest(w_)
        if st is not None and st[4] > 60000 and st[2] > 380:
            x, y, w, h = st[:4]
            x -= 4; y -= 4; w += 8; h += 8
            fm = filled(comp, 5)
            fm = cv2.resize(fm, (W, H), interpolation=cv2.INTER_LINEAR).astype(np.float32)
            fm = cv2.GaussianBlur(fm, (0, 0), 1.5)[..., None]
            f[:] = (f * (1 - fm) + 255 * fm + 0.5).astype(np.uint8)
            wk, hk = w * K, h * K
            fs = wk * 0.059
            t = text_img(["Liguei porque quero falar", "com você. Tô aqui quando", "você quiser."], font("Inter.ttf", fs, 600), INK, spacing=1.3)
            tall = h / w > 0.6
            top = y * K + (wk * 0.075 if tall else (hk - t.height) / 2)
            paste(f, t, x * K + wk * 0.085, top, anchor="tl")
            if tall:
                t2 = text_img(["Tô."], font("Inter.ttf", fs * 2.3, 900), RED)
                paste(f, t2, x * K + wk * 0.085, top + t.height + hk * 0.06, anchor="tl")
        elif i <= 557 or 634 <= i <= 642:
            # blurred entrance/exit of the card: just blank the smeared text
            w2 = cv2.erode((small.min(2) > 236).astype(np.uint8), np.ones((5, 5), np.uint8))
            w2[:480] = 0
            w2[1000:] = 0
            w2[:, (420 if i <= 557 else 330):] = 0
            st, comp = biggest(w2)
            if st is not None and st[4] > 2500:
                x, y, w, h = st[:4]
                fm = filled(comp, 3, close_left=(y + 4, y + h - 4) if x <= 6 else None)
                fm = cv2.resize(fm, (W, H), interpolation=cv2.INTER_LINEAR).astype(np.float32)
                fm = cv2.GaussianBlur(fm, (0, 0), 2)[..., None]
                f[:] = (f * (1 - fm) + 255 * fm + 0.5).astype(np.uint8)
    return f


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        ids = [int(a) for a in sys.argv[2:]]
        ims = [cv2.resize(process(i, L(i)), (432, 768), interpolation=cv2.INTER_AREA) for i in ids]
        rows = [np.hstack(ims[r:r + 6] + [np.zeros_like(ims[0])] * (6 - len(ims[r:r + 6]))) for r in range(0, len(ims), 6)]
        cv2.imwrite(f"{S}/fr/test.jpg", np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 88])
    else:
        V = sys.argv[1]
        out = sys.argv[2]
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "24", "-i", "-",
                              "-i", V, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-b:v", "7000k", "-maxrate", "9000k", "-bufsize", "14000k",
                              "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-c:a", "copy", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
        cap = cv2.VideoCapture(V)
        i = 0
        while True:
            ok, fr = cap.read()
            if not ok:
                break
            p.stdin.write(process(i, fr).tobytes())
            i += 1
        p.stdin.close()
        p.wait()
        print("frames", i)
