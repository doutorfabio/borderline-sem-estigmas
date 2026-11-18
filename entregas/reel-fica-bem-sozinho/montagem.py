import subprocess, sys, io, json, os, bisect
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

f32 = np.float32
W, H, FPS = 1080, 1920, 30
NF = 1420
IN, OR = "../in/", "../orig/"
GENP = {"A": IN+"e521e0a9.mp4", "B": IN+"0c6b7c71.mp4", "C": IN+"5472720b.mp4"}
MOTION, CHAVE, XIC, MESA = IN+"c8471695.mp4", IN+"29ed8a7c.mp4", IN+"3c022c99.mp4", IN+"65e348c8.mp4"
SEGOFF = {"A": -2, "B": 383, "C": 839}     # imagem 2 quadros adiantada: 1 da leitura do original + 1 do atraso do arquivo dele
SEGK = {"A": 401, "B": 547, "C": 580}
MAPJ = json.load(open(OR + "map.json"))
# cortes do corte original dele (quadros da linha mestra, 30 fps)
CUTS = [0, 126, 224, 316, 397, 483, 551, 601, 686, 745, 837, 861, 1020, 1101, 1174, 1236, 1344, 1420]
SHOT_SEG = "AAAA" + "BBBBBBB" + "CCCCCC"
GEN_RANGE = {0: (0, 100), 1: (100, 177), 2: (177, 248), 3: (248, 312), 4: (10, 79), 5: (79, 132), 6: (132, 171), 7: (171, 239), 8: (239, 285),
             9: (285, 359), 10: (359, 377), 11: (17, 142), 12: (142, 206), 13: (206, 264), 14: (264, 315), 15: (315, 398), 16: (398, 457)}
shot_of = lambda m: bisect.bisect_right(CUTS, m) - 1
T = lambda fr: fr / FPS

# ------------------------------------------------------------------ linha do tempo (quadros mestres)
M_IN, M_OUT = 150, 483                      # inserto: de "porque" ate o corte de "Pode mostrar"
Z145 = (601, 745)                           # S7 + S8: "No borderline ... disparar."
BIG_GATILHO = (628, 686)
BR_MESA = (745, 806, MESA, 0.45)
BIG_CULPA = (787, 806)
PUSH = (861, 1020)                          # S11: aproximacao lenta
BR_XIC = (1056, 1101, XIC, 1.0)
PSE = [1066, 1080, 1086]; PSE_END = 1116
BR_CHAVE = (1128, 1174, CHAVE, 0.95)
BIG_FINAL = (1344, NF + 1)
BROLLS = [BR_MESA, BR_XIC, BR_CHAVE]
BIGS = [BIG_GATILHO, BIG_CULPA, (PSE[0], PSE_END), BIG_FINAL]

def motion_tau(t):
    """tempo do inserto (s) para o tempo mestre t (s)"""
    if t < 5.45: return t - 5.00
    if t < 6.813: return 0.45
    if t < 8.363: return 0.45 + (t - 6.813)
    if t < 8.56: return 2.0 - 1/60
    if t < 10.56: return 2.0 + (t - 8.56)
    if t < 11.812: return 4.0 - 1/60
    if t < 13.551: return min(4.0 + (t - 11.812)*1.15, 6.0 - 1/60)
    if t < 14.47: return 6.0 - 1/60
    return min(6.0 + (t - 14.47)*1.15, 8.0 - 1/60)

def zoom_at(m):
    if Z145[0] <= m < Z145[1]: return 1.45
    if PUSH[0] <= m < PUSH[1]: return 1.30*(1.45/1.30)**((m - PUSH[0])/(PUSH[1] - PUSH[0] - 1))
    return 1.30

# ------------------------------------------------------------------ palavras (tempo local de cada gravacao) e blocos de legenda
WA = [("Sabe", 0.24), ("que", 0.42), ("tem", 0.52), ("borderline", 0.66), ("que", 1.00), ("só", 1.09), ("fica", 1.17), ("bem", 1.30), ("sozinho,", 1.65),
      ("e", 2.47), ("isso", 2.66), ("acaba", 2.82), ("confundindo", 3.02), ("com", 3.68), ("melhora.", 3.86),
      ("Faz", 4.26), ("sentido,", 4.42), ("porque", 5.00), ("sem", 5.26), ("gente", 5.44), ("por", 5.72), ("perto,", 5.88),
      ("ninguém", 6.31), ("se", 6.59), ("atrasa,", 6.85), ("ninguém", 7.53), ("te", 7.97), ("deixa", 8.28), ("no", 8.46), ("silêncio", 8.55),
      ("ou", 9.31), ("coloca", 9.78), ("pressão.", 10.06), ("Se", 10.70), ("ninguém", 10.90), ("cutuca,", 11.12), ("vem", 11.87), ("a", 12.11), ("paz", 12.25), ("de", 12.58), ("verdade.", 12.75)]
WB = [("Só", 0.46), ("que", 0.64), ("é", 0.79), ("uma", 0.85), ("paz", 0.96), ("que", 1.16), ("ainda", 1.24), ("não", 1.66), ("foi", 1.92), ("posta", 2.15), ("à", 2.67), ("prova.", 2.75),
      ("Pode", 3.29), ("mostrar", 3.42), ("que", 3.72), ("algo", 3.90), ("parou", 4.10), ("de", 4.72), ("te", 4.86), ("cutucar,", 4.98),
      ("e", 5.80), ("não", 5.96), ("que", 6.07), ("você", 6.15), ("melhorou,", 6.38), ("entendeu?", 6.73),
      ("No", 7.54), ("borderline,", 7.68), ("o", 8.10), ("gatilho", 8.14), ("quase", 8.60), ("sempre", 8.96), ("é", 9.38), ("gente.", 9.47),
      ("Sem", 10.05), ("ninguém,", 10.28), ("não", 10.77), ("tem", 11.02), ("o", 11.20), ("que", 11.27), ("disparar.", 11.35),
      ("E", 12.26), ("muita", 12.44), ("gente", 12.60), ("se", 12.77), ("afasta", 12.95), ("por", 13.39), ("culpa,", 13.55),
      ("pra", 13.985), ("não", 14.14), ("machucar", 14.28), ("ninguém.", 14.49), ("Eu", 15.24), ("entendo.", 15.42)]
WC = [("Mas", 0.73), ("o", 1.07), ("pior", 1.18), ("dia", 1.48), ("que", 1.86), ("você", 1.96), ("tem", 2.28), ("não", 2.56), ("é", 2.86), ("um", 2.98), ("bom", 3.12), ("dia", 3.28),
      ("de", 3.46), ("parâmetro", 3.58), ("pra", 4.20), ("sua", 4.36), ("vida", 4.56), ("toda.", 4.76), ("Nem", 5.26), ("pode", 5.47), ("ser.", 5.70),
      ("E", 6.16), ("é", 6.27), ("no", 6.33), ("tratamento", 6.40), ("que", 6.86), ("se", 6.95), ("treina", 7.20), ("ficar", 7.50), ("sem", 7.96), ("estourar.", 8.12),
      ("Às", 8.77), ("vezes", 8.90), ("todo", 9.06), ("mundo", 9.24), ("quer", 9.40), ("dar", 9.575), ("um", 9.78), ("tempo", 10.05), ("de", 10.34), ("todo", 10.55), ("mundo,", 10.84),
      ("e", 11.20), ("tem", 11.36), ("um", 11.46), ("jeito", 11.60), ("certo", 11.78), ("de", 12.12), ("ter", 12.43), ("o", 12.56), ("nosso", 12.68), ("tempo.", 12.84),
      ("Mas", 13.38), ("é", 13.54), ("importante", 13.72), ("trabalhar", 14.10), ("isso", 14.50), ("na", 14.63), ("terapia", 14.75), ("antes", 15.26), ("de", 15.58), ("decidir", 15.74), ("qualquer", 16.04), ("coisa.", 16.22),
      ("Manda", 16.78), ("isso", 17.00), ("aqui", 17.16), ("pra", 17.27), ("quem", 17.41), ("não", 17.56), ("entende", 17.84), ("alguma", 18.08), ("das", 18.38), ("suas", 18.54), ("atitudes.", 18.68)]
AUD_OFF = {"A": 0.0, "B": 12.88169, "C": 28.08836}
GROUPS = {"A": [3, 3, 3, 3, 3, 2, 3, 2, 3, 3, 2, 3, 3, 3, 2],
          "B": [3, 3, 3, 3, 3, 2, 3, 3, 2, 1, 2, 3, 3, 2, 2, 3, 3, 2, 2, 3, 1, 2],
          "C": [3, 2, 2, 3, 2, 2, 2, 2, 3, 3, 2, 2, 1, 2, 2, 3, 3, 3, 2, 3, 2, 3, 3, 2, 2, 3, 2, 3, 3, 2, 3]}
CAPS = []
for seg, words in (("A", WA), ("B", WB), ("C", WC)):
    assert sum(GROUPS[seg]) == len(words), (seg, sum(GROUPS[seg]), len(words))
    i = 0
    for g in GROUPS[seg]:
        CAPS.append([(w, t + AUD_OFF[seg]) for w, t in words[i:i+g]]); i += g
BOUNDS = [126, 150, 483, 551, 601, 686, 745, 806, 837, 861, 1020, 1056, 1101, 1128, 1174, 1236, 1344]   # trocas visiveis de imagem
CAP_S = []
for i, c in enumerate(CAPS):
    s_ = c[0][1] - 0.03 if i else 0.0
    for tb in BOUNDS:
        if abs(tb/FPS - s_) <= 0.07: s_ = tb/FPS; break
    CAP_S.append(s_)
CAP_T = []
for i, c in enumerate(CAPS):
    lw = c[-1][1]
    e = min(CAP_S[i+1] if i + 1 < len(CAPS) else 1e9, lw + 0.75)
    for tb in BOUNDS:
        if lw + 0.2 < tb/FPS < e: e = tb/FPS; break
    CAP_T.append((CAP_S[i], e))

# ------------------------------------------------------------------ texto
AB = lambda s: ImageFont.truetype("ArchivoBlack.ttf", s)
PP = lambda s: ImageFont.truetype("Poppins-SemiBold.ttf", s)
AN = lambda s: ImageFont.truetype("Anton.ttf", s)
MX = int(W*0.08); MAXW = W - 2*MX
BBOX = {}
def shadowed(text_layer, off=3, rad=6, alpha=1.5):
    a = text_layer.split()[3]
    sa = Image.new("L", (W, H), 0); sa.paste(a, (0, off))
    sa = sa.filter(ImageFilter.GaussianBlur(rad)).point(lambda v: min(255, int(v*alpha)))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(sa)
    return Image.alpha_composite(sh, text_layer)
def lines_layer(name, lines, font, top, lh, box_word=None, box_color=None, pad=(16, 8), visible=None, extra=None):
    boxes = Image.new("RGBA", (W, H), (0, 0, 0, 0)); txt = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    db, dt = ImageDraw.Draw(boxes), ImageDraw.Draw(txt)
    sp = dt.textlength(" ", font=font); cap = font.getbbox("H"); cap_top, cap_h = cap[1], cap[3] - cap[1]
    ext = [W, H, 0, 0]
    def grow(x0, y0, x1, y1):
        ext[0] = min(ext[0], x0); ext[1] = min(ext[1], y0); ext[2] = max(ext[2], x1); ext[3] = max(ext[3], y1)
    k = 0
    for i, words in enumerate(lines):
        ws = [dt.textlength(w, font=font) for w in words]; tw = sum(ws) + sp*(len(words) - 1)
        x = (W - tw)/2; y = top + i*lh
        for wi, (w, ww) in enumerate(zip(words, ws)):
            show = visible is None or k in visible
            bb = dt.textbbox((x, y - cap_top), w, font=font); grow(*bb)
            if (box_word == w) or (isinstance(box_word, int) and box_word == k):
                r = (x - pad[0], y - pad[1], x + ww + pad[0], y + cap_h + pad[1]); grow(*r)
                if show: db.rectangle(r, fill=box_color)
            if show: dt.text((x, y - cap_top), w, font=font, fill=(255, 255, 255, 255))
            x += ww + sp; k += 1
    if extra:
        f2, s, y2 = extra; tw = dt.textlength(s, font=f2); bb = dt.textbbox(((W - tw)/2, y2), s, font=f2); grow(*bb)
        dt.text(((W - tw)/2, y2), s, font=f2, fill=(255, 255, 255, 255))
    BBOX[name] = [round(v) for v in ext]
    flat = Image.alpha_composite(boxes, txt)
    return Image.alpha_composite(shadowed(flat), flat)
def fit(lines, maxsize, fontf):
    s = maxsize; d = ImageDraw.Draw(Image.new("L", (10, 10)))
    while max(d.textlength(" ".join(l), font=fontf(s)) for l in lines) > MAXW - 36: s -= 1
    return s
RED, BLK = (204, 0, 0, 255), (13, 13, 13, 255)
TL = [["POR", "QUE", "O", "BORDERLINE"], ["FICA", "BEM", "SOZINHO"]]
ts = fit(TL, 104, AN); _ch = AN(ts).getbbox("H"); _ch = _ch[3] - _ch[1]
TITLE = lines_layer("titulo", TL, AN(ts), 166, _ch + 26, "SOZINHO", RED, pad=(14, 9))
CREDIT = lines_layer("credito", [["Dr. Fabio Schmidt · médico · CRM-SP 183549"]], PP(31), 166 + 2*_ch + 26 + 9 + 22, 40)
BT, BLH, BS = 1222, 128, 96
L_GATILHO = lines_layer("O GATILHO É GENTE", [["O", "GATILHO"], ["É", "GENTE"]], AB(BS), BT, BLH, "GENTE", BLK)
L_CULPA = lines_layer("POR CULPA", [["POR", "CULPA"]], AB(112), 1285, BLH, "CULPA", BLK, pad=(18, 12))
L_PSE = [lines_layer("PERTO SEM ESTOURAR", [["PERTO", "SEM"], ["ESTOURAR"]], AB(BS), BT, BLH, "ESTOURAR", BLK, visible=set(range(n))) for n in (1, 2, 3)]
L_FINAL = lines_layer("MANDA PRA QUEM / VOCÊ AFASTOU", [["MANDA", "PRA", "QUEM"], ["VOCÊ", "AFASTOU"]], AB(86), 1206, 118, "AFASTOU", BLK, extra=(PP(34), "@drfabioschmidt", 1432))
CAP_CACHE = {}
def cap_layer(i, k):
    if (i, k) not in CAP_CACHE:
        ws = [w for w, _ in CAPS[i]]; s = 60; d = ImageDraw.Draw(Image.new("L", (10, 10)))
        while d.textlength(" ".join(ws), font=PP(s)) > MAXW - 40: s -= 1
        f = PP(s); cb = f.getbbox("H")
        CAP_CACHE[(i, k)] = lines_layer("leg%03d %s" % (i, " ".join(ws)), [ws], f, 1324 - (cb[3] - cb[1])/2, 80, k, BLK, pad=(13, 16))
    return CAP_CACHE[(i, k)]
def cap_at(t):
    for i, (s, e) in enumerate(CAP_T):
        if s <= t < e:
            c = CAPS[i]; k = max(0, sum(1 for w in c if t >= w[1] - 0.03) - 1)
            L = cap_layer(i, k); p = (t - s)/0.10
            if p < 1 and i > 0:
                Mv = Image.new("RGBA", (W, H), (0, 0, 0, 0)); Mv.paste(L, (0, int(round(14*(1 - p)))))
                a = Mv.split()[3].point(lambda v: int(v*(0.35 + 0.65*p))); Mv.putalpha(a); return Mv, s
            return L, s
    return None, None

# ------------------------------------------------------------------ fontes de imagem
def ff_frames(path, w, h, vf):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", path, "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    n = w*h*3
    while True:
        b = p.stdout.read(n)
        if len(b) < n: break
        yield np.frombuffer(b, np.uint8).reshape(h, w, 3)
luma = lambda x: 0.299*x[..., 0] + 0.587*x[..., 1] + 0.114*x[..., 2]
GEN, ORIG, BR, MOT, FRAME, DELTA = {}, {}, {}, {}, {}, {}
LG = json.load(open("landmarks.json")); LO = json.load(open(OR + "landmarks_orig.json"))

def load_sources(need_motion=True):
    for s in "ABC":
        GEN[s] = np.stack(list(ff_frames(GENP[s], 480, 854, "null")))
        ORIG[s] = np.memmap(OR + "in%s.raw" % s, dtype=np.uint8, mode="r", shape=(SEGK[s], 1920, 1080, 3))
    for a, b, path, ss in BROLLS:
        cache = "brcache_%s_%d_%d.npy" % (os.path.basename(path)[:8], int(ss*100), b - a)
        if os.path.exists(cache): BR[path] = np.load(cache)
        else:
            fr = list(ff_frames(path, W, H, "minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,scale=1080:1920:flags=lanczos"))
            i0 = int(round(ss*FPS)); BR[path] = np.stack(fr[i0:i0 + (b - a) + 2]); np.save(cache, BR[path])
    if need_motion:
        need = sorted({int(motion_tau(T(m) + 1e-4)*60) for m in range(M_IN, M_OUT)})
        import pickle
        if os.path.exists("motcache.pkl") and set(pickle.load(open("motcache.pkl", "rb")).keys()) == set(need): MOT.update(pickle.load(open("motcache.pkl", "rb")))
        else:
            for i, fr in enumerate(ff_frames(MOTION, W, H, "null")):
                if i in need:
                    bio = io.BytesIO(); Image.fromarray(fr).save(bio, "PNG", compress_level=1); MOT[i] = bio.getvalue()
            pickle.dump(MOT, open("motcache.pkl", "wb"))
    # enquadramento por tomada (marcos na imagem gerada) e ajuste fino do mapa por tomada
    for i in range(17):
        s = SHOT_SEG[i]; g0, g1 = GEN_RANGE[i]; R = LG[s][g0:g1]
        hair = float(np.median([r["top"][1] - 0.443*(r["chin"][1] - r["top"][1]) for r in R]))
        cx = float(np.median([(r["l"][0] + r["r"][0])/2 for r in R]))
        FRAME[i] = (cx, hair)
        a, b = MAPJ[s]["a"], MAPJ[s]["b"]; o0, o1 = CUTS[i] - SEGOFF[s], min(CUTS[i+1] - SEGOFF[s], SEGK[s])
        ko = np.arange(o0, o1); ox = np.array([LO[s][k]["nose"][0]*480 for k in ko]); oy = np.array([LO[s][k]["nose"][1]*854 for k in ko])
        js = np.arange(g0 + 1, g1 - 1); gx = np.array([LG[s][j]["nose"][0] for j in js]); gy = np.array([LG[s][j]["nose"][1] for j in js])
        best = (1e9, 0.0)
        for d in np.arange(-2.5, 2.51, 0.1):
            kk = (js - b - d)/a; ok = (kk >= o0) & (kk <= o1 - 1)
            if ok.sum() < 6: continue
            e = np.mean(np.abs(np.interp(kk[ok], ko, ox) - gx[ok]) + np.abs(np.interp(kk[ok], ko, oy) - gy[ok]))
            if e < best[0]: best = (e, float(d))
        DELTA[i] = best[1]

def map_frames(m):
    i = shot_of(m); s = SHOT_SEG[i]; k = m - SEGOFF[s]
    a, b = MAPJ[s]["a"], MAPJ[s]["b"] + DELTA[i]
    g0, g1 = GEN_RANGE[i]; o0, o1 = CUTS[i] - SEGOFF[s], min(CUTS[i+1] - SEGOFF[s], SEGK[s])
    j = min(max(int(round(a*k + b)), g0), g1 - 1)
    kq = min(max(int(round((j - b)/a)), o0), o1 - 1)
    return i, s, j, kq

K3 = np.ones((3, 3), np.uint8); K9 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)); KE = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
GYX = np.mgrid[0:854, 0:480].astype(f32)
_dis = None; _small_cache = {}
def small_products(s, j, kq):
    """fluxo (gerado -> original), peso de detalhe e ganho, em 480x854"""
    global _dis
    key_ = (s, j, kq)
    if key_ in _small_cache: return _small_cache[key_]
    if _dis is None:
        _dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM); _dis.setFinestScale(0)
    g = GEN[s][j]; osm = cv2.resize(np.asarray(ORIG[s][kq]), (480, 854), interpolation=cv2.INTER_AREA)
    G = luma(g.astype(f32)); O = luma(osm.astype(f32))
    mx = osm.max(-1).astype(f32); mn = osm.min(-1).astype(f32); sat = (mx - mn)/np.maximum(mx, 1)
    key = (((sat > 0.25) & (mx > 45)) | (O < 55)).astype(np.uint8)
    key = cv2.morphologyEx(cv2.morphologyEx(key, cv2.MORPH_OPEN, K3), cv2.MORPH_CLOSE, K9)
    n, lab = cv2.connectedComponents(key)
    r = LO[s][kq]; nx, ny = min(479, int(r["nose"][0]*480)), min(853, int(r["nose"][1]*854)); lbl = lab[ny, nx]
    if lbl == 0 and n > 1: lbl = 1 + int(np.argmax(np.bincount(lab.ravel())[1:]))
    key = (lab == lbl).astype(f32) if n > 1 else np.zeros_like(G)
    pre = lambda y: np.clip((y - cv2.GaussianBlur(y, (0, 0), 16))*2.5 + 128, 0, 255).astype(np.uint8)
    flow = _dis.calc(pre(G), pre(cv2.GaussianBlur(O, (0, 0), 0.7)), None)
    kb = cv2.GaussianBlur(key, (0, 0), 5)
    med = (float(np.median(flow[..., 0][key > 0.5])), float(np.median(flow[..., 1][key > 0.5]))) if key.sum() > 50 else (0.0, 0.0)
    fx = np.where(kb > 0.03, cv2.GaussianBlur(flow[..., 0]*key, (0, 0), 5)/np.maximum(kb, 0.03), med[0])
    fy = np.where(kb > 0.03, cv2.GaussianBlur(flow[..., 1]*key, (0, 0), 5)/np.maximum(kb, 0.03), med[1])
    fx = cv2.GaussianBlur(np.clip(fx, -15, 15).astype(f32), (0, 0), 2); fy = cv2.GaussianBlur(np.clip(fy, -15, 15).astype(f32), (0, 0), 2)
    mxp, myp = GYX[1] + fx, GYX[0] + fy
    Ow = cv2.remap(O, mxp, myp, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    kw = cv2.remap(key, mxp, myp, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    inner = cv2.GaussianBlur(cv2.erode((kw > 0.5).astype(f32), KE), (0, 0), 2.2)
    mg, mo = cv2.GaussianBlur(G, (0, 0), 4), cv2.GaussianBlur(Ow, (0, 0), 4)
    dg, do = G - mg, Ow - mo
    vg, vo = cv2.GaussianBlur(dg*dg, (0, 0), 6), cv2.GaussianBlur(do*do, (0, 0), 6)
    gain = np.clip(np.sqrt((vg + 4)/(vo + 4)), 0.5, 1.2)
    resid = cv2.GaussianBlur((dg - gain*do)**2, (0, 0), 6)
    conf = np.clip(1.3 - 1.6*np.sqrt(resid/(vg + 25)), 0, 1)
    Wd = cv2.GaussianBlur((inner*conf).astype(f32), (0, 0), 1.5)
    out = (fx, fy, Wd, cv2.GaussianBlur(gain.astype(f32), (0, 0), 3))
    if len(_small_cache) > 6: _small_cache.clear()
    _small_cache[key_] = out
    return out

DETAIL = 1.0
ANCHOR = 0.25
def fala(m, z, debug=False):
    i, s, j, kq = map_frames(m)
    S = z*W/480.0; cx, hair = FRAME[i]
    x0 = min(max(cx - (W/2)/S, 0.0), 480 - W/S); y0 = min(max(hair - ANCHOR*H/S, 0.0), 854 - H/S)
    Minv = np.float32([[1/S, 0, x0 + 0.5/S - 0.5], [0, 1/S, y0 + 0.5/S - 0.5]])
    inv = cv2.WARP_INVERSE_MAP
    go = cv2.warpAffine(GEN[s][j].astype(f32), Minv, (W, H), flags=cv2.INTER_LANCZOS4 | inv, borderMode=cv2.BORDER_REPLICATE)
    bg = go - cv2.GaussianBlur(go, (0, 0), 2.2)
    if DETAIL > 0:
        fx, fy, Wd, gain = small_products(s, j, kq)
        wa = lambda a: cv2.warpAffine(a, Minv, (W, H), flags=cv2.INTER_LINEAR | inv, borderMode=cv2.BORDER_REPLICATE)
        fxo, fyo, Wo, gno = wa(fx), wa(fy), wa(Wd), wa(gain)
        gx = x0 + (np.arange(W, dtype=f32) + 0.5)/S - 0.5; gy = y0 + (np.arange(H, dtype=f32) + 0.5)/S - 0.5
        mapx = ((gx[None, :] + fxo) + 0.5)*(1080/480.0) - 0.5; mapy = ((gy[:, None] + fyo) + 0.5)*(1920/854.0) - 0.5
        oo = cv2.remap(np.asarray(ORIG[s][kq]), mapx.astype(f32), mapy.astype(f32), cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        ys = luma(oo.astype(f32)); hp = ys - cv2.GaussianBlur(ys, (0, 0), 2.2*z)
        out = go + (DETAIL*Wo*gno*hp)[..., None] + ((1 - Wo)*0.45)[..., None]*bg
    else:
        Wo = None; out = go + 0.5*bg
    out = (out*1.07 - 105)*1.06 + 105
    out = np.clip(out, 0, 255).astype(np.uint8)
    if debug: return out, (np.clip(go, 0, 255).astype(np.uint8), Wo, (i, s, j, kq))
    return out

def frame(m):
    t = T(m) + 1e-4
    in_motion = M_IN <= m < M_OUT
    base = None
    for a, b, path, ss in BROLLS:
        if a <= m < b: base = Image.fromarray(BR[path][m - a])
    if base is None:
        base = Image.open(io.BytesIO(MOT[int(motion_tau(t)*60)])).convert("RGB") if in_motion else Image.fromarray(fala(m, zoom_at(m)))
    im = base.convert("RGBA")
    if not in_motion: im.alpha_composite(TITLE)
    if Z145[0] <= m < Z145[1]: im.alpha_composite(CREDIT)
    big = None
    if BIG_GATILHO[0] <= m < BIG_GATILHO[1]: big = L_GATILHO
    elif BIG_CULPA[0] <= m < BIG_CULPA[1]: big = L_CULPA
    elif PSE[0] <= m < PSE_END: big = L_PSE[sum(1 for p in PSE if m >= p) - 1]
    elif m >= BIG_FINAL[0]: big = L_FINAL
    if big is not None: im.alpha_composite(big)
    else:
        L, cs = cap_at(t)
        if L is not None and not any(be <= m and cs < T(be) - 0.2 for bs, be in BIGS): im.alpha_composite(L)
    return im.convert("RGB")

def render_chunk(args):
    idx, f0, f1 = args
    cv2.setNumThreads(1)
    out = "part_%02d.mp4" % idx
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H), "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-preset", "fast", "-crf", "12", "-pix_fmt", "yuv420p", "-threads", "2", out], stdin=subprocess.PIPE)
    for m in range(f0, f1): enc.stdin.write(frame(m).tobytes())
    enc.stdin.close(); enc.wait()
    return out

if __name__ == "__main__":
    mode = sys.argv[1]
    load_sources()
    print("delta por tomada:", {i: round(DELTA[i], 1) for i in DELTA}); print("enquadramento:", {i: (round(FRAME[i][0], 1), round(FRAME[i][1], 1)) for i in FRAME}, flush=True)
    if mode == "stills":
        os.makedirs("../stills4", exist_ok=True)
        for m in [int(x) for x in sys.argv[2].split(",")]:
            frame(m).save("../stills4/f%04d.png" % m)
        [cap_layer(i, k) for i in range(len(CAPS)) for k in range(len(CAPS[i]))]
        json.dump({"bbox": BBOX, "caps": [(round(CAP_T[i][0], 2), round(CAP_T[i][1], 2), " ".join(w for w, _ in c)) for i, c in enumerate(CAPS)]}, open("layout4.json", "w"), ensure_ascii=False, indent=0)
    elif mode == "debug":
        os.makedirs("../stills4", exist_ok=True)
        for m in [int(x) for x in sys.argv[2].split(",")]:
            out, (go, Wo, info) = fala(m, zoom_at(m), debug=True)
            wim = np.repeat((Wo*255).astype(np.uint8)[..., None], 3, -1)
            Image.fromarray(np.concatenate([go, out, wim], 1)).save("../stills4/dbg%04d.jpg" % m, quality=93); print(m, info, flush=True)
    elif mode == "render":
        import multiprocessing as mp
        nproc = 4; bounds = [int(round(i*NF/8)) for i in range(9)]
        with mp.get_context("fork").Pool(nproc) as pool:
            parts = pool.map(render_chunk, [(i, bounds[i], bounds[i+1]) for i in range(8)], chunksize=1)
        open("parts.txt", "w").write("".join("file '%s'\n" % p for p in parts))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "parts.txt", "-c", "copy", "video4.mp4"], check=True)
        print("ok", flush=True)
