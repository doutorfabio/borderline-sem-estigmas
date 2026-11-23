// Reel "Ir embora" (23/11/2026). Tempos em quadros a 30 qps.
// A fala não é cortada: o tempo do vídeo final é o tempo da gravação.
// Tudo o que está escrito aqui é o que ele diz, palavra por palavra (large-v3).

export const FPS = 30;
export const TOTAL = 1291; // 43,03 s

export const CREME = "#F3EBDD";
export const CARVAO = "#161616";
export const VERMELHO = "#9E1B1B";

// Área segura (regra dele): 5% laterais, 12% à direita, 20% embaixo.
export const SEGURA = { esq: 54, dir: 950, topo: 96, base: 1536 };
export const CENTRO_X = (SEGURA.esq + SEGURA.dir) / 2; // 502

// Inserções de B-roll. Entram na palavra e saem em cima do corte que já existe
// na gravação, para não sobrar pedaço do take anterior.
export const INSERCAO_MESA = { de: 365, ate: 471 }; // 12,17 a 15,70 s: mesa (sorrisinho, tá adorável)
export const INSERCAO_CEL = { de: 544, ate: 607 }; // 18,13 a 20,23 s: celular (olha de novo e não vem)
export const INSERCAO_1 = { de: 776, ate: 878 }; // 25,87 a 29,27 s
export const INSERCAO_2 = { de: 1102, ate: 1239 }; // 36,73 a 41,30 s

// Texto grande sobre o rosto.
export const TEXTO_ROSTO = { de: 878, ate: 985 }; // 29,27 a 32,83 s

// Aproximações secas no rosto, sempre em começo de frase e nunca em B-roll.
export const APROXIMACOES: { de: number; ate: number; escala: number; origem?: string }[] = [
  // borderline e pânico? A imagem muda antes dos 2 s. Origem baixa: o queixo fica onde está
  // (ele se inclina para a câmera) e a legenda não encosta na barba.
  { de: 54, ate: 95, escala: 1.06, origem: "50% 60%" },
  { de: 309, ate: 367, escala: 1.07 }, // perto de pessoas que não me aturam
  { de: 1017, ate: 1102, escala: 1.06 }, // ... o meu medo já escolheu por mim
];

export type Palavra = { t: string; f: number; vermelho?: boolean };
export type Linha = { tam: number; palavras: Palavra[] };

// Inserção 1: Ir embora sempre vai parecer mais perigoso do que ficar.
export const TEXTO_1: Linha[] = [
  { tam: 128, palavras: [{ t: "IR", f: 776 }, { t: "EMBORA", f: 782 }] },
  {
    tam: 96,
    palavras: [
      { t: "SEMPRE", f: 791 },
      { t: "VAI", f: 811 },
      { t: "PARECER", f: 821 },
    ],
  },
  {
    tam: 128,
    palavras: [
      { t: "MAIS", f: 829 },
      { t: "PERIGOSO", f: 841, vermelho: true },
    ],
  },
  { tam: 108, palavras: [{ t: "DO QUE", f: 859 }, { t: "FICAR", f: 865 }] },
];

// Rosto: Relação ruim ainda parece melhor do que relação nenhuma.
export const TEXTO_ROSTO_LINHAS: Linha[] = [
  {
    tam: 120,
    palavras: [
      { t: "RELAÇÃO", f: 878, vermelho: true },
      { t: "RUIM", f: 889, vermelho: true },
    ],
  },
  {
    tam: 84,
    palavras: [
      { t: "AINDA", f: 898 },
      { t: "PARECE", f: 914 },
      { t: "MELHOR", f: 924 },
    ],
  },
  {
    tam: 76,
    palavras: [
      { t: "DO QUE", f: 938 },
      { t: "RELAÇÃO", f: 954 },
      { t: "NENHUMA", f: 962 },
    ],
  },
];

// Inserção 2: ... você volta a ter controle sobre si.
export const TEXTO_2: Linha[] = [
  {
    tam: 108,
    palavras: [
      { t: "VOCÊ", f: 1168 },
      { t: "VOLTA", f: 1175 },
      { t: "A TER", f: 1189 },
    ],
  },
  {
    tam: 100,
    palavras: [
      { t: "CONTROLE", f: 1205, vermelho: true },
      { t: "SOBRE SI", f: 1216 },
    ],
  },
];
export const TEXTO_2_JANELA = { de: 1168, ate: 1239 };

// Título de abertura, no primeiro quadro, abaixo do queixo: a pergunta que o vídeo
// responde, com palavras dele (dita em 24,5 s). Fica até o primeiro corte dele (3,17 s),
// embaixo da legenda, que segue na posição de sempre.
export const TITULO_JANELA = { de: 0, ate: 95 };
export const TITULO: Linha[] = [
  { tam: 76, palavras: [{ t: "POR QUE VOCÊ", f: -6 }] },
  { tam: 94, palavras: [{ t: "NÃO TERMINA?", f: -6, vermelho: true }] },
];
