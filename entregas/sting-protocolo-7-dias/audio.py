"""Sound for the Protocolo 7 Dias sting: Rising Forest (native ~124 BPM) + synthesized SFX.
Exact length 12.075 s, 48 kHz stereo, -14 LUFS, true peak <= -1 dBTP, fade only on the last 60 ms."""
import numpy as np, soundfile as sf, pyloudnorm as pyln, scipy.signal as ss, sys

SR = 48000
DUR = 12.075
N = int(round(DUR * SR))
DROP_SRC = 15.4963          # drop transient in the original file
DROP_DST = 0.048 + 0.4838 * 5   # beat 5 = 2.467 s
rng = np.random.default_rng(7)  # seeded

music, sr = sf.read(sys.argv[1], always_2d=True)
assert sr == SR
start = int(round((DROP_SRC - DROP_DST) * SR))
m = music[start:start + N].copy()
t = np.arange(N) / SR

# soft intro: muffled and lower before the drop, opens on the drop (filter + gain step, no fade)
d = int(DROP_DST * SR)
sos = ss.butter(2, 1400, "low", fs=SR, output='sos')
pre = ss.sosfilt(sos, m[:d + 2400], axis=0)[:d]
m[:d] = pre * 10 ** (-3 / 20)

def env_ar(n, a, r, curve=3.0):
    e = np.zeros(n)
    na, nr = int(a * SR), int(r * SR)
    e[:na] = (np.arange(na) / max(1, na)) ** curve
    e[na:na + nr] = (1 - np.arange(nr) / max(1, nr)) ** 2
    return e

def place(buf, x, at, gain_db, pan=0.0):
    i = int(round(at * SR))
    j = min(N, i + len(x))
    if j <= i: return
    g = 10 ** (gain_db / 20)
    l, r = np.sqrt((1 - pan) / 2), np.sqrt((1 + pan) / 2)
    buf[i:j, 0] += x[:j - i] * g * l * 1.4142
    buf[i:j, 1] += x[:j - i] * g * r * 1.4142

def norm(x): return x / (np.max(np.abs(x)) + 1e-12)

def whoosh(peak_at, rise=0.38, fall=0.16, lo=300, hi=3200):
    n = int((rise + fall) * SR)
    noise = rng.standard_normal(n)
    # sweep band-pass centre up through the rise, down on the fall
    out = np.zeros(n)
    blk = 512
    zi = None
    for k in range(0, n, blk):
        tt = k / SR
        frac = min(1, tt / rise) if tt < rise else max(0, 1 - (tt - rise) / fall)
        fc = lo * (hi / lo) ** frac
        sos = ss.butter(2, [fc * 0.6, min(fc * 1.7, SR / 2 - 100)], 'band', fs=SR, output='sos')
        if zi is None: zi = np.zeros((sos.shape[0], 2))
        out[k:k + blk], zi = ss.sosfilt(sos, noise[k:k + blk], zi=zi)
    e = env_ar(n, rise, fall, 2.2)
    return norm(out * e), peak_at - rise

def impact():
    n = int(0.45 * SR); tt = np.arange(n) / SR
    body = np.sin(2 * np.pi * (52 + 40 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 9)
    air = ss.sosfilt(ss.butter(2, 2500, 'low', fs=SR, output='sos'), rng.standard_normal(n)) * np.exp(-tt * 40) * 0.25
    return norm(body + air)

def click():
    n = int(0.012 * SR); tt = np.arange(n) / SR
    x = (np.sin(2 * np.pi * 3100 * tt) * 0.6 + rng.standard_normal(n) * 0.4) * np.exp(-tt * 520)
    return norm(ss.sosfilt(ss.butter(2, 900, 'high', fs=SR, output='sos'), x))

def tick():
    n = int(0.006 * SR); tt = np.arange(n) / SR
    x = (np.sin(2 * np.pi * 4200 * tt) * 0.5 + rng.standard_normal(n) * 0.5) * np.exp(-tt * 900)
    return norm(ss.sosfilt(ss.butter(2, 1800, 'high', fs=SR, output='sos'), x))

def hit():
    n = int(0.5 * SR); tt = np.arange(n) / SR
    tone = (np.sin(2 * np.pi * 220 * tt) + 0.5 * np.sin(2 * np.pi * 330 * tt) + 0.3 * np.sin(2 * np.pi * 660 * tt)) * np.exp(-tt * 7)
    thump = np.sin(2 * np.pi * (70 + 50 * np.exp(-tt * 40)) * tt) * np.exp(-tt * 14)
    snap = ss.sosfilt(ss.butter(2, [1500, 7000], 'band', fs=SR, output='sos'), rng.standard_normal(n)) * np.exp(-tt * 60)
    return norm(0.45 * tone + thump + 0.35 * snap)

def shimmer():
    n = int(1.6 * SR); tt = np.arange(n) / SR
    x = np.zeros(n)
    for k, f in enumerate([1568, 2093, 2637, 3136, 4186]):
        x += np.sin(2 * np.pi * f * tt + k) * (0.6 + 0.4 * np.sin(2 * np.pi * (5 + k) * tt)) / (k + 1)
    e = np.minimum(1, tt / 0.04) * np.exp(-tt * 2.6)
    return norm(x * e)

sfx = np.zeros((N, 2))
place(sfx, impact(), 0.10, -22)
for pk, pan in [(2.402, -0.2), (3.370, 0.15), (5.305, 0.0), (10.043, 0.0)]:
    w, at = whoosh(pk)
    place(sfx, w, at, -27, pan)
place(sfx, hit(), 6.240, -22)
place(sfx, hit(), 8.175, -22)
place(sfx, click(), 2.33, -26, 0.1)
place(sfx, click(), 3.83, -26, 0.1)
k = 0
for at in np.arange(4.04, 5.0001, 0.032):
    place(sfx, tick(), at + 0.004 * (rng.random() - 0.5), -38 - 3 * rng.random(), 0.25 * (rng.random() - 0.5)); k += 1
place(sfx, shimmer(), 10.05, -28)

mix = m + sfx
# loudness to -14 LUFS
meter = pyln.Meter(SR)
mix *= 10 ** ((-14 - meter.integrated_loudness(mix)) / 20)

def true_peak(x):
    up = ss.resample_poly(x, 4, 1, axis=0)
    return 20 * np.log10(np.max(np.abs(up)) + 1e-12)

# look-ahead limiter on 4x oversampled detection, ceiling -1.3 dBTP, then re-match loudness
def limit(x, ceil_db=-1.3):
    c = 10 ** (ceil_db / 20)
    up = np.abs(ss.resample_poly(x, 4, 1, axis=0)).max(axis=1)
    det = up.reshape(-1, 4).max(axis=1)[:len(x)]
    g = np.minimum(1, c / np.maximum(det, 1e-9))
    la = int(0.002 * SR)
    g = ss.minimum_filter1d(g, size=2 * la + 1) if hasattr(ss, 'minimum_filter1d') else g
    from scipy.ndimage import minimum_filter1d, uniform_filter1d
    g = minimum_filter1d(g, size=2 * la + 1)
    g = uniform_filter1d(g, size=la)
    # release smoothing
    rel = np.exp(-1 / (0.06 * SR)); out = g.copy()
    for i in range(1, len(out)):
        out[i] = min(g[i], out[i - 1] * rel + (1 - rel) * g[i]) if g[i] > out[i - 1] else g[i]
    return x * out[:, None]

for it in range(4):
    if true_peak(mix) <= -1.05: break
    mix = limit(mix)
    mix *= 10 ** ((-14 - meter.integrated_loudness(mix)) / 20)
# final safety: scale down if still above
tp = true_peak(mix)
if tp > -1.05: mix *= 10 ** ((-1.05 - tp) / 20)
# last 60 ms fade only
nf = int(0.060 * SR)
mix[-nf:] *= np.linspace(1, 0, nf)[:, None] ** 1.5
print('LUFS', round(meter.integrated_loudness(mix), 2), 'TP', round(true_peak(mix), 2), 'len', len(mix) / SR, 'ticks', k)
sf.write(sys.argv[2], mix.astype(np.float32), SR, subtype='FLOAT')
