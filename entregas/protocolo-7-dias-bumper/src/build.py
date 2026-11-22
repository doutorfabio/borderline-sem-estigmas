import base64, pathlib
d = pathlib.Path(__file__).parent
def ff(fam, f):
    b = base64.b64encode((d/f).read_bytes()).decode()
    return f'@font-face{{font-family:"{fam}";src:url(data:font/woff2;base64,{b}) format("woff2");font-display:block;}}'
css = "\n".join([ff("Archivo Black","archivo.woff2"), ff("Poppins","poppins.woff2"), ff("IBM Plex Mono","plex.woff2")])
src = (d/"bumper.src.html").read_text()
(d.parent/"protocolo-7-dias-bumper.html").write_text(src.replace("/*FONTS*/", css))
print("ok")
