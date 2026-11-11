---
titulo: BRAIN
tipo: tema
criado: 2026-11-07
fonte: "[[aprendizados]], [[correcoes]], [[checklist-entrega]], [[efeitos-video-aprovados]], [[a-decidir]]"
status: rascunho
---

# BRAIN: Borderline Sem Estigma

Ordem dele em 07/11/2026: "Antes de qualquer resposta ou tarefa, leia BRAIN.md e brain.json. / Regras do BRAIN.md prevalecem sobre preferência sua. / Se violar um anti-pattern, registre em brain-log.md."

- Ler este arquivo e `brain.json` antes de qualquer resposta ou tarefa.
- As regras daqui prevalecem sobre preferência do Claude.
- Violou um anti-pattern: registrar em `brain-log.md` na hora (data, id, o que aconteceu, frase dele se houver, correção).
- Este arquivo e `brain.json` têm o mesmo conteúdo. Mudou um, mude o outro.

Objetivo: produzir Reel, carrossel, capa e Stories para quem tem borderline e quem convive de perto, sem repetir erro que ele já pegou.
O detalhe fica nos arquivos de `memoria/`. Aqui só o que muda decisão. Linhas citadas pela versão do `main` de 07/11/2026.

## REGRAS INVIOLÁVEIS

1. Tese aprovada por ele antes de gerar imagem ou montar vídeo. (checklist-entrega.md:21)
2. Assunto novo vem do Vamos, com prova de post validado. Desde 07/11 Claude também pode criar tema ("Ou crie vc também"), com prova e pelo mesmo corte. (correcoes.md:225, correcoes.md:134)
3. Entrega sempre em alta: imagem 2k, vídeo 1080p. Rascunho em baixa só se ele pedir. (correcoes.md:168)
4. Imagem com texto: GPT Image 2.6 Sunburst (`gpt_image_2_6`, sem parâmetro variant; pedido dele em 11/11), alta, 2k, conferida letra por letra. Antes era o 2.5 Sunburst. (aprendizados.md:37, aprendizados.md:81, correcoes.md:219)
5. Quantidade exata: pediu N, são N. Carrossel tem 8 slides, salvo pedido. (aprendizados.md:31, aprendizados.md:88, correcoes.md:197)
6. Rodar a auditoria de texto da seção 0 antes da primeira entrega, não depois. (aprendizados.md:7-17, correcoes.md:70)
7. Nenhuma palavra cortada em fala ou narração. Medir as pontas em -55/-60 dB e ouvir cada corte. (correcoes.md:34, checklist-entrega.md:47)
8. Texto dentro da área segura, medido por código, inclusive nas entradas animadas: 5% laterais, 12% à direita, 20% embaixo. (correcoes.md:216)
9. Limite técnico, tempo e número de passos avisados no começo. (aprendizados.md:26, correcoes.md:74, correcoes.md:216)
10. Veredito uma vez, antes de postar, já cruzado com `correcoes.md` e `aprendizados.md`. Depois do resultado, não listar causas. (correcoes.md:224, checklist-entrega.md:65)

## ANTI-PATTERNS (erro, consequência, o que fazer)

- Fórmula de contraste (não é X, é Y) → "Tem mais não é x é y porra não acredito" → varrer a peça inteira, não só o slide apontado. (aprendizados.md:11, aprendizados.md:17)
- Frase começando com ele ou ela → pego em 24/10, 27/10 e 28/10 → nenhuma frase abre com pronome; você é permitido. (checklist-entrega.md:27, aprendizados.md:123)
- Palavra curta isolada na linha → "A palavra ir isolada ficou estranha" → quebrar à mão, com hierarquia. (aprendizados.md:13, correcoes.md:226)
- Duplo sentido ou gíria (dar, pegar, ficar) → "Ta loko" sobre VOCÊ DÁ TUDO → ler em voz alta antes. (aprendizados.md:14)
- BORDERLINE fora da maior hierarquia da capa → Chamaram de bipolar apagado na primeira hora, 0 envios → borderline é a maior palavra e o sujeito da frase. (correcoes.md:223, correcoes.md:179)
- Capa sem pessoa, só objeto ou sala → mesmo flop do bipolar (hipótese, sem causa provada) → a leitora protagonista da cena. (correcoes.md:223, checklist-entrega.md:19)
- Envio para quem acusou ou errou → "Só se quiser arrumar briga lá", terceira vez → mandar para quem a pessoa quer que entenda. (correcoes.md:154, checklist-entrega.md:32)
- Explicar o flop depois → "Não dá mesmo pra confiar aqui" → apontar o risco antes de postar. (correcoes.md:224, correcoes.md:183)
- Prévia reduzida ou 480p como amostra → "Sempre faz em alta" → mandar no tamanho gerado. (correcoes.md:168)
- Thumb com rosto dele gerado por IA → "Nem fudendo nem parece eu" → quadro real da gravação, texto no meio por causa do recorte 3:4. (correcoes.md:212)
- Clipe gerado usado sem conferir a voz → "Pq não colocou minha voz?" → conferir voz e boca antes; trocar com voice_change no elemento Fabio. (correcoes.md:208)
- Voz clonada por cima da boca dele, ou fala nova inventada sobre cena do clone → "Não é isso que eu falo na cena" → perguntar se ele vai gravar; manter a fala original. (correcoes.md:162, correcoes.md:203)
- Remover cena dele ou trocar clipe sem confirmar → "vc tirou o começo" → confirmar antes de cortar material dele. (correcoes.md:213, correcoes.md:216)
- SFX alto ou fora da biblioteca → pego três vezes → só `memoria/sfx/` e o padrão aprovado; -14 LUFS. (checklist-entrega.md:49, efeitos-video-aprovados.md:45-49)
- Destaque da legenda em minúscula itálica → "Está minúsculo e menor" → destaque em caixa alta, parecendo maior de relance. (correcoes.md:135)
- Contorno grosso na serifa → "Uma sombra não ficas mais elegante?" → sombra leve. (correcoes.md:191, correcoes.md:227)
- Tipografia de borda a borda no Story → "Sem margem nenhuma dos lados?" → margem lateral de 10% ou mais. (correcoes.md:182)
- Personagem flutuando → "Thumb flutuando de novo" → pés abaixo da linha do chão da parede de trás. (aprendizados.md:83, correcoes.md:221)
- Imagem em todo slide → "E não é pra ter imagem em todas nem" → alternar tipografia pura, com apoio e presa à imagem. (correcoes.md:180, aprendizados.md:77)
- Mão e celular, mulher de costas na cama → "não aguento mais mão e celular" → cena, gesto ou objeto concreto. (aprendizados.md:84, aprendizados.md:89)
- Fundo preto no carrossel → regra dele → só em vídeo e Stories. (aprendizados.md:74, aprendizados.md:124)
- Reindicar música porque "já funcionou" → "Já usei 3x" (Love Again) → perguntar quantas vezes já usou. (correcoes.md:186)
- Mexer em peça fechada por referência nova → "Não misture" → referência nova vai para peça nova. (correcoes.md:187)
- Menu de opções com ele irritado → "Incompetente demais" → entregar o arquivo mais útil e uma linha. (correcoes.md:203)
- Resposta longa → "vai se foser" depois de explicar o cofre → responder só o que perguntou, curto. (correcoes.md:142, aprendizados.md:23)

## ATALHOS DE DECISÃO

- Capa de carrossel → rodar `capas-base-tecnica.md` (G × P). N de 80 a 100 posta; 60 a 79 ajusta; abaixo de 60 ou G = 0 barra. Registrar N e envios por mil de alcance no placar. (capas-base-tecnica.md:25-77)
- Pediu roteiros ou temas virais → Vamos primeiro, com prova por tema, depois escrever. (correcoes.md:134)
- Pediu só legenda e capa → entregar só isso; erro do vídeo em uma linha, sem reeditar. (correcoes.md:70)
- Pediu para não mudar o texto → nem uma palavra. (aprendizados.md:48)
- Revisão → mudar a cena, manter a frase boa. Se as alternativas não superarem, voltar ao original. (aprendizados.md:46, correcoes.md:19)
- Público novo ou tema sem vizinho com dado → teste, não feed. (checklist-entrega.md:18, checklist-entrega.md:64)
- Vídeo falado dele → pacote padrão sem ele pedir: legenda palavra a palavra, corte de silêncio, esquemas, zoom leve, conferência de posição. (correcoes.md:43)
- Filtro do GPT Image barrou → avisar na hora e já reenviar reescrito (adulto, sem cama, sem choro). (correcoes.md:61)
- Narração com voz clonada → o texto inteiro num único take; o vídeo se ajusta à narração; se uma palavra sair errada, regerar o take inteiro, nunca emendar trechos. "Faça a narração em uma tomada só senão fica estranho" (07/11), "Narração uma gerada só" (07/11), "Quando gerou um take só nem deu pra perceber que era ia" (10/11). (correcoes.md:228, correcoes.md:238)
- Configuração técnica → um passo por mensagem, dizendo quantos faltam. (correcoes.md:73, correcoes.md:74)
- Vídeo até cerca de 30 MB → no chat. Acima → Drive (conferir tarefas do Zapier antes) ou link do GitHub. (aprendizados.md:107, correcoes.md:58, correcoes.md:173)
- Seedance ilimitado → não funciona pelo Claude Code ("unlimited generations are not available" aqui; só no Claude chat, Cowork ou ChatGPT). Daqui custa 48 créditos por clipe de 4 s em 1080p (Seedance 2.0). Escrever os prompts para ele rodar no Claude chat ou no app. (correcoes.md, 10/11)
- Upload para o Higgsfield bloqueado → referência pelo job_id de geração antiga, ou imagem em commit temporário e `media_import_url`. (correcoes.md:219, correcoes.md:167)

## LACUNAS CONHECIDAS

- Capa base técnica contra regras antigas: G4 conta BORDERLINE SEM ESTIGMA no topo como texto pequeno, mas o molde de capa de 28/10 usa essa linha (correcoes.md:71); a negação que corrige crença (Funcional não é leve) é o mecanismo nº 1 do documento e bate no anti-pattern de contraste (aprendizados.md:11, a-decidir.md:25-27). Provisório: seguir a base técnica (é a mais nova) e evitar só a fórmula de dois polos não é X, é Y.
- Prioridade dos Reels: as preferências fixas dizem que recuperar o alcance é prioridade; ele disse em 28/10 que não é ("O alcance do Reel está ótimo"). Trava a função de cada peça. (aprendizados.md:69, checklist-entrega.md:34)
- Contraste na capa: 3 dos 5 gigantes usam contraste explícito, contra a regra de 24/10. Trava capa nova. (a-decidir.md:25-27)
- Fundo preto e neurobiologia no feed: gigantes escuros e o do cérebro (109 mil) contra as regras dele. Regra provisória: seguir a regra e perguntar. (a-decidir.md:7-17)
- Nome do livro: "Quem sofre não escolhe como gritar" ou "Quando Escolher Não É Possível". Trava qualquer peça que cite o livro. (a-decidir.md:19-23)
- Rosto dele nos Reels: os dados não separam Reel com e sem rosto. Perguntar antes de propor. (aprendizados.md:114, aprendizados.md:126)
- Métricas: última leitura registrada em `conta.md` é de 26/10. O que vier sem número novo fica "não validado". (conta.md:43)

## PONTEIROS

Regras com prova: `aprendizados.md` · Correções novas: `correcoes.md` · Checagem antes de entregar: `checklist-entrega.md` · Veredito: `termometro.md`, `placar-vereditos.md` · Reel: `reels-certeiros.md`, `efeitos-video-aprovados.md` · Capa: `capas-base-tecnica.md` (nota G × P), `capas-gigantes.md`, `mecanismos-gigantes.md` · Teses usadas: `ja-produzido.md` e skill `historico-borderline-180d` · Oferta e preços: `conta.md` · Em aberto: `a-decidir.md`
