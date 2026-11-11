# Leitura dos dados: posts-180d.psv

## Origem e período

- Conta: @drfabioschmidt (Instagram, id 17841401503370732), conector `instagram` do Windsor.
- Período: publicações de 2026-04-13 a 2026-10-12. Coleta em 2026-10-13 (posts de 09 a 12/10 atualizados nessa data).
- 364 publicações: 239 Reels, 122 carrosséis, 3 imagens. Cada conteúdo aparece uma vez. Reenvios do mesmo conteúdo ficam no campo `flags` como `cop=`.
- Excluídos: dois posts de teste (legenda "FABIO", 3 views; Reel "Em 1960...", 1 view).

## Colunas

| Coluna | O que é | Natureza |
|---|---|---|
| data | Dia da publicação (UTC) | fato do Instagram |
| fmt | R = Reel, C = carrossel, I = imagem | fato do Instagram |
| codigo | Código do post. Reel: instagram.com/reel/CODIGO. Carrossel e imagem: instagram.com/p/CODIGO | fato do Instagram |
| views | Visualizações do post | fato do Instagram |
| alcance | Contas únicas alcançadas | fato do Instagram |
| compart | Compartilhamentos | fato do Instagram |
| salvos | Salvamentos | fato do Instagram |
| curtidas | Curtidas (total, como no app) | fato do Instagram |
| coment | Comentários (total, como no app) | fato do Instagram |
| ret_ms | Tempo médio assistido do Reel, em milissegundos. Vazio fora de Reels | fato do Instagram |
| skip3s | Fração das visualizações do Reel em que a pessoa saiu nos 3 primeiros segundos (0.5 = 50%). Vazio fora de Reels | fato do Instagram |
| cta | Chamada na legenda: C = pede COMEÇAR, GUIA ou EMPEZAR; P = oferta direta (Protocolo 7 Dias, livro, treinamento, materiais na bio); N = qualquer outra | leitura minha da legenda |
| eixo | Tema principal da legenda (códigos abaixo) | hipótese editorial |
| flags | Avisos (códigos abaixo) | leitura minha da legenda |
| tese | A explicação central da legenda, em uma linha | hipótese editorial |

`eixo` e `tese` vêm da legenda. Em Reels, a fala e a imagem podem dizer outra coisa. Em carrosséis, o texto dos slides não foi lido. Confirme no post pelo link antes de afirmar que dois conteúdos são a mesma tese.

## Eixos

AB abandono: medo de perder, sumiço, bloqueio, teste do vínculo.
AF alto funcionamento: competência aparente, máscara, desabar em casa.
DI dissociação.
CM manejo da crise por quem convive: o que fazer e dizer.
CV culpa e vergonha, em especial depois da crise.
ID identidade: espelho, não saber quem é.
IN invalidação e frases que machucam.
RO rótulo, estigma, diagnóstico, manipulação, narcisismo.
DD diagnóstico diferencial e comorbidade.
AL autolesão e ideação.
RE relacionamento: ciúme, parceiro, pessoa favorita, sexo.
IM impulsividade, explosão, regulação, corpo na crise.
VA vazio, anedonia, solidão.
IF infância, família de origem, ciclo geracional.
OF oferta direta (Protocolo 7 Dias, livro).
FT fora do tema, humor, medicação geral, conteúdo para outros médicos, aviso, sem texto.

Um eixo por publicação. É uma etiqueta para varrer o arquivo, não uma lista de temas permitidos ou proibidos.

## Flags

- `cop=CODIGO:VIEWS`: o mesmo conteúdo foi publicado de novo. Mostra o código e as views da cópia. Várias cópias vêm separadas por `&`.
- `neuro`: a legenda usa neurobiologia (regiões do cérebro, hormônios, nervo vago).
- `dado`: a legenda afirma número, estudo ou estatística. A fonte não foi verificada. Não reutilize sem fonte.
- `anedota`: a legenda conta caso, paciente ou relato em primeira pessoa. Origem não confirmada. Não reutilize como fato.
- `terceiro`: reação a vídeo ou cena de outra pessoa.
- `colab`: menção ou parceria com outro perfil.
- `linehan`: cita Linehan (1993). Confirmar a referência antes de repetir.
- `anomalia`: dado inconsistente no Instagram (alcance maior que views em DZfv2ivFB6W).
- "(legenda genérica)" no fim da tese: legenda curta, sem situação concreta. Leitura minha, não um julgamento sobre o vídeo.

## Limites

1. Retenção: `ret_ms` é tempo absoluto. A duração dos Reels não foi coletada, então não dá para calcular percentual assistido nem comparar vídeos de durações diferentes. Carrosséis não têm retenção.
2. Alcance, views, compartilhamentos, salvamentos e retenção são métricas diferentes. Não funda uma na outra.
3. Posts dos últimos 7 dias do arquivo ainda acumulam números.
4. Reenvios do mesmo conteúdo têm alcance muito diferente entre si no arquivo. Os dados não dizem por quê.
5. Não há dados de seguidores ganhos por post, horário, duração, fonte do tráfego ou comentários individuais.
6. Menos de 30 publicações por tese ou por eixo é amostra pequena. Não deduza causa.
7. Legendas antigas não comprovam o que afirmam e nem sempre seguem a voz atual (há emoji, travessão, hashtags, neurobiologia, termos como "psiquiatra"). Não copie a forma sem checar as regras.

## Como atualizar o arquivo

1. `get_data` do conector `instagram`, conta 17841401503370732.
2. Campos de conteúdo: `timestamp, media_id, media_type, media_permalink, media_caption, media_views, media_reach, media_shares, media_saved, media_total_like_count, media_total_comments_count`.
3. Campos de retenção, em chamada separada: `media_permalink, media_reel_avg_watch_time, media_reel_skip_rate`.
4. Use janelas de 14 dias. Janelas de 60 dias deram timeout. A de 14 dias respondeu bem, em até seis chamadas paralelas.
5. Cruze retenção e conteúdo pelo `media_permalink`.
6. Agrupe reenvios (mesma legenda em minutos de diferença). Fique com o de mais views como linha principal e registre os outros em `cop=`.
7. Classifique `eixo`, `cta`, `flags` e escreva a `tese` para cada post novo.
8. Insira as linhas novas no topo, mais recente primeiro, e rode `python3 -I scripts/resumo.py` para validar.
