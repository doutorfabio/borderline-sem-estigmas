import React, { useEffect, useState } from "react";
import {
  AbsoluteFill,
  OffthreadVideo,
  Sequence,
  continueRender,
  delayRender,
  staticFile,
  useCurrentFrame,
} from "remotion";
import { Colagem, Pedaco } from "./Colagem";
import {
  APROXIMACOES,
  CENTRO_X,
  INSERCAO_1,
  INSERCAO_2,
  INSERCAO_CEL,
  INSERCAO_MESA,
  TEXTO_1,
  TEXTO_2,
  TEXTO_2_JANELA,
  TEXTO_ROSTO,
  TEXTO_ROSTO_LINHAS,
  TITULO,
  TITULO_JANELA,
} from "./dados";
import { BLOCOS } from "./legenda";

const useFontes = () => {
  const [handle] = useState(() => delayRender("fontes"));
  useEffect(() => {
    const anton = new FontFace(
      "Anton",
      `url('${staticFile("fonts/anton.woff2")}') format('woff2')`,
    );
    const inter = new FontFace(
      "InterSB",
      `url('${staticFile("fonts/Inter-SemiBold.otf")}') format('opentype')`,
    );
    Promise.all([anton.load(), inter.load()]).then((fs) => {
      fs.forEach((f) => document.fonts.add(f));
      continueRender(handle);
    });
  }, [handle]);
};

// Legenda palavra por palavra, abaixo do queixo. Até 3 palavras por bloco.
// Palavra comum: etiqueta de papel carvão com Inter SemiBold creme (branco com
// sombra sumia na camiseta branca), entra quando é dita.
// Palavra de impacto: recorte de papel (o mesmo da colagem), bate na tela.
const Legenda: React.FC = () => {
  const frame = useCurrentFrame();
  const escondida =
    (frame >= INSERCAO_1.de && frame < TEXTO_ROSTO.ate) ||
    (frame >= TEXTO_2_JANELA.de && frame < TEXTO_2_JANELA.ate);
  if (escondida) return null;
  const k = BLOCOS.findIndex((b) => frame >= b.de && frame < b.ate);
  if (k < 0) return null;
  const bloco = BLOCOS[k];
  return (
    <div
      style={{
        position: "absolute",
        left: CENTRO_X,
        top: 1250,
        transform: "translate(-50%, -50%)",
        display: "flex",
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "center",
        gap: 9,
        whiteSpace: "nowrap",
      }}
    >
      {bloco.tokens.map((tk, j) => {
        if (tk.tipo !== "n") {
          return (
            <Pedaco
              key={j}
              texto={tk.t}
              tam={88}
              vermelho={tk.tipo === "vermelho"}
              entra={tk.f}
              id={900 + k * 7 + j}
            />
          );
        }
        return (
          <Pedaco
            key={j}
            texto={tk.t}
            tam={52}
            carvao
            entra={tk.f}
            id={900 + k * 7 + j}
          />
        );
      })}
    </div>
  );
};

const Textos: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <>
      {frame >= TITULO_JANELA.de && frame < TITULO_JANELA.ate && (
        <Colagem linhas={TITULO} topo={1314} centroX={CENTRO_X} idBase={800} entrelinha={-6} />
      )}
      {frame >= INSERCAO_1.de && frame < INSERCAO_1.ate && (
        <Colagem linhas={TEXTO_1} topo={215} centroX={CENTRO_X} idBase={100} />
      )}
      {frame >= TEXTO_ROSTO.de && frame < TEXTO_ROSTO.ate && (
        <Colagem
          linhas={TEXTO_ROSTO_LINHAS}
          topo={134}
          centroX={CENTRO_X}
          idBase={300}
          entrelinha={-6}
        />
      )}
      {frame >= TEXTO_2_JANELA.de && frame < TEXTO_2_JANELA.ate && (
        <Colagem linhas={TEXTO_2} topo={235} centroX={CENTRO_X} idBase={500} />
      )}
    </>
  );
};

// Só as camadas de texto, com fundo transparente, para medir a área segura.
export const IrEmboraTexto: React.FC = () => {
  useFontes();
  return (
    <AbsoluteFill>
      <Textos />
      <Legenda />
    </AbsoluteFill>
  );
};

export const IrEmbora: React.FC = () => {
  useFontes();
  const frame = useCurrentFrame();
  const ap = APROXIMACOES.find((a) => frame >= a.de && frame < a.ate);
  const escala = ap ? ap.escala : 1;

  return (
    <AbsoluteFill style={{ backgroundColor: "#0d0d0d" }}>
      <AbsoluteFill
        style={{
          transform: `scale(${escala})`,
          transformOrigin: ap?.origem ?? "50% 32%",
        }}
      >
        <OffthreadVideo src={staticFile("ir-embora/talk.mp4")} muted />
      </AbsoluteFill>

      <Sequence
        from={INSERCAO_MESA.de}
        durationInFrames={INSERCAO_MESA.ate - INSERCAO_MESA.de}
        layout="none"
      >
        <AbsoluteFill>
          <OffthreadVideo src={staticFile("ir-embora/brollMesa.mp4")} muted />
        </AbsoluteFill>
      </Sequence>

      <Sequence
        from={INSERCAO_CEL.de}
        durationInFrames={INSERCAO_CEL.ate - INSERCAO_CEL.de}
        layout="none"
      >
        <AbsoluteFill>
          <OffthreadVideo src={staticFile("ir-embora/brollCel.mp4")} muted />
        </AbsoluteFill>
      </Sequence>

      <Sequence
        from={INSERCAO_1.de}
        durationInFrames={INSERCAO_1.ate - INSERCAO_1.de}
        layout="none"
      >
        <AbsoluteFill>
          <OffthreadVideo src={staticFile("ir-embora/brollA.mp4")} muted />
        </AbsoluteFill>
      </Sequence>

      <Sequence
        from={INSERCAO_2.de}
        durationInFrames={INSERCAO_2.ate - INSERCAO_2.de}
        layout="none"
      >
        <AbsoluteFill>
          <OffthreadVideo src={staticFile("ir-embora/brollB.mp4")} muted />
        </AbsoluteFill>
      </Sequence>

      <Textos />
      <Legenda />
    </AbsoluteFill>
  );
};
