import React from "react";

// Desfoque de movimento de verdade: o mesmo desenho é feito em vários
// instantes dentro do tempo em que o obturador fica aberto, e os desenhos são
// somados. O borrão sai na direção e no tamanho do movimento.
//
// Parado, desenha uma vez só, direto na cor. Em movimento, as amostras são
// somadas em branco e só então recebem a cor: assim a tinta não muda de tom
// nem fica translúcida por arredondamento.

type Props = {
  id: string;
  cor: string;
  /** Instante do quadro, em segundos. */
  t: number;
  fps: number;
  /** Fração do quadro com o obturador aberto. 0,25 equivale a 90 graus. */
  abertura: number;
  /** Números (em px) que mudam quando o desenho se move. */
  medida: (t: number) => number[];
  /** Área em que o desenho pode aparecer. */
  regiao: { x: number; y: number; largura: number; altura: number };
  /** Desenha as formas sem cor fixa: preenchimento herdado, traço em currentColor. */
  children: (t: number) => React.ReactNode;
};

const PARADO = 0.05; // px de deslocamento dentro do obturador
const PASSO = 1.5; // px entre uma amostra e a seguinte

const quantasAmostras = (deslocamento: number): number => {
  if (deslocamento < PARADO) {
    return 1;
  }
  const alvo = deslocamento / PASSO;
  if (alvo <= 4) {
    return 4;
  }
  if (alvo <= 8) {
    return 8;
  }
  if (alvo <= 16) {
    return 16;
  }
  return 32;
};

export const Obturador: React.FC<Props> = ({
  id,
  cor,
  t,
  fps,
  abertura,
  medida,
  regiao,
  children,
}) => {
  const meio = abertura / fps / 2;
  const antes = medida(t - meio);
  const centro = medida(t);
  const depois = medida(t + meio);
  let deslocamento = 0;
  for (let i = 0; i < centro.length; i++) {
    deslocamento = Math.max(
      deslocamento,
      Math.abs(depois[i] - antes[i]),
      Math.abs(centro[i] - antes[i]),
      Math.abs(depois[i] - centro[i]),
    );
  }

  const n = quantasAmostras(deslocamento);
  if (n === 1) {
    return (
      <g fill="currentColor" style={{ color: cor }}>
        {children(t)}
      </g>
    );
  }

  const amostras = new Array(n).fill(0).map((_, j) => {
    const fracao = (j + 0.5) / n - 0.5;
    return t + fracao * 2 * meio;
  });
  // Cada amostra vale floor(255 / n) de 255: o ganho devolve a soma a 255.
  const ganho = 255 / (n * Math.floor(255 / n));

  return (
    <g>
      <filter
        id={id}
        filterUnits="userSpaceOnUse"
        x={regiao.x}
        y={regiao.y}
        width={regiao.largura}
        height={regiao.altura}
        colorInterpolationFilters="sRGB"
      >
        <feComponentTransfer in="SourceAlpha" result="cobertura">
          <feFuncA type="linear" slope={ganho} />
        </feComponentTransfer>
        <feFlood floodColor={cor} result="tinta" />
        <feComposite in="tinta" in2="cobertura" operator="in" />
      </filter>
      <g filter={`url(#${id})`}>
        <g fill="currentColor" style={{ color: "#fff", isolation: "isolate" }}>
          {amostras.map((instante, j) => (
            <g key={j} opacity={1 / n} style={{ mixBlendMode: "plus-lighter" }}>
              {children(instante)}
            </g>
          ))}
        </g>
      </g>
    </g>
  );
};
