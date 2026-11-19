# Como refazer

1. `npm i @fontsource/bodoni-moda @fontsource/archivo-black @fontsource/montserrat opentype.js`
2. `python3 build.py src.html ../protocolo-7-dias-tipografico.html` (embute as fontes e o opentype.js)
3. `node shoot.js render` gera os 450 quadros em `frames/` com `window.seek(n/30)`
4. `ffmpeg -framerate 30 -i frames/f%04d.png -c:v libx264 -pix_fmt yuv420p -crf 14 -an saida.mp4`

`node shoot.js measure` mede a área segura por pixel, com o recorte desligado.

## Efeitos sonoros

`python3 sfx.py ../../../memoria/sfx efeitos.wav` monta a trilha só com a biblioteca `memoria/sfx/`
(inclui `editorpro/Riser_Whoosh_Perfeito.mp3`, trazido do Drive em 19/11) e imprime a sincronia de cada efeito.
Depois: `ffmpeg -i video.mp4 -i efeitos.wav -c:v copy -c:a aac -b:a 192k saida.mp4`.
