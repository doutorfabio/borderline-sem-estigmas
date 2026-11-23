import subprocess, re, json
def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)
def medir(f):
    r = run(f'ffmpeg -hide_banner -i {f} -af ebur128=peak=true:framelog=quiet -f null -')
    t = r.stderr[r.stderr.rindex('Summary:'):]
    I = float(re.search(r'I:\s+(-?[\d.]+) LUFS', t).group(1))
    tp = float(re.search(r'Peak:\s+(-?[\d.]+) dBFS', t).group(1))
    lra = float(re.search(r'LRA:\s+(-?[\d.]+) LU', t).group(1))
    return I, tp, lra
# 1. voz: ruído leve, de-esser, compressão suave
run('ffmpeg -v error -y -i voz_raw.wav -af "highpass=f=80,afftdn=nr=10:nf=-58,deesser=i=0.25:m=0.5:f=0.5:s=o,acompressor=threshold=-20dB:ratio=2:attack=10:release=150:makeup=1:knee=6" -ar 48000 -c:a pcm_s24le voz_proc.wav')
vI, vtp, vlra = medir('voz_proc.wav')
print('voz tratada', vI, vtp, vlra)
# 2. ambiente: 20 dB abaixo da voz enquanto ele fala, sobe ~3 dB nas pausas
alvo = vI - 17.0
gA = alvo - (-47.8); gB = alvo - (-36.0)
print('ganho ambiente A %.1f dB, B %.1f dB' % (gA, gB))
ins1 = (776/30, (878-776)/30); ins2 = (1102/30, (1239-1102)/30)
fc = (
 f"[0:a]asplit=2[v1][vk];"
 f"[1:a]atrim=0:{ins1[1]:.4f},afade=t=in:d=0.02,afade=t=out:st={ins1[1]-0.02:.4f}:d=0.02,volume={gA:.2f}dB,adelay={int(ins1[0]*1000)}:all=1[a];"
 f"[2:a]atrim=0:{ins2[1]:.4f},afade=t=in:d=0.02,afade=t=out:st={ins2[1]-0.02:.4f}:d=0.02,volume={gB:.2f}dB,adelay={int(ins2[0]*1000)}:all=1[b];"
 f"[a][b]amix=inputs=2:normalize=0:duration=longest,apad=whole_dur=43.034[amb];"
 f"[amb][vk]sidechaincompress=threshold=0.02:ratio=1.3:attack=20:release=300[ambd];"
 f"[ambd]asplit=2[ambo][ambm];"
 f"[v1][ambm]amix=inputs=2:normalize=0:duration=first[mix]"
)
r = run(f'ffmpeg -v error -y -i voz_proc.wav -i ambA.wav -i ambB.wav -filter_complex "{fc}" -map "[mix]" -c:a pcm_s24le mix_pre.wav -map "[ambo]" -c:a pcm_s24le amb_so.wav')
print(r.stderr[-400:])
mI, mtp, mlra = medir('mix_pre.wav')
print('mix antes do master', mI, mtp, mlra)
# 3. master: ganho + limitador, até -14 LUFS e pico verdadeiro <= -1 dBTP
g = -14.0 - mI
for k in range(4):
    run(f'ffmpeg -v error -y -i mix_pre.wav -af "volume={g:.2f}dB,alimiter=limit=0.794:level=disabled:attack=4:release=70,aresample=48000" -c:a pcm_s24le master.wav')
    I, tp, lra = medir('master.wav')
    print('master tentativa', k, 'ganho %.2f' % g, I, tp, lra)
    if abs(I + 14.0) < 0.15: break
    g += (-14.0 - I)
json.dump({'vozI': vI, 'gA': gA, 'gB': gB, 'ganho': g, 'I': I, 'tp': tp, 'lra': lra}, open('som.json', 'w'))
