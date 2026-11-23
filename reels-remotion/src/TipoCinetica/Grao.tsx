import React from "react";

// Grão de 35 mm preso à letra. O ruído muda a cada quadro e entra só onde já
// existe tinta (operador atop): a transparência do tipo não é tocada, então
// nada de grão vaza para o fundo nem para o vídeo de baixo.

type Props = {
  id: string;
  quadro: number;
  x: number;
  y: number;
  largura: number;
  altura: number;
  /** Opacidade máxima de um grão. Leve: perto de 0,3. */
  forca?: number;
  /** Tamanho do grão: mais alto, mais fino. */
  frequencia?: number;
};

export const FiltroGrao: React.FC<Props> = ({
  id,
  quadro,
  x,
  y,
  largura,
  altura,
  forca = 0.28,
  frequencia = 0.45,
}) => {
  return (
    <filter
      id={id}
      filterUnits="userSpaceOnUse"
      x={x}
      y={y}
      width={largura}
      height={altura}
      colorInterpolationFilters="sRGB"
    >
      <feTurbulence
        type="fractalNoise"
        baseFrequency={frequencia}
        numOctaves={3}
        seed={quadro * 13 + 5}
        result="ruido"
      />
      {/* Um canal só, copiado para cor e para opacidade. */}
      <feColorMatrix
        in="ruido"
        type="matrix"
        values="1 0 0 0 0  1 0 0 0 0  1 0 0 0 0  1 0 0 0 0"
        result="mono"
      />
      {/* Metade dos grãos clareia, metade escurece; perto do meio, nada. */}
      <feComponentTransfer in="mono" result="grao">
        <feFuncR type="discrete" tableValues="0 1" />
        <feFuncG type="discrete" tableValues="0 1" />
        <feFuncB type="discrete" tableValues="0 1" />
        <feFuncA type="table" tableValues={`${forca} 0 ${forca}`} />
      </feComponentTransfer>
      <feComposite in="grao" in2="SourceGraphic" operator="atop" />
    </filter>
  );
};
