import { useEffect, useState } from "react";
import { cancelRender, continueRender, delayRender, staticFile } from "remotion";

export const ANTON = "Anton";

// Lido do arquivo da fonte (head.unitsPerEm = 2048).
export const ALTURA_CAIXA = 1760 / 2048; // topo da caixa alta
export const ALTURA_ACENTO = 2254 / 2048; // topo de Ê e Ó
export const DESCIDA_Q = 187 / 2048; // cauda do Q abaixo da linha de base

let carga: Promise<void> | null = null;

const carregarAnton = (): Promise<void> => {
  if (!carga) {
    const fonte = new FontFace(
      ANTON,
      `url('${staticFile("fonts/anton.woff2")}') format('woff2')`,
    );
    carga = fonte.load().then(() => {
      document.fonts.add(fonte);
    });
  }
  return carga;
};

/** Segura o render até a Anton estar pronta para medir e desenhar. */
export const useAnton = (): boolean => {
  const [pronta, setPronta] = useState(false);
  const [espera] = useState(() => delayRender("Carregando a fonte Anton"));

  useEffect(() => {
    carregarAnton()
      .then(() => {
        setPronta(true);
        continueRender(espera);
      })
      .catch((erro) => {
        cancelRender(erro);
      });
  }, [espera]);

  return pronta;
};

export type Glifo = {
  ch: string;
  /** Posição da pena, a partir do começo da linha, já com o kerning. */
  x: number;
  avanco: number;
  /** Ordem entre as letras da linha, sem contar espaço. */
  ordem: number;
  /** Índice da palavra na linha. */
  palavra: number;
};

export type Linha = {
  texto: string;
  largura: number;
  glifos: Glifo[];
};

const CORPO_DE_MEDIDA = 1000;

/**
 * Mede a linha letra por letra com o kerning da própria fonte. Cada letra é
 * desenhada sozinha (para poder cair, subir ou esticar), mas no lugar exato
 * em que ficaria se a linha fosse um texto só.
 */
export const medirLinha = (texto: string, corpo: number): Linha => {
  const ctx = document.createElement("canvas").getContext("2d");
  if (!ctx) {
    throw new Error("Sem canvas para medir o texto");
  }
  ctx.font = `${CORPO_DE_MEDIDA}px ${ANTON}`;
  ctx.fontKerning = "normal";
  const escala = corpo / CORPO_DE_MEDIDA;
  const largura = (s: string) => ctx.measureText(s).width * escala;

  const letras = Array.from(texto);
  const glifos: Glifo[] = [];
  let ordem = 0;
  let palavra = 0;
  letras.forEach((ch, i) => {
    if (ch === " ") {
      palavra += 1;
      return;
    }
    const ate = letras.slice(0, i + 1).join("");
    const avanco = largura(ch);
    glifos.push({ ch, x: largura(ate) - avanco, avanco, ordem, palavra });
    ordem += 1;
  });

  return { texto, largura: largura(texto), glifos };
};
