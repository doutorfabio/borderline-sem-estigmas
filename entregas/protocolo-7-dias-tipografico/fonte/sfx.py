# Trilha de efeitos do filme tipográfico Protocolo 7 Dias.
# Só usa a biblioteca memoria/sfx/ (EditorPro e gerados). Tempos presos às deixas do filme.
import subprocess, sys, numpy as np, wave
LIB = sys.argv[1]; OUT = sys.argv[2]
SR = 48000; DUR = 15.0
mix = np.zeros((int(SR*DUR), 2), dtype=np.float64)

def clip(path, ss, dur, af=None):
    cmd = ['ffmpeg','-v','error','-ss',str(ss),'-t',str(dur),'-i',LIB+'/'+path]
    cmd += ['-af', 'aresample=%d' % SR + ((','+af) if af else ''), '-ac','2','-ar',str(SR),'-f','f32le','-']
    raw = subprocess.run(cmd, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1,2).astype(np.float64)

def place(x, t, peak_db, fin=0.004, fout=0.05):
    x = x.copy(); n = len(x)
    a, b = int(fin*SR), int(fout*SR)
    if a>0: x[:a] *= np.linspace(0,1,a)[:,None]
    if b>0: x[-b:] *= np.linspace(1,0,b)[:,None]
    x *= (10**(peak_db/20)) / (np.abs(x).max() + 1e-12)
    i = int(round(t*SR)); j = min(len(mix), i+n)
    mix[i:j] += x[:j-i]

EV = []   # registro: (tempo no filme, o que é, arquivo)
def ev(t, what, f): EV.append((t, what, f))

# 1) Pressão da laje sobre a frase: fio de aço esticando, termina em 2,60 s
place(clip('gerados/Fio_de_aco_esticando.m4a', 0.16, 1.44), 1.16, -21, fin=0.12, fout=0.30); ev(1.16, 'tensão: a laje aperta a frase', 'Fio_de_aco_esticando')
# 2) improvisa vira IMPROVISA
place(clip('editorpro/Futurista_Click7.mp3', 0.03, 0.27), 2.58, -18, fout=0.12); ev(2.60, 'clique: improvisa passa para a letra pesada', 'Futurista_Click7')
# 3) Letras de IMPROVISA batem no chão (3,20 a 3,38 s)
place(clip('gerados/Letreiro_de_aeroporto.m4a', 0.30, 0.24), 3.17, -20, fin=0.01, fout=0.05); ev(3.17, 'letras de IMPROVISA tocam o chão', 'Letreiro_de_aeroporto (trecho)')
# 4) A laje desce: whoosh abafado, sem subgrave
place(clip('editorpro/Whoosh_Abafado.mp3', 0.70, 1.05, 'highpass=f=110,highpass=f=110'), 3.02, -20, fin=0.25, fout=0.45); ev(3.02, 'a laje desce', 'Whoosh_Abafado (filtro passa-alta 110 Hz)')
# 5) A laje assenta: carimbo meio tom abaixo, abafado
place(clip('gerados/Ficha_deslizando_e_carimbo.m4a', 3.20, 0.50, 'asetrate=%d,aresample=%d,highpass=f=90,lowpass=f=1100' % (int(SR*0.8), SR)), 3.72, -14, fout=0.25); ev(3.78, 'a laje assenta sobre IMPROVISA', 'Ficha_deslizando_e_carimbo (carimbo, mais grave e abafado)')
# 6) Sete colunas: um deslize curto e um estalo por coluna; o estalo sobe meio tom a cada coluna
steps = [5.15] + [5.05 + 0.3*k + 0.27 for k in range(1,7)]
for k in range(7):
    c = 5.05 + 0.3*k; r = 2 ** (k/12.0)
    place(clip('editorpro/Whoosh_Swipe9.mp3', 0.07, 0.25), c + 0.03, -27 + 0.4*k, fin=0.01, fout=0.08)
    place(clip('editorpro/Futurista_Click7.mp3', 0.03, 0.24, 'asetrate=%d,aresample=%d' % (int(SR*r), SR)), steps[k] - 0.02/r, -18 + 0.7*k, fout=0.10)
    ev(steps[k], 'coluna %d encosta na laje' % (k+1), 'Futurista_Click7 (+%d semitons) e Whoosh_Swipe9' % k)
# 6b) Subida de ar por baixo das sete colunas; o auge cai quando a laje nivela (7,12 s)
place(clip('editorpro/Riser_Whoosh_Perfeito.mp3', 0.75, 2.75), 4.97, -18, fin=0.35, fout=0.45); ev(7.12, 'laje nivela (auge da subida de ar)', 'Riser_Whoosh_Perfeito (Drive)')
# 7) Sete dias.: silêncio de propósito (400 ms de imobilidade)
# 8) Piso, letra a letra (8,62 a 9,44 s), e batida final quando assenta
place(clip('gerados/Letreiro_de_aeroporto.m4a', 2.90, 0.82), 8.62, -18, fin=0.03, fout=0.06); ev(8.62, 'piso entra letra a letra', 'Letreiro_de_aeroporto (corrida)')
place(clip('gerados/Letreiro_de_aeroporto.m4a', 4.05, 0.30), 9.40, -13, fout=0.12); ev(9.45, 'piso assenta', 'Letreiro_de_aeroporto (batida final)')
# 9) Câmera desce
place(clip('editorpro/Whoosh_Fino6.mp3', 0.30, 1.00), 10.82, -18, fin=0.05, fout=0.25); ev(11.00, 'câmera desce', 'Whoosh_Fino6')
# 10) Protocolo 7 Dias.
place(clip('editorpro/HUD_Pop-Up2.mp3', 0.03, 0.45), 11.58, -19, fout=0.18); ev(11.60, 'Protocolo 7 Dias. entra', 'HUD_Pop-Up2')
# 11) Cupom: ficha desliza e carimbo no BLACK26
place(clip('gerados/Ficha_deslizando_e_carimbo.m4a', 1.45, 0.50), 12.58, -21, fin=0.03, fout=0.15); ev(12.60, 'linha do cupom entra', 'Ficha_deslizando_e_carimbo (deslize)')
place(clip('gerados/Ficha_deslizando_e_carimbo.m4a', 3.20, 0.55, 'highpass=f=90'), 12.855, -10, fout=0.25); ev(12.90, 'carimbo no BLACK26', 'Ficha_deslizando_e_carimbo (carimbo)')

mix *= 10**(4/20)   # ganho geral: pico mais alto em -6 dBFS
pk = np.abs(mix).max()
print('pico da mixagem: %.1f dBFS' % (20*np.log10(pk)))
out = np.clip(mix, -1, 1)
w = wave.open(OUT, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out*32767).astype('<i2').tobytes()); w.close()
# fração de energia abaixo de 120 Hz
m = mix.mean(axis=1); X = np.abs(np.fft.rfft(m))**2; f = np.fft.rfftfreq(len(m), 1/SR)
print('energia abaixo de 120 Hz: %.1f%%' % (100*X[f<120].sum()/X.sum()))
# conferência de sincronia: pico local de cada evento
for t, what, fn in sorted(EV):
    a, b = int((t-0.12)*SR), int((t+0.25)*SR); seg = np.abs(m[a:b]); tp = (a + int(np.argmax(seg)))/SR
    print('%6.2f s  %-44s pico em %6.3f s (%+4.0f ms)  %5.1f dBFS  %s' % (t, what, tp, (tp-t)*1000, 20*np.log10(seg.max()+1e-9), fn))
