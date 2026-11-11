import { useEffect } from "react";
import { AbsoluteFill } from "remotion";
import { useAnimeTimeline } from "../anime/useAnimeTimeline";
import { Anton, loadAnton } from "../load-font";

// Parte 2 da série de mitos, para publicar depois de MitoRindo.
// Mito: se apega a qualquer um. Dois círculos: ela corre para quem trouxe
// calma, e o medo de perder aparece em volta dos dois.

const VERMELHO = "#c83c1e";

const texto: React.CSSProperties = {
  position: "absolute",
  left: 90,
  right: 90,
  textAlign: "center",
  opacity: 0,
};

const circulo: React.CSSProperties = {
  position: "absolute",
  top: 1180,
  width: 150,
  height: 150,
  borderRadius: "50%",
  opacity: 0,
};

const rotulo: React.CSSProperties = {
  position: "absolute",
  top: 1460,
  width: 360,
  textAlign: "center",
  fontSize: 44,
  color: "#bdbdbd",
  opacity: 0,
};

export const MitoApego: React.FC = () => {
  useEffect(() => {
    loadAnton();
  }, []);

  const ref = useAnimeTimeline((tl, $) => {
    const entra = { opacity: [0, 1], y: [40, 0], duration: 450 };
    const sai = { opacity: 0, duration: 350 };

    tl.add($(".t1"), entra, 200)
      .add($(".ela, .r-ela"), { opacity: [0, 1], duration: 500 }, 600)
      .add($(".t2"), entra, 2400)
      .add(
        $(".falso"),
        {
          opacity: [0, 1],
          scale: [2.2, 1],
          rotate: [-14, -8],
          duration: 420,
          ease: "outBack",
        },
        3500,
      )
      .add($(".t1, .t2, .falso"), sai, 5000)
      .add($(".t3"), entra, 5300)
      .add(
        $(".outro, .r-outro"),
        { opacity: [0, 1], scale: [0.6, 1], duration: 600, ease: "outBack" },
        5600,
      )
      .add($(".r-ela"), { opacity: 0, duration: 250 }, 7000)
      .add($(".ela"), { x: [0, 330], duration: 650, ease: "outExpo" }, 7100)
      .add($(".t3"), sai, 8600)
      .add($(".t4"), entra, 8900)
      .add(
        $(".anel"),
        { opacity: [0, 1], scale: [1.6, 1], duration: 700, ease: "outQuad" },
        9300,
      )
      .add(
        $(".anel"),
        { scale: [1, 1.08, 1], duration: 900, loop: 2, ease: "inOutSine" },
        10000,
      )
      .add($(".t4, .ela, .outro, .r-outro, .anel"), sai, 12600)
      .add($(".t5, .assinatura"), entra, 13000);
  });

  return (
    <AbsoluteFill
      ref={ref}
      style={{
        backgroundColor: "#050505",
        color: "white",
        fontFamily: Anton,
        textTransform: "uppercase",
      }}
    >
      <div
        className="t1"
        style={{ ...texto, top: 300, fontSize: 116, lineHeight: 1.05 }}
      >
        Se apega a qualquer um.
      </div>
      <div
        className="t2"
        style={{ ...texto, top: 610, fontSize: 80, color: "#bdbdbd" }}
      >
        Então é carência?
      </div>
      <div
        className="falso"
        style={{
          ...texto,
          left: 0,
          right: 0,
          top: 760,
          fontSize: 150,
          color: VERMELHO,
          letterSpacing: 6,
        }}
      >
        FALSO
      </div>

      <div
        className="t3"
        style={{ ...texto, top: 330, fontSize: 106, lineHeight: 1.1 }}
      >
        Não é qualquer um. É quem trouxe calma.
      </div>
      <div
        className="t4"
        style={{ ...texto, top: 330, fontSize: 106, lineHeight: 1.1 }}
      >
        A pressa vem do medo de <span style={{ color: VERMELHO }}>perder</span>{" "}
        essa calma.
      </div>

      <div
        className="anel"
        style={{
          position: "absolute",
          top: 1080,
          left: 360,
          width: 360,
          height: 350,
          borderRadius: "50%",
          border: `10px dashed ${VERMELHO}`,
          opacity: 0,
        }}
      />
      <div
        className="ela"
        style={{ ...circulo, left: 95, background: "white", zIndex: 1 }}
      />
      <div
        className="outro"
        style={{ ...circulo, left: 505, background: "#8a8a8a" }}
      />
      <div className="r-ela" style={{ ...rotulo, left: -10 }}>
        ela
      </div>
      <div className="r-outro" style={{ ...rotulo, left: 400 }}>
        quem trouxe calma
      </div>

      <div
        className="t5"
        style={{ ...texto, top: 640, fontSize: 106, lineHeight: 1.1 }}
      >
        Manda pra quem achou que era carência.
      </div>
      <div
        className="assinatura"
        style={{
          ...texto,
          top: 1560,
          fontSize: 36,
          color: "#8a8a8a",
          fontFamily: "sans-serif",
          textTransform: "none",
        }}
      >
        Dr. Fabio Schmidt, médico, CRM-SP 183549
      </div>
    </AbsoluteFill>
  );
};
