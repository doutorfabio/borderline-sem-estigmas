# Reel 30 s: O que o borderline faz antes da crise (7 sinais)

Template de origem: Orange dot motion system, de @ultimaxbt, em https://prompt-motion.com/ultimaxbt-bbebf5
Rodar no Claude com Opus 5.5 e esforço no máximo (recomendação do site).

## Prompt final

```
<inputs>
Do not ask me for anything. Every input is below. Do not wait for approval at any step.
Topic: a 30-second Instagram Reel for Dr. Fabio Schmidt, a Brazilian physician who explains borderline personality disorder without stigma. It is the video version of his carousel about the 7 signs that show up hours before a crisis. The viewer is someone who lives with a person who has borderline.
Accent color: red #CC0000.
Audio: none. I add the music in Instagram.
</inputs>

<direction>
A 2D motion design film in vertical 9:16. Near-black canvas #0D0D0D, bold cream typography #F2EADB, grey #8C8C8C for secondary lines, and one vivid red dot. The red dot is the person with borderline. It connects every scene and never leaves the screen: it starts as the full stop of the opening title, then acts out each of the 7 signs with its own behaviour while the type names the sign, and it ends as the full stop of the last sentence. Small cream dots are the people at home. Every movement must mean something: the dot shows the sign, it never decorates. Keep the motion sharp and controlled, with small spring overshoots and no dead time.
Type: Montserrat ExtraBold capitals for titles; Fraunces 900 Italic capitals for the one key word of each title, in cream, which the red dot underlines with a thick red stroke as it passes; Montserrat Medium for the one support line under each title. Red is used only for the dot and the strokes it draws. Never red letters.
Safe area: every letter and the dot stay inside x 7%–88% and y 14%–78% at all times, including entrances and exits. The right 12% and bottom 20% belong to the Instagram interface.
Banned: photos, people, faces, hands, phones, brains, neurons, pills, icons, emojis, stock footage, gradients, glows, particle bursts, glitch, corner brackets, timecodes, HUD marks, code-style labels, quotation marks, English words on screen, any text beyond the locked message, lines that begin with ele or ela, random transitions and motion that is not connected to an element already on screen.
</direction>

<message>
Locked. Brazilian Portuguese, exact spelling and accents. Do not translate, soften, add or remove words. [KEY] marks the key word of each title.
Open: O QUE O BORDERLINE FAZ / ANTES DA [CRISE]. then, large: 7 SINAIS
Counter label, small, same position in every sign: SINAL 1 DE 7 up to SINAL 7 DE 7
1. FICA [QUIETO] / DE REPENTE  ·  support: Por dentro, alerta máximo.
2. RESPOSTAS [CURTAS] / DEMAIS  ·  tiny replies next to the dot: Tô bem.  Tanto faz.  ·  support: Sobrecarga emocional.
3. EVITA [CONTATO] / VISUAL  ·  support: O corpo tentando não transbordar.
4. PEQUENAS [COISAS] / IRRITAM DEMAIS  ·  support: O copo no lugar errado.
5. SOME PRO [QUARTO]  ·  support: Ir atrás é o erro mais comum.
6. PARA DE [COMER] / OU COME DEMAIS  ·  support: Algo está errado por dentro.
7. DORME [MAL] / OU NÃO DORME  ·  support: Sem sono, qualquer gatilho vira crise.
Close: VOCÊ VIU ALGUM / DESSES [HOJE]?  then: RECONHECER O SINAL / ANTES MUDA TUDO.  then: MANDA PRA QUEM CONVIVE / COM BORDERLINE.
End lockup, small, cream: DR. FABIO SCHMIDT · MÉDICO · CRM-SP 183549
</message>

<structure>
Exactly 30.00 seconds on a 120 BPM grid (one beat = 0.5s), with a visual change on every beat.
0.0–3.0s  Open. The title slams in line by line. The full stop after CRISE is the red dot. It detaches, bounces once and a huge 7 SINAIS counts up from 1 to 7 behind it, one number per half beat.
3.0–6.0s  Sign 1. The dot has been pulsing on the beat. It stops dead and stays perfectly still while the letters keep settling around it; inside the stillness it trembles by one pixel, very fast.
6.0–9.0s  Sign 2. Long cream bars arrive from the left like questions. The dot answers each one with a very short dash. The tiny replies pop beside it. The bars keep coming, longer each time.
9.0–12.0s  Sign 3. A cream dot approaches and tries to line up with the red dot. Each time it gets level, the red dot slides away, like two magnets that repel. Then a thin ring appears around the red dot, holding it in as it swells slightly.
12.0–15.0s  Sign 4. A small cream square moves four pixels out of place. The red dot reacts far too much: it jolts, grows and shakes every letter on screen, then snaps back.
15.0–18.0s  Sign 5. A cream rectangle opens like a door. The dot goes in and the door shuts, leaving only a thin red line of light under it. The cream dot starts toward the door and stops halfway.
18.0–21.0s  Sign 6. A row of small cream circles passes like plates. The dot lets all of them go by untouched. Then a second row passes and it swallows every one, growing with each.
21.0–24.0s  Sign 7. The canvas dims while a clock hand sweeps one full turn. Every cream dot fades to grey, asleep. The red dot stays lit and flickers.
24.0–30.0s  Close. The seven behaviours shrink into a row of seven small red marks under VOCÊ VIU ALGUM DESSES HOJE? The next two sentences replace it one at a time. The red dot lands as the full stop after BORDERLINE. The lockup line fades in. Hold the last 1.5s perfectly still.
In every sign: the counter label ticks up, a giant numeral sits at 8% opacity on the right, the title lands first, the dot underlines the key word, the support line appears in the last beat.
</structure>

<build>
1. One HTML file, 1080x1920 at 30fps. Compute every visual from time inside seek(t): no CSS transitions, timers or state carried between frames.
2. Use closed-form springs for every landing, jolt and door. A value that changes target many times is the sum of one spring per change.
3. Give the red dot one continuous route through all nine scenes. It never teleports and never disappears, except behind the door in sign 5, where its light stays visible.
4. Animate titles per line and the key word on its own timing. Outgoing and incoming text get separate timing so letters never overlap.
5. Motion blur: 4 subframes per frame, blended.
6. Render one still per scene (9 stills) for yourself. Fix anything cramped, any short word left alone on a line, low contrast, wrong accents or anything outside the safe area. Then render the full film.
7. Export an MP4: H.264, 1080x1920, 30fps, no audio. Give me the MP4 and the HTML file.
</build>

<gotchas>
The red must stay the same red in every scene and appear on nothing but the dot and its strokes. When the dot shakes the type in sign 4, the letters must return to exactly where they were. The support line must be readable for at least one full second. Portuguese accents must render: Tô, alerta máximo, não, está, é, VOCÊ. Do not let the giant numeral compete with the title.
</gotchas>

<start>
Build it now. Do not ask questions.
</start>
```

## O que mudou em relação ao carrossel

- Cada sinal ficou com o título e uma linha de apoio, para caber em 30 s (93 palavras no total).
- Saíram as frases em não é X, é Y (Não é calma. É o sistema nervoso...; Não é grosseria; Não é hábito; Não é descaso).
- Saíram sistema nervoso e cérebro, pela regra de não usar neurobiologia.
- Saíram as aspas e o travessão.
- Saiu 2 dias seguidos, prepare-se: é um número sem fonte.
- Saiu Comenta qual sinal, para não pedir relato de crise nos comentários.
- Vermelho só no ponto e no traço que ele desenha; a palavra-chave fica em creme, itálica.
