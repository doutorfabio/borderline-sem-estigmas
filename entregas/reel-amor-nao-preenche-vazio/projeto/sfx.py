# Mistura a narração com efeitos da biblioteca memoria/sfx/editorpro.
# Uso: python3 sfx.py voz.wav cues-narracao.js saida.wav
import sys, json, subprocess, wave, os, numpy as np
SR=48000
LIB=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","..","memoria","sfx","editorpro")
def load(path,hp=None):
    # canal esquerdo só: a redução padrão de estéreo para mono do ffmpeg soma 3 dB
    af=["-af","pan=mono|c0=c0"+(",highpass=f=%d"%hp if hp else "")]
    raw=subprocess.run(["ffmpeg","-loglevel","error","-i",path,*af,"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.float32).copy()
voz=load(sys.argv[1]); C=json.loads(open(sys.argv[2]).read().split("=",1)[1].rstrip(";\n"))
mix=np.zeros(len(voz),dtype=np.float32)
# (arquivo, instante do evento em s, pico alvo em dBFS)
EV=[("Whoosh_Swipe9.mp3",C["s2"]+.03,-27),("Whoosh_Fino6.mp3",C["s2n"],-27),("Whoosh_Swipe9.mp3",C["s3"]+.03,-28),
    ("Whoosh_Fino6.mp3",C["s4"],-27),("HUD_Pop-Up2.mp3",C["r1"]+.04,-27),("HUD_Pop-Up2.mp3",C["r2"]+.04,-27),
    ("HUD_Pop-Up2.mp3",C["r3"]+.04,-27),("Futurista_Click7.mp3",C["door"]+.12,-26),("Whoosh_Swipe9.mp3",C["s5"]+.03,-27),
    ("HUD_Pop-Up2.mp3",C["s6"]+.04,-27)]
for f,t,db in EV:
    x=load(os.path.join(LIB,f),hp=150)          # sem grave
    pk=int(np.argmax(np.abs(x)))
    x*=10**(db/20)/np.abs(x).max()               # pico no nível alvo
    n=int(.01*SR); x[-n:]*=np.linspace(1,0,n)
    i=int(t*SR)-pk                                # o pico cai no evento
    a=max(0,i); b=min(len(mix),i+len(x))
    mix[a:b]+=x[a-i:b-i]
    print("%-22s evento %.2f s  pico %d dBFS"%(f,t,db))
out=voz+mix
w=wave.open(sys.argv[3],"wb");w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR)
st=np.repeat((np.clip(out,-1,1)*32767).astype(np.int16)[:,None],2,axis=1)
w.writeframes(st.tobytes());w.close()
vrms=20*np.log10(np.sqrt(np.mean(voz[np.abs(voz)>0.01]**2)))
print("média da voz %.1f dBFS; maior pico de efeito %.1f dBFS"%(vrms,20*np.log10(np.abs(mix).max())))
