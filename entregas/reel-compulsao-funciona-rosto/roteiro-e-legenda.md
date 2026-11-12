# Reel: Borderline, a compulsão funciona. Por isso repete. (versão com o rosto dele)

12/11/2026. 13,8 s, 1080x1920, 30 fps. Ele aparece na abertura e no fecho; o meio é colagem com texto na tela, sem voz. Função: alcance.

- Clipe dele: Higgsfield, job 87d4c85f-7c04-419b-aeb4-e45db7c6d6e0 (vertical, 480x854, fundo trocado por parede escura). Não está no repositório.
- Abertura (0 a 2,6 s do clipe): A compulsão no borderline funciona.
- Meio (texto, sem voz): Comer, comprar, beber: o alívio vem na hora e dura minutos. A culpa chega depois e fica. A dor volta maior e pede alívio de novo.
- Fecho (segunda tomada, 6,95 a 9,05 s do clipe): Esse ciclo tem tratamento.
- Envio: MANDA PRA QUEM VOCÊ QUER QUE ENTENDA ESSE CICLO.

Para refazer os quadros do clipe: `ffmpeg -ss 0 -t 3.2 -i clipe.mp4 -vf "crop=480:600:0:40,scale=704:880:flags=lanczos,unsharp=5:5:0.5,fps=30" assets/fa/%03d.jpg` e o mesmo com `-ss 6.95 -t 2.1` em `assets/fb/`.

Legenda do post: a mesma de `reel-compulsao-funciona/roteiro-e-legenda.md`.
