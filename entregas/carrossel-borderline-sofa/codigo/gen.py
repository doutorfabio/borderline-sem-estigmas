import base64, sys, os
S = sys.argv[1]
B = S + '/build'; F = S + '/fonts'
def b64(p): return base64.b64encode(open(p,'rb').read()).decode()
fonts = f"""
@font-face{{font-family:'Anton';src:url(data:font/woff2;base64,{b64(F+'/fontsource-anton-5.3.0/files/anton-latin-400-normal.woff2')}) format('woff2');}}
@font-face{{font-family:'DM Serif Display';src:url(data:font/woff2;base64,{b64(F+'/fontsource-dm-serif-display-5.3.0/files/dm-serif-display-latin-400-normal.woff2')}) format('woff2');}}
"""
CAP_A = 0.859375; CAP_S = 0.671875
def fa(cap): return round(cap / CAP_A)   # corpo Anton para altura de maiúscula
def fs(cap): return round(cap / CAP_S)   # corpo DM Serif
INK='#111111'; RED='#B3261E'; BLUE='#8EB9D8'
css = fonts + f"""
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1792px;height:2240px;overflow:hidden;background:#fff}}
.slide{{position:relative;width:1792px;height:2240px;overflow:hidden;background:#EEE9E1}}
.bg{{position:absolute;inset:0;width:1792px;height:2240px}}
.blk{{position:absolute;left:0;right:0;text-align:center}}
.ln{{display:block;white-space:nowrap;color:{INK};line-height:1.29}}
.a{{font-family:'Anton';letter-spacing:0.005em}}
.s{{font-family:'DM Serif Display';letter-spacing:0}}
.red{{color:{RED}}}
.blue{{color:{BLUE};-webkit-text-stroke:12px {INK};paint-order:stroke fill}}
.rec{{position:absolute;mix-blend-mode:multiply}}
.pill{{display:inline-block;border:7px solid {INK};border-radius:999px;background:#F4F0E8;padding:38px 70px 30px}}
body.m .bg, body.m .rec, body.m svg, body.m .deco{{visibility:hidden}}
body.m .slide{{background:#fff}}
body.m .ln{{color:#000 !important;-webkit-text-stroke-color:#000 !important}}
body.m .pill{{border-color:transparent;background:transparent}}
"""
def page(body, bg):
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{css}</style></head>
<body><div class="slide"><img class="bg" src="bg-{bg}.png">{body}</div></body></html>"""

slides = {}
A140 = fa(140)
# ---------- 2: bolha no sofá ----------
slides[2] = page(f"""
<div class="blk" style="top:120px">
  <span class="ln a" style="font-size:{A140}px">O QUE PRENDE NO SOFÁ</span>
  <span class="ln a" style="font-size:{A140}px">MUITAS VEZES É</span>
  <span class="ln s red" style="font-size:{fs(196)}px;line-height:1.02;margin-top:6px">VERGONHA</span>
  <span class="ln a" style="font-size:{A140}px">DO QUE FOI DITO ONTEM.</span>
  <img src="rec-bolha-sofa.png" class="deco" style="display:block;margin:40px auto 0;width:840px;mix-blend-mode:multiply">
</div>
""", 'b')
# ---------- 3: dentro da bolha ----------
def bubble_icon(size):
    return f"""<svg class="deco" width="{size}" height="{size}" viewBox="0 0 100 100" style="flex:none">
<circle cx="50" cy="50" r="42" fill="{BLUE}" fill-opacity="0.55" stroke="{INK}" stroke-width="7"/>
<path d="M28 38 A26 26 0 0 1 46 22" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round"/></svg>"""
item = lambda t: f"""<div style="display:flex;align-items:center;gap:40px;margin-top:84px">{bubble_icon(104)}<span class="ln a" style="font-size:{A140}px">{t}</span></div>"""
slides[3] = page(f"""
<div class="blk" style="top:430px">
  <span class="ln a blue" style="font-size:{fa(186)}px">DENTRO DA BOLHA</span>
  <span class="ln a" style="font-size:{A140}px;margin-top:10px">ACONTECE ISTO:</span>
</div>
<div style="position:absolute;top:1060px;left:0;right:0;display:flex;justify-content:center">
 <div style="display:flex;flex-direction:column;align-items:flex-start">
  {item('REPETIR A BRIGA')}{item('IMAGINAR O PIOR')}{item('ESPERAR ALGUÉM VIR')}
 </div>
</div>
""", 'd')
# ---------- 4: ciclo ----------
nodes = [('CRISE',''),('VERGONHA','blue'),('BOLHA',''),('A CASA EM SILÊNCIO',''),('MAIS VERGONHA','blue')]
pills = ''.join(f"""<div class="row" style="height:{232}px;display:flex;justify-content:center;align-items:center;margin-bottom:{118 if i<4 else 0}px"><div class="pill"><span class="ln a {c}" style="font-size:{A140}px;line-height:1">{t}</span></div></div>""" for i,(t,c) in enumerate(nodes))
slides[4] = page(f"""
<div id="chain" style="position:absolute;top:{(2240-(5*232+4*118))//2}px;left:120px;width:1360px">{pills}</div>
<svg id="arrows" width="1792" height="2240" style="position:absolute;inset:0"></svg>
""", 'c')
# ---------- 5: três sinais ----------
rule = f'<div class="deco" style="width:220px;height:8px;background:{INK};margin:40px auto 44px"></div>'
slides[5] = page(f"""
<div class="blk" style="top:175px">
  <span class="ln a" style="font-size:{fa(176)}px">TRÊS SINAIS DE</span>
  <span class="ln s" style="font-size:{fs(150)}px;line-height:1.08">ESCONDERIJO:</span>
  <div class="deco" style="height:50px"></div>
  <span class="ln a" style="font-size:{A140}px">EVITA OLHAR</span>
  {rule}
  <span class="ln a" style="font-size:{A140}px">RESPONDE COM</span>
  <span class="ln a" style="font-size:{A140}px">UMA PALAVRA</span>
  {rule}
  <span class="ln a" style="font-size:{A140}px">SE ENCOLHE QUANDO</span>
  <span class="ln a" style="font-size:{A140}px">ALGUÉM ENTRA</span>
</div>
""", 'b')
# ---------- 6: mulher com a caneca ----------
wh = 1220; ww = round(380 * wh / 780)
slides[6] = page(f"""
<div class="blk" style="top:170px;left:170px;text-align:left">
  <span class="ln a" style="font-size:{fa(190)}px">DÁ PARA CUIDAR</span>
  <span class="ln a blue" style="font-size:{fa(190)}px">SEM INVADIR:</span>
</div>
<div class="blk" style="top:1140px;left:188px;text-align:left">
  <span class="ln a" style="font-size:{A140}px">DEIXAR O PRATO</span>
  <span class="ln a" style="font-size:{A140}px">PERTO E SAIR.</span>
</div>
<img class="rec" src="rec-mulher.png" style="left:{1792-ww}px;top:{2240-wh-40}px;width:{ww}px;height:{wh}px">
""", 'c')
# ---------- 7: interativo ----------
opt = lambda n, l1, l2, mt: f"""<div style="display:flex;align-items:center;gap:56px;margin-top:{mt}px">
 <span class="ln s blue" style="font-size:{fs(250)}px;line-height:0.9;-webkit-text-stroke-width:10px;width:300px;text-align:right">{n}</span>
 <div style="text-align:left"><span class="ln a" style="font-size:{A140}px;line-height:1.15">{l1}</span><span class="ln a" style="font-size:{A140}px;line-height:1.15">{l2}</span></div></div>"""
slides[7] = page(f"""
<div class="blk" style="top:150px;left:-10px">
  <span class="ln a" style="font-size:{fa(180)}px">NESSA SALA,</span>
  <span class="ln a blue" style="font-size:{fa(180)}px">VOCÊ É QUAL?</span>
</div>
<div style="position:absolute;top:790px;left:-40px;right:0;display:flex;justify-content:center">
 <div>{opt('1.','QUEM ESTÁ','NA BOLHA',0)}{opt('2.','QUEM PASSA','PELA SALA',56)}</div>
</div>
<div class="blk" style="top:1700px;left:-10px">
  <span class="ln a" style="font-size:{A140}px">RESPONDE SÓ</span>
  <span class="ln a" style="font-size:{A140}px">COM O NÚMERO.</span>
</div>
""", 'a')
# ---------- 8: fecho ----------
slides[8] = page(f"""
<div class="blk" style="top:190px">
  <span class="ln a" style="font-size:{A140}px">A FAMÍLIA NÃO PRECISA</span>
  <span class="ln a" style="font-size:{A140}px">ESTOURAR A BOLHA.</span>
  <div class="deco" style="height:60px"></div>
  <span class="ln a" style="font-size:{fa(196)}px">BASTA FICAR</span>
  <span class="ln s" style="font-size:{fs(176)}px;line-height:1.1">POR PERTO</span>
  <span class="ln a blue" style="font-size:{fa(196)}px">ATÉ ELA ABRIR.</span>
</div>
<div class="blk" style="top:1690px;left:172px;text-align:left">
  <div class="deco" style="width:150px;height:8px;background:{INK};margin-bottom:40px"></div>
  <span class="ln a" style="font-size:{A140}px;line-height:1.16">BORDERLINE TEM</span>
  <span class="ln a" style="font-size:{A140}px;line-height:1.16">TRATAMENTO.</span>
</div>
<img class="rec" src="rec-bolha-disco.png" style="left:1250px;top:1720px;width:400px;height:400px">
""", 'd')
for n, h in slides.items():
    open(f'{B}/slide-{n}.html', 'w').write(h)
print('gerados', sorted(slides))
