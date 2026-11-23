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
import { Colagem } from "./Colagem";
import {
  APROXIMACOES,
  CENTRO_X,
  FPS,
  INSERCAO_1,
  INSERCAO_2,
  LEGENDAS,
  TEXTO_1,
  TEXTO_2,
  TEXTO_2_JANELA,
  TEXTO_ROSTO,
  TEXTO_ROSTO_LINHAS,
} from "./dados";

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

const Legenda: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  const escondida =
    (frame >= INSERCAO_1.de && frame < TEXTO_ROSTO.ate) ||
    (frame >= TEXTO_2_JANELA.de && frame < TEXTO_2_JANELA.ate);
  if (escondida) return null;
  const atual = LEGENDAS.find((l) => t >= l.de && t < l.ate);
  if (!atual) return null;
  return (
    <div
      style={{
        position: "absolute",
        left: CENTRO_X,
        top: 1250,
        transform: "translate(-50%, -50%)",
        width: 800,
        textAlign: "center",
        fontFamily: "InterSB",
        fontWeight: 600,
        fontSize: 48,
        lineHeight: 1.22,
        color: "#FFFFFF",
        textShadow:
          "0 2px 10px rgba(0,0,0,0.62), 0 1px 3px rgba(0,0,0,0.55), 0 0 22px rgba(0,0,0,0.28)",
      }}
    >
      {atual.linhas.map((l, i) => (
        <div key={i} style={{ whiteSpace: "nowrap" }}>
          {l}
        </div>
      ))}
    </div>
  );
};

const Textos: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <>
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
        style={{ transform: `scale(${escala})`, transformOrigin: "50% 32%" }}
      >
        <OffthreadVideo src={staticFile("ir-embora/talk.mp4")} muted />
      </AbsoluteFill>

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
