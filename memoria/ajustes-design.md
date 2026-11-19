---
titulo: Ajustes finos de design
tipo: regra
criado: 2026-11-19
fonte: "Vídeo enviado por ele em 19/11/2026 (10 ajustes finos de design, 48 s), com o pedido: Assista e incorpore essas regras de ajustes"
status: ativo
---

# Ajustes finos de design

Pedido dele em 19/11/2026: "Assista e incorpore essas regras de ajustes".
Origem: Reel de terceiro com 10 ajustes de interface. São regras de execução visual, não de conteúdo clínico.

Valem para tudo que o Claude monta em código: páginas (`site-curso/`, `novo/`, `respirar/`), composições HyperFrames e Remotion (cartões, infográficos, legendas, sobreposições), artifacts e slides de carrossel feitos em HTML.
Imagem gerada por modelo (GPT Image) não recebe CSS. Ali, os itens 1, 2, 5 e 9 entram como direção no comando e são conferidos no resultado.

Não substituem regra anterior. Área segura, fonte, cores da marca e padrão de efeitos (`efeitos-video-aprovados.md`) continuam valendo.

## As 10 regras

1. **Raio concêntrico.** Caixa arredondada dentro de outra não usa o mesmo raio. Raio de dentro = raio de fora menos o espaçamento entre elas.
   `.fora { border-radius: 48px; padding: 16px; } .dentro { border-radius: 32px; }` (48 − 16)

2. **Borda com transparência.** Borda sólida em hex fica feia conforme o fundo. Usar borda semitransparente, que se mistura com o que está atrás.
   `border: 1px solid oklch(0 0 0 / 0.12);` (no escuro: `oklch(1 0 0 / 0.12)`)

3. **Paleta em OKLCH.** O olho percebe o brilho de cada cor de um jeito; HSL não iguala esse brilho. Definir cores em OKLCH. Cores da marca já fixadas (vermelho `#CC0000`) mantêm o valor; só se escreve em OKLCH o equivalente.
   `color: oklch(0.55 0.21 27);`

4. **Degradê em OKLCH.** Degradê que fica cinza no meio: interpolar em OKLCH.
   `background: linear-gradient(in oklch, #f5a623, #e0457b);`

5. **Ícone no peso do texto.** Ícone de traço fino ao lado de texto em negrito parece desleixado. Espessura do traço acompanha o peso da fonte (Montserrat ExtraBold pede traço grosso).
   `svg { stroke-width: 2.5; }` ao lado de texto 800; `1.5` ao lado de texto 400

6. **Pontas com máscara.** Fileira que rola na horizontal (galeria, carrossel na página) some nas bordas com máscara, sem corte seco.
   `mask-image: linear-gradient(to right, transparent, #000 8%, #000 92%, transparent);`

7. **Troca com desfoque.** Ao trocar um ícone ou palavra por outro no mesmo lugar, usar um pouco de desfoque na transição.
   `transition: opacity .2s, filter .2s;` saída com `opacity: 0; filter: blur(4px);`

8. **Profundidade no escuro.** Sombra quase não aparece em fundo escuro. Dar profundidade com superfícies mais claras por camada.
   fundo `oklch(0.16 0 0)`, cartão `oklch(0.21 0 0)`, cartão acima `oklch(0.26 0 0)`

9. **Altura dinâmica no celular.** `100vh` dá problema no Safari do celular. Usar `dvh`, com `vh` antes como reserva.
   `min-height: 100vh; min-height: 100dvh;`

10. **Mistura multiply.** Foto de produto com fundo branco sobre fundo colorido: `multiply` faz o branco sumir.
    `img { mix-blend-mode: multiply; }`

## Como conferir

- Antes de entregar peça em código, passar pelas 10 e anotar as que não se aplicam.
- Medir por código o que dá para medir: raios aninhados, bordas em hex sólido, `100vh` sem `dvh`, degradês sem `in oklch`.
- Se uma regra daqui bater numa regra dele já registrada, vale a dele e o conflito vai para `a-decidir.md`.
