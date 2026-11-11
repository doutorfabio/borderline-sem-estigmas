# Padrão de efeitos — @drfabioschmidt

Este é o **único** padrão de efeitos de edição em uso. Ele foi extraído do vídeo
final aprovado "borderline x psicopata"
(Drive: `1p02HetQbymlbG4HTG4BI4FsHR8EGMN70`, versão corrigida:
`1aRD09eZDC-U7QVYuqpIhLzmN1fg_wIFs`).
Nenhum outro preset ou efeito deve ser usado sem pedido explícito.

## Formato
- Vertical 9:16, mesma resolução e fps do arquivo gravado.
- Duração definida pelo roteiro. Não cortar fala quando o pedido for "não mudar o tamanho".

## Cortes e zoom
- Cortes secos, sempre em cima dos cortes que já existem na gravação. Nunca deixar
  fragmento menor que ~1 s entre dois cortes ("retalho").
- Zoom punch leve (de 1,05× a 1,16×) aplicado a um trecho inteiro entre dois cortes,
  nas frases de impacto. O enquadramento fica um pouco acima do centro, para manter o rosto.

## B-roll
- Entra **por cima** da imagem, e a fala continua por baixo. O áudio do b-roll vai mudo.
- Cada inserção usa **uma única cena** do clipe, sem atravessar os cortes internos
  do b-roll gerado.
- Clima cinematográfico escuro e quente, com leve redução de saturação.
- Se o b-roll for mais lento que o vídeo (24 fps → 30 fps), recriar os quadros
  intermediários para o movimento não trepidar.

## Textos na tela
- **Gancho:** 2 ou 3 linhas em CAIXA ALTA, branco, negrito (Montserrat ExtraBold),
  com sombra leve, no terço superior. As linhas aparecem juntas.
  Exemplo: `FEZ ALGUÉM CHORAR. / FOI PESQUISAR / SE ERA PSICOPATA.`
- **Sobre b-roll:** palavra-chave grande em CAIXA ALTA no centro, com complemento
  pequeno logo abaixo. Exemplos: `TRAVA` + `por sentir demais`;
  `tentando` / `não` / `DESMONTAR`.
- Frase de impacto sobre o rosto vai no terço superior, nunca em cima da boca
  ou do microfone.
- Nada nos 20% de baixo nem na lateral direita (área dos botões do Instagram).

## Transições
- Flash branco curto (~0,1 s) na abertura e na saída do primeiro b-roll.
- Fade para preto curto no último ~0,1 s do vídeo.
- **Não usar** quadros pretos dentro do vídeo. No original, eles eram um erro e
  foram removidos na versão corrigida.

## Som
- Biblioteca padrão de efeitos: `memoria/sfx/` (pacote EditorPro dele, 07/11). Usar esses arquivos sempre que houver necessidade; ver `memoria/sfx/README.md`.
- Whoosh curto e baixo (0,22 s, pico em −27 dBFS) na entrada de cada b-roll.
- Clique seco e baixo (12 ms, pico em −26 dBFS) nos zooms.
- Sem graves ("boom") nem efeitos chamativos.
- Volume final normalizado em **−14 LUFS**, pico ≤ −1 dBFS.

## Checagem antes de entregar
1. Conferir quadro a quadro que não há quadros pretos ou brancos indesejados.
2. Conferir que nenhum trecho entre cortes tem menos de ~1 s.
3. Medir o volume (−14 LUFS).
4. Ler cada texto na tela: ortografia, posição e se não cobre o rosto.
