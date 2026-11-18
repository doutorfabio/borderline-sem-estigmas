# Áudio do Reel Lugar mais seguro

- `A_Warm_Resolve.m4a`: música do Suno (prompt em `../prompts-suno.txt`). 64,9 s, 120 BPM medidos, primeira nota em 0,17 s, final desacelerando com acorde em 61,5 s.
- `Dry_Foley_Sequence.m4a` e `Eight_Foley_Sounds.m4a`: efeitos do Suno. Vieram curtos (5,9 s e 4,3 s) e sem os oito sons separados. Foram cortados pelo formato do som, sem escuta: batida seca (porta), clique agudo (trinco e alfinete), ruídos curtos (pincel), riscos (checks e sublinhados), cliques leves (teclas).
- O estalo das trocas de ícone e a gota da lágrima são o `pop.mp3` da biblioteca aprovada (`.claude/skills/media-use/audio/assets/sfx/`).

Montagem em `../src/mix_audio.py`: música do zero até 20,0 s, emenda de 60 ms no compasso para o trecho final da música (acorde final em 33,3 s, quando a imagem para), efeitos sem grave (passa-altas em 115 Hz), mix em -14,0 LUFS e pico de -1,9 dBFS.
