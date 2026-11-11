import { useEffect } from "react";
import { AbsoluteFill } from "remotion";
import { useAnimeTimeline } from "../anime/useAnimeTimeline";
import { Anton, loadAnton } from "../load-font";

// Reel de 15 s, só texto e linha animada. Mito: tava rindo agora há pouco,
// então é fingimento. A linha mostra a emoção subindo e caindo em pouco tempo.

const VERMELHO = "#c83c1e";

const texto: React.CSSProperties = {
  position: "absolute",
  left: 90,
  right: 90,
  textAlign: "center",
  opacity: 0,
};

const rotulo: React.CSSProperties = {
  position: "absolute",
  fontSize: 44,
  color: "#bdbdbd",
  opacity: 0,
};

export const MitoRindo: React.FC = () => {
  useEffect(() => {
    loadAnton();
  }, []);

  const ref = useAnimeTimeline((tl, $) => {
    const entra = { opacity: [0, 1], y: [40, 0], duration: 450 };
    const sai = { opacity: 0, duration: 350 };

    tl.add($(".t1"), entra, 200)
      .add(
        $(".linha-sobe"),
        { strokeDashoffset: [1, 0], duration: 1800, ease: "outSine" },
        400,
      )
      .add($(".r-riso"), { opacity: [0, 1], duration: 400 }, 1900)
      .add($(".t2"), entra, 2600)
      .add(
        $(".falso"),
        {
          opacity: [0, 1],
          scale: [2.2, 1],
          rotate: [-14, -8],
          duration: 420,
          ease: "outBack",
        },
        3700,
      )
      .add($(".t1, .t2, .falso"), sai, 5200)
      .add(
        $(".linha-cai"),
        { strokeDashoffset: [1, 0], duration: 1200, ease: "inOutQuad" },
        5300,
      )
      .add($(".r-dor"), { opacity: [0, 1], duration: 400 }, 6300)
      .add($(".t3"), entra, 6700)
      .add($(".t3"), sai, 9500)
      .add($(".t4"), entra, 9900)
      .add($(".t4, .grafico"), sai, 12600)
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
        Tava rindo agora há pouco.
      </div>
      <div
        className="t2"
        style={{ ...texto, top: 610, fontSize: 80, color: "#bdbdbd" }}
      >
        Então é fingimento?
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
        A emoção pode virar em minutos ou horas.
      </div>
      <div
        className="t4"
        style={{ ...texto, top: 330, fontSize: 116, lineHeight: 1.1 }}
      >
        O riso era real.
        <br />
        <span style={{ color: VERMELHO }}>A dor também.</span>
      </div>

      <div
        className="grafico"
        style={{
          position: "absolute",
          left: 90,
          top: 980,
          width: 900,
          height: 560,
        }}
      >
        <svg
          width={900}
          height={560}
          viewBox="0 0 900 560"
          style={{ overflow: "visible" }}
        >
          <line
            x1={0}
            y1={280}
            x2={900}
            y2={280}
            stroke="#2a2a2a"
            strokeWidth={4}
          />
          <path
            className="linha-sobe"
            d="M 0 300 C 120 300, 180 90, 330 80"
            fill="none"
            stroke="white"
            strokeWidth={12}
            strokeLinecap="round"
            pathLength={1}
            strokeDasharray={1}
            strokeDashoffset={1}
          />
          <path
            className="linha-cai"
            d="M 330 80 C 420 80, 440 470, 560 480 S 760 430, 900 470"
            fill="none"
            stroke={VERMELHO}
            strokeWidth={12}
            strokeLinecap="round"
            pathLength={1}
            strokeDasharray={1}
            strokeDashoffset={1}
          />
        </svg>
        <div className="r-riso" style={{ ...rotulo, left: 270, top: 0 }}>
          riso
        </div>
        <div className="r-dor" style={{ ...rotulo, left: 520, top: 500 }}>
          dor
        </div>
      </div>

      <div
        className="t5"
        style={{ ...texto, top: 640, fontSize: 106, lineHeight: 1.1 }}
      >
        Manda pra quem chamou de fingimento.
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
