import sys, subprocess, json, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

D = "/tmp/claude-0/-home-user-borderline-sem-estigmas/5120ea19-98ff-54bd-8290-fbde345ccb73/scratchpad/"
W, H, FPS = 1080, 1920, 24
BIG = D + "fonts/ArchivoBlack-Regular.ttf"
POP = D + "fonts/Poppins-SemiBold.ttf"
RED = (204, 0, 0, 255)
WHITE = (255, 255, 255, 255)
FREEZE = 3.5
FADE = 3


def parse(line):
    # returns list of (text, color)
    out = []
    for m in re.finditer(r"\[([^\]]+)\]|([^\[]+)", line):
        if m.group(1):
            out.append((m.group(1), RED))
        else:
            out.append((m.group(2), WHITE))
    return out


def text_layer(lines, font_path, size, center_y, stroke, shadow, lh):
    f = ImageFont.truetype(font_path, size)
    asc, desc = f.getmetrics()
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    ds = ImageDraw.Draw(shad)
    n = len(lines)
    total = (n - 1) * lh + asc + desc
    y0 = center_y - total / 2
    for i, ln in enumerate(lines):
        segs = parse(ln)
        plain = "".join(t for t, _ in segs)
        x = (W - f.getlength(plain)) / 2
        y = y0 + i * lh
        pre = ""
        for t, col in segs:
            xx = x + f.getlength(pre)
            if shadow:
                ds.text((xx + 4, y + 7), t, font=f, fill=(0, 0, 0, 170), stroke_width=stroke, stroke_fill=(0, 0, 0, 170))
            d.text((xx, y), t, font=f, fill=col, stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
            pre += t
    if shadow:
        shad = shad.filter(ImageFilter.GaussianBlur(6))
        shad.alpha_composite(img)
        img = shad
    return img


def big(lines, size, cy=1250):
    return text_layer(lines, BIG, size, cy, 5, True, round(size * 1.06))


def sub(lines, size=46, cy=1380):
    return text_layer(lines, POP, size, cy, 3, False, round(size * 1.22))


# ---- estilo v2 do churrasco: discreto, sem contorno, sombra leve ----
POPM = D + "fonts/Poppins-Medium.ttf"
CREAM = (250, 244, 232, 255)


def soft_layer(lines, font_path, size, center_y, lh, band=False, tight=1.5, drop=0.55):
    """Texto sem contorno. Sombra em duas camadas: borda difusa curta + queda suave.
    band=True: palavra entre colchetes vira letra creme em faixa vermelha (fundo escuro)."""
    f = ImageFont.truetype(font_path, size)
    asc, desc = f.getmetrics()
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bands = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    db = ImageDraw.Draw(bands)
    n = len(lines)
    total = (n - 1) * lh + asc + desc
    y0 = center_y - total / 2
    for i, ln in enumerate(lines):
        segs = parse(ln)
        plain = "".join(t for t, _ in segs)
        x = (W - f.getlength(plain)) / 2
        y = y0 + i * lh
        pre = ""
        for t, col in segs:
            xx = x + f.getlength(pre)
            if col == RED and band:
                l, tp, r, bt = d.textbbox((xx, y), t, font=f)
                px = round(size * 0.14)
                cap_top = y + asc - size * 0.78
                base = y + asc + size * 0.26
                db.rounded_rectangle((l - px, cap_top, r + px, base), radius=round(size * 0.10), fill=RED)
                d.text((xx, y), t, font=f, fill=CREAM)
            else:
                d.text((xx, y), t, font=f, fill=col)
            pre += t
    a = np.array(img)[:, :, 3].astype(np.float32) / 255.0
    ab = np.array(bands)[:, :, 3].astype(np.float32) / 255.0
    solid = Image.fromarray((np.maximum(a, ab) * 255).astype(np.uint8))
    edge = np.clip(np.array(solid.filter(ImageFilter.GaussianBlur(max(2.0, size * 0.035)))).astype(np.float32) / 255.0 * tight, 0, 1) * 0.80
    dr = np.array(solid.filter(ImageFilter.GaussianBlur(size * 0.16))).astype(np.float32) / 255.0
    dr = np.roll(dr, round(size * 0.05), axis=0) * drop
    sa = 1 - (1 - edge) * (1 - np.clip(dr, 0, 1))
    out = np.zeros((H, W, 4), np.uint8)
    out[:, :, 3] = (sa * 255).astype(np.uint8)
    out = Image.fromarray(out, "RGBA")
    out.alpha_composite(bands)
    out.alpha_composite(img)
    return out


def big2(lines, size, cy=1250, band=False):
    return soft_layer(lines, POP, size, cy, round(size * 1.16), band=band)


def sub2(lines, size=42, cy=1380):
    return soft_layer(lines, POPM, size, cy, round(size * 1.28), tight=1.7, drop=0.6)


def bbox(img):
    a = np.array(img)[:, :, 3]
    ys, xs = np.where(a > 8)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def build(cfg):
    name = cfg["name"]
    layers = []  # (start_frame, end_frame_exclusive, img, label)
    for L in cfg["layers"]:
        img = L["img"]
        x0, y0, x1, y1 = bbox(img)
        ok = x0 >= 90 and x1 <= W - 90 and y0 >= 250 and y1 <= 1480
        print(f"{name} {L['label']!r:60} bbox x{x0}-{x1} y{y0}-{y1} {'OK' if ok else 'FORA DA ZONA'}")
        if not ok:
            sys.exit("zona segura")
        layers.append((round(L["t0"] * FPS), round(L["t1"] * FPS), np.array(img).astype(np.float32) / 255.0, L["label"]))

    # decode base scene frames
    cmd = ["ffmpeg", "-v", "error", "-i", D + cfg["src"], "-filter_complex", cfg["vf"], "-map", "[v]",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    frames = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    nscene = len(frames)
    nfreeze = round(FREEZE * FPS)
    total = nscene + nfreeze
    print(name, "scene frames", nscene, "total", total, "dur", total / FPS)
    last = Image.fromarray(frames[-1])
    frozen = np.array(last.filter(ImageFilter.GaussianBlur(7))).astype(np.float32) * 0.35
    lastf = frames[-1].astype(np.float32)

    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-i", D + cfg["name"] + "_audio.wav",
                            "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
                            "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                            "-movflags", "+faststart", D + name + "_final.mp4"], stdin=subprocess.PIPE)
    RAMP = 6
    for i in range(total):
        if i < nscene:
            fr = frames[i].astype(np.float32)
        else:
            k = min(1.0, (i - nscene + 1) / RAMP)
            fr = lastf * (1 - k) + frozen * k
        for s, e, arr, _ in layers:
            if s <= i < e:
                a = min(1.0, 1.0 if s == 0 else (i - s + 1) / FADE, (e - i) / FADE)
                al = arr[:, :, 3:4] * a
                fr = fr * (1 - al) + arr[:, :, :3] * 255.0 * al
        enc.stdin.write(np.clip(fr, 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close()
    enc.wait()
    return nscene, total


def srt(name, items):
    def ts(t):
        ms = round(t * 1000)
        return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"
    with open(D + name + "_final.srt", "w") as f:
        for i, (a, b, t) in enumerate(items, 1):
            f.write(f"{i}\n{ts(a)} --> {ts(b)}\n{t}\n\n")


SC = "scale=1080:-2:flags=lanczos,crop=1080:1920"
FR = 1 / FPS

which = sys.argv[1]
if which == "churrasco":
    END = 481 / FPS  # 20.0417
    cfg = dict(name="churrasco", src="churrasco_src.mp4",
               vf=f"[0:v]{SC},trim=end_frame=481,setpts=PTS-STARTPTS[v]",
               layers=[
                   dict(label="Borderline é tudo [igual].", t0=0.0, t1=1.375, img=big2(["Borderline é", "tudo [igual]."], 80)),
                   dict(label="Manipula, mente, some.", t0=1.70, t1=4.25, img=sub2(["Manipula, mente, some."])),
                   dict(label="Quantas você conheceu?", t0=4.50, t1=6.25, img=sub2(["Quantas você conheceu?"])),
                   dict(label="[Uma.]", t0=6.375, t1=7.50, img=big2(["[Uma.]"], 84)),
                   dict(label="E você perguntou pra ela?", t0=7.67, t1=9.70, img=sub2(["E você perguntou pra ela?"])),
                   dict(label="Ela tem [borderline]. Ninguém na mesa sabe.", t0=16.5, t1=END,
                        img=big2(["Ela tem", "[borderline].", "Ninguém na", "mesa sabe."], 66, cy=1280, band=True)),
                   dict(label="TESE churrasco", t0=END, t1=END + FREEZE,
                        img=big2(["Quem tem borderline", "pode estar na sua mesa,", "[ouvindo] tudo."], 68, cy=900, band=True)),
                   dict(label="CHAMADA churrasco", t0=END, t1=END + FREEZE,
                        img=sub2(["Manda pra quem você", "queria que entendesse."], 40, cy=1112)),
               ])
    srt("churrasco", [(0.0, 1.375, "Borderline é tudo igual."), (1.70, 4.25, "Manipula, mente, some."),
                      (4.50, 6.25, "Quantas você conheceu?"), (6.375, 7.50, "Uma."),
                      (7.67, 9.70, "E você perguntou pra ela?")])
else:
    A_END = 31  # frames kept from start (1.2917 s)
    B0 = 114    # 4.75 s
    B1 = 384    # 16.0 s
    off = A_END / FPS - B0 / FPS  # source -> final
    END = (A_END + B1 - B0) / FPS
    cfg = dict(name="bar", src="bar_src.mp4",
               vf=(f"[0:v]{SC},split[x][y];[x]trim=end_frame={A_END},setpts=PTS-STARTPTS[a];"
                   f"[y]trim=start_frame={B0}:end_frame={B1},setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1[v]"),
               layers=[
                   dict(label="Terminei com ela hoje.", t0=6.08 + off, t1=7.95 + off, img=sub(["Terminei com ela hoje."])),
                   dict(label="Antes que ela terminasse comigo.", t0=8.00 + off, t1=10.30 + off,
                        img=sub(["Antes que ela terminasse comigo."])),
                   dict(label="Ela [nem] ia terminar.", t0=12.10 + off, t1=14.10 + off,
                        img=big(["Ela [nem] ia", "terminar."], 110)),
                   dict(label="No borderline", t0=END, t1=END + FREEZE, img=sub(["No borderline"], 50, cy=640)),
                   dict(label="TESE bar", t0=END, t1=END + FREEZE,
                        img=big(["O [medo] de ser", "deixado pode", "terminar o que", "não ia acabar."], 88, cy=900)),
                   dict(label="CHAMADA bar", t0=END, t1=END + FREEZE,
                        img=sub(["Manda pra quem ficou", "sem entender o término."], 44, cy=1170)),
               ])
    srt("bar", [(6.08 + off, 7.95 + off, "Terminei com ela hoje."),
                (8.00 + off, 10.30 + off, "Antes que ela terminasse comigo."),
                (12.10 + off, 13.10 + off, "Ela nem ia terminar.")])
    print("first speech final t =", 6.13 + off, "END", END)

json.dump({k: [(L["label"], L["t0"], L["t1"]) for L in cfg["layers"]] for k in ["layers"]},
          open(D + which + "_layers.json", "w"))
if len(sys.argv) > 2 and sys.argv[2] == "preview":
    for L in cfg["layers"]:
        print(L["label"], bbox(L["img"]))
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", D + cfg["src"], "-filter_complex", cfg["vf"], "-map", "[v]",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    frames = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    frozen = Image.fromarray((np.array(Image.fromarray(frames[-1]).filter(ImageFilter.GaussianBlur(7))).astype(np.float32) * 0.35).astype(np.uint8))
    tiles = []
    for t in [float(x) for x in sys.argv[3:]]:
        i = round(t * FPS)
        base = (Image.fromarray(frames[i]) if i < len(frames) else frozen).convert("RGBA")
        for L in cfg["layers"]:
            if L["t0"] <= t < L["t1"]:
                base.alpha_composite(L["img"])
        base.convert("RGB").save(D + f"prev_{t}.jpg", quality=92)
else:
    build(cfg)
