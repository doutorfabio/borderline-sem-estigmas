# Base das colagens curtas (12/11/2026)

Molde aprovado por ele em 12/11 ("Crie mais outros assim de outros temas"): frase fixa com BORDERLINE em vermelho, recorte de colagem, cartão de papel com gráfico ou tabela, ícone de colagem dele como quem fala, legenda de até 3 palavras, envio no fim. Até 15 s.

Cada peça fica numa pasta irmã com `comp.html`, `words.json` (se narrada), `sfx.json` e `assets/`.

1. Narração em take único (seed_audio, voz Fabio). `python3 prep_voz.py take.wav palavras.json <peca> 0.3` encurta pausas no mesmo take e remapeia a legenda.
2. `node render.js <peca> <saida> stills|all <duracao>` (Playwright). Confere por código a área segura: 5% laterais, 12% à direita, 20% embaixo.
3. `python3 audio.py <peca> <duracao> mix.wav`: efeitos de `memoria/sfx/editorpro` a -27 dBFS, voz na frente, -14 LUFS.
4. ffmpeg junta quadros e áudio em 1080x1920, 30 fps.

Recortes: GPT Image 2.6 em fundo verde chapado. Se o fundo vier de outra cor, usar remove_background e refazer a borda de papel.
