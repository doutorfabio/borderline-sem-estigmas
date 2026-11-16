# Injeta tempos.json no index.html -> render.html
import json,re
s=open('index.html').read(); t=open('tempos.json').read()
s=re.sub(r'/\*TEMPOS\*/.*?/\*FIM\*/','/*TEMPOS*/'+t+'/*FIM*/',s,flags=re.S)
open('render.html','w').write(s)
