import base64,sys
d='node_modules/@fontsource/'
def b(p): return base64.b64encode(open(p,'rb').read()).decode()
s=open('src.html').read()
s=s.replace('/*OPENTYPE*/',open('node_modules/opentype.js/dist/opentype.min.js').read())
s=s.replace('/*BODONI600*/',b(d+'bodoni-moda/files/bodoni-moda-latin-600-normal.woff'))
s=s.replace('/*ARCHIVOBLACK*/',b(d+'archivo-black/files/archivo-black-latin-400-normal.woff'))
s=s.replace('/*MONT700*/',b(d+'montserrat/files/montserrat-latin-700-normal.woff'))
s=s.replace('/*MONT500*/',b(d+'montserrat/files/montserrat-latin-500-normal.woff'))
open('protocolo-7-dias-tipografico.html','w').write(s)
print(len(s))
