import React, { useMemo } from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import {
  ALTURA_ACENTO,
  ALTURA_CAIXA,
  ANTON,
  Linha,
  medirLinha,
  useAnton,
} from "./anton";
import { expo, misturar, molaCritica } from "./fisica";
import { FiltroGrao } from "./Grao";
import { Obturador } from "./Obturador";
import {
  ALTURA,
  CENTRO_X,
  LARGURA,
  SEGURA,
  TINTA,
  VERMELHO,
} from "./quadro";

// Batida 2: a soltura da batida 1. Texto exato, nada a mais.
const LINHA_1 = "VOCÊ SÓ VOLTA";
const LINHA_2 = "A TER VOTO";

// Tipo: Anton, um corpo só, duas linhas no mesmo eixo.
const CAIXA = 143; // altura da caixa alta, em px
const CORPO = CAIXA / ALTURA_CAIXA;
const VAO = 31; // da linha de base até o topo da linha seguinte
const BASE_1 = 322;
const BASE_2 = BASE_1 + VAO + CAIXA;

const ABERTURA = 0.25;

// 0,0 a 1,4 s: a linha vermelha entra pelo canto de baixo, à direita, solta.
const ANCORA = { x: 1002, y: 596 };
const ESPESSURA = 13;
const T_DESENHO = 1.4;
const TAU_DESENHO = 0.3;
const PENDULO_GRAUS = 4; // o cadarço inteiro balança em torno da âncora
const PENDULO_HZ = 0.6;
const ONDA_PX = 14; // onda leve que corre até a ponta solta
const ONDA_HZ = 0.85;
const TAU_BALANCO = 2.4;

// 1,4 a 2,8 s: VOCÊ SÓ VOLTA sobe, letra depois de letra, sem passar do ponto.
const T_LETRAS = 1.4;
const PASSO_LETRA = 0.055;
const OMEGA_LETRA = 10;
const SUBIDA_1 = ALTURA_ACENTO * CORPO + 15;

// 2,8 a 4,2 s: A TER VOTO sobe; a linha para, endireita e pousa sob VOTO.
const T_LINHA_2 = 2.8;
const PASSO_PALAVRA = 0.1;
const OMEGA_PALAVRA = 11;
const SUBIDA_2 = CAIXA + 15;
const T_PARA = 2.9; // para de balançar
const TAU_PARA = 0.14;
const T_FORMA = 2.95; // endireita
const OMEGA_FORMA = 11;
const T_POUSO = 3.02; // pousa
const OMEGA_POUSO = 8.5;
const Y_SUBLINHADO = BASE_2 + 28;

// 4,2 a 5,0 s: tudo parado; o sublinhado fecha com uma cauda de marcador.
const T_CAUDA = 4.2;
const TAU_CAUDA = 0.07;
const CAUDA_PX = 46;

const N_CORPO = 120;
const N_CAUDA = 24;

type Ponto = [number, number];

const sobeLetra = (ordem: number, t: number): number | null => {
  const passou = t - (T_LETRAS + PASSO_LETRA * ordem);
  if (passou < 0) {
    return null;
  }
  return SUBIDA_1 * (1 - molaCritica(passou, OMEGA_LETRA));
};

const sobePalavra = (palavra: number, t: number): number | null => {
  const passou = t - (T_LINHA_2 + PASSO_PALAVRA * palavra);
  if (passou < 0) {
    return null;
  }
  return SUBIDA_2 * (1 - molaCritica(passou, OMEGA_PALAVRA));
};

/** Quanto a linha ainda balança: decai devagar e some quando ela para. */
const balanco = (t: number): number => {
  if (t < T_PARA) {
    return Math.exp(-Math.max(t, 0) / TAU_BALANCO);
  }
  return Math.exp(-T_PARA / TAU_BALANCO) * Math.exp(-(t - T_PARA) / TAU_PARA);
};

/** A linha solta: u = 0 na âncora (canto de baixo, à direita), u = 1 na ponta. */
const solto = (u: number, t: number): Ponto => {
  const vida = balanco(t);
  // Forma de descanso: um S frouxo, com a ponta solta virada para cima.
  const curva = u > 0.78 ? Math.pow((u - 0.78) / 0.22, 2) : 0;
  const dx = -470 * u + 14 * Math.sin(2 * Math.PI * 1.1 * u);
  const dy =
    -44 * u -
    30 * Math.sin(2 * Math.PI * 0.95 * u + 0.15) * (0.3 + 0.7 * u) -
    20 * curva;
  // Pêndulo: gira em torno da âncora.
  const giro =
    ((PENDULO_GRAUS * Math.PI) / 180) *
    Math.sin(2 * Math.PI * PENDULO_HZ * t + 0.3) *
    vida;
  const rx = dx * Math.cos(giro) - dy * Math.sin(giro);
  const ry = dx * Math.sin(giro) + dy * Math.cos(giro);
  // Onda: cresce para a ponta solta.
  const fase = 2 * Math.PI * ONDA_HZ * t - 1.9 * Math.PI * u;
  const ponta = Math.pow(u, 1.5) * vida;
  return [
    ANCORA.x + rx + 0.3 * ONDA_PX * ponta * Math.cos(fase),
    ANCORA.y + ry + ONDA_PX * ponta * Math.sin(fase + 0.4),
  ];
};

type Voto = { esq: number; dir: number };

/** O sublinhado: feito à mão, sobe de leve para a direita, com tremor. */
const sublinhado = (u: number, voto: Voto): Ponto => {
  const xDir = voto.dir + 9;
  const xEsq = voto.esq - 7;
  return [
    xDir - u * (xDir - xEsq),
    Y_SUBLINHADO -
      2.5 +
      5 * u +
      1.5 * Math.sin(2 * Math.PI * 1.6 * u + 1) +
      0.8 * Math.sin(2 * Math.PI * 3.7 * u),
  ];
};

const centro = (pontos: Ponto[]): Ponto => {
  let x = 0;
  let y = 0;
  for (const p of pontos) {
    x += p[0];
    y += p[1];
  }
  return [x / pontos.length, y / pontos.length];
};

const comprimento = (pontos: Ponto[]): number => {
  let soma = 0;
  for (let i = 1; i < pontos.length; i++) {
    soma += Math.hypot(
      pontos[i][0] - pontos[i - 1][0],
      pontos[i][1] - pontos[i - 1][1],
    );
  }
  return soma;
};

const US = new Array(N_CORPO).fill(0).map((_, i) => i / (N_CORPO - 1));

/** Linha central da cauda: sai da ponta direita e escorrega para baixo. */
const centroDaCauda = (w: number, origem: Ponto): Ponto => [
  origem[0] + CAUDA_PX * w,
  origem[1] + 2 * w + 13 * w * w,
];

/** A cauda afina, como marcador saindo do papel. */
const meiaLargura = (w: number): number =>
  (ESPESSURA / 2) * (1 - 0.72 * Math.pow(w, 1.2));

/** Contorno da cauda até a fração `frente` do seu comprimento. */
const fitaDaCauda = (frente: number, origem: Ponto): string => {
  const passos = Math.max(2, Math.ceil(N_CAUDA * frente));
  const cima: Ponto[] = [];
  const baixo: Ponto[] = [];
  for (let i = 0; i <= passos; i++) {
    const w = (frente * i) / passos;
    const c = centroDaCauda(w, origem);
    const adiante = centroDaCauda(w + 0.01, origem);
    const dx = adiante[0] - c[0];
    const dy = adiante[1] - c[1];
    const norma = Math.hypot(dx, dy);
    const h = meiaLargura(w);
    cima.push([c[0] + (dy / norma) * h, c[1] - (dx / norma) * h]);
    baixo.push([c[0] - (dy / norma) * h, c[1] + (dx / norma) * h]);
  }
  const raio = meiaLargura(frente).toFixed(2);
  const ponto = (p: Ponto) => `${p[0].toFixed(2)} ${p[1].toFixed(2)}`;
  const ultimo = baixo[baixo.length - 1];
  return (
    `M${cima.map(ponto).join(" L")} ` +
    `A${raio} ${raio} 0 0 1 ${ponto(ultimo)} ` +
    `L${baixo.reverse().map(ponto).join(" L")} Z`
  );
};

type Traco = {
  /** Corpo da linha, da ponta direita (âncora) para a esquerda. */
  d: string;
  comprimento: number;
  /** Quanto do corpo já foi desenhado, de 0 a 1. */
  desenho: number;
  /** Cauda de marcador, ou null antes de ela começar. */
  cauda: string | null;
  amostra: number[];
};

/** A linha inteira num instante. */
const tracar = (t: number, voto: Voto): Traco => {
  const mForma = molaCritica(t - T_FORMA, OMEGA_FORMA);
  const mPouso = molaCritica(t - T_POUSO, OMEGA_POUSO);
  const soltos = US.map((u) => solto(u, t));
  const alvos = US.map((u) => sublinhado(u, voto));
  const cSolto = centro(soltos);
  const cAlvo = centro(alvos);
  const corpo: Ponto[] = US.map((_, i) => [
    misturar(cSolto[0], cAlvo[0], mPouso) +
      misturar(soltos[i][0] - cSolto[0], alvos[i][0] - cAlvo[0], mForma),
    misturar(cSolto[1], cAlvo[1], mPouso) +
      misturar(soltos[i][1] - cSolto[1], alvos[i][1] - cAlvo[1], mForma),
  ]);

  const desenho =
    t >= T_DESENHO ? 1 : expo(t, TAU_DESENHO) / expo(T_DESENHO, TAU_DESENHO);
  const fecha = expo(t - T_CAUDA, TAU_CAUDA);

  const d = corpo
    .map((p, i) => `${i === 0 ? "M" : "L"}${p[0].toFixed(2)} ${p[1].toFixed(2)}`)
    .join(" ");

  const amostra: number[] = [desenho * 500, fecha * CAUDA_PX];
  for (let i = 0; i < corpo.length; i += 17) {
    amostra.push(corpo[i][0], corpo[i][1]);
  }
  const ultimo = corpo[corpo.length - 1];
  amostra.push(ultimo[0], ultimo[1]);

  return {
    d,
    comprimento: comprimento(corpo),
    desenho,
    cauda: fecha > 0.02 ? fitaDaCauda(fecha, corpo[0]) : null,
    amostra,
  };
};

export type VoceSoVoltaProps = {
  /** Cor de fundo da prévia. null: fundo transparente (overlay). */
  fundo: string | null;
};

const xDaLinha = (linha: Linha): number => CENTRO_X - linha.largura / 2;

export const VoceSoVolta: React.FC<VoceSoVoltaProps> = ({ fundo }) => {
  const quadro = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pronta = useAnton();
  const t = quadro / fps;

  const medidas = useMemo(() => {
    if (!pronta) {
      return null;
    }
    const l1 = medirLinha(LINHA_1, CORPO);
    const l2 = medirLinha(LINHA_2, CORPO);
    const letrasDeVoto = l2.glifos.filter((g) => g.palavra === 2);
    const v = letrasDeVoto[0];
    const o = letrasDeVoto[letrasDeVoto.length - 1];
    // Tinta de VOTO: o V começa 23 e o O acaba 64 antes do avanço (em 2048).
    const voto: Voto = {
      esq: xDaLinha(l2) + v.x + (23 / 2048) * CORPO,
      dir: xDaLinha(l2) + o.x + o.avanco - (64 / 2048) * CORPO,
    };
    return { l1, l2, voto };
  }, [pronta]);

  if (!medidas) {
    return <AbsoluteFill style={{ backgroundColor: fundo ?? "transparent" }} />;
  }

  const { l1, l2, voto } = medidas;
  const x1 = xDaLinha(l1);
  const x2 = xDaLinha(l2);
  const regiao = { x: 0, y: 0, largura: LARGURA, altura: SEGURA.base + 20 };
  const tipo: React.CSSProperties = {
    fontFamily: ANTON,
    fontSize: CORPO,
    textRendering: "geometricPrecision",
  };

  return (
    <AbsoluteFill style={{ backgroundColor: fundo ?? "transparent" }}>
      <svg
        width={LARGURA}
        height={ALTURA}
        viewBox={`0 0 ${LARGURA} ${ALTURA}`}
        style={tipo}
      >
        <defs>
          <FiltroGrao
            id="vv-grao"
            quadro={quadro}
            x={regiao.x}
            y={regiao.y}
            largura={regiao.largura}
            altura={regiao.altura}
          />
          {/* Borda de marcador: o traço não sai liso como régua. */}
          <filter
            id="vv-marcador"
            filterUnits="userSpaceOnUse"
            x={regiao.x}
            y={regiao.y}
            width={regiao.largura}
            height={regiao.altura}
            colorInterpolationFilters="sRGB"
          >
            <feTurbulence
              type="fractalNoise"
              baseFrequency="0.03 0.11"
              numOctaves={2}
              seed={4}
              result="tremor"
            />
            <feDisplacementMap
              in="SourceGraphic"
              in2="tremor"
              scale={3.2}
              xChannelSelector="R"
              yChannelSelector="G"
            />
          </filter>
          {/* As letras sobem de trás da própria linha de base. */}
          <linearGradient
            id="vv-borda-1"
            gradientUnits="userSpaceOnUse"
            x1={0}
            y1={BASE_1 + 3}
            x2={0}
            y2={BASE_1 + 13}
          >
            <stop offset={0} stopColor="#fff" stopOpacity={1} />
            <stop offset={1} stopColor="#fff" stopOpacity={0} />
          </linearGradient>
          <mask
            id="vv-mascara-1"
            maskUnits="userSpaceOnUse"
            x={0}
            y={0}
            width={LARGURA}
            height={SEGURA.base}
            style={{ maskType: "alpha" }}
          >
            <rect
              x={0}
              y={0}
              width={LARGURA}
              height={SEGURA.base}
              fill="url(#vv-borda-1)"
            />
          </mask>
          <linearGradient
            id="vv-borda-2"
            gradientUnits="userSpaceOnUse"
            x1={0}
            y1={BASE_2 + 3}
            x2={0}
            y2={BASE_2 + 13}
          >
            <stop offset={0} stopColor="#fff" stopOpacity={1} />
            <stop offset={1} stopColor="#fff" stopOpacity={0} />
          </linearGradient>
          <mask
            id="vv-mascara-2"
            maskUnits="userSpaceOnUse"
            x={0}
            y={0}
            width={LARGURA}
            height={SEGURA.base}
            style={{ maskType: "alpha" }}
          >
            <rect
              x={0}
              y={0}
              width={LARGURA}
              height={SEGURA.base}
              fill="url(#vv-borda-2)"
            />
          </mask>
        </defs>

        {/* A linha vermelha: cadarço solto que vira sublinhado. Sem grão. */}
        <g filter="url(#vv-marcador)">
          <Obturador
            id="vv-borrao-linha"
            cor={VERMELHO}
            t={t}
            fps={fps}
            abertura={ABERTURA}
            regiao={regiao}
            medida={(i) => tracar(i, voto).amostra}
          >
            {(i) => {
              const traco = tracar(i, voto);
              if (traco.comprimento * traco.desenho < 0.75) {
                return null;
              }
              return (
                <>
                  {/* O corpo se desenha a partir da âncora, por stroke-dashoffset. */}
                  <path
                    d={traco.d}
                    fill="none"
                    stroke="currentColor"
                    strokeWidth={ESPESSURA}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeDasharray={traco.comprimento}
                    strokeDashoffset={traco.comprimento * (1 - traco.desenho)}
                  />
                  {traco.cauda ? <path d={traco.cauda} /> : null}
                </>
              );
            }}
          </Obturador>
        </g>

        {/* O tipo, com grão só nele. */}
        <g filter="url(#vv-grao)">
          <g mask="url(#vv-mascara-1)">
            <Obturador
              id="vv-borrao-1"
              cor={TINTA}
              t={t}
              fps={fps}
              abertura={ABERTURA}
              regiao={regiao}
              medida={(i) =>
                l1.glifos.map((g) => sobeLetra(g.ordem, i) ?? SUBIDA_1)
              }
            >
              {(i) => (
                <g transform={`translate(${x1} ${BASE_1})`}>
                  {l1.glifos.map((g) => {
                    const dy = sobeLetra(g.ordem, i);
                    if (dy === null) {
                      return null;
                    }
                    return (
                      <text key={g.ordem} x={g.x} y={dy}>
                        {g.ch}
                      </text>
                    );
                  })}
                </g>
              )}
            </Obturador>
          </g>

          <g mask="url(#vv-mascara-2)">
            <Obturador
              id="vv-borrao-2"
              cor={TINTA}
              t={t}
              fps={fps}
              abertura={ABERTURA}
              regiao={regiao}
              medida={(i) => [0, 1, 2].map((p) => sobePalavra(p, i) ?? SUBIDA_2)}
            >
              {(i) => (
                <g transform={`translate(${x2} ${BASE_2})`}>
                  {l2.glifos.map((g) => {
                    const dy = sobePalavra(g.palavra, i);
                    if (dy === null) {
                      return null;
                    }
                    return (
                      <text key={g.ordem} x={g.x} y={dy}>
                        {g.ch}
                      </text>
                    );
                  })}
                </g>
              )}
            </Obturador>
          </g>
        </g>
      </svg>
    </AbsoluteFill>
  );
};
