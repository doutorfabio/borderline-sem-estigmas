# Reel Todo o amor da casa não preenche o vazio do borderline: prompt de 20 s

Origem: carrossel de 24/10/2026 (103 mil views). Template: Paper-style product launch film, de @ik_builds (prompt-motion.com/ik-builds-b8bdcf). Função: alcance. Chamada: envio.

Ficaram de fora, por tempo de leitura: slide do sofá, a tira de fotos (o texto do slide 2 ficou), a lista de três itens e a linha o vazio existe mesmo com todo esse amor.

```
Crie um filme de motion graphics de 20,0 s. HyperFrames + GSAP, sem narração, sem filmagem, sem foto, sem rosto.
Formato: 1080x1920 (9:16), 30 fps, MP4. Sem áudio (a trilha entra depois).
Estilo: folha de papel claro, corações de papel recortado com física real, linha de canetão que se desenha na hora, tipografia cinética enorme, trocas secas entre claro e escuro, uma ideia nova a cada 1,5 a 2 s.

ASSUNTO
Vídeo educativo do Dr. Fabio Schmidt (@drfabioschmidt) para quem convive com alguém com borderline. Ideia única: o amor da família é real e chega, mas não fica guardado; por isso o vazio continua, e isso se cuida com tratamento. Não é anúncio. Não acrescente nenhuma frase.

OBJETO CONDUTOR
Corações de papel vermelho recortado, desenhados em código (SVG), com uma dobra leve no meio e sombra curta. Eles obedecem à gravidade em todas as cenas. Nunca enchem nada: atravessam, escorregam, caem. Cor chapada, borda nítida, sem textura estranha, sem brilho.

TEXTO TRAVADO (exatamente estas palavras, nesta ordem, com estas quebras de linha; nada além disso aparece na tela)

Cena 1, 0,0 a 3,4 s, papel claro.
TODO O AMOR DA CASA
NÃO PREENCHE O
VAZIO
DO BORDERLINE
VAZIO é a maior palavra do quadro, só em contorno preto, sem preenchimento, ocupando quase toda a largura segura. As outras linhas em preto cheio. A partir de 0,3 s os corações caem do topo em fila, entram na palavra VAZIO, passam por dentro das letras sem parar e saem por baixo, formando um monte no chão, entre VAZIO e DO BORDERLINE. A palavra continua vazia até o fim da cena. No canto de baixo, pequeno: @drfabioschmidt

Cena 2, 3,4 a 6,6 s.
De 3,4 a 4,7 s, papel claro, tipo grande:
A TARDE
FOI BOA.
Em 4,7 s, troca seca para escuro. Linha pequena em serifa itálica: à noite,
E o tipo grande, em vermelho:
PARECIA QUE NUNCA
TINHA ACONTECIDO.
Na troca para o escuro, os corações que ainda estavam no quadro caem para fora.

Cena 3, 6,6 a 9,4 s, escuro.
Linha pequena em serifa itálica: sente de verdade, às vezes demais.
Tipo grande, primeira linha em papel, segunda em vermelho:
QUANDO ACABA,
NÃO SOBRA NADA.
Um único coração fica pousado no canto de baixo à direita. Quando NÃO SOBRA NADA assenta, ele escorrega e cai para fora do quadro.

Cena 4, 9,4 a 14,0 s, troca seca para papel claro.
Título:
UM DIA BOM, EM GRÁFICO.
O canetão preto desenha os dois eixos. O canetão vermelho desenha a linha subindo da esquerda para a direita e, no caminho, pousa três corações sobre ela, cada um com sua palavra em serifa itálica: riu, depois conversou, depois ficou bem. Em 12,0 s a linha despenca na vertical até o zero e segue reta no chão; os três corações soltam da linha e caem. Embaixo do ponto da queda, em tipo condensado pequeno: FECHOU A PORTA
Em 12,8 s entra, em serifa itálica, centralizada: o que foi sentido não fica guardado.

Cena 5, 14,0 a 17,2 s, papel claro.
Tipo grande, em preto:
SEU AMOR
NÃO ESTÁ FALHANDO.
Em 15,4 s, tipo grande, em vermelho:
O VAZIO SE CUIDA
COM TRATAMENTO.
Quatro corações pousam no canto de baixo à direita e ficam parados. É a única cena em que eles ficam.

Cena 6, 17,2 a 20,0 s, papel claro.
Tipo grande, duas linhas em preto e a última em vermelho:
MANDE PARA QUEM
ACHA QUE NÃO AMOU
O BASTANTE.
Uma fila de corações cai pela margem direita, dentro da área segura, e forma um monte pequeno embaixo. Pequeno, à esquerda, embaixo: @drfabioschmidt
De 19,0 a 20,0 s nada se move.

REGRAS
- Nada de interface de player (barra, tempo, fps, cabeçalho). Nenhum termo de animador na tela. Nenhuma moldura de canto, etiqueta ou rótulo decorativo.
- Nenhuma frase entre aspas. Sem travessão. Sem emoji. Sem logotipo.
- Sem cérebro, sem pessoa, sem casa desenhada, sem sofá, sem foto.
- Nenhuma palavra curta sozinha numa linha, fora VAZIO na capa. Use as quebras de linha dadas.
- Área segura: todo texto e todo monte de corações, inclusive durante as entradas animadas, fica a pelo menos 5% da borda esquerda, 12% da borda direita, 8% do topo e 20% da base. Meça por código em cada cena.
- Cada tela de tipo grande fica legível, parada, por pelo menos 0,9 s.

ACABAMENTO
- Cores: papel #F4F0E6, tinta #0D0D0D, vermelho #B3261E. Modo escuro: fundo #0D0D0D com texto #F4F0E6 e vermelho #CC2A22. Cor chapada, sem degradê; grão de papel bem fino só no modo claro.
- Fontes: Anton para o tipo grande, em caixa alta; Source Serif 4 itálica para as linhas pequenas e as palavras do gráfico; Montserrat 600 para o @.
- Linhas do gráfico desenhadas com stroke-dashoffset, com traço de canetão levemente irregular.
- Física: gravidade, colisão e atrito reais nos corações, calculados de forma determinística a partir do tempo (mesmo resultado em qualquer seek). Squash e stretch leve na queda, follow-through nas palavras.
- Consulte o registro do HyperFrames antes de criar componente do zero. Todo estado inicial definido em t=0 (seek-safe). Nunca cobrir uma saída. Um movimento principal por transição; nada de push, slide ou giro genérico.

COMEÇO
Mostre o storyboard com os tempos e um quadro de conferência por cena. Depois renderize sem me perguntar mais nada e entregue o MP4 final em 1080x1920.
```
