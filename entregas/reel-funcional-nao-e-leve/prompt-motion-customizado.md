# Reel 30 s: Borderline funcional não é borderline leve

Template de origem: TechHalla kinetic type bumper, de @techhalla, em https://prompt-motion.com/techhalla-90b8ec
Rodar no Claude com Opus 5.5 e esforço no máximo (recomendação do site).

## Prompt final

```
You are a world-class motion designer making a 30.00s kinetic typography Reel for Dr. Fabio Schmidt, a Brazilian physician who explains borderline personality disorder without stigma. It is the video version of his most shared carousel. It must feel like the best designer in the room made a street poster that moves: sober, heavy, precise. Showreel stakes: if this is weak, you don't get hired.

DURATION: exactly 30.00 seconds. Not a loop: it ends on a held lockup.
FORMAT: one HTML file, 1080×1920 (vertical 9:16, Instagram Reel), 30fps. When it is done, also render it to MP4 (H.264, 1080×1920, 30fps, no audio).
SAFE AREA: every letter stays inside x 7%–88% and y 14%–78% of the frame at all times, including during entrances and exits. The right 12% and the bottom 20% belong to the Instagram interface.

PALETTE (strict):
- bg #0D0D0D
- cream #F2EADB for all readable type
- grey #8C8C8C for lines that have already been read
- red #CC0000 only as a solid block behind one word per beat (the word on it stays cream). Never red letters on the dark background.
No other hues. No gradients.

TYPE SYSTEM:
1) Display: Montserrat ExtraBold or Black, capitals, tracking -20. 1 to 4 words per line.
2) Emphasis: Fraunces 900 Italic, capitals, only for the single word that sits on the red block in each beat.
3) Quiet line: Montserrat Medium, sentence case, only where marked (quiet).
Optical kerning. Never one font for everything. No script fonts, no monospace.

MESSAGE (locked, Brazilian Portuguese, exact spelling and accents; do not translate, soften, add or remove words; no quotation marks anywhere). [RED] marks the word on the red block.
1. BORDERLINE FUNCIONAL / NÃO É / BORDERLINE [LEVE]
2. TRABALHA. / PAGA AS CONTAS. / RESPONDE MENSAGENS. / SORRI NO ALMOÇO. / E [CHORA] NO CARRO / ANTES DE ENTRAR EM CASA.
3. O MUNDO VÊ ALGUÉM / QUE [FUNCIONA]. / POR DENTRO, TUDO / ESTÁ DESMORONANDO.
4. A DOR [NÃO] É MENOR. / A PESSOA APRENDEU / A ESCONDER MELHOR.
5. VERGONHA [DOBRADA]. / QUANDO FINALMENTE / PEDE AJUDA, OUVE: / (quiet) Mas você parece tão bem. / E VOLTA A SE CALAR.
6. O SOFRIMENTO / QUE NÃO APARECE / NÃO RECEBE [NOME].
7. FUNCIONAR NÃO É / O OPOSTO [DE SOFRER].
8. PARECER BEM / NÃO É [ESTAR BEM]. / MANDA PRA QUEM / PRECISA SABER.
End lockup, small, cream: DR. FABIO SCHMIDT · MÉDICO · CRM-SP 183549

NARRATIVE ARC (30s, 120 BPM, one beat = 0.5s, downbeat at t=0):
0.0–3.0s  HOOK. BORDERLINE FUNCIONAL slams in from below with spring overshoot. NÃO É punches in alone, huge, for one beat. BORDERLINE LEVE lands; the red block wipes in behind LEVE from left to right.
3.0–8.5s  THE LIST. The four short lines hit one per 1.5 beats, stacking downward; each new line pushes the previous ones up and turns them grey. Hard stop of one beat on black. Then E CHORA NO CARRO / ANTES DE ENTRAR EM CASA. arrives slower and larger; red block behind CHORA.
8.5–12.5s  O MUNDO VÊ ALGUÉM QUE FUNCIONA. locks to a poster grid, perfectly still and tidy. Then the grid breaks: the letters of that line sag and slide a few pixels out of alignment while POR DENTRO, TUDO ESTÁ DESMORONANDO. is revealed through a mask made from the outgoing letterforms.
12.5–16.0s  A DOR NÃO É MENOR. slams; red block behind NÃO. A PESSOA APRENDEU A ESCONDER MELHOR. enters and the word ESCONDER slides halfway behind a solid bg-coloured bar, half hidden but still legible.
16.0–21.0s  VERGONHA DOBRADA. the word DOBRADA folds: it duplicates and the copy drops under it like a folded sheet, red block behind the top one. QUANDO FINALMENTE PEDE AJUDA, OUVE: stacks fast. The quiet line types on, small and light. Then a cream bar closes over the whole screen from top and bottom like a mouth shutting, leaving only E VOLTA A SE CALAR. in the slit, tracking tightening to nothing.
21.0–24.0s  O SOFRIMENTO QUE NÃO APARECE starts at 12% opacity, almost invisible, and only NÃO RECEBE NOME. comes to full cream; red block behind NOME.
24.0–26.5s  FUNCIONAR NÃO É O OPOSTO DE SOFRER. one line per beat, horizontal smash-pan between the two lines; red block behind DE SOFRER.
26.5–30.0s  CLOSE. PARECER BEM NÃO É ESTAR BEM. centers; red block behind ESTAR BEM. MANDA PRA QUEM PRECISA SABER. rises under it. The lockup line fades in below. Hold the last 1.5s perfectly still.

CONCRETE TECHNIQUES (required, implement, don't approximate):
1. seek(t) is a pure function of time. No CSS transitions, no setInterval, no state across frames.
2. Springs are closed-form step responses, one spring per target change.
3. Kinetic type: per-line or per-word spring (y, opacity, blur). Stagger 125ms.
4. Mask reveal in beat 3: the incoming text is revealed by a path mask derived from the outgoing line's outlines.
5. Camera: one orthographic camera; only punch-in (1.0→1.06) and horizontal smash-pans on beats. No drift.
6. Motion blur: 4 subframes per frame, blended.
7. Something lands on every beat for the first 6 seconds; after that, at least every other beat.
8. Pre-pass: export one still per beat block (8 frames) before the full render. Fix cramped type, orphan short words alone on a line, low contrast and anything outside the safe area. Then render.

BANNED:
Corner brackets, frame marks, timecodes, HUD elements, small labels or code-style crumbs, anything that reads as AI-made. Photos, people, faces, hands, phones, brains, neurons, pills, icons, emojis, particles, glitch, gradients, bouncy cartoon easing. Quotation marks. English words on screen. Any text beyond the locked message. Lines that begin with ele or ela. Red letters on the dark background.
```

## Campos do Customize do site (se preferir usar o formulário)

O formulário só acrescenta um bloco no fim e mantém as frases do TechHalla travadas no prompt, por isso o prompt final acima é o caminho melhor.

- What it's for: Reel de 30 s em português do Brasil, versão em vídeo do carrossel Borderline funcional não é borderline leve, do Dr. Fabio Schmidt (médico)
- Format: 1080×1920 · Vertical 9:16
- Length (seconds): 30
- Colours: #0D0D0D, #F2EADB, #CC0000
- Typeface: Montserrat
- Anything else: colar o bloco MESSAGE e o bloco BANNED do prompt final

## O que mudou em relação ao carrossel

- Saiu o Ela do começo da lista (Trabalha. Paga as contas.), pela regra de não começar frase com ele ou ela.
- Saíram as aspas de FUNCIONA e de Mas você parece tão bem.
- Saiu a linha É borderline sofrendo onde ninguém vê, que junto do título formava não é X, é Y.
- Os slides 6, 7 e 8 ficaram só com a frase principal, para caber em 30 s (86 palavras no total).
- Palavra de destaque em creme sobre faixa vermelha, pela regra de 16/11 (vermelho como letra some no fundo escuro).
