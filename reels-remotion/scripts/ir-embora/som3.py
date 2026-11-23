# Som completo do Reel Ir embora: voz tratada (voz_proc.wav, feita em som.py), ambiente dos 4 B-rolls,
# efeitos da biblioteca, música Ringing Chord (Suno, versão 1 da gravação de tela) e master em -14 LUFS.
import subprocess, re, json
SFX = '/home/user/borderline-sem-estigmas/memoria/sfx/editorpro/'
MUS = '../mus/gravacao.wav'
def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)
def medir(f):
    r = run(f'ffmpeg -hide_banner -i {f} -af ebur128=peak=true:framelog=quiet -f null -')
    t = r.stderr[r.stderr.rindex('Summary:'):]
    return (float(re.search(r'I:\s+(-?[\d.]+) LUFS', t).group(1)), float(re.search(r'Peak:\s+(-?[\d.]+) dBFS', t).group(1)), float(re.search(r'LRA:\s+(-?[\d.]+) LU', t).group(1)))
vI = medir('voz_proc.wav')[0]
G = 13.7  # ganho de master medido nas passadas anteriores
# ambiente: 20 dB abaixo da voz enquanto ele fala, sobe ~3 dB nas pausas
alvo = vI - 17.0
amb = [  # arquivo, LUFS do arquivo, quadro de entrada, quadros
 ('ambMesa.wav', -31.4, 365, 106),
 ('ambCel.wav',  -36.2, 544, 63),
 ('ambA.wav',    -47.8, 776, 102),
 ('ambB.wav',    -36.0, 1102, 137),
]
sfx = [  # arquivo, pico do arquivo, início em s, pico final desejado
 ('Whoosh_Swipe9.mp3',   -1.8, 365/30 - 0.160, -24.0),   # entra a mesa
 ('Whoosh_Fino6.mp3',    -8.4, 544/30 - 0.737, -24.0),   # entra o celular
 ('Whoosh_Swipe9.mp3',   -1.8, 776/30 - 0.160, -24.0),   # entra o tênis preso
 ('Whoosh_Fino6.mp3',    -8.4, 1102/30 - 0.737, -24.0),  # entra o tênis solto
 ('Shutter_Camera2.mp3',  2.4, 841/30 + 0.067 - 0.238, -23.0),  # PERIGOSO
 ('Shutter_Camera.mp3',   0.3, 878/30 + 0.067 - 0.133, -23.0),  # RELAÇÃO RUIM
 ('Shutter_Camera.mp3',   0.3, 1205/30 + 0.067 - 0.133, -23.0), # CONTROLE
 ('Futurista_Click4.mp3', 4.9, 309/30 - 0.086, -27.0),   # aproximação 1
 ('Futurista_Click4.mp3', 4.9, 1017/30 - 0.086, -27.0),  # aproximação 2
 ('HUD_Pop-Up2.mp3',     -2.3, 54/30 + 0.067 - 0.062, -27.0),   # BORDERLINE
 ('HUD_Pop-Up2.mp3',     -2.3, 243/30 + 0.067 - 0.062, -26.0),  # EU FICO
 ('HUD_Pop-Up2.mp3',     -2.3, 751/30 + 0.067 - 0.062, -26.0),  # NÃO TERMINA ENTÃO?
 ('HUD_Pop-Up2.mp3',     -2.3, 1058/30 + 0.067 - 0.062, -26.0), # MEDO
]
ins = ' -i voz_proc.wav' + ''.join(f' -i {f}' for f, *_ in amb) + ''.join(f' -i {SFX}{f}' for f, *_ in sfx) + f' -i {MUS}'
fc = '[0:a]asplit=2[v1][vk];'
for k, (f, lufs, q, n) in enumerate(amb):
    d = n / 30; g = alvo - lufs
    fc += f"[{k+1}:a]atrim=0:{d:.4f},afade=t=in:d=0.02,afade=t=out:st={d-0.02:.4f}:d=0.02,volume={g:.2f}dB,adelay={int(round(q/30*1000))}:all=1[a{k}];"
fc += ''.join(f'[a{k}]' for k in range(len(amb))) + f"amix=inputs={len(amb)}:normalize=0:duration=longest,apad=whole_dur=43.034[amb];"
fc += "[amb][vk]sidechaincompress=threshold=0.02:ratio=1.3:attack=20:release=300[ambd];"
b = 1 + len(amb)
for k, (f, pk, t0, alv) in enumerate(sfx):
    g = (alv - G) - pk
    fc += f"[{b+k}:a]aresample=48000,highpass=f=150,volume={g:.2f}dB,adelay={int(round(t0*1000))}:all=1[s{k}];"
fc += ''.join(f'[s{k}]' for k in range(len(sfx))) + f"amix=inputs={len(sfx)}:normalize=0:duration=longest,apad=whole_dur=43.034[sfx];"
# música: versão 1 começa em 1,08 s da gravação; pulo 0,44 s para a quebra cair em "ameniza" (38,1 s)
m = b + len(sfx)
INI = 1.08 + 0.44
GM = (vI - 16.0) - (-14.3)   # corpo da música 16 dB abaixo da voz
fc += f"[{m}:a]atrim={INI:.2f}:{INI+43.034:.3f},asetpts=PTS-STARTPTS,highpass=f=70,afade=t=in:d=0.05,afade=t=out:st=42.2:d=0.83,volume={GM:.2f}dB[mus];"
fc += "[v1][ambd][sfx][mus]amix=inputs=4:normalize=0:duration=first[mix]"
r = run(f'ffmpeg -v error -y{ins} -filter_complex "{fc}" -map "[mix]" -ac 2 -ar 48000 -c:a pcm_s24le mix_pre3.wav')
print(r.stderr[-500:])
r = run(f'ffmpeg -v error -y -i {MUS} -af "atrim={INI:.2f}:{INI+43.034:.3f},asetpts=PTS-STARTPTS,volume={GM:.2f}dB" -ar 48000 mus_so.wav')
print('música sozinha (pré-master):', medir('mus_so.wav'), '| voz:', vI)
mI, mtp, mlra = medir('mix_pre3.wav')
print('mix antes do master', mI, mtp, mlra)
g = -14.0 - mI
for k in range(5):
    run(f'ffmpeg -v error -y -i mix_pre3.wav -af "volume={g:.2f}dB,alimiter=limit=0.794:level=disabled:attack=4:release=70,aresample=48000" -c:a pcm_s24le master3.wav')
    I, tp, lra = medir('master3.wav')
    print('master', k, 'ganho %.2f' % g, I, tp, lra)
    if abs(I + 14.0) < 0.12: break
    g += (-14.0 - I)
json.dump({'ganho': g, 'I': I, 'tp': tp, 'lra': lra}, open('som3.json', 'w'))
