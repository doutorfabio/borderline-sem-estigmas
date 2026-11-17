# Reel 30 s: O que o borderline faz antes da crise (7 sinais)

Template de origem: Swiss-style motion showreel, de @levabashidze, em https://prompt-motion.com/levabashidze-2d713a
(O prompt dele no site é uma linha genérica; o prompt abaixo descreve o visual do vídeo dele e põe o texto do carrossel.)
Rodar no Claude com Opus 5.5 e esforço no máximo (recomendação do site).
Descartado por ele em 17/11: Orange dot motion system (ponto colorido que atravessa as cenas).

## Prompt final

```
You are a world-class motion designer. Make a 30.00-second kinetic typography Reel in Swiss poster style for Dr. Fabio Schmidt, a Brazilian physician who explains borderline personality disorder without stigma. It is the video version of his carousel about the 7 signs that show up hours before a crisis. The viewer lives with someone who has borderline. It must be instantly clear, loud and precise: a numbered list where every sign is a poster that moves. Do not ask me anything. Do not wait for approval. Build it.

FORMAT: one HTML file, 1080x1920 (vertical 9:16, Instagram Reel), 30fps, exactly 30.00s, no audio. When it is done, render an MP4 (H.264, 1080x1920, 30fps) and give me the MP4 and the HTML.
SAFE AREA: all text stays inside x 7%–88% and y 14%–78% at all times, including entrances and exits. The right 12% and bottom 20% belong to the Instagram interface.

STYLE (Swiss poster that moves):
- Full-bleed flat backgrounds that flip on the beat between three colours only: black #0D0D0D, cream #F2EADB, red #CC0000. No other hues, no gradients.
- Type: Montserrat ExtraBold or Black capitals for titles, tight tracking, set on a strict grid, flush left. One key word per title in Fraunces 900 Italic. Support line in Montserrat SemiBold, sentence case.
- Colour of type by background. On black: cream type, key word cream on a solid red block. On cream: black type, key word red. On red: black type, key word cream.
- Chapter system, same position in every sign: a small counter label at the top left of the safe area (SINAL 1 DE 7 ... SINAL 7 DE 7) and a thin progress bar with 7 segments under it; one more segment fills at each sign.
- A giant chapter numeral (1 to 7) at 8% opacity on the right side, behind the type.
- Transitions: hard background flips, horizontal smash-pans and a ticker band of repeated bold text. Nothing fades slowly.

MESSAGE (locked, Brazilian Portuguese, exact spelling and accents; do not translate, soften, add or remove words; no quotation marks). [KEY] marks the key word.
Open: O QUE O BORDERLINE FAZ / ANTES DA [CRISE]  then, huge: 7 SINAIS
1. FICA [QUIETO] / DE REPENTE  ·  support: Por dentro, alerta máximo.
2. RESPOSTAS [CURTAS] / DEMAIS  ·  two tiny replies: Tô bem.  Tanto faz.  ·  support: Sobrecarga emocional.
3. EVITA [CONTATO] / VISUAL  ·  support: O corpo tentando não transbordar.
4. PEQUENAS [COISAS] / IRRITAM DEMAIS  ·  support: O copo no lugar errado.
5. SOME PRO [QUARTO]  ·  support: Ir atrás é o erro mais comum.
6. PARA DE [COMER] / OU COME DEMAIS  ·  support: Algo está errado por dentro.
7. DORME [MAL] / OU NÃO DORME  ·  support: Sem sono, qualquer gatilho vira crise.
Close: VOCÊ VIU ALGUM / DESSES [HOJE]?  then: RECONHECER O SINAL / ANTES MUDA TUDO.  then: MANDA PRA QUEM CONVIVE / COM BORDERLINE.
End lockup, small: DR. FABIO SCHMIDT · MÉDICO · CRM-SP 183549

TIMELINE (120 BPM, one beat = 0.5s, something changes on every beat):
0.0–3.0s  OPEN, black. The title slams in line by line from below with spring overshoot; red block wipes in behind CRISE. Then 7 SINAIS fills the frame while the numeral counts 1 to 7, one number per half beat.
3.0–6.0s  SIGN 1, black. The title arrives shaking and loud, then freezes dead still for one full beat: nothing on screen moves.
6.0–9.0s  SIGN 2, cream. The title lands, then gets cropped shorter from the right on each beat, as if cut off. The two tiny replies pop in, small, under it.
9.0–12.0s  SIGN 3, red. The two title lines slide in opposite directions and never line up; the key word turns away from the viewer and comes back.
12.0–15.0s  SIGN 4, black. PEQUENAS COISAS is set very small. IRRITAM DEMAIS slams in enormous and shakes the whole frame, then settles.
15.0–18.0s  SIGN 5, cream. The word SOME slides behind a solid black vertical panel, like a door closing, and stays hidden; PRO QUARTO remains.
18.0–21.0s  SIGN 6, red. The first line squeezes thin and small. The second line swells extra wide and heavy until it almost touches the safe-area edges.
21.0–24.0s  SIGN 7, black. The background dims further. The title flickers like a lamp that will not switch off while a thin cream clock hand sweeps one full turn behind it.
24.0–30.0s  CLOSE, cream. One beat: a ticker band of the seven titles runs across in stacked rows, one row red. Then VOCÊ VIU ALGUM DESSES HOJE? lands. Then RECONHECER O SINAL ANTES MUDA TUDO. replaces it. Then MANDA PRA QUEM CONVIVE COM BORDERLINE. with the lockup line under it. Hold the last 1.5s perfectly still.
In every sign: the background flips on the downbeat, the counter and progress bar update, the title lands in the first second, the motion idea plays in the second, the support line is on screen for the whole last second.

BUILD:
1. Compute every visual from time inside seek(t). No CSS transitions, timers or state carried between frames.
2. Springs are closed-form step responses; one spring per target change.
3. Animate titles per line or per word, with separate timing for outgoing and incoming text so letters never overlap.
4. Motion blur: 4 subframes per frame, blended.
5. Before the full render, export one still per scene (9 stills) for yourself. Fix cramped type, any short word left alone on a line, weak contrast, wrong accents and anything outside the safe area. Then render.

BANNED: photos, people, faces, hands, phones, brains, neurons, pills, icons, emojis, particles, glows, gradients, glitch, 3D objects, corner brackets, frame marks, timecodes, HUD marks, code-style labels, anything that reads as AI-made. Quotation marks. English words on screen. Any text beyond the locked message. Lines that begin with ele or ela. Red letters on the black background.
```

## O que mudou em relação ao carrossel

- Cada sinal ficou com o título e uma linha de apoio, para caber em 30 s (93 palavras no total).
- Saíram as frases em não é X, é Y (Não é calma. É o sistema nervoso...; Não é grosseria; Não é hábito; Não é descaso).
- Saíram sistema nervoso e cérebro, pela regra de não usar neurobiologia.
- Saíram as aspas e o travessão.
- Saiu 2 dias seguidos, prepare-se: é um número sem fonte.
- Saiu Comenta qual sinal, para não pedir relato de crise nos comentários.
