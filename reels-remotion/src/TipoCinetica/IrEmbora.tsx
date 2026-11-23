import React, { useMemo } from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import {
  ALTURA_CAIXA,
  ANTON,
  DESCIDA_Q,
  Glifo,
  medirLinha,
  useAnton,
} from "./anton";
import {
  expo,
  impulsoCritico,
  molaSub,
  quedaExpo,
  velocidade,
} from "./fisica";
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

// Batida 1. Texto exato, nada a mais.
const LINHA_1 = "IR EMBORA";
const LINHA_2 = "PARECE MAIS PERIGOSO";
const LINHA_3 = "DO QUE FICAR";

// Tipo: Anton, um corpo só, três linhas no mesmo eixo.
const CAIXA = 93; // altura da caixa alta, em px
const CORPO = CAIXA / ALTURA_CAIXA;
const VAO = 22; // da linha de base até o topo da linha seguinte
const BASE_1 = 303;
const BASE_2 = BASE_1 + VAO + CAIXA;
const BASE_3 = BASE_2 + VAO + CAIXA;
const EMPURRAO = 6; // quanto PERIGOSO levanta a linha de cima

const ABERTURA = 0.25; // obturador a 90 graus: borrão leve

// 0,0 a 1,2 s: IR EMBORA entra pela esquerda e segue para a borda direita.
const TAU_ENTRADA = 0.13;
const V_DERIVA = 230; // px/s, a deriva que sobra depois da entrada
const T_ESTICA = 1.2; // o cordão estica
// 1,2 a 2,2 s: para, o A estica, e a palavra volta para o centro.
const TAU_PARADA = 0.05;
const T_SOLTA = 1.42;
const FOLGA_BORDA = 3; // px entre o pé do A e a linha dos 6%
const ESTICA_A = 17; // px a mais na largura do A
const TAU_ESTICA = 0.07;
const TAU_RELAXA = 0.045;
const OMEGA_VOLTA = 17;
const ZETA_VOLTA = 0.62; // passa do centro uma vez (8%) e para
// Inclinação para a frente, em graus.
const INCLINA_DESEJO = 5;
const INCLINA_TENSAO = 3.5;
const INCLINA_VELOC = 9;

// 2,2 a 3,6 s: PARECE, MAIS e PERIGOSO caem, um por vez.
const QUEDAS = [
  { comeca: 2.22, dura: 0.2, afunda: 2.5 },
  { comeca: 2.48, dura: 0.2, afunda: 2.5 },
  { comeca: 2.76, dura: 0.22, afunda: 4 },
];
const POUSO_PERIGOSO = QUEDAS[2].comeca + QUEDAS[2].dura;
const PESO_QUEDA = 3.2;
const ALTURA_QUEDA = BASE_2 - (BASE_1 + EMPURRAO + 2);
const TAU_EMPURRAO = 0.05;

// 3,6 a 5,0 s: DO QUE FICAR assenta e tudo para.
const T_FICAR = 3.6;
const TAU_FICAR = 0.1;
const ALTURA_FICAR = BASE_3 - (BASE_2 + 2 - DESCIDA_Q * CORPO);

type Viagem = {
  x: (t: number) => number;
  inclina: (t: number) => number;
  estica: (t: number) => number;
};

const criarViagem = (largura: number, folgaDoA: number): Viagem => {
  const xCentro = CENTRO_X - largura / 2;
  const picoEstica = ESTICA_A * expo(T_SOLTA - T_ESTICA, TAU_ESTICA);
  // Onde a palavra para: o pé do A, já esticado, a FOLGA_BORDA da linha segura.
  const xPara = SEGURA.dir - FOLGA_BORDA - picoEstica - largura + folgaDoA;
  // Começa escondida atrás da máscara da margem esquerda.
  const xInicio = SEGURA.esq - largura - 34;

  // Entrada exponencial mais deriva constante, emendada sem tranco na parada.
  const norma = 1 - Math.exp(-T_ESTICA / TAU_ENTRADA);
  const c = Math.exp(-T_ESTICA / TAU_ENTRADA) / (TAU_ENTRADA * norma);
  const delta =
    (xPara - V_DERIVA * TAU_PARADA - xInicio - V_DERIVA * T_ESTICA) /
    (1 + c * TAU_PARADA);
  const vChegada = delta * c + V_DERIVA;
  const xChegada = xPara - vChegada * TAU_PARADA;

  const xSolta =
    xPara - (xPara - xChegada) * Math.exp(-(T_SOLTA - T_ESTICA) / TAU_PARADA);
  const vSolta =
    ((xPara - xChegada) / TAU_PARADA) *
    Math.exp(-(T_SOLTA - T_ESTICA) / TAU_PARADA);

  const x = (t: number): number => {
    if (t < T_ESTICA) {
      return (
        xInicio +
        (delta * (1 - Math.exp(-t / TAU_ENTRADA))) / norma +
        V_DERIVA * t
      );
    }
    if (t < T_SOLTA) {
      return (
        xPara - (xPara - xChegada) * Math.exp(-(t - T_ESTICA) / TAU_PARADA)
      );
    }
    return (
      xCentro +
      molaSub(t - T_SOLTA, OMEGA_VOLTA, ZETA_VOLTA, xSolta - xCentro, vSolta)
    );
  };

  const picoDesejo =
    INCLINA_DESEJO + INCLINA_TENSAO * expo(T_SOLTA - T_ESTICA, TAU_ESTICA);
  const inclina = (t: number): number => {
    let desejo = INCLINA_DESEJO;
    if (t >= T_SOLTA) {
      desejo = picoDesejo * Math.exp(-(t - T_SOLTA) / 0.06);
    } else if (t >= T_ESTICA) {
      desejo = INCLINA_DESEJO + INCLINA_TENSAO * expo(t - T_ESTICA, TAU_ESTICA);
    }
    const v = Math.abs(velocidade(x, t));
    return desejo + INCLINA_VELOC * Math.tanh(v / 1500);
  };

  const estica = (t: number): number => {
    if (t < T_ESTICA) {
      return 0;
    }
    if (t < T_SOLTA) {
      return ESTICA_A * expo(t - T_ESTICA, TAU_ESTICA);
    }
    return picoEstica * Math.exp(-(t - T_SOLTA) / TAU_RELAXA);
  };

  return { x, inclina, estica };
};

/** Linha de base de IR EMBORA: sobe alguns px quando PERIGOSO pousa. */
const base1 = (t: number): number =>
  BASE_1 + EMPURRAO * (1 - expo(t - POUSO_PERIGOSO, TAU_EMPURRAO));

/** Deslocamento vertical de uma palavra da linha 2. null: ainda não entrou. */
const queda = (palavra: number, t: number): number | null => {
  const { comeca, dura, afunda } = QUEDAS[palavra];
  const passou = t - comeca;
  if (passou < 0) {
    return null;
  }
  if (passou < dura) {
    return -ALTURA_QUEDA * (1 - quedaExpo(passou / dura, PESO_QUEDA));
  }
  return impulsoCritico(passou - dura, 30, afunda);
};

/** Deslocamento vertical de DO QUE FICAR. null: ainda não entrou. */
const assenta = (t: number): number | null => {
  if (t < T_FICAR) {
    return null;
  }
  return -ALTURA_FICAR * Math.exp(-(t - T_FICAR) / TAU_FICAR);
};

const Letras: React.FC<{ glifos: Glifo[] }> = ({ glifos }) => {
  return (
    <>
      {glifos.map((g) => (
        <text key={g.ordem} x={g.x} y={0}>
          {g.ch}
        </text>
      ))}
    </>
  );
};

export type IrEmboraProps = {
  /** Cor de fundo da prévia. null: fundo transparente (overlay). */
  fundo: string | null;
};

export const IrEmbora: React.FC<IrEmboraProps> = ({ fundo }) => {
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
    const l3 = medirLinha(LINHA_3, CORPO);
    const a = l1.glifos[l1.glifos.length - 1];
    // O A da Anton: 964 de tinta num avanço de 994 (em 2048).
    const tintaDoA = (964 / 994) * a.avanco;
    const viagem = criarViagem(l1.largura, a.avanco - tintaDoA);
    return { l1, l2, l3, a, tintaDoA, viagem };
  }, [pronta]);

  if (!medidas) {
    return <AbsoluteFill style={{ backgroundColor: fundo ?? "transparent" }} />;
  }

  const { l1, l2, l3, a, tintaDoA, viagem } = medidas;
  const x2 = CENTRO_X - l2.largura / 2;
  const x3 = CENTRO_X - l3.largura / 2;
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
            id="ie-grao"
            quadro={quadro}
            x={0}
            y={0}
            largura={regiao.largura}
            altura={regiao.altura}
          />
          {/* Margem esquerda: IR EMBORA nasce de dentro da área segura. */}
          <linearGradient
            id="ie-borda-esq"
            gradientUnits="userSpaceOnUse"
            x1={SEGURA.esq}
            y1={0}
            x2={SEGURA.esq + 40}
            y2={0}
          >
            <stop offset={0} stopColor="#fff" stopOpacity={0} />
            <stop offset={1} stopColor="#fff" stopOpacity={1} />
          </linearGradient>
          <mask
            id="ie-mascara-1"
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
              fill="url(#ie-borda-esq)"
            />
          </mask>
          {/* Linha 2 cai de trás da linha de base de IR EMBORA. */}
          <linearGradient
            id="ie-borda-2"
            gradientUnits="userSpaceOnUse"
            x1={0}
            y1={BASE_1 + EMPURRAO + 3}
            x2={0}
            y2={BASE_1 + EMPURRAO + 11}
          >
            <stop offset={0} stopColor="#fff" stopOpacity={0} />
            <stop offset={1} stopColor="#fff" stopOpacity={1} />
          </linearGradient>
          <mask
            id="ie-mascara-2"
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
              fill="url(#ie-borda-2)"
            />
          </mask>
          {/* Linha 3 assenta de trás da linha de base da linha 2. */}
          <linearGradient
            id="ie-borda-3"
            gradientUnits="userSpaceOnUse"
            x1={0}
            y1={BASE_2 + 3}
            x2={0}
            y2={BASE_2 + 11}
          >
            <stop offset={0} stopColor="#fff" stopOpacity={0} />
            <stop offset={1} stopColor="#fff" stopOpacity={1} />
          </linearGradient>
          <mask
            id="ie-mascara-3"
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
              fill="url(#ie-borda-3)"
            />
          </mask>
        </defs>

        <g filter="url(#ie-grao)">
          {/* IR EMBORA: vai, é segurada, volta. O A estica no puxão. */}
          <g mask="url(#ie-mascara-1)">
            <Obturador
              id="ie-borrao-1"
              cor={TINTA}
              t={t}
              fps={fps}
              abertura={ABERTURA}
              regiao={regiao}
              medida={(i) => [
                viagem.x(i),
                Math.tan((viagem.inclina(i) * Math.PI) / 180) * CAIXA,
                viagem.estica(i),
                base1(i),
              ]}
            >
              {(i) => (
                <g
                  transform={`translate(${viagem.x(i)} ${base1(i)}) skewX(${-viagem.inclina(i)})`}
                >
                  <Letras glifos={l1.glifos.slice(0, -1)} />
                  <g
                    transform={`translate(${a.x} 0) scale(${1 + viagem.estica(i) / tintaDoA} 1)`}
                  >
                    <text x={0} y={0}>
                      {a.ch}
                    </text>
                  </g>
                </g>
              )}
            </Obturador>
          </g>

          {/* PARECE MAIS PERIGOSO: cada palavra cai pesada; PERIGOSO por último. */}
          <g mask="url(#ie-mascara-2)">
            <Obturador
              id="ie-borrao-2"
              cor={TINTA}
              t={t}
              fps={fps}
              abertura={ABERTURA}
              regiao={regiao}
              medida={(i) => [0, 1].map((p) => queda(p, i) ?? -ALTURA_QUEDA)}
            >
              {(i) => (
                <>
                  {[0, 1].map((p) => {
                    const dy = queda(p, i);
                    if (dy === null) {
                      return null;
                    }
                    return (
                      <g key={p} transform={`translate(${x2} ${BASE_2 + dy})`}>
                        <Letras
                          glifos={l2.glifos.filter((g) => g.palavra === p)}
                        />
                      </g>
                    );
                  })}
                </>
              )}
            </Obturador>
            {/* O vermelho é só de PERIGOSO. */}
            <Obturador
              id="ie-borrao-perigoso"
              cor={VERMELHO}
              t={t}
              fps={fps}
              abertura={ABERTURA}
              regiao={regiao}
              medida={(i) => [queda(2, i) ?? -ALTURA_QUEDA]}
            >
              {(i) => {
                const dy = queda(2, i);
                if (dy === null) {
                  return null;
                }
                return (
                  <g transform={`translate(${x2} ${BASE_2 + dy})`}>
                    <Letras glifos={l2.glifos.filter((g) => g.palavra === 2)} />
                  </g>
                );
              }}
            </Obturador>
          </g>

          {/* DO QUE FICAR: assenta de uma vez, sem passar do ponto. */}
          <g mask="url(#ie-mascara-3)">
            <Obturador
              id="ie-borrao-3"
              cor={TINTA}
              t={t}
              fps={fps}
              abertura={ABERTURA}
              regiao={regiao}
              medida={(i) => [assenta(i) ?? -ALTURA_FICAR]}
            >
              {(i) => {
                const dy = assenta(i);
                if (dy === null) {
                  return null;
                }
                return (
                  <g transform={`translate(${x3} ${BASE_3 + dy})`}>
                    <Letras glifos={l3.glifos} />
                  </g>
                );
              }}
            </Obturador>
          </g>
        </g>
      </svg>
    </AbsoluteFill>
  );
};
