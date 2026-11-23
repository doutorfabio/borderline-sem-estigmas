import subprocess, re, json
SFX = '/home/user/borderline-sem-estigmas/memoria/sfx/editorpro/'
def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)
def medir(f, extra=''):
    r = run(f'ffmpeg -hide_banner {extra} -i {f} -af ebur128=peak=true:framelog=quiet -f null -')
    t = r.stderr[r.stderr.rindex('Summary:'):]
    I = float(re.search(r'I:\s+(-?[\d.]+) LUFS', t).group(1))
    tp = float(re.search(r'Peak:\s+(-?[\d.]+) dBFS', t).group(1))
    lra = float(re.search(r'LRA:\s+(-?[\d.]+) LU', t).group(1))
    return I, tp, lra
som = json.load(open('som.json'))
G = som['ganho']  # ganho do master medido na passada anterior
# (arquivo, pico do arquivo em dBFS, início em s, pico final desejado em dBFS)
itens = [
 ('Whoosh_Swipe9.mp3',   -1.8, 776/30 - 0.160, -24.0),   # entrada do B-roll A
 ('Shutter_Camera2.mp3',  2.4, 841/30 + 0.067 - 0.238, -23.0),  # PERIGOSO
 ('Shutter_Camera.mp3',   0.3, 878/30 + 0.067 - 0.133, -23.0),  # RELAÇÃO RUIM
 ('Whoosh_Fino6.mp3',    -8.4, 1102/30 - 0.737, -24.0),  # entrada do B-roll B
 ('Shutter_Camera.mp3',   0.3, 1205/30 + 0.067 - 0.133, -23.0), # CONTROLE
 ('Futurista_Click4.mp3', 4.9, 309/30 - 0.086, -27.0),   # aproximação 1
 ('Futurista_Click7.mp3', 6.1, 544/30 - 0.051, -27.0),   # aproximação 2
 ('Futurista_Click4.mp3', 4.9, 1017/30 - 0.086, -27.0),  # aproximação 3
]
ins = ''.join(f' -i {SFX}{f}' for f, *_ in itens)
fc = ''
for k, (f, pk, t0, alvo) in enumerate(itens):
    g = (alvo - G) - pk
    fc += f"[{k}:a]aresample=48000,highpass=f=150,volume={g:.2f}dB,adelay={int(round(t0*1000))}:all=1[s{k}];"
fc += ''.join(f'[s{k}]' for k in range(len(itens))) + f"amix=inputs={len(itens)}:normalize=0:duration=longest,apad=whole_dur=43.034[sfx]"
r = run(f'ffmpeg -v error -y{ins} -filter_complex "{fc}" -map "[sfx]" -ac 2 -c:a pcm_s24le sfx_so.wav')
print(r.stderr[-300:])
r = run('ffmpeg -v error -y -i mix_pre.wav -i sfx_so.wav -filter_complex "[0:a][1:a]amix=inputs=2:normalize=0:duration=first[m]" -map "[m]" -c:a pcm_s24le mix_pre2.wav')
print(r.stderr[-300:])
mI, mtp, mlra = medir('mix_pre2.wav')
print('mix com efeitos, antes do master', mI, mtp, mlra)
g = -14.0 - mI
for k in range(4):
    run(f'ffmpeg -v error -y -i mix_pre2.wav -af "volume={g:.2f}dB,alimiter=limit=0.794:level=disabled:attack=4:release=70,aresample=48000" -c:a pcm_s24le master.wav')
    I, tp, lra = medir('master.wav')
    print('master', k, 'ganho %.2f' % g, I, tp, lra)
    if abs(I + 14.0) < 0.15: break
    g += (-14.0 - I)
# pico dos efeitos sozinhos no domínio final
r = run(f'ffmpeg -hide_banner -i sfx_so.wav -af "volume={g:.2f}dB,astats=metadata=0:measure_overall=Peak_level" -f null -')
print('pico dos efeitos sozinhos no master:', re.findall(r'Peak level dB: (-?[\d.]+)', r.stderr)[-1])
json.dump({'ganho': g, 'I': I, 'tp': tp, 'lra': lra}, open('som2.json', 'w'))
