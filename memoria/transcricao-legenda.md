---
titulo: Transcrição e legenda cinética no Claude Code
tipo: tema
criado: 2026-11-12
fonte: sessão de 2026-11-12 (Reel O borderline pergunta do seu passado)
status: rascunho
---

# Transcrição e legenda cinética: o que funciona neste ambiente

Registrado em 12/11/2026. A transcrição travou cerca de 40 minutos por bloqueio de rede e ele reclamou ("Meu Deus não vai acabar nunca?"). Começar por aqui evita repetir.

## Transcrição com tempo por palavra

- Ambiente Default já tem liberados (aprovados por ele em 12/11): huggingface.co, cdn-lfs.huggingface.co, cas-bridge.xethub.hf.co, cdn-lfs-us-1.hf.co, us.aws.cdn.hf.co.
- Comando que funcionou: `HF_HUB_DISABLE_XET=1 uvx --from faster-whisper python tr.py audio.wav words.json`, modelo `large-v3`, `compute_type=int8`, `language="pt"`, `word_timestamps=True`.
- Sem `HF_HUB_DISABLE_XET=1` o download tenta cas-server.xethub.hf.co, que é bloqueado.
- Passar o áudio como array numpy (wav 16 kHz mono lido com `wave`), porque o `av` instalado pelo uvx quebra em `decode_audio` (erro metadata_errors).
- O modelo tem 3 GB; rodar o download em segundo plano. Fica no cache só enquanto o contêiner viver.
- O `transcribe.cjs` da skill embedded-captions não roda aqui (HyperFrames CLI ausente). Os pacotes npm @skillninja são barrados pelo classificador de permissão.

## Receita da legenda usada em 12/11 (aguardando a reação dele)

- Pipeline: quadros em JPG (ffmpeg) + index.html com `setT(t, quadro)` + Playwright em /opt/node-tools/node_modules/playwright com 4 páginas em paralelo (1238 quadros em cerca de 3 min) + ffmpeg (crf 19, maxrate 5400k, cabe em 30 MB para 41 s).
- Legenda no centro em y = 1368 de 1920, largura máxima 760 px, até 3 palavras por bloco, quebra de linha feita à mão, palavra entra quando é falada. Montserrat 800 caixa alta 68 px branca com contorno de 2 px e sombra; destaque em Fraunces 900 itálica caixa alta 1,52x, vermelho #EE2A22 só com sombra (o #CC0000 some em cima da camiseta preta).
- Um só movimento de entrada para as palavras comuns e um só para os destaques. Primeiro bloco já inteiro no quadro 0.
- Área segura medida por código em todos os quadros (esquerda 54, direita 950, embaixo 1536). O destaque entra com escala 1,2 e pode estourar a direita: por isso a largura máxima é 760 e não 800.
- Contador 1/3, 2/3, 3/3 em pílula escura acima da legenda quando a fala enumera; as barras se juntam em uma quando a fala diz que é a mesma coisa.
- Zoom contínuo de 1,0 a 1,06/1,09 só em trechos de impacto entre cortes dele, mais um punch de 3% nas trocas de lugar.
- Som: voz com compressor leve e ganho até -14 LUFS (pico -1,3 dBFS); 15 efeitos de memoria/sfx/editorpro (Swipe9 e Fino6 nas trocas de lugar, Click4 nos números, HUD_Pop-Up2 nos destaques fortes, Riser_Ouro_Curto baixo antes da pergunta central); pico dos efeitos sozinhos em -15,9 dBFS. Pedido dele: "Sfx ponderados".
- Dos efeitos de referência do charliehills (12/11, "só se couber"): entrou só a lógica do Words kinetic e do contador. Partículas, líquido, gráfico, cartões, órbita e celular ficaram fora por não terem ligação com a fala.
- Fonte do projeto: `videos/reel-pergunta-do-passado/` no branch claude/blissful-gates-p0qnng.

## Quadro solto nos cortes (correção dele em 12/11)

- Ele: "Verifique as transições as vezes aparece um frame errado e some".
- Causa: a montagem dele (gravação original) trazia 1 quadro de outra tomada em dois cortes (8,53 s e 21,57 s). A v1 saiu com eles porque só conferi os cortes pela folha de 1 quadro por segundo.
- Correção: cada quadro solto trocado pelo quadro seguinte, sem mudar duração nem áudio.
- Regra: antes de legendar gravação já cortada por ele, tirar a nota de cena de todos os quadros (`select='gte(scene,0)',metadata=print`) e olhar os 6 quadros em volta de cada corte. Dois saltos altos em quadros seguidos é quadro solto. Avisar e corrigir na primeira entrega.

## Música (12/11)

- Ele pediu prompt para o Suno com até 400 caracteres e recusou a primeira sugestão (violão abafado, sem bateria): "Mas quero estilo indie". Prompt indie aceito: indie bedroom pop, guitarra limpa com chorus, baixo quente, bateria lo-fi de vassourinha, pad, 88 BPM, lá menor resolvendo em dó maior. Gerou A Minor Resolves (102 s).
- Mixagem usada: trecho final da faixa (61,13 s até o fim) para o encerramento natural cair no fim do vídeo; passa-altas 130 Hz; ducking pela voz; música sozinha em -32,5 LUFS, 18,6 LU abaixo da voz; total -14 LUFS.
