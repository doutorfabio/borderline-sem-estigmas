import cv2, numpy as np, json
FACES = json.load(open("faces.json"))
CUTS = [0, 76, 170, 264, 296, 384, 472, 557, 670, 755, 822]
BROLL = [(76, 169), (207, 263), (308, 383), (557, 669)]
def facebox(n):
    t = n / 30; seg = max(c for c in CUTS[:-1] if c <= n); nxt = CUTS[CUTS.index(seg) + 1]
    c = [f for f in FACES if seg / 30 <= f["t"] < nxt / 30]
    f = min(c, key=lambda r: abs(r["t"] - t)); return f["x"], f["y"], f["w"], f["h"]
def deshine(rgb, n, strength=1.0):
    if any(a <= n <= b for a, b in BROLL): return rgb
    x, y, w, h = facebox(n)
    x0, x1 = max(0, int(x - 0.15 * w)), min(rgb.shape[1], int(x + 1.15 * w))
    y0, y1 = max(0, int(y - 0.45 * h)), min(rgb.shape[0], int(y + 0.95 * h))
    crop = rgb[y0:y1, x0:x1]
    lab = cv2.cvtColor(crop, cv2.COLOR_RGB2LAB).astype(np.float32)
    L, A, B = lab[..., 0], lab[..., 1], lab[..., 2]
    hsv = cv2.cvtColor(crop, cv2.COLOR_RGB2HSV).astype(np.float32)
    S = hsv[..., 1] / 255
    # tom de pele local sem o brilho: abertura morfológica + desfoque grande
    k = max(15, int(w * 0.13) | 1)
    Lb = cv2.morphologyEx(L, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    Lb = cv2.GaussianBlur(Lb, (0, 0), k / 2)
    Ab = cv2.GaussianBlur(A, (0, 0), k); Bb = cv2.GaussianBlur(B, (0, 0), k)
    # pele: crominância de pele (A,B acima do neutro) na vizinhança
    skin = ((Ab > 135) & (Bb > 140)).astype(np.float32)
    skin = cv2.GaussianBlur(skin, (0, 0), k / 3)
    diff = L - Lb
    m = np.clip((diff - 3) / 16, 0, 1) * np.clip((0.62 - S) / 0.3, 0, 1) * skin
    # zona: testa inteira (acima dos olhos) e nariz; olhos, dentes e barba ficam de fora
    zy = np.arange(crop.shape[0])[:, None] + y0; zx = np.arange(crop.shape[1])[None] + x0
    fore = (zy < y + 0.30 * h).astype(np.float32) * np.ones_like(zx, np.float32)
    nose = ((zy >= y + 0.30 * h) & (zy < y + 0.66 * h) & (zx > x + 0.36 * w) & (zx < x + 0.64 * w)).astype(np.float32)
    cheek = ((zy >= y + 0.50 * h) & (zy < y + 0.62 * h) & (((zx > x + 0.12 * w) & (zx < x + 0.32 * w)) | ((zx > x + 0.68 * w) & (zx < x + 0.88 * w)))).astype(np.float32)
    zone = cv2.GaussianBlur(np.maximum(np.maximum(fore, nose), cheek), (0, 0), 0.04 * w)
    m = m * zone
    m = cv2.GaussianBlur(m, (0, 0), 2.0) * strength
    L2 = L - m * np.maximum(diff, 0) * 0.95
    A2 = A + m * (Ab - A) * 0.85; B2 = B + m * (Bb - B) * 0.85
    out = cv2.cvtColor(np.clip(np.dstack([L2, A2, B2]), 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB)
    # borda suave da caixa
    fe = np.ones(m.shape, np.float32); pad = 12
    fe[:pad] *= np.linspace(0, 1, pad)[:, None]; fe[-pad:] *= np.linspace(1, 0, pad)[:, None]
    fe[:, :pad] *= np.linspace(0, 1, pad)[None]; fe[:, -pad:] *= np.linspace(1, 0, pad)[None]
    res = rgb.copy()
    res[y0:y1, x0:x1] = (crop * (1 - fe[..., None]) + out * fe[..., None]).astype(np.uint8)
    return res
if __name__ == "__main__":
    import subprocess, sys
    tiles = []
    for n in map(int, sys.argv[1:]):
        fr = subprocess.run(["ffmpeg", "-v", "error", "-i", "base.mp4", "-vf", f"select=eq(n\\,{n})", "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        im = np.frombuffer(fr, np.uint8).reshape(1920, 1080, 3)
        x, y, w, h = facebox(n); y0 = max(0, int(y - 0.45 * h)); y1 = min(1920, int(y + 0.95 * h)); x0 = max(0, int(x - 0.15 * w)); x1 = min(1080, int(x + 1.15 * w))
        a = im[y0:y1, x0:x1]; b = deshine(im, n)[y0:y1, x0:x1]
        pair = np.hstack([a, b]); pair = cv2.resize(pair, (int(pair.shape[1] * 520 / pair.shape[0]), 520))
        tiles.append(pair)
    [cv2.imwrite(f"deshine_{i}.jpg", cv2.cvtColor(tl, cv2.COLOR_RGB2BGR)) for i, tl in enumerate(tiles)]
