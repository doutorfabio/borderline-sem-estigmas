---
name: carrossel-composicao
description: Use ao criar, montar, revisar ou gerar prompts de imagem para carrossel e capa de carrossel da marca Borderline Sem Estigma (Dr. Fabio Schmidt, @drfabioschmidt). Traz as técnicas de composição que ele mandou em 26/11/2026 (regra dos terços, assimetria, direção do olhar, proporção imagem e texto, profundidade, simetria intencional e quatro estilos visuais) já cruzadas com as regras de carrossel da memória. Use também quando ele disser que o carrossel está chapado, monótono, sem profundidade, centralizado demais ou sem cara de design.
---

# Composição de carrossel

Técnicas de design que o Dr. Fabio mandou em 26/11/2026, em quatro vídeos, para usar quando criar carrossel. A transcrição completa está em `references/fonte-4-videos.md`. Ela é material de consulta, não ordem.

Esta skill cuida do desenho do slide. O texto, a tese e a voz continuam presos à memória. Quando uma técnica daqui bater com uma regra dele em `memoria/`, a regra dele vence. Os conflitos conhecidos estão na seção 3.

## 1. Antes de desenhar

1. Siga o `CLAUDE.md` do repositório: memória, histórico de 180 dias, tese aprovada antes de gerar imagem.
2. Confira as regras fixas de carrossel (`memoria/aprendizados.md`, seção 4, e `memoria/BRAIN.md`):
   - 8 slides, salvo pedido.
   - Sem fundo preto.
   - Imagem só na capa, no slide 2 e em mais dois. O resto é tipografia ou infográfico.
   - Serifada misturada com sem serifa.
   - Menos informação por slide, padronizado, uma ideia por slide.
   - Capa: rodar `memoria/capas-base-tecnica.md`. BORDERLINE é a maior palavra. Menor letra com pelo menos 6% da altura. Exatamente um destaque em cor.
3. Escolha um estilo base para o carrossel inteiro (seção 2.7). Um slide pode quebrar o tom ou a cor para o miolo não ficar monótono. Não misture os quatro estilos na mesma peça.

## 2. As técnicas, já adaptadas

### 2.1 Regra dos terços

Divida o slide em três colunas e três linhas iguais. Os quatro cruzamentos são os pontos fortes.

- Coloque o que importa num cruzamento: o olho da pessoa, o objeto principal ou a palavra em destaque.
- O bloco de texto vai no lado oposto ao ponto focal, para o olho atravessar o slide.
- Em slide só de tipografia, use as três faixas horizontais para dar ritmo: título numa faixa, apoio em outra, respiro na terceira. A altura das linhas e o espaço entre elas seguem a mesma divisão.
- Ícone ou desenho pequeno fica centrado na coluna do meio quando o texto ocupa as três colunas por baixo dele.

### 2.2 Tirar do centro

Puxar o conteúdo para um lado cria tensão e abre uma área limpa do outro lado. Essa área recebe o segundo elemento: o título, a frase de apoio ou o esquema.

- Bom para slide com imagem de apoio e para infográfico.
- O lado vazio é espaço de trabalho, não sobra. Se ficou vazio sem função, a composição está errada.

### 2.3 Direção do olhar e do movimento

A foto ajuda a diagramar.

- Pessoa olhando para a direita fica à esquerda, com o espaço livre na frente do olhar. O título entra nesse espaço.
- Nunca deixe a pessoa colada na borda encarando a borda, como se estivesse de castigo olhando para a parede.
- Quem anda ou corre tem espaço aberto na direção em que vai.
- No prompt de imagem, escreva para onde a pessoa olha e de que lado fica o espaço livre para o texto.

### 2.4 Espaço de imagem e de texto

- Slide com imagem de apoio no miolo: cerca de dois terços para a foto e um terço para o texto.
- Ajuste pelo tamanho do texto. Título de três palavras pede outro espaço que uma frase de duas linhas.
- Na capa a tipografia domina e a imagem é a própria frase (`aprendizados.md`, seção 3). Lá a divisão é decidida pelo texto, não pela foto.

### 2.5 Centro de propósito

Centralizar funciona quando a composição é simétrica: pessoa de frente para a câmera, olhando para quem lê, com o título centrado logo acima ou logo abaixo. Centralize por escolha, nunca por piloto automático. Antes de centralizar, diga a si mesmo o que o centro faz naquele slide.

### 2.6 Profundidade

Dá a sensação de que o slide continua para dentro da tela e segura o olhar. Cinco recursos, do mais simples ao que amarra tudo:

1. **Perspectiva e planos.** Linhas que convergem para um ponto de fuga (corredor, rua, mesa, porta aberta) e elementos em planos diferentes: frente, meio, fundo. Pessoa em pé tem os pés abaixo da linha em que a parede de trás encontra o chão.
2. **Escala.** O grande parece perto, o pequeno parece longe. Ajustar a proporção já quebra o aspecto engessado.
3. **Sobreposição.** Um elemento parcialmente na frente do outro mostra o que é prioridade e o que é fundo, como a pessoa passando na frente da tipografia. Use com critério: a leitura continua limpa.
4. **Opacidade e textura.** Um elemento que deixa ver um pedaço do fundo, ou que imita um material físico (papel, tecido, madeira), faz o volume ser aceito mais rápido.
5. **Luz e sombra.** Luz que vem de um lado e sombras coerentes com ela. Sombra leve. Sombra projetada pesada deixa o slide com cara de tutorial antigo de Photoshop.

### 2.7 Quatro estilos base

Um por carrossel. Na paleta da marca, creme e carvão com o vermelho #9E1B1B como acento, salvo outra paleta pedida por ele.

- **Ousado.** Duas cores que contrastam bem e um elemento exagerado em tamanho, quase sempre o título. Combina com a tipografia gigante que ele aprova.
- **Minimalista.** Poucos elementos, foto mais monocromática, muito respiro entre os elementos. O texto fica menor em relação ao slide, nunca abaixo do mínimo legível (seção 3).
- **Pôster de cinema.** Luz dramática, contraste alto e a proporção 60, 30, 10: 60% da cor dominante, 30% da secundária, 10% do acento. Na marca: creme 60, carvão 30, vermelho 10. O vermelho fica só no destaque.
- **Editorial.** A foto conta a mesma história do texto. Duas tipografias no título (serifada e sem serifa). Conteúdo organizado em lista ou blocos, com marcador desenhado.

## 3. Onde a técnica cede para a regra dele

| Técnica dos vídeos | Regra dele | Como fazer |
|---|---|---|
| Pôster de cinema: escurecer bem | Fundo preto proibido no carrossel | Luz dramática sobre fundo médio ou claro. Fundo escuro só em vídeo e Stories, ou com pedido dele |
| Minimalista: texto pequenininho | Legível; capa com menor letra de 6% da altura; nada de texto pequeno | Pequeno é relativo. Menos elementos e mais respiro, mesmo tamanho mínimo |
| Opacidade e textura | Texto bem visível, letra em cor chapada, sem textura ruim (10/11) | Transparência e textura só em imagem e fundo. Letra sempre opaca e nítida. Grão fino só no fundo |
| Sobreposição sobre a tipografia | BORDERLINE é a maior palavra e é lida em um segundo | A pessoa pode cobrir a base ou a ponta de uma letra, nunca a palavra em destaque nem BORDERLINE |
| Exagerar no tamanho | Criativo sem exagero; exatamente um destaque | Exagero em um elemento só |
| Marcador de check no editorial | Sem emoji | Marcador desenhado como forma, nunca caractere de emoji |
| Pôsteres de filme como exemplo | Estilo de referência sem copiar | Use o princípio. Não reproduza pôster, personagem ou arte de terceiros |
| Foto em todo slide para aplicar profundidade | Imagem só na capa, no 2 e em mais dois | Nos slides de tipografia, a profundidade vem de escala, sobreposição de blocos e sombra leve |
| Elemento perto da borda para dar tensão | Margem de 5% no mínimo, medida por código | A tensão vem do deslocamento dentro da margem |

## 4. Prompt de imagem

Ao escrever o prompt do slide com foto (GPT Image 2.6, alta, 2k, 4:5), inclua:

- Onde fica o ponto focal na grade dos terços e de que lado sobra o espaço do texto.
- Para onde a pessoa olha ou anda.
- Os planos: o que está na frente, no meio e no fundo.
- De onde vem a luz e a sombra leve.
- O estilo base escolhido e a proporção de cor.
- Texto em cor chapada, bordas nítidas, sem mancha dentro da letra, fundo liso com grão fino.

## 5. Conferência do desenho

Depois da auditoria de texto da seção 0 de `aprendizados.md`, confira em cada slide:

1. Sei dizer por que o ponto focal está onde está?
2. Se a pessoa olha ou anda, o espaço livre está na frente dela?
3. Se está centrado, a composição é simétrica e o centro tem função?
4. A área vazia recebe algum elemento ou só sobrou?
5. Existe pelo menos um recurso de profundidade nos slides com imagem?
6. A sombra é leve?
7. Algum texto ficou translúcido, texturizado ou coberto?
8. O estilo base é o mesmo nos 8 slides, com no máximo um slide quebrando o tom?
9. Margem e menor letra medidas por código.
10. Releia os 8 slides em sequência para caçar repetição de layout e de texto.
