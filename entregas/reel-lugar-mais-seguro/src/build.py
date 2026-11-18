# Inlines fonts and prepared assets into one self-contained HTML.
# usage: python3 build.py <assets_dir> <fonts_node_modules> <out.html>
import sys, os, base64, json
here=os.path.dirname(os.path.abspath(__file__))
assets, fonts, out = sys.argv[1], sys.argv[2], sys.argv[3]
b64=lambda p: base64.b64encode(open(p,'rb').read()).decode()
F={'__FONT_ANTON__':'anton/files/anton-latin-400-normal.woff2',
   '__FONT_FRAUNCES_400__':'fraunces/files/fraunces-latin-400-normal.woff2',
   '__FONT_KEY__':'bodoni-moda/files/bodoni-moda-latin-900-italic.woff2',
   '__FONT_COURIER_400__':'courier-prime/files/courier-prime-latin-400-normal.woff2',
   '__FONT_COURIER_700__':'courier-prime/files/courier-prime-latin-700-normal.woff2'}
names={'A01':'A01_crab','A02':'A02_shell','A03':'A03_dinner','A04':'A04_vanity','A05':'A05_door','A06':'A06_mirror','A07':'A07_cup',
       'I01':'I01_frog','I02':'I02_shell','I03':'I03_key','I04':'I04_tear','I05':'I05_pearls','I06':'I06_hands'}
A={}
for k,n in names.items():
    e={'a':'data:image/webp;base64,'+b64(os.path.join(assets,n+'_a.webp'))}
    s=os.path.join(assets,n+'_s.webp'); m=os.path.join(assets,n+'_m.png')
    if os.path.exists(s): e['s']='data:image/webp;base64,'+b64(s)
    if os.path.exists(m): e['m']='data:image/png;base64,'+b64(m)
    A[k]=e
html=open(os.path.join(here,'reel.template.html'),encoding='utf-8').read()
for k,p in F.items(): html=html.replace(k,b64(os.path.join(fonts,'@fontsource',p)))
html=html.replace('__ASSETS_JSON__',json.dumps(A))
open(out,'w',encoding='utf-8').write(html)
print(out, round(len(html)/1e6,2),'MB')
