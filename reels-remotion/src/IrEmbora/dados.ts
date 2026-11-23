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
export const INSERCAO_1 = { de: 776, ate: 878 }; // 25,87 a 29,27 s
export const INSERCAO_2 = { de: 1102, ate: 1239 }; // 36,73 a 41,30 s

// Texto grande sobre o rosto.
export const TEXTO_ROSTO = { de: 878, ate: 985 }; // 29,27 a 32,83 s

// Aproximações secas no rosto, sempre em começo de frase e nunca em B-roll.
export const APROXIMACOES = [
  { de: 309, ate: 367, escala: 1.07 }, // perto de pessoas que não me aturam
  { de: 544, ate: 607, escala: 1.07 }, // daí você olha de novo e não vem de novo
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

// Legenda pequena, exatamente como falado. Quebra de linha feita à mão.
// de/ate em segundos da gravação.
export const LEGENDAS: { de: number; ate: number; linhas: string[] }[] = [
  { de: 0.0, ate: 1.76, linhas: ["E se eu tiver as duas coisas", "ao mesmo tempo,"] },
  { de: 1.76, ate: 3.04, linhas: ["borderline e pânico?"] },
  { de: 3.04, ate: 4.24, linhas: ["Uma parte minha quer correr"] },
  { de: 4.24, ate: 6.58, linhas: ["e a outra morre de pavor", "de ficar sozinha."] },
  { de: 6.6, ate: 8.04, linhas: ["Então eu faço o pior dos dois,"] },
  { de: 8.08, ate: 8.78, linhas: ["eu fico."] },
  { de: 8.82, ate: 10.28, linhas: ["Fico no lugar que me assusta,"] },
  { de: 10.28, ate: 12.16, linhas: ["perto de pessoas", "que não me aturam,"] },
  { de: 12.16, ate: 13.92, linhas: ["mas tendo que fazer", "aquele sorrisinho"] },
  { de: 13.92, ate: 15.58, linhas: ["e dizer que tá adorável."] },
  { de: 15.6, ate: 16.76, linhas: ["Então você fica", "com o celular na mão"] },
  { de: 16.76, ate: 18.08, linhas: ["esperando uma resposta", "que não vem,"] },
  { de: 18.1, ate: 20.12, linhas: ["daí você olha de novo", "e não vem de novo,"] },
  { de: 20.16, ate: 22.1, linhas: ["daí você pede desculpa", "por perguntar,"] },
  { de: 22.1, ate: 23.48, linhas: ["pede desculpa por existir,"] },
  { de: 23.48, ate: 24.4, linhas: ["aí todo mundo pergunta,"] },
  { de: 24.46, ate: 25.84, linhas: ["mas por que você", "não termina então?"] },
  // 25,87 a 32,83 s: textos grandes na tela, legenda escondida
  { de: 32.88, ate: 34.32, linhas: ["Não é que eu goste de sofrer,"] },
  { de: 34.32, ate: 36.66, linhas: ["mas é que o meu medo", "já escolheu por mim."] },
  { de: 36.74, ate: 38.9, linhas: ["No dia que esse medo ameniza,"] },
  // 38,92 a 41,30 s: texto grande na tela, legenda escondida
  { de: 41.3, ate: 42.14, linhas: ["Se você também é assim,"] },
  { de: 42.18, ate: 43.04, linhas: ["deixa um like aqui."] },
];
