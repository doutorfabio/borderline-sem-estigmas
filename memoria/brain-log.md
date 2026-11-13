---
titulo: Registro de violações do BRAIN
tipo: tema
criado: 2026-11-07
fonte: informado pelo Dr. Fabio em 2026-11-07
status: revisado
---

# Registro de violações

Cada vez que uma peça ou resposta violar um anti-pattern de [[BRAIN]] (ids em `brain.json`), registre aqui na hora, mais recente no topo. Atualize também `ultima_violacao` do item em `brain.json`.

Formato: `- AAAA-MM-DD · id · o que aconteceu · frase dele (se houver) · como foi corrigido`

## Registros

- 2026-11-13 · r10 · Reel pergunta do passado entregue em três versões (12/11) sem veredito feed ou teste e sem linha no placar; Claude escreveu que não fez veredito porque o pedido era só legenda e Sfx. Postado, flopou. Ele: "Flopou / Arruma / Se vira". Correção: v4 recortada e veredito de teste dado e registrado antes de postar.
- 2026-11-10 · a1 · Capa 12 do desafio (A EMOÇÃO DO BORDERLINE CHEGA EM ONDA, NÃO EM GOTA.) saiu com fórmula de contraste X, não Y. Achado pelo próprio Claude no funil pedido por ele. Barrada.
- 2026-11-07 · a1 · Na fala que segue o gancho do Reel da vergonha, Claude escreveu "Parece orgulho. Quase sempre é vergonha.", fórmula de contraste, e entregou sem varrer. Achado pelo próprio Claude na revisão da nota pedida por ele ("Nota"). Trocado por "O que trava a desculpa é a vergonha."
- 2026-11-07 · r10 · Carrossel TER BORDERLINE NÃO TIRA SEU DIREITO DE SOFRER entregue só com a nota da base técnica (95), sem veredito feed ou teste pelo termômetro, sem cruzar com o placar e sem registro em placar-vereditos.md antes de ele postar. Flopou. Ele: "Flopou de novo / Vai se fuser vc nak sabe usar essa merda de memórias". Correção: nota de capa não substitui veredito; toda peça pronta para postar sai com veredito feed ou teste escrito e registrado no placar antes da entrega.

## 2026-11-11, a14 (SFX alto)
- O que aconteceu: nos Reels 3 frases e rosto neutro, o áudio original do Seedance ficou como fundo quase no mesmo volume da narração (fundo -26,7 e -29,9 LUFS contra narração -29,9 e -30,9 antes do ganho). Não medi o fundo contra a voz antes de entregar.
- Frase dele: "Música mto alta".
- Correção: fundo abaixado para cerca de 20 LU abaixo da voz nos dois, com ducking; mix final -14 LUFS; só o áudio foi remontado.
- Regra prática: medir a loudness do fundo sozinho e da voz sozinha antes do mix; fundo pelo menos 18 a 20 LU abaixo da voz.

## 2026-11-11, regra 9 (limite técnico não avisado)
- O que aconteceu: ele perdeu a conta do GitHub e pedi que criasse o repositório novo com o nome `Novo`. A sessão não aceita dois repositórios com o mesmo nome, mesmo de donos diferentes, e o envio travou depois de ele já ter criado e vinculado. Não conferi o limite antes de passar o passo.
- Frase dele: "Esse novo foi q eu criei e vc pediu e está vazio".
- Correção: pedir só a troca do nome do repositório novo; o envio sai desta sessão em seguida.
- Regra prática: ao pedir repositório novo para receber o conteúdo de uma sessão em andamento, o nome tem de ser diferente do repositório já ligado à sessão.
