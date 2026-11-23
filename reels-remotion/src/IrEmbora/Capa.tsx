import React, { useEffect, useState } from "react";
import {
  AbsoluteFill,
  Img,
  continueRender,
  delayRender,
  staticFile,
} from "remotion";
import { Colagem } from "./Colagem";
import { Linha } from "./dados";

// Capa: quadro real da gravação no momento do texto grande (quadro 980).
// O texto vai no meio, abaixo do queixo, para sobreviver ao recorte 3:4 da grade.
const LINHAS: Linha[] = [
  { tam: 132, palavras: [{ t: "BORDERLINE", f: 0, vermelho: true }] },
  { tam: 100, palavras: [{ t: "RELAÇÃO", f: 0 }, { t: "RUIM", f: 0 }] },
  {
    tam: 78,
    palavras: [
      { t: "AINDA", f: 0 },
      { t: "PARECE", f: 0 },
      { t: "MELHOR", f: 0 },
    ],
  },
  {
    tam: 70,
    palavras: [
      { t: "DO QUE", f: 0 },
      { t: "RELAÇÃO", f: 0 },
      { t: "NENHUMA", f: 0 },
    ],
  },
];

export const IrEmboraCapa: React.FC = () => {
  const [handle] = useState(() => delayRender("fonte"));
  useEffect(() => {
    const anton = new FontFace(
      "Anton",
      `url('${staticFile("fonts/anton.woff2")}') format('woff2')`,
    );
    anton.load().then((f) => {
      document.fonts.add(f);
      continueRender(handle);
    });
  }, [handle]);
  return (
    <AbsoluteFill style={{ backgroundColor: "#0d0d0d" }}>
      <Img src={staticFile("ir-embora/capa-base.png")} />
      <Colagem linhas={LINHAS} topo={1072} centroX={540} idBase={700} entrelinha={-6} />
    </AbsoluteFill>
  );
};
