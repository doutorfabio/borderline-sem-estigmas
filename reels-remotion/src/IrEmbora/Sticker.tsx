import React, { useEffect, useState } from "react";
import { AbsoluteFill, continueRender, delayRender, staticFile } from "remotion";
import { Pedaco } from "./Colagem";

// Sticker de papel recortado, fundo transparente, com borda branca de adesivo.
export const Sticker: React.FC<{ texto: string; vermelho: boolean; id: number }> = ({ texto, vermelho, id }) => {
  const [h] = useState(() => delayRender("fonte"));
  useEffect(() => {
    const f = new FontFace("Anton", `url('${staticFile("fonts/anton.woff2")}') format('woff2')`);
    f.load().then((x) => { document.fonts.add(x); continueRender(h); });
  }, [h]);
  const contorno = [0, 45, 90, 135, 180, 225, 270, 315]
    .map((a) => `drop-shadow(${(Math.cos((a * Math.PI) / 180) * 14).toFixed(1)}px ${(Math.sin((a * Math.PI) / 180) * 14).toFixed(1)}px 0 #FFFFFF)`)
    .join(" ");
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <div style={{ filter: `${contorno} drop-shadow(0 16px 22px rgba(0,0,0,0.35))`, transform: "rotate(-4deg)" }}>
        <Pedaco texto={texto} tam={260} vermelho={vermelho} entra={-20} id={id} />
      </div>
    </AbsoluteFill>
  );
};
