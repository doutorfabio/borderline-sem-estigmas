---
titulo: Radar de pauta
tipo: tema
criado: 2026-11-07
fonte: informado pelo Dr. Fabio em 2026-11-07
status: revisado
---

# Radar de pauta e formatador

Protocolo dele de 07/11/2026. Só texto, sem gerar mídia. Saída em PT-BR; prompt de imagem ou vídeo em inglês.

## Fontes de repetição

Ele citou `docs/06` (hooks) e `docs/09` (anti-patterns), que não existem no repositório. Equivalentes usados até ele dizer outra coisa:
- Hooks e temas já usados: `ja-produzido.md`, `ganchos-50-2026-10-30.md`, `reels-certeiros.md`, skill `historico-borderline-180d`.
- Anti-patterns: [[BRAIN]] e `brain.json`.

## Modos

- SINALIZAR: até 5 temas, ranqueados.
- DESENVOLVER: tema escolhido + notas cruas dele. Formatar sem mudar as notas, só a forma.
- RECUSAR: tema abaixo do corte. Uma linha com o motivo e o ajuste.

## Critérios (0 a 5 cada)

1. Tensão: conflito, não só informação.
2. Especificidade: número, nome, cena ou detalhe concreto.
3. Aposta: o público perde algo se ignorar.
4. Novidade: ângulo não batido; marcar se for óbvio.
5. Prova: sustentável com o que ele tem (dado, print, caso, demo).
6. Produzibilidade: cabe em story, carrossel ou reel com o acervo dele.

Corte: soma mínima 24/30 e nenhum critério abaixo de 3. Abaixo disso, não entrega.

## Saída SINALIZAR

[TEMA] uma linha, frase nominal, sem "como fazer"
[POR QUÊ] 1 linha com o conflito
[PROVA NECESSÁRIA] o que ele precisa ter em mãos
[FORMATO] reel, carrossel ou story, e o motivo
[GANCHO SEMENTE] 1 linha, até 12 palavras
[NOTAS] 1.x · 2.x · 3.x · 4.x · 5.x · 6.x · TOTAL xx/30
[RISCO] o que pode soar genérico e como evitar

## Saída DESENVOLVER

[ESTRUTURA] beats numerados (reel: gancho 0-2 s, 3 beats, fecho; carrossel: capa, progressão, fecho; story: sequência com CTA)
[HOOKS] 3, um por eixo: contradição, número, cena
[COPY] texto final por beat
[CTA] 1 linha, específica
[LEGENDA] 1 parágrafo + 3 hashtags
[PROMPT VISUAL] bloco em inglês por beat
[CHECK] onde pode cair em anti-pattern e o ajuste

## Regras duras

1. Tema sem tensão não entra, mesmo útil.
2. Proibido "5 dicas", "você sabia", "descubra como".
3. Gancho com até 12 palavras, sem pergunta de sim ou não.
4. Cada hook testa um eixo diferente.
5. Faltou prova: marcar "sem prova" e dizer o que buscar. Nunca inventar dado.
6. No DESENVOLVER, preservar as notas dele.
7. Máximo 5 temas por rodada. Menos e melhor.

## Conflitos com o BRAIN (aguardando decisão dele)

- BRAIN r2 (correcoes.md:225): assunto novo vem do Vamos, Claude repassa sem opinar. O modo SINALIZAR pede que Claude proponha e dê nota. Provisório: temas saem do Vamos; Claude aplica o corte e as notas.
- Eixo contradição dos hooks contra o anti-pattern a1 (fórmula não é X, é Y). Provisório: contradição só como fato inesperado, nunca na fórmula.
- Sem gerar mídia contra BRAIN r4 (pedido de capa já inclui gerar a imagem). Provisório: neste modo vale só texto; capa gerada só com pedido fora do modo.
