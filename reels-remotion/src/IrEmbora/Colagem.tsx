import React from "react";
import { useCurrentFrame } from "remotion";
import { CARVAO, CREME, Linha, VERMELHO } from "./dados";

// Colagem de papel recortado, em stop motion. Cada palavra é um pedaço de
// papel que bate na tela no quadro em que é falada.

const semente = (n: number) => {
  const x = Math.sin(n * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x);
};

const GRAO =
  "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>\")";

const recorte = (id: number, folga: number) => {
  const a = 1 + semente(id + 1) * folga;
  const b = 1 + semente(id + 2) * folga;
  const c = 1 + semente(id + 3) * folga;
  const d = 1 + semente(id + 4) * folga;
  const e = 18 + semente(id + 5) * 60;
  return `polygon(0px ${a}px, ${e}% 0px, calc(100% - ${b}px) ${b * 0.6}px, 100% calc(100% - ${c}px), ${100 - e}% 100%, ${d}px calc(100% - ${d * 0.5}px))`;
};

const Pedaco: React.FC<{
  texto: string;
  tam: number;
  vermelho?: boolean;
  entra: number;
  id: number;
}> = ({ texto, tam, vermelho, entra, id }) => {
  const frame = useCurrentFrame();
  const lf = frame - entra;
  // Antes de entrar, o pedaço fica invisível mas ocupa o lugar exato,
  // para a linha não andar quando a palavra chegar.
  const invisivel = lf < 0;

  const giroBase = (semente(id) - 0.5) * 3.2;
  const sobeBase = (semente(id + 9) - 0.5) * 8;

  // Três poses, duas de 2 quadros cada, depois assenta.
  let escala = 1;
  let giro = giroBase;
  let dy = sobeBase;
  let sombra = 7;
  if (invisivel) {
    // pose de descanso
  } else if (lf < 2) {
    escala = 1.1;
    giro = giroBase + (semente(id + 7) > 0.5 ? 3.5 : -3.5);
    dy = sobeBase - 8;
    sombra = 20;
  } else if (lf < 4) {
    escala = 0.965;
    giro = giroBase - 1.4;
    dy = sobeBase + 3;
    sombra = 4;
  } else {
    // Respiro de stop motion: troca de pose a cada 6 quadros, bem pequeno.
    const passo = Math.floor(lf / 6);
    giro = giroBase + (semente(id + passo * 13) - 0.5) * 0.7;
    dy = sobeBase + (semente(id + passo * 29) - 0.5) * 1.6;
  }

  const fundo = vermelho ? VERMELHO : CREME;
  const cor = vermelho ? CREME : CARVAO;

  const papel = (
    <div
      style={{
        position: "relative",
        background: fundo,
        clipPath: recorte(id, vermelho ? 5 : 7),
        padding: `${tam * 0.07}px ${tam * 0.16}px ${tam * 0.05}px`,
      }}
    >
      {/* meio-tom impresso numa ponta do papel */}
      {!vermelho && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            backgroundImage:
              "radial-gradient(circle at center, rgba(22,22,22,0.20) 0 1.5px, transparent 1.7px)",
            backgroundSize: "7px 7px",
            WebkitMaskImage:
              semente(id + 3) > 0.5
                ? "linear-gradient(100deg, black 0%, transparent 34%)"
                : "linear-gradient(280deg, black 0%, transparent 34%)",
          }}
        />
      )}
      {/* fibra do papel */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: GRAO,
          mixBlendMode: "multiply",
          opacity: vermelho ? 0.5 : 0.32,
        }}
      />
      <span
        style={{
          position: "relative",
          display: "block",
          fontFamily: "Anton",
          fontSize: tam,
          lineHeight: 1.08,
          letterSpacing: "0.012em",
          color: cor,
          whiteSpace: "nowrap",
        }}
      >
        {texto}
      </span>
    </div>
  );

  return (
    <div
      style={{
        visibility: invisivel ? "hidden" : "visible",
        transform: `translateY(${dy}px) rotate(${giro}deg) scale(${escala})`,
        filter: `drop-shadow(0px ${sombra}px ${sombra * 0.9}px rgba(0,0,0,0.42))`,
      }}
    >
      {vermelho ? (
        // filete creme em volta do papel vermelho
        <div
          style={{
            background: CREME,
            padding: 7,
            clipPath: recorte(id + 50, 6),
          }}
        >
          {papel}
        </div>
      ) : (
        papel
      )}
    </div>
  );
};

export const Colagem: React.FC<{
  linhas: Linha[];
  topo: number;
  centroX: number;
  idBase: number;
  entrelinha?: number;
}> = ({ linhas, topo, centroX, idBase, entrelinha = -4 }) => {
  return (
    <div
      style={{
        position: "absolute",
        top: topo,
        left: centroX,
        transform: "translateX(-50%)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: entrelinha,
      }}
    >
      {linhas.map((linha, i) => (
        <div
          key={i}
          style={{
            display: "flex",
            flexDirection: "row",
            alignItems: "center",
            gap: Math.round(linha.tam * 0.06),
          }}
        >
          {linha.palavras.map((p, j) => (
            <Pedaco
              key={j}
              texto={p.t}
              tam={linha.tam}
              vermelho={p.vermelho}
              entra={p.f}
              id={idBase + i * 10 + j}
            />
          ))}
        </div>
      ))}
    </div>
  );
};
