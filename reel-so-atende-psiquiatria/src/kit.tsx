import React from "react";
import { Easing, interpolate } from "remotion";

export const C = {
  bg: "#EDE4D3",
  ink: "#1A1A1A",
  brick: "#A62B24",
  paper: "#F7F0E3",
  coat: "#FCFAF5",
  gray: "#9A948A",
  faint: "#BDB2A0",
};
export const SW = 6;
export const GROUND = 1320;
export const TITLE = "'Archivo Black', sans-serif";
export const BODY = "'Poppins', sans-serif";

const ease = Easing.out(Easing.cubic);
/** 0..1 progress from `at` over `d` seconds */
export const prog = (t: number, at: number, d = 0.45) =>
  interpolate(t, [at, at + d], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });

export const fmt = (n: number) => String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
export const count = (t: number, at: number, target: number, d = 0.9) => fmt(Math.round(target * prog(t, at, d)));

/** fade + leve deslocamento para cima */
export const FadeUp: React.FC<{ t: number; at: number; d?: number; dy?: number; style?: React.CSSProperties; children: React.ReactNode; out?: number }> = ({ t, at, d = 0.45, dy = 26, style, children, out }) => {
  const p = prog(t, at, d);
  const o = out !== undefined ? 1 - prog(t, out, 0.3) : 1;
  return <div style={{ ...style, opacity: p * o, transform: `translateY(${(1 - p) * dy}px)` }}>{children}</div>;
};

/** grupo SVG com fade + deslocamento */
export const GUp: React.FC<{ t: number; at: number; d?: number; dy?: number; children: React.ReactNode; out?: number }> = ({ t, at, d = 0.45, dy = 22, children, out }) => {
  const p = prog(t, at, d);
  const o = out !== undefined ? 1 - prog(t, out, 0.3) : 1;
  return <g opacity={p * o} transform={`translate(0 ${(1 - p) * dy})`}>{children}</g>;
};

/** bloco de titulo dentro da area segura (topo 250, laterais 90) */
export const TitleBox: React.FC<{ top?: number; children: React.ReactNode; style?: React.CSSProperties }> = ({ top = 285, children, style }) => (
  <div style={{ position: "absolute", top, left: 90, width: 900, textAlign: "center", ...style }}>{children}</div>
);

export const Big: React.FC<{ size: number; color?: string; children: React.ReactNode; style?: React.CSSProperties }> = ({ size, color = C.ink, children, style }) => (
  <div style={{ fontFamily: TITLE, fontSize: size, lineHeight: 1.04, color, letterSpacing: -0.5, ...style }}>{children}</div>
);

export const Small: React.FC<{ size?: number; weight?: number; color?: string; children: React.ReactNode; style?: React.CSSProperties }> = ({ size = 40, weight = 600, color = C.ink, children, style }) => (
  <div style={{ fontFamily: BODY, fontSize: size, fontWeight: weight, lineHeight: 1.25, color, ...style }}>{children}</div>
);

export const Ground: React.FC<{ y?: number; x1?: number; x2?: number }> = ({ y = GROUND, x1 = 110, x2 = 970 }) => (
  <line x1={x1} y1={y} x2={x2} y2={y} stroke={C.ink} strokeWidth={SW} strokeLinecap="round" />
);

/** Figura humana simples, sem rosto. (x,y) = pes. Altura ~ 330*s */
export const Person: React.FC<{ x: number; y: number; s?: number; fill?: string; coat?: boolean; lean?: number; hand?: boolean; op?: number }> = ({ x, y, s = 1, fill = C.paper, coat = false, lean = 0, hand = false, op = 1 }) => {
  const body = coat ? C.coat : fill;
  return (
    <g transform={`translate(${x} ${y}) scale(${s}) rotate(${lean})`} opacity={op} strokeLinejoin="round" strokeLinecap="round">
      <rect x={-42} y={-124} width={36} height={124} rx={10} fill={C.ink} stroke={C.ink} strokeWidth={SW} />
      <rect x={6} y={-124} width={36} height={124} rx={10} fill={C.ink} stroke={C.ink} strokeWidth={SW} />
      <path d={hand ? "M54,-236 Q86,-262 52,-292" : "M54,-236 Q76,-196 70,-128"} fill="none" stroke={C.ink} strokeWidth={SW + 10} />
      <path d={hand ? "M54,-236 Q86,-262 52,-292" : "M54,-236 Q76,-196 70,-128"} fill="none" stroke={body} strokeWidth={10} />
      <path d="M-54,-236 Q-76,-196 -70,-128" fill="none" stroke={C.ink} strokeWidth={SW + 10} />
      <path d="M-54,-236 Q-76,-196 -70,-128" fill="none" stroke={body} strokeWidth={10} />
      <path d="M-60,-112 L-54,-232 Q-50,-254 -28,-256 L28,-256 Q50,-254 54,-232 L60,-112 Z" fill={body} stroke={C.ink} strokeWidth={SW} />
      {coat && (
        <>
          <path d="M-24,-254 L0,-196 L24,-254" fill="none" stroke={C.ink} strokeWidth={SW - 1} />
          <path d="M-14,-246 Q-34,-182 -4,-170 Q20,-166 22,-196" fill="none" stroke={C.brick} strokeWidth={5} />
          <circle cx={22} cy={-200} r={7} fill={C.brick} />
          <line x1={0} y1={-196} x2={0} y2={-116} stroke={C.ink} strokeWidth={4} />
        </>
      )}
      <circle cx={0} cy={-296} r={36} fill={body === C.coat ? C.paper : body} stroke={C.ink} strokeWidth={SW} />
      {hand && <circle cx={50} cy={-298} r={12} fill={body} stroke={C.ink} strokeWidth={SW - 1} />}
    </g>
  );
};

/** Figura sentada. (x,y) = pes no chao */
export const Seated: React.FC<{ x: number; y: number; s?: number }> = ({ x, y, s = 1 }) => (
  <g transform={`translate(${x} ${y}) scale(${s})`} strokeLinejoin="round" strokeLinecap="round">
    <rect x={20} y={-150} width={34} height={150} rx={10} fill={C.ink} stroke={C.ink} strokeWidth={SW} />
    <rect x={-50} y={-160} width={104} height={36} rx={12} fill={C.ink} stroke={C.ink} strokeWidth={SW} />
    <path d="M-52,-148 L-48,-262 Q-44,-284 -22,-286 L28,-286 Q50,-284 52,-262 L48,-148 Z" fill={C.paper} stroke={C.ink} strokeWidth={SW} />
    <path d="M40,-262 Q64,-220 66,-170" fill="none" stroke={C.ink} strokeWidth={SW + 10} />
    <path d="M40,-262 Q64,-220 66,-170" fill="none" stroke={C.paper} strokeWidth={10} />
    <circle cx={2} cy={-326} r={36} fill={C.paper} stroke={C.ink} strokeWidth={SW} />
  </g>
);

export const Chair: React.FC<{ x: number; y: number }> = ({ x, y }) => (
  <g transform={`translate(${x} ${y})`} strokeLinejoin="round" strokeLinecap="round">
    <rect x={-62} y={-262} width={22} height={150} rx={8} fill={C.paper} stroke={C.ink} strokeWidth={SW} />
    <rect x={-66} y={-124} width={130} height={22} rx={8} fill={C.paper} stroke={C.ink} strokeWidth={SW} />
    <line x1={-52} y1={-102} x2={-52} y2={0} stroke={C.ink} strokeWidth={SW} />
    <line x1={50} y1={-102} x2={50} y2={0} stroke={C.ink} strokeWidth={SW} />
  </g>
);

export type MiniKind = "psiq" | "clin" | "res" | "outra" | "vazio";
/** boneco da grade. (x,y) = base */
export const Mini: React.FC<{ x: number; y: number; kind: MiniKind; s?: number; op?: number }> = ({ x, y, kind, s = 1, op = 1 }) => {
  const m: Record<MiniKind, { f: string; st: string; dash?: string }> = {
    psiq: { f: C.ink, st: C.ink },
    clin: { f: C.brick, st: C.brick },
    res: { f: "none", st: C.ink, dash: "5 6" },
    outra: { f: C.gray, st: C.gray },
    vazio: { f: "none", st: C.faint },
  };
  const v = m[kind];
  return (
    <g transform={`translate(${x} ${y}) scale(${s})`} opacity={op}>
      <circle cx={0} cy={-40} r={11} fill={v.f} stroke={v.st} strokeWidth={3.5} strokeDasharray={v.dash} />
      <path d="M-19,-2 L-19,-10 Q-19,-26 0,-26 Q19,-26 19,-10 L19,-2 Z" fill={v.f} stroke={v.st} strokeWidth={3.5} strokeDasharray={v.dash} strokeLinejoin="round" />
    </g>
  );
};

/** fachada simples com placa CAPS. (x,y)=canto inferior esquerdo */
export const CapsBuilding: React.FC<{ x: number; y: number; w: number; h: number; doorText?: string; doorOp?: number }> = ({ x, y, w, h, doorText, doorOp = 1 }) => {
  const dw = 150, dh = 250;
  const dx = x + w / 2 - dw / 2;
  return (
    <g strokeLinejoin="round" strokeLinecap="round">
      <rect x={x} y={y - h} width={w} height={h} fill={C.paper} stroke={C.ink} strokeWidth={SW} />
      <rect x={x - 20} y={y - h - 26} width={w + 40} height={26} fill={C.ink} stroke={C.ink} strokeWidth={SW} />
      <rect x={x + w / 2 - 120} y={y - h + 34} width={240} height={86} rx={8} fill={C.brick} stroke={C.ink} strokeWidth={SW} />
      <text x={x + w / 2} y={y - h + 98} textAnchor="middle" fontFamily={TITLE} fontSize={58} fill={C.paper}>CAPS</text>
      {[0, 1].map((i) => (
        <rect key={i} x={i === 0 ? x + 40 : x + w - 40 - 110} y={y - h + 160} width={110} height={90} fill={C.coat} stroke={C.ink} strokeWidth={SW} />
      ))}
      <rect x={dx} y={y - dh} width={dw} height={dh} fill={C.ink} stroke={C.ink} strokeWidth={SW} />
      <circle cx={dx + dw - 24} cy={y - dh / 2} r={7} fill={C.paper} />
      {doorText && (
        <g opacity={doorOp}>
          <line x1={dx + 30} y1={y - dh + 30} x2={dx + dw / 2} y2={y - dh + 6} stroke={C.paper} strokeWidth={3} />
          <line x1={dx + dw - 30} y1={y - dh + 30} x2={dx + dw / 2} y2={y - dh + 6} stroke={C.paper} strokeWidth={3} />
          <rect x={dx - 16} y={y - dh + 30} width={dw + 32} height={64} rx={6} fill={C.coat} stroke={C.brick} strokeWidth={6} />
          <text x={dx + dw / 2} y={y - dh + 76} textAnchor="middle" fontFamily={TITLE} fontSize={doorText.length > 7 ? 30 : 36} fill={C.brick}>{doorText}</text>
        </g>
      )}
    </g>
  );
};

/** Legenda pequena da narracao, na parte de baixo da area segura (termina em y=1490) */
export const Caption: React.FC<{ t: number; chunks: { text: string; start: number; end: number }[] }> = ({ t, chunks }) => {
  const c = chunks.find((k) => t >= k.start && t < k.end);
  if (!c) return null;
  const p = prog(t, c.start, 0.12);
  return (
    <div style={{ position: "absolute", left: 120, width: 840, top: 1380, height: 110, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ fontFamily: BODY, fontWeight: 600, fontSize: 36, lineHeight: 1.28, color: C.ink, textAlign: "center", opacity: p, textWrap: "balance" as never }}>{c.text}</div>
    </div>
  );
};
