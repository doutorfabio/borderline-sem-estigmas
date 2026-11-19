# Como refazer

1. `npm i @fontsource/bodoni-moda @fontsource/archivo-black @fontsource/montserrat opentype.js`
2. `python3 build.py src.html ../protocolo-7-dias-tipografico.html` (embute as fontes e o opentype.js)
3. `node shoot.js render` gera os 450 quadros em `frames/` com `window.seek(n/30)`
4. `ffmpeg -framerate 30 -i frames/f%04d.png -c:v libx264 -pix_fmt yuv420p -crf 14 -an saida.mp4`

`node shoot.js measure` mede a área segura por pixel, com o recorte desligado.
