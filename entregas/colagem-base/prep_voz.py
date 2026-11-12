# uso: prep_voz.py <take.wav> <palavras_brutas.json> <pasta-da-peca> [pausa_max]
# Encurta pausas no mesmo take, tira o silencio inicial e remapeia os tempos das palavras.
import sys,json,subprocess,os
raw,wj,out=sys.argv[1:4]; keep=sys.argv[4] if len(sys.argv)>4 else '0.36'
here=os.path.dirname(os.path.abspath(__file__))
r=json.loads(subprocess.run([sys.executable,os.path.join(here,'aperta_pausas.py'),raw,'/tmp/_ap.wav',keep],capture_output=True,text=True,check=True).stdout)
cuts=r['cuts']; head=max(0,(r['sil'][0][1]-0.08) if r['sil'] and r['sil'][0][0]==0 else 0)
def m(t): return round(max(0,t-sum(min(b,t)-a for a,b in cuts if t>a)-head),2)
W=json.load(open(wj)); json.dump([[w,m(a),m(b)] for w,a,b in W],open(os.path.join(out,'words.json'),'w'),ensure_ascii=False)
subprocess.run(['ffmpeg','-v','error','-y','-i','/tmp/_ap.wav','-af',f'atrim=start={head},asetpts=PTS-STARTPTS',os.path.join(out,'assets','voz.wav')],check=True)
print('dur',round(r['dur']-head,2),'cortes',len(cuts),'ultima palavra termina',m(W[-1][2]))
