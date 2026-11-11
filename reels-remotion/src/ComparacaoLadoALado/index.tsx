import { useEffect } from "react";
import { AbsoluteFill } from "remotion";
import { z } from "zod";
import { useAnimeTimeline } from "../anime/useAnimeTimeline";
import { loadFont, TheBoldFont } from "../load-font";

// Modelo de comparação simultânea: câmera parada, dois lados com rótulo,
// a diferença cresce na tela. Troque os rótulos no painel de props do Studio.
export const comparacaoSchema = z.object({
  rotuloEsquerda: z.string(),
  rotuloDireita: z.string(),
  corDestaque: z.string(),
});

const BLOCOS = 6;
const BLOCO_ALTURA = 110;

const Pilha: React.FC<{ lado: "esq" | "dir"; cor: string }> = ({
  lado,
  cor,
}) => {
  return (
    <div
      style={{
        position: "relative",
        width: 300,
        height: BLOCOS * BLOCO_ALTURA,
      }}
    >
      {Array.from({ length: BLOCOS }).map((_, i) => (
        <div
          key={i}
          className={`bloco-${lado} bloco-${lado}-${i}`}
          style={{
            position: "absolute",
            left: 0,
            bottom: i * BLOCO_ALTURA,
            width: 300,
            height: BLOCO_ALTURA - 12,
            borderRadius: 14,
            background: i === 0 ? cor : "#f2f2f2",
            boxShadow: "0 0 40px rgba(255,255,255,0.15)",
            opacity: 0,
          }}
        />
      ))}
    </div>
  );
};

export const ComparacaoLadoALado: React.FC<
  z.infer<typeof comparacaoSchema>
> = ({ rotuloEsquerda, rotuloDireita, corDestaque }) => {
  useEffect(() => {
    loadFont();
  }, []);

  const ref = useAnimeTimeline((tl, $) => {
    // Rótulos aparecem primeiro.
    tl.add($(".rotulo"), { opacity: [0, 1], y: [30, 0], duration: 500 }, 0);

    // Lado esquerdo: a pilha sobe bloco a bloco.
    for (let i = 0; i < BLOCOS; i++) {
      tl.add(
        $(`.bloco-esq-${i}`),
        { opacity: [0, 1], y: [-200, 0], ease: "outBounce", duration: 700 },
        800 + i * 1500,
      );
    }

    // Lado direito: o primeiro bloco entra e é reajustado sem sair do lugar.
    tl.add(
      $(".bloco-dir-0"),
      { opacity: [0, 1], y: [-200, 0], ease: "outBounce", duration: 700 },
      800,
    );
    for (let i = 0; i < BLOCOS; i++) {
      tl.add(
        $(".bloco-dir-0"),
        {
          rotate: [0, -6, 5, 0],
          x: [0, -14, 10, 0],
          duration: 1100,
          ease: "inOutSine",
        },
        1800 + i * 1500,
      );
    }
  });

  return (
    <AbsoluteFill
      ref={ref}
      style={{
        backgroundColor: "#050505",
        fontFamily: TheBoldFont,
        color: "white",
      }}
    >
      <div
        style={{
          position: "absolute",
          top: 420,
          left: 0,
          right: 0,
          display: "flex",
          justifyContent: "space-around",
        }}
      >
        {[rotuloEsquerda, rotuloDireita].map((rotulo) => (
          <div
            key={rotulo}
            className="rotulo"
            style={{
              width: 420,
              textAlign: "center",
              fontSize: 54,
              lineHeight: 1.1,
              opacity: 0,
            }}
          >
            {rotulo}
          </div>
        ))}
      </div>
      <div
        style={{
          position: "absolute",
          bottom: 380,
          left: 0,
          right: 0,
          display: "flex",
          justifyContent: "space-around",
          alignItems: "flex-end",
        }}
      >
        <Pilha lado="esq" cor={corDestaque} />
        <Pilha lado="dir" cor={corDestaque} />
      </div>
    </AbsoluteFill>
  );
};
