# Reel: o que é dissociação

Público: quem vive. Função: alcance. Cerca de 40 s, 1080x1920.

Ângulo: definição didática com as três formas e quando procurar avaliação. A dissociação já saiu em 8 posts entre abril e setembro (espectador, olhar que trava, apagão, quieta na mesa). Em 01/11 ficou combinado que o tema só voltaria pelo ângulo de quando procurar avaliação. Por isso este Reel fecha nesse ponto.

## Vídeos

- Mesa (5ad959b6): 0 a 8 s sorriso que apaga e câmera recuando; 9 a 10 s vira silhueta; 11 a 15 s plano aberto, família rindo e ela pequena no fim do corredor. É o vídeo principal.
- Cama (0fe4cd07): 0 a 11 s o parceiro se afasta no escuro; corte em 11,3 s de volta ao close. Usar só a volta, no trecho do pé no chão.
- Os dois estão abaixo de 1080p (480p e 720p). Precisam de upscale antes da montagem.

## Fala (narração dele, um take só) e tela

| # | Tempo | Fala | Imagem | Texto na tela |
|---|---|---|---|---|
| 1 | 0 a 4 s | Você está rindo na mesa. E, de repente, tudo fica longe. | Mesa 0 a 4 s, cor | pequeno: você está rindo na mesa e, de repente, / grande: TUDO FICA LONGE. |
| 2 | 4 a 8 s | As vozes, o prato, o próprio corpo. Parece que você assiste de fora. | Mesa 4 a 8 s; a retícula cresce de baixo para cima | só legenda |
| 3 | 8 a 12 s | Isso tem nome: dissociação. A mente se desconecta do que está acontecendo. | Cartão coral, silhueta em retícula | DISSOCIAÇÃO / a mente se desconecta do que está acontecendo. |
| 4 | 12 a 15 s | Às vezes, o estranho é você. O corpo parece de outra pessoa. | Cartão creme, rosto em retícula | O CORPO PARECE DE OUTRA PESSOA. / despersonalização |
| 5 | 15 a 18 s | Às vezes, o estranho é o mundo. Tudo parece um cenário. | Sala em retícula, faixa coral | O MUNDO PARECE UM CENÁRIO. / desrealização |
| 6 | 18 a 21 s | E às vezes some um pedaço do seu dia. Você não lembra o que disse ou fez. | Cartão amarelo, só tipografia | SOME UM PEDAÇO DO SEU DIA. / lacuna de memória |
| 7 | 21 a 25 s | No borderline, aparece no estresse forte e passa. De fora, quase ninguém percebe. | Mesa 11 a 15 s, cor | DE FORA, QUASE NINGUÉM PERCEBE. |
| 8 | 25 a 30 s | Na hora, traga o corpo de volta. Pé no chão. Água fria nas mãos. Diga em voz alta onde você está. | Cama a partir de 11,3 s | 1 PÉ NO CHÃO / 2 ÁGUA FRIA NAS MÃOS / 3 DIGA ONDE ESTÁ |
| 9 | 30 a 36 s | Vale procurar avaliação se está ficando frequente, se você perde pedaços do dia, se já se machucou sem sentir, ou se nunca tinha acontecido antes. | Cartão creme | VALE AVALIAR SE + 4 itens |
| 10 | 36 a 40 s | Manda para quem você quer que entenda esse momento. | Cartão coral | MANDA PARA QUEM VOCÊ QUER QUE ENTENDA ESSE MOMENTO. |

## Sistema visual

- A regra que organiza tudo: com cor, você está presente. Com retícula, você saiu. A retícula entra no bloco 2 e só some no bloco 7, quando a família aparece em cor e ninguém nota.
- Paleta das referências: amarelo #F7E040, coral #EA6060, tinta #161412, creme #F2ECDF. Fundo liso, sem grão, porque a retícula já é a textura.
- Tipos: Anton em caixa alta para a frase grande; Inter Black para complemento e etiqueta do termo. O termo clínico entra pequeno, numa etiqueta com borda, sempre depois da experiência.
- Retícula: pontos a 45 graus, célula de 13 px, gerada pelo `retícula.py` a partir do próprio vídeo.
- Área segura medida por código em todos os quadros: 5% à esquerda, 12% à direita, 20% embaixo.
- Legenda automática: pequena, ao redor de 68% da altura, nos trechos de vídeo. Nos cartões o texto do cartão é a própria fala, sem legenda junto.

## Movimento (adaptado do TechHalla kinetic type bumper, do painel Motion)

Do modelo fica a técnica de cartaz de rua em movimento. Saem a paleta, o fundo preto e o ritmo de vinheta em loop.

1. Cada frase grande entra letra por letra, subindo com mola curta (atraso de 125 ms entre letras), no tempo da fala.
2. Desalinhamento de impressão: só nos quadros de impacto (DISSOCIAÇÃO, O CORPO, O MUNDO), uma cópia do texto em amarelo ou coral deslocada 3 a 5 px por 4 quadros, depois volta ao lugar.
3. Troca de cartão por máscara: a palavra que sai abre o buraco por onde entra o próximo cartão.
4. Câmera: só aproximação de 1,00 para 1,08 nos cartões e corte seco nos vídeos. Nada de deriva.
5. Retícula animada: no bloco 2 a célula cresce de 2 para 13 px em 1 s, de baixo para cima, com o vídeo ainda andando. No bloco 8 faz o caminho inverso no corte da cama.
6. SOME UM PEDAÇO DO SEU DIA: o fim da frase se desfaz em pontos enquanto ele fala.
7. Desfoque de movimento pela média de 4 instantes por quadro.
8. Som: whoosh baixo na entrada de cada cartão, clique seco no desalinhamento, biblioteca `memoria/sfx/`, final em -14 LUFS.

## Legenda do post

Você está na mesa, rindo, e de repente tudo fica longe. Isso tem nome: dissociação.

No borderline, ela costuma aparecer em estresse forte e passar. Quem está perto quase nunca percebe.

Se está ficando frequente, se você perde pedaços do dia ou se já se machucou sem sentir, vale procurar avaliação.

Manda para quem você quer que entenda esse momento.

Em risco imediato, ligue 188 (CVV) ou 192 (SAMU).

Conteúdo educativo. Não substitui avaliação.
