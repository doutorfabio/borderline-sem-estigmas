import json, sys, subprocess, statistics as st
import numpy as np
from deshine import deshine
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, NF = 1080, 1920, 30, 822
SAFE_L, SAFE_R, SAFE_T, SAFE_B = 90, 950, 90, 1536   # 90 px + 12% direita + 20% embaixo
CX = (SAFE_L + SAFE_R) // 2
CREAM = (0xF4, 0xE9, 0xD5); AMBER = (0xF2, 0xB5, 0x44); WHITE = (255, 255, 255)
F_SERIF = "/mnt/skills/examples/canvas-design/canvas-fonts/Gloock-Regular.ttf"
F_HEAVY = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
F_CAP = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
F_CAPB = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
_fc = {}
def font(p, s):
    k = (p, int(s))
    if k not in _fc: _fc[k] = ImageFont.truetype(p, int(s))
    return _fc[k]

words = json.load(open("words.json"))
for w in words: w["w"] = w["w"].strip(",.")

# ---------- rosto: queixo por take (cortes da gravação em quadros de 30 fps)
CUTS = [0, 76, 170, 264, 296, 384, 472, 557, 670, 755, 822]
BROLL = [(76, 169), (207, 263), (308, 383), (557, 669)]
faces = json.load(open("faces.json"))
chin = {}
for a, b in zip(CUTS, CUTS[1:]):
    s = [f for f in faces if a / FPS <= f["t"] < b / FPS]
    chin[a] = st.median([f["y"] + f["h"] + 0.05 * f["w"] for f in s])
def in_broll(n): return any(a <= n <= b for a, b in BROLL)
def chin_at(n):
    seg = max(c for c in CUTS[:-1] if c <= n)
    return chin[seg]

# ---------- texto grande
BT = [  # t0, t_exit (None = até o fim), centro y, linhas
    (1.53, 3.15, 1235, [[("A", "s"), ("FESTA", "h")], [("INTEIRA", "s")]]),
    (10.18, 11.80, 1300, [[("POR", "s"), ("DENTRO", "h")]]),
    (17.50, 19.12, 470, [[("NÃO TINHA MAIS", "s")], [("NINGUÉM", "h")]]),
    (23.53, 25.15, 340, [[("JÁ TINHA SE", "s")], [("DESPEDIDO", "h")]]),
    (25.25, None, 300, [[("SÓ VIU A", "s")], [("FESTA", "h")]]),
]
SER, HEV = 132, 200
TRK = 0.07
def tbbox(f, tx):
    """bbox com espaçamento entre letras (serifa)"""
    if f.path != F_SERIF: return f.getbbox(tx, anchor="ls")
    x = 0; x0 = None; t = b = 0
    for ch in tx:
        bb = f.getbbox(ch, anchor="ls")
        if ch != " ":
            x0 = x + bb[0] if x0 is None else x0; t = min(t, bb[1]); b = max(b, bb[3]); x1 = x + bb[2]
        x += f.getlength(ch) + TRK * f.size
    return (x0, t, x1, b)
def ttext(d, xy, tx, f, fill):
    if f.path != F_SERIF: d.text(xy, tx, font=f, anchor="ls", fill=fill); return
    x, y = xy
    for ch in tx:
        d.text((x, y), ch, font=f, anchor="ls", fill=fill); x += f.getlength(ch) + TRK * f.size
def layout_bt(lines):
    """retorna lista de (texto, tipo, size, x, baseline) e bbox de tinta"""
    scale = 1.0
    while True:
        rows = []
        for ln in lines:
            items = []; x = 0
            for i, (tx, k) in enumerate(ln):
                f = font(F_SERIF if k == "s" else F_HEAVY, (SER if k == "s" else HEV) * scale)
                if i: x += 0.30 * SER * scale
                bb = tbbox(f, tx)
                items.append([tx, k, f, x - bb[0], bb]); x += bb[2] - bb[0]
            asc = max(-it[4][1] for it in items); desc = max(it[4][3] for it in items)
            rows.append((items, x, asc, desc))
        if max(r[1] for r in rows) <= (SAFE_R - SAFE_L) - 10: break
        scale *= 0.97
    gap = 30 * scale
    total = sum(r[2] + r[3] for r in rows) + gap * (len(rows) - 1)
    return rows, total, gap

BT_L = [(t0, te, cy, *layout_bt(ls)) for t0, te, cy, ls in BT]

def ease_out(p, k=3): p = min(max(p, 0), 1); return 1 - (1 - p) ** k

def draw_bt(img, sh, t):
    hide = False; boxes = []
    for t0, te, cy, rows, total, gap in BT_L:
        if t < t0 or (te is not None and t > te + 0.12): continue
        hide = True
        fade = 1.0 if te is None or t <= te else 1 - (t - te) / 0.12
        y = cy - total / 2
        for items, wdt, asc, desc in rows:
            base = y + asc; x0 = CX - wdt / 2
            for tx, k, f, xo, bb in items:
                if k == "s":
                    e = ease_out((t - t0) / 0.30); a = e * fade; dy = 16 * (1 - e); f2 = f; col = CREAM
                    xx = x0 + xo
                else:
                    p = (t - t0 - 0.10) / 0.32; e = ease_out(p, 4); a = min(max(p / 0.45, 0), 1) * fade
                    dy = -34 * (1 - e); sc = min(1.04 - 0.04 * e, (SAFE_R - SAFE_L - 6) / (bb[2] - bb[0])); col = AMBER
                    f2 = font(F_HEAVY, f.size * sc)
                    bb2 = f2.getbbox(tx, anchor="ls"); wc = bb[2] - bb[0]; xx = x0 + xo + bb[0] + wc / 2 - (bb2[2] + bb2[0]) / 2
                if a <= 0: continue
                d = ImageDraw.Draw(img); ds = ImageDraw.Draw(sh)
                ttext(ds, (xx, base + dy + 6), tx, f2, (0, 0, 0, int(215 * a)))
                ttext(d, (xx, base + dy), tx, f2, col + (int(255 * a),))
                bq = tbbox(f2, tx); boxes.append((xx + bq[0], base + dy + bq[1], xx + bq[2], base + dy + bq[3]))
            y = base + desc + gap
    return hide, boxes

# ---------- legenda pequena
CHUNKS = [(0, 3), (4, 6), (12, 16), (17, 19), (20, 23), (24, 27), (28, 31), (32, 36), (37, 40),
          (44, 49), (50, 53), (54, 58), (59, 62), (63, 65), (70, 74), (75, 78), (79, 81), (82, 86)]
IMPACT = {"sofreu", "parabéns", "quarto", "indignação", "controlar", "tarde"}
HIDES = [(t0, (te if te else 99) + 0.12) for t0, te, *_ in BT]
def hidden(t): return any(a <= t < b for a, b in HIDES)
# janela de exibição de cada bloco
CW = []
for i, (a, b) in enumerate(CHUNKS):
    s = words[a]["s"] - 0.08
    e = words[CHUNKS[i + 1][0]]["s"] - 0.08 if i + 1 < len(CHUNKS) else words[b]["e"] + 0.3
    for ha, hb in HIDES:
        if ha <= s < hb: s = hb
        if s < ha < e: e = ha
    if e - s >= 0.25: CW.append((a, b, s, e))
CS, CSB = 58, 62
def cap_layout(a, b):
    toks = []
    for w in words[a:b + 1]:
        imp = w["w"].lower() in IMPACT
        tx = w["w"].upper() if imp else w["w"]
        f = font(F_CAPB if imp else F_CAP, CSB if imp else CS)
        toks.append((tx, f, imp, w))
    sp = 0.30 * CS; maxw = SAFE_R - SAFE_L - 20
    lines = [[]]; lw = [0]
    for tk in toks:
        tw = tk[1].getlength(tk[0])
        if lines[-1] and lw[-1] + sp + tw > maxw: lines.append([]); lw.append(0)
        lw[-1] += (sp if lines[-1] else 0) + tw; lines[-1].append((tk, tw))
    if len(lines) == 1 and lw[0] > 0.62 * maxw and len(toks) >= 5:   # equilibrar em 2 linhas
        best = None
        for k in range(2, len(toks) - 1):
            w1 = sum(t[1].getlength(t[0]) for t in toks[:k]) + sp * (k - 1)
            w2 = sum(t[1].getlength(t[0]) for t in toks[k:]) + sp * (len(toks) - k - 1)
            if len(toks[k][0]) <= 2 and False: pass
            sc = max(w1, w2)
            if best is None or sc < best[0]: best = (sc, k)
        k = best[1]
        lines = [[(t, t[1].getlength(t[0])) for t in toks[:k]], [(t, t[1].getlength(t[0])) for t in toks[k:]]]
        lw = [sum(x[1] for x in l) + sp * (len(l) - 1) for l in lines]
    assert len(lines) <= 2, (a, b)
    return lines, lw, sp
LH = 74
def draw_cap(img, sh, t, n):
    for a, b, s, e in CW:
        if s <= t < e: break
    else: return []
    lines, lw, sp = cap_layout(a, b)
    hblk = LH * len(lines)
    if 557 <= n <= 669: top = 1075          # cozinha: acima do balcão, sem cobrir o nome
    elif in_broll(n): top = 1330
    else: top = chin_at(n) + 0.08 * H
    top = min(top, SAFE_B - hblk)
    ent = ease_out((t - s) / 0.12); dy0 = 10 * (1 - ent)
    d = ImageDraw.Draw(img); ds = ImageDraw.Draw(sh); boxes = []
    for li, (ln, wl) in enumerate(zip(lines, lw)):
        x = CX - wl / 2; base = top + LH * li + 56 + dy0
        for (tx, f, imp, w), tw in ln:
            if t < w["s"]: al = 0.62
            else: al = 1.0
            act = w["s"] <= t < max(w["e"], w["s"] + 0.12)
            sc = 1 + 0.07 * ease_out((t - w["s"]) / 0.08) if act else 1.0
            f2 = font(f.path, f.size * sc) if sc != 1 else f
            tw2 = f2.getlength(tx); xx = x + tw / 2 - tw2 / 2
            col = AMBER if imp else WHITE
            a = al * ent
            ds.text((xx, base + 3), tx, font=f2, anchor="ls", fill=(0, 0, 0, int(235 * a)), stroke_width=3, stroke_fill=(0, 0, 0, int(235 * a)))
            d.text((xx, base), tx, font=f2, anchor="ls", fill=col + (int(255 * a),))
            boxes.append(d.textbbox((xx, base), tx, font=f2, anchor="ls"))
            x += tw + sp
    return boxes

def overlay(n):
    t = n / FPS
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hide, bb1 = draw_bt(img, sh, t)
    sh_bt = sh.filter(ImageFilter.GaussianBlur(12)) if bb1 else None
    sh2 = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bb2 = []
    if not hide: bb2 = draw_cap(img, sh2, t, n)
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if sh_bt: out = Image.alpha_composite(out, sh_bt)
    if bb2: out = Image.alpha_composite(out, sh2.filter(ImageFilter.GaussianBlur(7)))
    out = Image.alpha_composite(out, img)
    return out, bb1, bb2

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "frames":   # quadros de conferência
        base = sys.argv[2]
        for n in map(int, sys.argv[3:]):
            fr = subprocess.run(["ffmpeg", "-v", "error", "-i", base, "-vf", f"select=eq(n\\,{n})", "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
            im = Image.fromarray(deshine(np.frombuffer(fr, np.uint8).reshape(H, W, 3), n)).convert("RGBA")
            ov, b1, b2 = overlay(n)
            im = Image.alpha_composite(im, ov).convert("RGB")
            for bx in b1 + b2:
                ok = bx[0] >= SAFE_L and bx[2] <= SAFE_R and bx[1] >= SAFE_T and bx[3] <= SAFE_B
                if not ok: print("FORA DA MARGEM", n, bx)
            im.save(f"chk/f{n:04d}.png")
            print(n, f"{n/FPS:.2f}s", "BT" if b1 else "", "cap" if b2 else "", [tuple(map(int, b)) for b in (b1 or b2)][:1])
    elif mode == "render":
        dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", sys.argv[2], "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                                "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-pix_fmt", "yuv420p", sys.argv[3]], stdin=subprocess.PIPE)
        bad = 0
        for n in range(NF):
            fr = dec.stdout.read(W * H * 3)
            if len(fr) < W * H * 3: break
            im = Image.fromarray(deshine(np.frombuffer(fr, np.uint8).reshape(H, W, 3), n)).convert("RGBA")
            ov, b1, b2 = overlay(n)
            for bx in b1 + b2:
                if not (bx[0] >= SAFE_L and bx[2] <= SAFE_R and bx[1] >= SAFE_T and bx[3] <= SAFE_B): bad += 1
            enc.stdin.write(Image.alpha_composite(im, ov).convert("RGB").tobytes())
        enc.stdin.close(); enc.wait(); print("frames", n + 1, "fora da margem:", bad)
    elif mode == "srt":
        def ts(x):
            ms = int(round(x * 1000)); return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"
        SRT = [(0, 3), (4, 9), (10, 13), (14, 16), (17, 19), (20, 23), (24, 27), (28, 31), (32, 36), (37, 40), (41, 43), (44, 49), (50, 53), (54, 58),
               (59, 62), (63, 65), (66, 69), (70, 74), (75, 78), (79, 81), (82, 86), (87, 92), (93, 97), (98, 103)]
        assert [i for a, b in SRT for i in range(a, b + 1)] == list(range(len(words)))
        out = []
        for k, (a, b) in enumerate(SRT):
            s = words[a]["s"]; e = words[SRT[k + 1][0]]["s"] if k + 1 < len(SRT) else 27.4
            out.append(f"{k+1}\n{ts(s)} --> {ts(e)}\n{' '.join(w['w'] for w in words[a:b+1])}\n")
        open(sys.argv[2], "w").write("\n".join(out)); print("\n".join(out))
    elif mode == "info":
        print("chin", chin); print("CW", [(" ".join(w['w'] for w in words[a:b+1]), round(s, 2), round(e, 2)) for a, b, s, e in CW])
