import sys,re
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
m=re.search(r'<title>.*?</title>',s); title=m.group(0); s=s.replace(title,'',1)
head=f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{title}
<meta property="og:title" content="Uma respiração para cada momento">
<meta property="og:description" content="Respirações guiadas e gratuitas para ansiedade, insônia, briga em família e crise. Dr. Fabio Schmidt, médico, CRM-SP 183549.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://curso.drfabioschmidt.net/respirar/">
<link rel="icon" href="/favicon-32.png" sizes="32x32">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}img{{max-width:100%}}</style>
'''
# move the <meta>/<link>/<style> block (everything before first <div class="pagina">) into head
i=s.index('<div class="pagina">')
out=head+s[:i].strip()+'\n</head>\n<body>\n'+s[i:].strip()+'\n</body>\n</html>\n'
open(dst,'w',encoding='utf-8').write(out)
print('ok',len(out))
