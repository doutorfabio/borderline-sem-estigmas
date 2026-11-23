// Quadro e área de tipo comuns às batidas de tipografia cinética.

export const LARGURA = 1080;
export const ALTURA = 1920;
export const FPS = 30;
export const DURACAO = 150; // 5,00 s

export const TINTA = "#121212";
export const VERMELHO = "#9E1B1B";
export const CREME = "#F3EBDD";

// Todo o tipo mora no terço de cima, a 6% ou mais de cada borda.
const MARGEM = 0.06;
export const SEGURA = {
  esq: LARGURA * MARGEM, // 64,8
  dir: LARGURA * (1 - MARGEM), // 1015,2
  topo: ALTURA * MARGEM, // 115,2
  base: ALTURA / 3, // 640
};

export const CENTRO_X = LARGURA / 2;
