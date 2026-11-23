# Reel Ir embora (23/11/2026)

Composições em `src/IrEmbora/`: IrEmbora (vídeo), IrEmboraTexto (só texto, para medir área segura), IrEmboraCapa.

Material em `videos/guardados-2026-11-23/` (fala, B-rolls, tipos antigos). Preparo, nesta ordem:

1. Cor (`grade.txt`) aplicada à fala e aos B-rolls com ffmpeg; B-rolls de 24 para 30 qps com `minterpolate` e de 720p para 1080p. Saídas em `public/ir-embora/` (talk.mp4, brollA.mp4, brollB.mp4, capa-base.png), fora do git.
2. `npx remotion bundle` e `npx remotion render <bundle> IrEmbora video.mp4 --muted --crf=10 --jpeg-quality=95 --browser-executable=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell`.
3. Som: `som.py` (voz tratada e ambiente dos B-rolls) e `som2.py` (efeitos de `memoria/sfx/editorpro` e master em -14 LUFS).
4. Final: ffmpeg com `noise=c0s=8:c0f=t+u`, libx264 crf 19, maxrate 5000k, AAC 192k.
5. Área segura: render de IrEmboraTexto em PNG e `medir.py`.

`words.json`: transcrição palavra por palavra (faster-whisper large-v3).
